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

from tulliolo.bip39.entropy import Entropy, ENTROPY_SIZE_RANGE, TransformationAlgorithm
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

        entropy = Entropy.from_value(vector["entropy"])
        LOGGER.info(f"generated entropy: {entropy.value.hex()}")

        assert entropy == vector["entropy"]
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
        LOGGER.info(f"generated entropy: {entropy.value.hex()}")

        LOGGER.info(f"STOP  test dynamic {count}")


class TestError:
    @pytest.mark.parametrize("iter_data", enumerate(get_error_data("entropy")))
    def test_error(self, iter_data):
        count, vector = iter_data
        count += 1
        LOGGER.info(f"START test error {count}:\n{json.dumps(vector, indent=2)}")

        try:
            Entropy.from_value(vector["entropy"])
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
    @pytest.mark.parametrize(
        "iter_data", enumerate([
            (vector, algorithm) for vector in get_vector_data() for algorithm in TransformationAlgorithm
        ])
    )
    def test_transformation(self, iter_data):
        num, (vector, algorithm) = iter_data
        vector["algorithm"] = algorithm.value

        group = num // len(TransformationAlgorithm) + 1
        count = num % len(TransformationAlgorithm)

        LOGGER.info(f"START test transformation {group}.{count}:\n{json.dumps(vector, indent=2)}")

        entropy = Entropy.from_value(vector["entropy"])
        LOGGER.info(f"generated entropy: {entropy.value.hex()}")

        entropy_t = entropy.transform(algorithm)
        LOGGER.info(f"applied {algorithm.value} transformation to entropy: {entropy_t.value.hex()}")

        bin_value = bin(int(entropy.value.hex(), 16))[2:].zfill(len(entropy))
        bin_value_t = bin(int(entropy_t.value.hex(), 16))[2:].zfill(len(entropy_t))

        LOGGER.info(
            "bit representations:\n\t"
            f"{bin_value}\n\t"
            f"{bin_value_t}"
        )

        if algorithm == TransformationAlgorithm.NEGATIVE:
            assert all([
                b != b_t for b, b_t in zip(bin_value, bin_value_t)
            ]), "invalid negative transformation: bits are not inverted"
        elif algorithm == TransformationAlgorithm.MIRROR:
            assert bin_value == bin_value_t[::-1], "invalid reversal transformation: bits are not swapped"

        LOGGER.info(f"STOP  test transformation {group}.{count}")
