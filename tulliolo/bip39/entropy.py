#!/usr/bin/python3
#
#   Copyright (C) 2022 Tullio Loffredo, @tulliolo
#
#   It is subject to the license terms in the LICENSE file found in the top-level
#   directory of this distribution.
#
#   No part of this software, including this file, may be copied, modified,
#   propagated, or distributed except according to the terms contained in the
#   LICENSE file.
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
"""
A module implementing the entropy (ENT) as defined in bip39 specs:

https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
"""
import enum
import logging
import math
import secrets

ENTROPY_SIZE_MIN = ENTROPY_SIZE_DEF = 128  # bits
ENTROPY_SIZE_MAX = 256  # bits
ENTROPY_SIZE_STEP = 32  # bits

ENTROPY_SIZE_RANGE = range(ENTROPY_SIZE_MIN, ENTROPY_SIZE_MAX + ENTROPY_SIZE_STEP, ENTROPY_SIZE_STEP)

LOGGER = logging.getLogger(__name__)


class TransformationAlgorithm(enum.Enum):
    """
    The supported entropy transformation algorithms:

    - NEGATIVE (DEFAULT): inverts all bits, like in a negative;
    - MIRROR: reads all bits from right to left, like in front of a mirror.
    """
    NEGATIVE = DEFAULT = "negative"
    MIRROR = "mirror"

    @property
    def description(self) -> str:
        """
        A description of the current instance.
        :return:
        """
        return (
            "inverts all bits, like in a negative"
            if self == TransformationAlgorithm.NEGATIVE else
            "reads all bits from right to left, like in front of a mirror"
        )


class Entropy:
    """
    The entropy (ENT), as defined in bip39 specs:

    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#generating-the-mnemonic
    """

    _create_key = object()

    def __init__(self, create_key, value: bytes):
        """
        Builds a new entropy instance. It cannot be directly invoked (see from_value and generate methods).
        :param create_key: a key for this class, locking the direct invocation of the constructor
        :param value: an entropy value in bytes
        """
        assert create_key == self._create_key, \
            "entropy must be created by from_value or generate"

        self._value = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entropy):
            try:
                other = Entropy.from_value(other)
            except Exception as e:
                LOGGER.warning(
                    f"cannot convert '{other}' into {Entropy} | "
                    f"{' | '.join(e.args)}"
                )
                return False

        return self._value == other._value

    def __len__(self) -> int:
        """
        Returns the entropy size in bits
        :return:
        """
        return len(self._value) * 8  # bits

    @classmethod
    def from_value(cls, value: bytearray | bytes | int | str) -> "Entropy":
        """
        Imports an entropy value generated from another source.
        :param value: the entropy value
        :return:
        """
        if isinstance(value, (bytes, bytearray)):
            value = bytes(value)
        elif isinstance(value, int):
            size = math.ceil(value.bit_length() / ENTROPY_SIZE_STEP) * ENTROPY_SIZE_STEP // 8  # bytes
            value = value.to_bytes(size, byteorder="big")
        elif isinstance(value, str):
            try:
                value = bytes.fromhex(value)
            except ValueError as e:
                LOGGER.error(f"invalid entropy type | {str(e)}")
                raise TypeError(
                    "invalid entropy type",
                    f"'{value}' is not a hex string"
                ) from None
        else:
            LOGGER.error("invalid entropy type")
            raise TypeError(
                "invalid entropy type",
                f"type {type(value)} cannot be converted to entropy bytes"
            )

        size = len(value) * 8  # bits
        if size not in ENTROPY_SIZE_RANGE:
            LOGGER.error("invalid entropy size")
            raise ValueError(
                "invalid entropy size",
                f"expected: {'/'.join(str(v) for v in ENTROPY_SIZE_RANGE)} bits",
                f"obtained: {size} bits"
            )

        return cls(cls._create_key, value)

    @classmethod
    def generate(cls, size: int = ENTROPY_SIZE_DEF) -> "Entropy":
        """
        Generates an entropy using a cryptographically secure generator.
        :param size: the size in bits
        :return:
        """
        size = int(size)

        if size not in ENTROPY_SIZE_RANGE:
            LOGGER.error("invalid entropy size")
            raise ValueError(
                "invalid entropy size",
                f"expected: {'/'.join([str(v) for v in ENTROPY_SIZE_RANGE])} bits",
                f"obtained: {size} bits"
            )

        value = secrets.SystemRandom().randbytes(size // 8)
        return cls(cls._create_key, value)

    def transform(self, algorithm: TransformationAlgorithm = TransformationAlgorithm.DEFAULT) -> "Entropy":
        """
        Applies a transformation on the current entropy.
        :param algorithm: the algorithm to apply
        :return:
        """
        size = len(self)
        value = int.from_bytes(self._value, byteorder="big")

        return (
            Entropy.from_value((2**size - value - 1).to_bytes(size // 8, byteorder='big'))
            if algorithm == TransformationAlgorithm.NEGATIVE else
            Entropy.from_value(
                int(
                    bin(value)[2:].zfill(size)[::-1], 2
                ).to_bytes(size // 8, byteorder='big')
            )
        )

    @property
    def value(self) -> bytes:
        """
        The entropy value in bytes
        :return:
        """
        return self._value
