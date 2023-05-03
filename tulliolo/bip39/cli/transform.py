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
import argparse
import readline

from tulliolo.bip39.cli import __prompt__ as prompt
from tulliolo.bip39.cli.command import command
from tulliolo.bip39.entropy import TransformationAlgorithm
from tulliolo.bip39.utils.common import normalize_string
from tulliolo.bip39.utils.mnemonic import transform, validate

PROG = "transform"
HELP = "transform a mnemonic for plausible deniability"


def init_parser(parser: argparse.ArgumentParser):
    """
    Initializes the transformation parser
    :param parser: the root parser
    :return:
    """
    parser.add_argument(
        "-a", "--algorithm",
        choices=[a.value for a in TransformationAlgorithm],
        default=TransformationAlgorithm.DEFAULT.value,
        help=f"the algorithm to apply on entropy (DEFAULT={TransformationAlgorithm.DEFAULT.value})"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--split",
        action="store_true",
        help="split a 24 words mnemonic in two 12 words mnemonics"
    )
    group.add_argument(
        "-j", "--join",
        action="store_true",
        help="join two 12 words mnemonics in a 24 words mnemonic"
    )


@command("transformation")
def run_command(options: argparse.Namespace):
    """
    Transforms (and rebuilds) a mnemonic using the following options:

    - -a, --algorithm: the transformation algorithm; allowed algorithms are:

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
        mnemonics.append(validate(normalize_string(input(prompt))).value)
    print()

    print(
        "splitting" if options.split else "joining" if options.join else "applying",
        f"{options.algorithm} transformation..."
    )
    result = transform(
        *mnemonics, algorithm=TransformationAlgorithm(normalize_string(options.algorithm)),
        split=options.split, join=options.join
    )

    print("\ntransformation success!")
    print("\n".join(m.value for m in result))
