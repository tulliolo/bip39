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
from enum import Enum


class Transformation(Enum):
    """
    A class implementing some bitwise, reversible, transformation algorithms; the supported algorithms are:

    - NEGATIVE (DEFAULT): inverts all bits, like in a negative;
    - MIRROR: reads all bits from right to left, like in front of a mirror.
    """
    NEGATIVE = DEFAULT = "negative"
    MIRROR = "mirror"

    @property
    def description(self) -> str:
        """
        A description of the current instance.
        :return:
        """
        return (
            "inverts all bits, like in a negative"
            if self == Transformation.NEGATIVE else
            "reads all bits from right to left, like in front of a mirror"
        )

    def __call__(self, value: bytes) -> bytes:
        """
        Applies the current transformation
        :param value:
        :return:
        """
        size = len(value) * 8  # bits
        value = int.from_bytes(value, byteorder="big")

        return (
            (2**size - value - 1).to_bytes(size // 8, byteorder='big')
            if self == Transformation.NEGATIVE else
            int(
                bin(value)[2:].zfill(size)[::-1], 2
            ).to_bytes(size // 8, byteorder='big')
        )
