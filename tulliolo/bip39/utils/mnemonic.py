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
A collection of utils for bip39 mnemonics.
"""
import logging
from typing import Iterable

from tulliolo.bip39.entropy import ENTROPY_SIZE_STEP, Entropy, TransformationAlgorithm
from tulliolo.bip39.mnemonic import WORD_SIZE, Mnemonic, WORD_COUNT_ALL
from tulliolo.bip39.utils.common import normalize_string

LOGGER = logging.getLogger(__name__)


def generate(size: int) -> Mnemonic:
    """
    Generates a mnemonic.
    :param size: the desired number of words
    :return: a new mnemonic instance
    """
    size = (int(size) * WORD_SIZE // ENTROPY_SIZE_STEP) * ENTROPY_SIZE_STEP
    return Mnemonic.from_entropy(Entropy.generate(size))


def transform(
        *mnemonics: str, algorithm: TransformationAlgorithm, split: bool = False, join: bool = False
) -> tuple[Mnemonic]:
    """
    Transforms a mnemonic; supported transformation algorithms are:

    - negative: invert all entropy bits, like in a negative;
    - mirror: read entropy bits from right to left, like in front of a mirror.
    :param mnemonics: a list of 1 or 2 (only for join) mnemonics
    :param algorithm: the transformation algorithm
    :param split: applies transformation on a 24 words mnemonic and then splits it in two 12 words mnemonics
    :param join: joins two 12 words mnemonics in a 24 words mnemonic and then applies transformation
    :return: the resulting 1 or 2 (only for split) mnemonics
    """
    if split:
        if len(mnemonics) > 1:
            LOGGER.warning(
                "too many mnemonic values, extra arguments will be ignored | "
                f"expected: 1 | obtained: {len(mnemonics)}")

        mnemonic = mnemonics[0].split()
        if len(mnemonic) != max(WORD_COUNT_ALL):
            LOGGER.error("invalid mnemonic size")
            raise ValueError(
                "invalid mnemonic size",
                f"expected: {max(WORD_COUNT_ALL)}",
                f"obtained: {len(mnemonic)}"
            )

        entropy = Mnemonic.from_value(mnemonic).entropy.transform(algorithm).value
        size = len(entropy) // 2

        result = [
            Mnemonic.from_entropy(e) for e in [
                Entropy.from_value(entropy[:size]),
                Entropy.from_value(entropy[size:])
            ]
        ]

    elif join:
        if len(mnemonics) < 2:
            LOGGER.error("too few mnemonic values")
            raise ValueError(
                "too few mnemonic values",
                "expected: 2",
                f"obtained: {len(mnemonics)}"
            )

        if len(mnemonics) > 2:
            LOGGER.warning(
                "too many mnemonic values, extra arguments will be ignored | "
                f"expected: 2 | obtained: {len(mnemonics)}")

        mnemonics = mnemonics[:2]
        entropy = bytes(0)
        for mnemonic in mnemonics:
            mnemonic = mnemonic.split()
            if len(mnemonic) != min(WORD_COUNT_ALL):
                LOGGER.error("invalid mnemonic size")
                raise ValueError(
                    "invalid mnemonic size",
                    f"expected: {min(WORD_COUNT_ALL)}",
                    f"obtained: {len(mnemonic)}"
                )
            entropy += Mnemonic.from_value(mnemonic).entropy.value

        result = [
            Mnemonic.from_entropy(
                Entropy.from_value(entropy).transform(algorithm)
            )
        ]

    else:
        if len(mnemonics) > 1:
            LOGGER.warning(
                "too many mnemonic values, extra arguments will be ignored | "
                f"expected: 1 | obtained: {len(mnemonics)}")

        result = [
            Mnemonic.from_entropy(
                Mnemonic.from_value(mnemonics[0]).entropy.transform(algorithm)
            )
        ]

    return tuple(result)


def validate(mnemonic: str | bytes | bytearray | Iterable[str], fix_checksum: bool = False) -> Mnemonic:
    """
    Validates a mnemonic value.
    :param mnemonic: the mnemonic value to be validated
    :param fix_checksum: if set, corrects the checksum
    (useful when the mnemonic value is 'manually' generated, e.g. by rolling dices)
    :return: the valid mnemonic
    """
    return Mnemonic.from_value(mnemonic, fix_checksum)
