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

from generator import seed
from generator.entropy import Entropy
from generator.seed import Seed
from utils import encryption


def __print_header():
    print(
        "************************\n"
        "** mnemonic_transform **\n"
        "************************\n"
        "Turns a 12/15/18/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, "
        "useful for plausible deniability.\n"
        "Transformation is reversible running the same tool, with the same parameters.\n"
    )


def __mnemonic_transform(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Splits a 24 words bip39 mnemonic into two 12 words bip39 mnemonics, "
                    "useful for plausible deniability.\n"
                    "Transformation is reversible running the same tool, with the same parameters."
    )
    parser.add_argument(
        "-g", "--generate", action="store", default="0",
        help="generate a new n words mnemonic (DEFAULT n = 0 -> NO GENERATION)\n"
             f"supported numbers of words are: "
             f"{', '.join(str(num) for num in seed.WORD_COUNT_ALL)}"
    )
    parser.add_argument(
        "-e", "--encryption", action="store", default="0",
        help="encrypt the original entropy with different algorithms (enhance original seed obfuscation)\n"
             "supported algorithms are:\n"
             "0) NEGATIVE (DEFAULT): invert all bits\n"
             "1) REVERSAL: swap all bits")
    options = parser.parse_args(args)

    __print_header()

    try:
        if not options.encryption.isnumeric() or not int(options.encryption) in range(2):
            raise ValueError("invalid encryption algorithm:\n\t"
                             "expected: 0-1\n\t"
                             f"obtained: {options.encryption}")
        if not (
                options.generate.isnumeric() and int(options.generate) in [0, *seed.WORD_COUNT_ALL]
        ):
            raise ValueError("invalid number of words:\n\t"
                             f"expected: 0, {', '.join(str(num) for num in seed.WORD_COUNT_ALL)}\n\t"
                             f"obtained: {options.generate}")

        wcount = int(options.generate)

        if wcount > 0:
            original_seed = Seed.from_entropy(
                Entropy.generate(int(options.generate) * seed.WORD_SIZE // 8 * 8)
            )
            original_entropy = original_seed.entropy
            print(f"generating a {options.generate} words mnemonic:\n{' '.join(original_seed.mnemonic)}")
        else:
            print("insert a valid bip39 mnemonic:")
            original_mnemonic = input("mnemonic > ").strip().split()
            original_entropy = Seed.from_mnemonic(original_mnemonic).entropy
            wcount = len(original_mnemonic)

        print(
            f"\nGenerating a new {wcount} words mnemonics for plausible deniability.\n"
            "Please, take note of this mnemonics, together with the encryption algorithm, "
            "in order to rebuild the original mnemonic:"
        )

        algorithm = encryption.Algorithm.NEGATIVE if int(options.encryption) == 0 else encryption.Algorithm.REVERSAL
        entropy = encryption.encrypt(original_entropy, algorithm)
        mnemonic = Seed.from_entropy(entropy).mnemonic
        print(f"\nmnemonic: {' '.join(mnemonic)}")

    except Exception as e:
        print(e)
        print()
        parser.print_usage()
        exit(-1)


if __name__ == "__main__":
    __mnemonic_transform()
