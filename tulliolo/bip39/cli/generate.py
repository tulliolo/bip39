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

from tulliolo.bip39.cli.command import command
from tulliolo.bip39.mnemonic import WORD_COUNT_ALL
from tulliolo.bip39.utils.mnemonic import generate

PROG = "generate"
HELP = "generate a mnemonic"


def init_parser(parser: argparse.ArgumentParser):
    """
    Initializes the generator parser.
    :param parser: the root parser
    :return:
    """
    parser.add_argument(
        "-s", "--size",
        type=int,
        choices=WORD_COUNT_ALL,
        default=min(WORD_COUNT_ALL),
        help=f"the number of words to be generated (DEFAULT={min(WORD_COUNT_ALL)})"
    )


@command("generate")
def run_command(options: argparse.Namespace):
    """
    Generates a new mnemonic using the following options:

    - -s, --size: the length of the mnemonic (DEFAULT=12)
    :param options: the full list of cli options
    :return:
    """
    print(f"generating a {options.size} words mnemonic...")
    mnemonic = generate(options.size)
    print("\ngenerate success!")
    print(mnemonic.value)
