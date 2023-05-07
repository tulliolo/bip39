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
import getpass
import pathlib

from tulliolo.bip39.cli import __prompt__ as prompt
from tulliolo.bip39.cli.command import command
from tulliolo.bip39.mnemonic import Mnemonic
from tulliolo.bip39.utils import encryption
from tulliolo.bip39.utils.common import normalize_string
from tulliolo.bip39.utils.steganography import Direction, encode, decode

PROG = "steganography"
HELP = "hide/reveal a mnemonic with steganography"


@command("encoding")
def __run_encode(options: argparse.Namespace):
    """
    Uses steganography to encode a mnemonic in an image file;
    allowed options are:

    - -i, --input-file: an input file containing an image
    - -o, --output-path: the output path where to save the encoded image
    - -r, --read-direction: the traversing direction for image pixels; it can be:

      - horizontal (DEFAULT): pixels are traversed from left to right, starting from top
      - vertical: pixels are traversed from top to bottom, starting from left
      - reverse-horizontal: pixels are traversed from right to left, starting from bottom
      - reverse-vertical: pixels are traversed from bottom to top, starting from right
    :param options: the full list of cli options
    :return:
    """
    print("enter a mnemonic:")
    mnemonic = " ".join(Mnemonic.from_value(input(prompt)).value)

    print("\nenter a password to encrypt the mnemonic (or leave blank):")
    password = getpass.getpass(prompt=prompt)
    if password:
        print("insert again...:")
        if password != getpass.getpass(prompt=prompt):
            raise ValueError("password did not match!")
        print("encrypting mnemonic...")
        mnemonic = encryption.encrypt(mnemonic, password)

    print("\nencoding image...")
    output_file_name = encode(
        mnemonic,
        options.input_file, options.output_path,
        Direction(normalize_string(options.read_direction))
    )

    print(f"\nencoding success!\n{output_file_name}")


@command("decoding")
def __run_decode(options: argparse.Namespace):
    """
    Uses steganography to decode a mnemonic from an image file;
    allowed options are:

    - -i, --input-file: an image file containing an encoded mnemonic
    - -r, --read-direction: the traversing direction for image pixels; it can be:

      - horizontal (DEFAULT): pixels are traversed from left to right, starting from top
      - vertical: pixels are traversed from top to bottom, starting from left
      - reverse-horizontal: pixels are traversed from right to left, starting from bottom
      - reverse-vertical: pixels are traversed from bottom to top, starting from right
    :param options: the full list of cli options
    :return:
    """
    print("\nenter a password to decrypt the mnemonic (or leave blank):")
    password = getpass.getpass(prompt=prompt)
    if password:
        print("insert again...:")
        if password != getpass.getpass(prompt=prompt):
            raise ValueError("password did not match!")

    print("\ndecoding image...")
    mnemonic = decode(
        options.input_file,
        Direction(normalize_string(options.read_direction))
    )

    if mnemonic:
        print(f"decoding success!")
        if password:
            print("\ndecrypting mnemonic...")
            mnemonic = encryption.decrypt(mnemonic, password)
            print(f"decrypting success!")

        print(mnemonic.decode("utf-8"))
    else:
        raise ValueError("cannot find a message")


def init_parser(parser: argparse.ArgumentParser):
    """
    Initializes the steganography parser
    :param parser: the root parser
    :return:
    """
    subparsers = parser.add_subparsers(dest="subcommand", required=True, help="list of sub-commands")
    eparser = subparsers.add_parser("encode", help="hide a mnemonic in an image with steganography")
    dparser = subparsers.add_parser("decode", help="reveal a mnemonic in an image with steganography")

    eparser.add_argument(
        "-i", "--input-file",
        type=argparse.FileType('rb'),
        required=True,
        help=f"the source image file"
    )
    dparser.add_argument(
        "-i", "--input-file",
        type=argparse.FileType('rb'),
        required=True,
        help=f"the source image file"
    )
    eparser.add_argument(
        "-o", "--output-path",
        type=pathlib.Path,
        default=".",
        help=f"the destination path (DEFAULT is the current path)"
    )
    eparser.add_argument(
        "-r", "--read-direction",
        choices=[direction.value for direction in Direction],
        default=Direction.DEFAULT.value,
        help=f"traverse the image pixels in different directions (DEFAULT={Direction.DEFAULT.value})"
    )
    dparser.add_argument(
        "-r", "--read-direction",
        choices=[direction.value for direction in Direction],
        default=Direction.DEFAULT.value,
        help=f"traverse the image pixels in different directions (DEFAULT={Direction.DEFAULT.value})"
    )


def run_command(options: argparse.Namespace):
    """
    Uses steganography to hide or reveal a message; allowed options are:

    - -e, --encode: encode a mnemonic (optionally encrypted with a password) in an image file
    - -d --decode: decode a mnemonic (optionally encrypted with a password) from an image file
    :param options: the full list of cli options
    :return:
    """
    if options.subcommand == "encode":
        __run_encode(options)
    else:
        __run_decode(options)
