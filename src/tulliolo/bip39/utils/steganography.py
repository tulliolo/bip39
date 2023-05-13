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
"""
Some utilities to hide/reveal messages in images with a steganograpy algorithm.
"""
from __future__ import annotations

import enum
import logging
import math
import operator
import pathlib
import time
from io import FileIO
from typing import Tuple, Iterable

from PIL import Image

LOGGER = logging.getLogger(__name__)


Coordinates = Tuple[int, int]
Pixel = Tuple[int, int, int]


class Direction(enum.Enum):
    """
    The direction used to traverse the image pixels:

    - horizontal: from left to right, starting from top;
    - vertical: from top to bottom, starting from left;
    - reverse_horizontal: from right to left, starting from bottom;
    - reverse_vertical: from bottom to top, starting from right.
    """
    HORIZONTAL = DEFAULT = "horizontal"
    VERTICAL = "vertical"
    REVERSE_HORIZONTAL = "reverse-horizontal"
    REVERSE_VERTICAL = "reverse-vertical"

    @property
    def description(self) -> str:
        """
        Returns a description of the current instance.
        :return: the description string
        """
        return (
            "from left to right, starting from top" if self == Direction.HORIZONTAL else
            "from top to bottom, starting from left" if self == Direction.VERTICAL else
            "from right to left, starting from bottom" if self == Direction.REVERSE_HORIZONTAL else
            "from bottom to top, starting from right"
        )


def __get_modified_pixels(image: Image, message: bytes, direction: Direction) -> Iterable[
    Tuple[Coordinates, Pixel, Pixel]
]:
    """
    Traverses the image and returns the modified pixels.
    :param image: the image
    :param message: the message to be hidden
    :param direction: the traversing direction for the image pixels
    :return: a generator of pixel coordinate, original pixel, modified pixel
    """
    image_size = operator.mul(*image.size)  # pixels
    message_size = len(message) * 3  # pixels

    if image_size < message_size:
        LOGGER.error("invalid size")
        raise ValueError(
            "invalid size",
            "message is too long for this image"
        )

    # encode message
    for i, value in enumerate(message):
        for j in range(3):
            ordinal = 3 * i + j
            coordinates, pixel = __get_pixel(image, direction, ordinal)
            yield coordinates, pixel, \
                tuple(
                    (pixel[k] & (2 ** 8 - 2)) | ((value >> (7 - ((ordinal % 3) * 3 + k))) & 1)
                    if (ordinal % 3) * 3 + k < 8 else
                    (pixel[k] & (2 ** 8 - 2)) | 1 if i < (len(message) - 1) else
                    pixel[k] & (2 ** 8 - 2)
                    for k in range(3)
                )


def __get_pixel(image: Image, direction: Direction, ordinal: int) -> Tuple[Coordinates, Pixel]:
    """
    Gets the nth pixel in the desired direction.
    :param image: the image
    :param direction: the traversing direction for the image pixels
    :param ordinal: the pixel ordinal
    :return: the pixel with its coordinates
    """
    image_size = operator.mul(*image.size)  # pixels
    image_width = image.size[0]  # pixels
    image_height = image.size[1]  # pixels

    index = (
        ordinal if direction == Direction.HORIZONTAL else
        ((ordinal * image_width) + (ordinal // image_height)) % image_size if direction == Direction.VERTICAL else
        (image_size - ordinal - 1) % image_size if direction == Direction.REVERSE_HORIZONTAL else
        (((image_size - ordinal - 1) * image_width) + (image_size - ordinal - 1) // image_height) % image_size
    )

    coordinates = (index % image_width, index // image_width)
    return coordinates, image.getpixel(coordinates)


def encode(
        message: str | bytes,
        input_file: FileIO | pathlib.Path | str,
        output_path: pathlib.Path | str,
        direction: Direction = Direction.DEFAULT
) -> pathlib.Path:
    """
    Hides a message in an image with steganography.
    :param message: the message
    :param input_file: the input (image) file
    :param output_path: the output path
    :param direction: the traversing direction for the image pixels
    :return: the output (image) file
    """
    if isinstance(message, str):
        message = bytes(message, 'utf-8')

    if isinstance(output_path, str):
        output_path = pathlib.Path(output_path)
    if not output_path.exists():
        output_path.mkdir()

    with Image.open(input_file, mode='r') as input_image:
        input_file_name = input_file.name.split('/')[-1].split('.')[0]
        output_file = pathlib.Path(
            f"{str(output_path)}/"
            f"{input_file_name}_"
            f"{direction.value}_"
            f"{time.strftime('%Y%m%d-%H%M%S')}.png"
        )

        output_image = input_image.copy()
        LOGGER.debug(f"modifying pixels {direction.description}")
        LOGGER.debug("coordinates, original pixel -> modified pixel")
        for coordinates, original_pixel, modified_pixel in __get_modified_pixels(input_image, message, direction):
            LOGGER.debug(f"{coordinates}, {original_pixel} -> {modified_pixel}")
            output_image.putpixel(coordinates, modified_pixel)

        output_image.save(output_file)
        return output_file


def decode(
        input_file: FileIO | pathlib.Path | str,
        direction: Direction = Direction.DEFAULT
) -> bytes:
    """
    Reveals a message hidden in an image.
    :param input_file: the input (image) file carrying the hidden message
    :param direction: the traversing direction for the image pixels
    :return: the message bytes (or 0 if not found)
    """
    with Image.open(input_file, mode='r') as image:
        image_size = operator.mul(*image.size)  # pixels

        i = 0
        goon = True
        message = 0
        message_size = 0
        LOGGER.debug("coordinates -> pixel")
        while goon and i < image_size - 1:
            coordinates, pixel = __get_pixel(image, direction, i)
            LOGGER.debug(f"{coordinates} -> {pixel}")

            for j in range(3):
                message, message_size, goon = ((message << 1) | (pixel[j] & 1), message_size + 1, True) \
                    if (i % 3) * 3 + j < 8 else (message, message_size, True) \
                    if (pixel[j] & 1) else (message, message_size, False)

            i += 1

        if goon:
            LOGGER.warning("cannot find an hidden message")
            message = 0
        else:
            LOGGER.debug(f"found an encrypted {message_size} bytes length message")
            message = message.to_bytes(math.ceil(message_size / 8), byteorder='big')

        return message
