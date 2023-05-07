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
import json
import logging
import pathlib
import pytest

from tests.common import load_data
from tulliolo.bip39.mnemonic import WORD_COUNT_ALL, Mnemonic
from tulliolo.bip39.utils import steganography

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def init_module():
    base_path = str(pathlib.Path(__file__).parent)
    pytest.input_file = pathlib.Path(f"{base_path}/data/test_image.jpg")
    pytest.output_path = pathlib.Path(f"{base_path}/data/output")

    # prepare output path
    if not pytest.output_path.exists():
        pytest.output_path.mkdir()
    for file in [f for f in pytest.output_path.iterdir() if f.is_file()]:
        file.unlink()


def run_test(
        vcount, dcount, test_type,
        mnemonic, direction
):
    output_file = None

    try:
        test_dict = {
            "mnemonic": mnemonic,
            "direction": direction.value
        }
        LOGGER.info(f"START test {test_type} {vcount}.{dcount}:\n{json.dumps(test_dict, indent=2)}")

        output_file = steganography.encode(
            mnemonic,
            pytest.input_file,
            pytest.output_path,
            direction
        )
        result = steganography.decode(
            output_file,
            direction
        ).decode("utf-8")

        assert result == mnemonic, (
            "mnemonic does not match!",
            f"expected: {mnemonic}"
            f"obtained: {result}"
        )

    finally:
        if output_file:
            output_file.unlink()

        LOGGER.info(f"STOP  test {test_type} {vcount}.{dcount}")


class TestStatic:
    @pytest.mark.parametrize("iter_direction", enumerate([direction for direction in steganography.Direction]))
    @pytest.mark.parametrize("iter_data", enumerate(load_data("vector")))
    def test_static(self, iter_direction, iter_data):
        vcount, vector = iter_data
        dcount, direction = iter_direction
        vcount += 1

        vector["direction"] = direction.value
        mnemonic = " ".join(Mnemonic(vector["entropy"]).value)

        run_test(
            vcount, dcount, "static",
            mnemonic, direction
        )


class TestDynamic:
    @pytest.mark.parametrize("iter_direction", enumerate([direction for direction in steganography.Direction]))
    @pytest.mark.parametrize("iter_data", enumerate(WORD_COUNT_ALL))
    def test_static(self, iter_direction, iter_data):
        vcount, size = iter_data
        dcount, direction = iter_direction
        vcount += 1

        mnemonic = " ".join(Mnemonic.generate(size).value)

        run_test(
            vcount, dcount, "dynamic",
            mnemonic, direction
        )
