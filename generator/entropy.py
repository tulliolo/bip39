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
import hashlib
import secrets

SHA256_ROUNDS = 2048  # sha256 rounds (number)

PASS_SIZE = 32  # bytes
SALT_SIZE = 16  # bytes


class Entropy:
    @classmethod
    def generate(cls, size) -> int:
        return secrets.SystemRandom().getrandbits(size)


class BetterEntropy(Entropy):
    @classmethod
    def generate(cls, size=None) -> bytes:
        return hashlib.pbkdf2_hmac(
            'sha256',
            secrets.SystemRandom().randbytes(PASS_SIZE),
            secrets.SystemRandom().randbytes(SALT_SIZE),
            SHA256_ROUNDS
        )
