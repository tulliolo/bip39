#!/usr/bin/python3
#
#   Copyright (C) 2023 Tullio Loffredo, @tulliolo
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
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
"""
A module implementing the entropy (ENT) as defined in bip39 specs:

https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
"""
import logging
import math
import secrets

from typing import ByteString, Type, TypeVar

from tulliolo.bip39.utils.transformation import Transformation

ENTROPY_SIZE_MIN = ENTROPY_SIZE_DEF = 128  # bits
ENTROPY_SIZE_MAX = 256  # bits
ENTROPY_SIZE_STEP = 32  # bits

ENTROPY_SIZE_RANGE = range(ENTROPY_SIZE_MIN, ENTROPY_SIZE_MAX + ENTROPY_SIZE_STEP, ENTROPY_SIZE_STEP)

LOGGER = logging.getLogger(__name__)


HexString = TypeVar("HexString", bound=str)
T = TypeVar("T", bound="Entropy")


class Entropy:
    """
    The entropy (ENT), as defined in bip39 specs:

    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#generating-the-mnemonic
    """
    def __init__(self: T, value: ByteString | HexString | int) -> None:
        """
        Builds a new Entropy instance.
        :param value: an entropy value
        """
        try:
            if isinstance(value, ByteString):
                value = bytes(value)
            elif isinstance(value, str):
                value = bytes.fromhex(value)
            elif isinstance(value, int):
                value = int(value)
                size = math.ceil(value.bit_length() / ENTROPY_SIZE_STEP) * ENTROPY_SIZE_STEP // 8  # bytes
                value = value.to_bytes(size, byteorder="big")
            else:
                raise TypeError(f"cannot convert {type(value)} to entropy")
        except TypeError as e:
            e.args = (
                "invalid entropy type",
                *e.args
            )
            LOGGER.error(" | ".join(e.args))
            raise e.with_traceback(e.__traceback__)
        except Exception as e:
            e.args = (
                "invalid entropy value",
                *e.args
            )
            LOGGER.error(" | ".join(e.args))
            raise e.with_traceback(e.__traceback__)

        size = len(value) * 8  # bits
        if size not in ENTROPY_SIZE_RANGE:
            LOGGER.error("invalid entropy size")
            raise ValueError(
                "invalid entropy size",
                f"expected: {'/'.join(str(v) for v in ENTROPY_SIZE_RANGE)} bits",
                f"obtained: {size} bits"
            )

        self._entropy_value = value

    def __eq__(self: T, other: T) -> bool:
        if not isinstance(other, type(self)):
            LOGGER.warning(f"invalid type | cannot compare {type(self)} with {type(other)}")
            return False

        return self._entropy_value == other._entropy_value

    def __len__(self: T) -> int:
        """
        Returns the entropy size in bits.
        :return:
        """
        return len(self._entropy_value) * 8  # bits

    @classmethod
    def generate(cls: Type[T], size: int) -> T:
        """
        Generates an entropy using a cryptographically secure generator.
        :param size: the size in bits
        :return:
        """
        try:
            if size not in ENTROPY_SIZE_RANGE:
                raise ValueError(
                    f"expected: {'/'.join(str(v) for v in ENTROPY_SIZE_RANGE)} bits",
                    f"obtained: {size} bits"
                )

            token = secrets.token_bytes(size // 8)
        except Exception as e:
            e.args = (
                "invalid entropy size",
                *e.args
            )
            LOGGER.error(" | ".join(e.args))
            raise e.with_traceback(e.__traceback__)

        return cls(token)

    @property
    def info(self: T) -> dict:
        """
        Returns a dict representation of this instance.
        :return:
        """
        return {
            "size": len(self._entropy_value) * 8,  # bits
            "value": self._entropy_value.hex()
        }

    @property
    def value(self: T) -> bytes:
        return self._entropy_value

    def transform(self: T, transformation: Transformation) -> T:
        """
        Applies a transformation on entropy
        :param transformation:
        :return:
        """
        return self.__class__(transformation(self._entropy_value))
