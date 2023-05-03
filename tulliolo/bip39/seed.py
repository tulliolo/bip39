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
A module implementing the seed as defined in bip39 specs:

https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
"""
import hashlib
import logging

from tulliolo.bip39.mnemonic import Mnemonic

LOGGER = logging.getLogger(__name__)


class Seed:
    """
    The seed, as defined in bip39 specs:

    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#from-mnemonic-to-seed
    """
    def __init__(self, mnemonic: Mnemonic, passphrase: str = ""):
        """
        Builds a new seed instance.
        :param mnemonic: the mnemonic
        :param passphrase: an optional passphrase
        """
        if not isinstance(mnemonic, Mnemonic):
            LOGGER.error("invalid mnemonic type")
            raise TypeError(
                "invalid mnemonic type",
                f"expected: {Mnemonic}",
                f"obtained: {type(mnemonic)}"
            )

        self._mnemonic = mnemonic
        self._passphrase = str(passphrase)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Seed):
            LOGGER.warning(f"'{other}' is not of type {Seed}")
            return False

        return self._mnemonic == other._mnemonic and self._passphrase == other._passphrase

    @property
    def mnemonic(self) -> Mnemonic:
        """
        The mnemonic.
        :return:
        """
        return self._mnemonic

    @property
    def value(self) -> bytes:
        """
        The seed (encoded) value.
        :return:
        """
        return hashlib.pbkdf2_hmac('sha512',
                                   bytes(self._mnemonic.value, 'utf-8'),
                                   bytes('mnemonic' + self._passphrase, 'utf-8'), 2048)

    @property
    def info(self) -> dict:
        """
        A descriptor for this seed instance.
        :return:
        """
        return {
            "mnemonic": self._mnemonic.value,
            "passphrase": self._passphrase
        }
