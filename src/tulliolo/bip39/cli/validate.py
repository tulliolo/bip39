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
from tulliolo.bip39.mnemonic import Mnemonic
from tulliolo.bip39.utils.common import normalize_string

PROG = "validate"
HELP = "validate a mnemonic, or correct the last word according to the checksum"


def init_parser(parser: argparse.ArgumentParser):
    """
    Initialize the validator parser
    :param parser: the root parser
    :return:
    """
    parser.add_argument(
        "-f", "--fix-checksum",
        action="store_true",
        help="fix the mnemonic checksum; useful e.g. when the mnemonic was 'manually' generated (e.g. rolling dices)"
    )


@command("validation")
def run_command(options: argparse.Namespace):
    """
    Validates a mnemonic, using the following options:

    - -f, --fix-checksum: if set, corrects the checksum
    (useful when the mnemonic value is 'manually' generated, e.g. by rolling dices)
    :param options: the full list of cli options
    :return:
    """
    print("enter a mnemonic:")
    mnemonic = normalize_string(" ".join(input(prompt).split()))

    result = " ".join(Mnemonic.from_value(mnemonic, options.fix_checksum).value)

    if result == mnemonic:
        print(f"\nvalidation success!")
    else:
        print(f"\nvalidation success... with fixed checksum:\n{result}")
