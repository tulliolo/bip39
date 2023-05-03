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
Main module for bip39-cli implementation.
"""
import argparse
import sys

from tulliolo.bip39 import __version__ as version
from tulliolo.bip39.cli import generate, validate, transform, steganography

HEADER = (
        "*" * len(f"* bip39-cli v{version} *") +
        f"\n* bip39-cli v{version} *\n" +
        "*" * len(f"* bip39-cli v{version} *") + "\n"
)


def main(args=None):
    """
    Initializes the cli and launches commands
    :param args:
    :return:
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"{HEADER}A collection of bip39 tools"
    )
    parser.add_argument(
        "-v", "--version",
        action="version", version=f"%(prog)s v{version}",
        help="show the version and exit"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="list of commands")
    generate.init_parser(
        subparsers.add_parser(generate.PROG, help=generate.HELP)
    )
    steganography.init_parser(
        subparsers.add_parser(steganography.PROG, help=steganography.HELP)
    )
    transform.init_parser(
        subparsers.add_parser(transform.PROG, help=transform.HELP)
    )
    validate.init_parser(
        subparsers.add_parser(validate.PROG, help=validate.HELP)
    )

    options = parser.parse_args(args)
    print(HEADER)

    if options.command == generate.PROG:
        code = generate.run_command(options)
    elif options.command == steganography.PROG:
        code = steganography.run_command(options)
    elif options.command == transform.PROG:
        code = transform.run_command(options)
    elif options.command == validate.PROG:
        code = validate.run_command(options)
    else:
        raise NotImplemented(f"command {options.command} not implemented")

    exit(code)


if __name__ == "__main__":
    main()
