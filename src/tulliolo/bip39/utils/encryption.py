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
Some encryption utilities.
"""
import base64
import hashlib
import logging

from cryptography.fernet import Fernet

LOGGER = logging.getLogger(__name__)


def encrypt(message: str | bytes, password: str) -> bytes:
    """
    Encrypts a message with a password.
    :param message: the message, in string or bytes
    :param password: the password
    :return: the encrypted message
    """
    if not password:
        raise ValueError("password cannot be empty")
    if isinstance(message, str):
        message = bytes(message, 'utf-8')

    key = base64.urlsafe_b64encode(hashlib.sha256(bytes(password, 'utf-8')).digest())
    f = Fernet(key)
    return f.encrypt(message)


def decrypt(message: str | bytes, password: str) -> bytes:
    """
    Decrypts a message with a password.
    :param message: the message, in string or bytes
    :param password: the password
    :return: the decrypted message
    """
    if not password:
        raise ValueError("password cannot be empty")
    if isinstance(message, str):
        message = bytes(message, 'utf-8')

    key = base64.urlsafe_b64encode(hashlib.sha256(bytes(password, 'utf-8')).digest())
    f = Fernet(key)
    message = f.decrypt(message)

    return message
