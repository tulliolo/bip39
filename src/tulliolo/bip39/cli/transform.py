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
import argparse
import readline

from tulliolo.bip39.cli import __prompt__ as prompt
from tulliolo.bip39.cli.command import command
from tulliolo.bip39.mnemonic import WORD_COUNT_ALL, Mnemonic
from tulliolo.bip39.utils.transformation import Transformation

PROG = "transform"
HELP = "transform (or restore) a mnemonic, e.g. to create side-wallets hiding the original"

WORD_COUNT_SPLIT = [
    wcount for wcount in WORD_COUNT_ALL if not (wcount % 2) and (wcount // 2) in WORD_COUNT_ALL
]
WORD_COUNT_JOIN = [
    wcount for wcount in WORD_COUNT_ALL if (wcount * 2) in WORD_COUNT_ALL
]


def init_parser(parser: argparse.ArgumentParser):
    """
    Initializes the transformation parser
    :param parser: the root parser
    :return:
    """
    parser.add_argument(
        "-t", "--transformation",
        choices=[t.value for t in Transformation],
        default=Transformation.DEFAULT.value,
        help=f"the transformation to apply on entropy (DEFAULT={Transformation.DEFAULT.value})"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--split",
        action="store_true",
        help=f"split a {', '.join(str(wcount) for wcount in WORD_COUNT_SPLIT)} words mnemonic "
             f"in two {', '.join(str(wcount) for wcount in WORD_COUNT_JOIN)} words mnemonics"
    )
    group.add_argument(
        "-j", "--join",
        action="store_true",
        help=f"join two {', '.join(str(wcount) for wcount in WORD_COUNT_JOIN)} words mnemonics "
             f"in a {', '.join(str(wcount) for wcount in WORD_COUNT_SPLIT)} words mnemonic"
    )


@command("transformation")
def run_command(options: argparse.Namespace):
    """
    Transforms (and rebuilds) a mnemonic using the following options:

    - -t, --transformation: the transformation to apply; allowed transformations are:

      - negative: invert all entropy bits, like in a negative
      - mirror: read entropy bits from right to left, like in front of a mirror
    - -s, --split: applies the transformation to a 24 words mnemonic and splits it into two 12 words mnemonics
    - -j, --join: joins two 12 words mnemonics into one 24 words mnemonic and applies the transformation
    :param options: the full list of cli options
    :return:
    """
    mnemonics = []
    for i in range(1 + options.join):
        print(
            "enter",
            "first" if options.join and i == 0 else "second" if options.join and i == 1 else "a",
            "mnemonic"
        )
        mnemonics.append(Mnemonic.from_value(input(prompt)))
    print()

    if options.split and len(mnemonics[0]) not in WORD_COUNT_SPLIT:
        raise ValueError(
            "invalid mnemonic size:",
            f"expected: {', '.join(str(wcount) for wcount in WORD_COUNT_SPLIT)}",
            f"obtained: {len(mnemonics[0])}"
        )

    if options.join and not (
            len(mnemonics[0]) == len(mnemonics[1]) and
            all([len(mnemonic) in WORD_COUNT_JOIN for mnemonic in mnemonics])
    ):
        raise ValueError(
            "invalid mnemonics size:",
            f"both mnemonics must be {', '.join(str(wcount) for wcount in WORD_COUNT_JOIN)} words length"
        )

    print(
        "splitting" if options.split else "joining" if options.join else "applying",
        f"{options.transformation} transformation..."
    )

    result = Mnemonic(mnemonics[0].entropy + mnemonics[1].entropy) if options.join else mnemonics[0]
    result = result.transform(Transformation(options.transformation))

    result = [
        Mnemonic(result.entropy[:len(result.entropy) // 2]),
        Mnemonic(result.entropy[len(result.entropy) // 2:])
    ] if options.split else [result]

    print("\ntransformation success!")
    print("\n".join(" ".join(m.value) for m in result))
