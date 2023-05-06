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
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
import json
import logging
import pytest

from tulliolo.bip39.entropy import Entropy, ENTROPY_SIZE_RANGE, Transformation
from common import get_vector_data, get_error_data

LOGGER = logging.getLogger(__name__)


def format_value(value) -> str:
    return hex(value)[2:] if isinstance(value, int) else str(value)


class TestStatic:
    @pytest.mark.parametrize("iter_data", enumerate(get_vector_data()))
    def test_static(self, iter_data):
        count, vector = iter_data
        count += 1
        LOGGER.info(f"START test static {count}:\n{json.dumps(vector, indent=2)}")

        entropy = Entropy(vector["entropy"])
        LOGGER.info(f"generated entropy:\n{json.dumps(entropy.info, indent=2)}")

        hex_value = format_value(vector["entropy"])
        assert entropy.value.hex() == hex_value

        LOGGER.info(f"STOP  test static {count}")


class TestDynamic:
    @pytest.mark.parametrize("iter_data", enumerate(ENTROPY_SIZE_RANGE))
    def test_dynamic(self, iter_data):
        count, size = iter_data
        count += 1
        LOGGER.info(f"START test dynamic {count}: {size}")

        entropy = Entropy.generate(size)
        LOGGER.info(f"generated entropy:\n{json.dumps(entropy.info, indent=2)}")

        LOGGER.info(f"STOP  test dynamic {count}")


class TestError:
    @pytest.mark.parametrize("iter_data", enumerate(get_error_data("entropy")))
    def test_error(self, iter_data):
        count, vector = iter_data
        count += 1
        LOGGER.info(f"START test error {count}:\n{json.dumps(vector, indent=2)}")

        try:
            Entropy(vector["entropy"])
            raise ValueError("the test was successful...")
        except Exception as e:
            LOGGER.error(" | ".join(e.args))
            assert e.args[0] == vector["error"], (
                "error mismatch\n\t",
                f"expected: {vector['error']}",
                f"obtained: {e.args[0]}"
            )
        finally:
            LOGGER.info(f"STOP  test error {count}")


class TestTransformation:
    @pytest.mark.parametrize("iter_transformation", enumerate((
            transformation for transformation in Transformation
    )))
    @pytest.mark.parametrize("iter_data", enumerate(get_vector_data()))
    def test_transformation(self, iter_transformation, iter_data):
        vcount, vector = iter_data
        tcount, transformation = iter_transformation
        vcount += 1

        vector["transformation"] = transformation.value

        LOGGER.info(f"START test transformation {vcount}.{tcount}:\n{json.dumps(vector, indent=2)}")

        entropy_o = Entropy(vector["entropy"])
        LOGGER.info(f"generated entropy:\n{json.dumps(entropy_o.info, indent=2)}")

        entropy_t = entropy_o.transform(transformation)
        LOGGER.info(
            f"applied {transformation.value} transformation to entropy:\n"
            f"{json.dumps(entropy_t.info, indent=2)}"
        )

        entropy_t = entropy_t.transform(transformation)
        LOGGER.info(
            f"applied {transformation.value} transformation to entropy:\n"
            f"{json.dumps(entropy_t.info, indent=2)}"
        )

        assert entropy_o == entropy_t
