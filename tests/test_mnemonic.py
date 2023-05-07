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
from typing import Iterable

import pytest

from tests.common import load_data
from tulliolo.bip39.entropy import Entropy, Transformation
from tulliolo.bip39.mnemonic import Mnemonic, WORD_COUNT_ALL
from tulliolo.bip39.utils.common import normalize_string
from tulliolo.bip39.utils.mnemonic import generate, validate, transform

LOGGER = logging.getLogger(__name__)


def format_entropy(value) -> str:
    return hex(value)[2:] if isinstance(value, int) else str(value)


def format_mnemonic(value) -> str:
    return (
        normalize_string(value) if isinstance(value, str) else
        " ".join(value) if isinstance(value, Iterable) else
        value
    )


@pytest.fixture()
def passphrase() -> str:
    return "TREZOR"


class TestStatic:
    @pytest.mark.parametrize("iter_data", enumerate(load_data("vector")))
    def test_static(self, iter_data, passphrase):
        count, vector = iter_data
        count += 1
        LOGGER.info(f"START test static {count}:\n{json.dumps(vector, indent=2)}")

        mnemonic_e = Mnemonic(vector["entropy"])
        LOGGER.info(f"generated mnemonic from entropy:\n{json.dumps(mnemonic_e.info, indent=2)}")

        mnemonic_w = Mnemonic.from_value(vector["mnemonic"])
        LOGGER.info(f"generated mnemonic from words:\n{json.dumps(mnemonic_w.info, indent=2)}")

        assert mnemonic_e == mnemonic_w, (
            "mnemonic objects mismatch",
            "mnemonics generated from entropy and from words does not match"
        )

        value_e = format_entropy(vector["entropy"])
        value_oe = mnemonic_e.entropy.hex()
        value_ow = mnemonic_w.entropy.hex()
        assert value_e == value_oe == value_ow, (
            "entropy value mismatch",
            f"expected: {value_e}",
            f"obtained: {value_oe}, {value_ow}"
        )

        value_e = format_mnemonic(vector["mnemonic"])
        value_oe = " ".join(mnemonic_e.value)
        value_ow = " ".join(mnemonic_w.value)
        assert value_e == value_oe == value_ow, (
            "mnemonic value mismatch",
            f"expected: {value_e}",
            f"obtained: {value_oe}, {value_ow}"
        )

        value_e = vector["rootseed"]
        value_oe = mnemonic_e.encode(passphrase).hex()
        value_ow = mnemonic_w.encode(passphrase).hex()
        assert value_e == value_oe == value_ow, (
            "seed value mismatch",
            f"expected: {value_e}",
            f"obtained: {value_oe}, {value_ow}"
        )

        LOGGER.info(f"STOP  test static {count}")


class TestError:
    @pytest.mark.parametrize("iter_data", enumerate(load_data("error")))
    def test_error(self, iter_data):
        count, vector = iter_data
        count += 1
        LOGGER.info(f"START test error {count}:\n{json.dumps(vector, indent=2)}")

        try:
            mnemonic = Mnemonic.from_value(vector["mnemonic"]) if "mnemonic" in vector else Mnemonic(vector["entropy"])
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


# class TestDynamic:
#     @pytest.mark.parametrize("iter_data", enumerate(WORD_COUNT_ALL))
#     def test_dynamic(self, iter_data):
#         count, size = iter_data
#         count += 1
#         LOGGER.info(f"START test dynamic {count}: {size}")
#
#         mnemonic = generate(size)
#         LOGGER.info(f"generated mnemonic:\n{json.dumps(mnemonic.info, indent=2)}")
#
#         LOGGER.info(f"STOP  test dynamic {count}")
#
#
# class TestError:
#     @pytest.mark.parametrize("iter_data", enumerate(get_error_data("mnemonic")))
#     def test_error(self, iter_data):
#         count, vector = iter_data
#         count += 1
#         LOGGER.info(f"START test error {count}:\n{json.dumps(vector, indent=2)}")
#
#         try:
#             Mnemonic.from_words(vector["mnemonic"])
#             raise ValueError("the test was successful...")
#         except Exception as e:
#             LOGGER.error(" | ".join(e.args))
#             assert e.args[0] == vector["error"], (
#                 "error mismatch\n\t",
#                 f"expected: {vector['error']}",
#                 f"obtained: {e.args[0]}"
#             )
#         finally:
#             LOGGER.info(f"STOP  test error {count}")
#
#
# class TestTransform:
#     @pytest.mark.parametrize("iter_data", enumerate(get_vector_data()))
#     @pytest.mark.parametrize("iter_algorithm", enumerate([algorithm for algorithm in Transformation]))
#     def test_transformation(self, iter_data, iter_algorithm):
#         vcount, vector = iter_data
#         acount, algorithm = iter_algorithm
#         vcount += 1
#
#         mnemonic = validate(vector["mnemonic"])
#         test_dict = {
#             "mnemonic": mnemonic.value,
#             "transformation": algorithm.value
#         }
#         LOGGER.info(f"START test transformation {vcount}.{acount}:\n{json.dumps(test_dict, indent=2)}")
#
#         result = transform(mnemonic.value, algorithm=algorithm)[0]
#         LOGGER.info(f"applied {algorithm.value} transformation: {result.value}")
#
#         result = transform(result.value, algorithm=algorithm)[0]
#         LOGGER.info(f"applied {algorithm.value} transformation: {result.value}")
#
#         assert result == mnemonic, (
#             "mnemonic mismatch!"
#             f"expected: {mnemonic.value}"
#             f"obtained: {result.value}"
#         )
#
#         if len(mnemonic) == max(WORD_COUNT_ALL):
#             result = transform(mnemonic.value, algorithm=algorithm, split=True)
#             LOGGER.info(f"splitting with {algorithm.value} transformation: {' | '.join(m.value for m in result)}")
#
#             result = transform(*[m.value for m in result], algorithm=algorithm, join=True)[0]
#             LOGGER.info(f"joining with {algorithm.value} transformation: {result.value}")
#
#             assert result == mnemonic, (
#                 "mnemonic mismatch!"
#                 f"expected: {mnemonic.value}"
#                 f"obtained: {result.value}"
#             )
#
#         LOGGER.info(f"STOP  test transformation {vcount}.{acount}")
