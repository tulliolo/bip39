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
import enum
import logging
import math
import secrets

from typing import ByteString, TypeVar

from tulliolo.bip39.utils.transformation import Transformation

ENTROPY_SIZE_MIN = ENTROPY_SIZE_DEF = 128  # bits
ENTROPY_SIZE_MAX = 256  # bits
ENTROPY_SIZE_STEP = 32  # bits

ENTROPY_SIZE_RANGE = range(ENTROPY_SIZE_MIN, ENTROPY_SIZE_MAX + ENTROPY_SIZE_STEP, ENTROPY_SIZE_STEP)

LOGGER = logging.getLogger(__name__)


HexString = TypeVar("HexString", bound=str)


class Entropy:
    """
    The entropy (ENT), as defined in bip39 specs:

    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#generating-the-mnemonic
    """
    def __init__(self, value: ByteString | HexString | int):
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

        self._value = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            LOGGER.warning(f"invalid entropy type | cannot compare {self} with {type(other)}")
            return False

        return self._value == other._value

    def __len__(self) -> int:
        """
        Returns the entropy size in bits.
        :return:
        """
        return len(self._value) * 8  # bits

    @classmethod
    def generate(cls, size: int) -> "Entropy":
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
        except TypeError as e:
            e.args = (
                "invalid size type",
                *e.args
            )
            LOGGER.error(" | ".join(e.args))
            raise e.with_traceback(e.__traceback__)
        except Exception as e:
            e.args = (
                "invalid size value",
                *e.args
            )
            LOGGER.error(" | ".join(e.args))
            raise e.with_traceback(e.__traceback__)

        return cls(token)

    @property
    def value(self) -> bytes:
        return self._value

    def transform(self, transformation: Transformation) -> "Entropy":
        """
        Applies a transformation on entropy
        :param transformation:
        :return:
        """
        return Entropy(transformation(self._value))
