#!/usr/bin/python3
#
#   Copyright (C) 2023 Tullio Loffredo (@tulliolo)
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
A module implementing the bip39 specs:
https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
"""
import hashlib
import logging
import math
import secrets
from typing import Iterable, TypeVar, Tuple, ByteString

from tulliolo.bip39.utils.common import normalize_string
from tulliolo.bip39.utils.transformation import Transformation
from tulliolo.bip39.wordlist import wordlist

ENTROPY_SIZE_MIN = ENTROPY_SIZE_DEF = 128  # bits
ENTROPY_SIZE_MAX = 256  # bits
ENTROPY_SIZE_STEP = 32  # bits

ENTROPY_SIZE_RANGE = range(ENTROPY_SIZE_MIN, ENTROPY_SIZE_MAX + ENTROPY_SIZE_STEP, ENTROPY_SIZE_STEP)

WORD_SIZE = 11  # bits

WORD_COUNT_ALL = tuple(
    math.ceil(entropy_size / WORD_SIZE) for entropy_size in ENTROPY_SIZE_RANGE
)
WORD_COUNT_DEF = WORD_COUNT_ALL[ENTROPY_SIZE_RANGE.index(ENTROPY_SIZE_DEF)]

CHECKSUM_SIZE_ALL = tuple(
    word_count * WORD_SIZE - entropy_size
    for word_count, entropy_size in zip(WORD_COUNT_ALL, ENTROPY_SIZE_RANGE)
)

LOGGER = logging.getLogger(__name__)

HexString = TypeVar("HexString", bound=str)
T = TypeVar("T", bound="Entropy")


class Mnemonic:
    """
    A class implementing the bip39 specs:
    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

    The class also provides a function to transform (or restore) the entropy that can be used to create some
    side-mnemonics hiding the original.
    """
    def __init__(self, entropy: ByteString | HexString | int):
        """
        Creates a new mnemonic instance from entropy.
        :param entropy:
        """
        try:
            if isinstance(entropy, ByteString):
                entropy = bytes(entropy)
            elif isinstance(entropy, str):
                entropy = bytes.fromhex(entropy)
            elif isinstance(entropy, int):
                entropy = int(entropy)
                entropy_size = math.ceil(entropy.bit_length() / ENTROPY_SIZE_STEP) * ENTROPY_SIZE_STEP // 8  # bytes
                entropy = entropy.to_bytes(entropy_size, byteorder="big")
            else:
                raise TypeError(f"cannot convert {type(entropy)} to entropy")
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

        entropy_size = len(entropy) * 8  # bits
        if entropy_size not in ENTROPY_SIZE_RANGE:
            args = (
                "invalid entropy size",
                f"expected: {', '.join(str(v) for v in ENTROPY_SIZE_RANGE)} bits",
                f"obtained: {entropy_size} bits"
            )
            LOGGER.error(" | ".join(args))
            raise ValueError(*args)

        self._entropy = entropy

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            LOGGER.warning(f"invalid type | cannot compare {type(self)} with {type(other)}")
            return False

        return self._entropy == other._entropy

    def __len__(self) -> int:
        """
        Returns the mnemonic length in words.
        :return:
        """
        entropy_size = len(self._entropy) * 8  # bits
        return WORD_COUNT_ALL[ENTROPY_SIZE_RANGE.index(entropy_size)]

    @classmethod
    def from_value(cls, value: str | Iterable[str], fix_checksum: bool = False) -> "Mnemonic":
        """
        Creates a new mnemonic instance from a list of words.
        :param value: the list of words
        :param fix_checksum: if set, corrects the checksum; it can be useful when the words are 'manually' generated
        (e.g. by rolling dices)
        :return:
        """
        if isinstance(value, str):
            value = normalize_string(value).split()
        elif isinstance(value, Iterable):
            value = [normalize_string(v) for v in value]
        else:
            args = (
                "invalid mnemonic type",
                f"cannot convert {type(value)} to mnemonic"
            )
            LOGGER.error(" | ".join(args))
            raise TypeError(*args)

        word_count = len(value)
        if word_count not in WORD_COUNT_ALL:
            args = (
                "invalid mnemonic size",
                f"expected: {', '.join(str(v) for v in WORD_COUNT_ALL)} words",
                f"obtained: {word_count} words"
            )
            LOGGER.error(" | ".join(args))
            raise ValueError(*args)

        entropy_size, checksum_size = [
            (e, c) for w, e, c in zip(WORD_COUNT_ALL, ENTROPY_SIZE_RANGE, CHECKSUM_SIZE_ALL)
            if w == word_count
        ][0]

        LOGGER.debug("index -> word")
        sequence = 0
        for word in value:
            try:
                wid = wordlist.index(word)
                LOGGER.debug(f"{wid:4}  -> {word}")
            except ValueError as e:
                e.args = (
                    "invalid mnemonic value",
                    *e.args
                )
                LOGGER.error(" | ".join(e.args))
                raise e.with_traceback(e.__traceback__)
            sequence = (sequence << WORD_SIZE) | wid

        entropy = (sequence >> checksum_size).to_bytes(entropy_size // 8, byteorder="big")
        checksum = sequence & (2 ** checksum_size - 1)

        result = Mnemonic(entropy)
        if checksum != result.checksum:
            args = (
                "invalid checksum",
                f"expected: {hex(result.checksum)[2:]}",
                f"obtained: {hex(checksum)[2:]}"
            )
            if fix_checksum:
                LOGGER.warning(" | ".join(args))
            else:
                LOGGER.error(" | ".join(args))
                raise ValueError(*args)

        return result

    @classmethod
    def generate(cls, size: int) -> "Mnemonic":
        """
        Generates a new mnemonic instance using a cryptographically secure generator.
        :param size: the mnemonic length in words
        :return:
        """
        try:
            size = int(size)
            if size not in WORD_COUNT_ALL:
                args = (
                    f"expected: {', '.join(str(v) for v in WORD_COUNT_ALL)} words",
                    f"obtained: {size} words"
                )
                LOGGER.error(" | ".join(args))
                raise ValueError(*args)

            entropy_size = ENTROPY_SIZE_RANGE[WORD_COUNT_ALL.index(size)] // 8  # bytes
            token = secrets.token_bytes(entropy_size)
        except Exception as e:
            e.args = (
                "invalid mnemonic size",
                *e.args
            )
            LOGGER.error(" | ".join(e.args))
            raise e.with_traceback(e.__traceback__)

        return Mnemonic(token)

    @property
    def checksum(self) -> int:
        """
        Calculates the checksum.
        :return:
        """
        entropy_size = len(self._entropy) * 8  # bits
        checksum_size = CHECKSUM_SIZE_ALL[ENTROPY_SIZE_RANGE.index(entropy_size)]

        entropy_hash = hashlib.sha256(self._entropy).digest()
        return entropy_hash[0] >> (8 - checksum_size)

    @property
    def entropy(self) -> bytes:
        """
        Returns the entropy.
        :return:
        """
        return self._entropy

    @property
    def info(self) -> dict:
        """
        Provides a dict representation of this instance.
        :return:
        """
        return {
            "entropy": self._entropy.hex(),
            "checksum": hex(self.checksum)[2:],
            "value": {key + 1: entropy for key, entropy in enumerate(self.value)}
        }

    @property
    def value(self) -> Tuple[str]:
        """
        Returns the list of words.
        :return:
        """
        entropy_size = len(self._entropy) * 8  # bits
        word_count, checksum_size = [
           (w, c) for w, e, c in zip(WORD_COUNT_ALL, ENTROPY_SIZE_RANGE, CHECKSUM_SIZE_ALL) if e == entropy_size
        ][0]

        sequence = (int.from_bytes(self._entropy, byteorder="big") << checksum_size) | self.checksum

        return tuple([
            str(
                wordlist[
                    sequence >> ((word_count - i - 1) * WORD_SIZE) & (2 ** WORD_SIZE - 1)
                    ]
            ) for i in range(word_count)
        ])

    def encode(self, passphrase: str = "") -> bytes:
        """
        Generates the seed, encoding the mnemonic with an optional passphrase.
        :param passphrase: an optional passphrase
        :return:
        """
        passphrase = normalize_string(passphrase)
        return hashlib.pbkdf2_hmac(
            "sha512",
            bytes(" ".join(self.value), 'utf-8'),
            bytes("mnemonic" + passphrase, 'utf-8'), 2048
        )

    def transform(self, transformation: Transformation) -> "Mnemonic":
        """
        A function to transform (or restore) the entropy that can be used to create some side-mnemonics hiding the
        original.
        :param transformation: the transformation to apply
        :return:
        """
        return Mnemonic(transformation(self._entropy))
