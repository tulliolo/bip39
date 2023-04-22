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
import sys

from generator.entropy import BetterEntropy
from generator.seed import Seed
from utils import encryption, mnemonic


def __print_header():
    print(
        "**********************\n"
        "** mnemonic_split24 **\n"
        "**********************\n"
        "Splits a 24 words bip39 mnemonic into two 12 words bip39 mnemonics, useful for plausible deniability.\n"
    )


def __mnemonic_split24(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Splits a 24 words bip39 mnemonic into two 12 words bip39 mnemonics, "
                    "useful for plausible deniability."
    )
    parser.add_argument(
        "-g", "--generate", action="store_true", default=False,
        help="generate a new 24 words mnemonic (default = False)"
    )
    parser.add_argument(
        "-e", "--encryption", action="store", default="0",
        help="encrypt the original entropy with different algorithms (enhance original seed obfuscation)\n"
             "supported algorithms are:\n"
             "0) NONE: no encryption applied (DEFAULT)\n"
             "1) NEGATIVE: invert all bits\n"
             "2) REVERSAL: swap all bits")
    options = parser.parse_args(args)

    __print_header()

    try:
        if not options.encryption.isnumeric() or not int(options.encryption) in range(3):
            raise ValueError("invalid encryption algorithm:\n\t"
                             "expected: 0-2\n\t"
                             f"obtained: '{options.encryption}'")
        if options.generate:
            original_mnemonic = Seed.from_entropy(BetterEntropy.generate()).mnemonic
            print(f"generating a 24 words mnemonic:\n{' '.join(original_mnemonic)}")
        else:
            print("insert a valid 24 words bip39 mnemonic:")
            original_mnemonic = input("mnemonic > ").strip().split()

        print(
            "\nGenerating two 12 words mnemonics for plausible deniability.\n"
            "Please, take note of these mnemonics, together with the encryption algorithm, "
            "in order to rebuild the original 24 words mnemonic:"
        )

        for count, half_mnemonic in enumerate(
                mnemonic.split(original_mnemonic, encryption.Algorithm(int(options.encryption)))
        ):
            print(
                f"mnemonic {'r' if count else 'l'}: {' '.join(half_mnemonic)}"
            )

    except Exception as e:
        print(e)
        print()
        parser.print_usage()
        exit(-1)


if __name__ == "__main__":
    __mnemonic_split24()
