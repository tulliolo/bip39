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
import secrets
import string
from typing import Iterable

import pytest

from tests.common import load_data
from tulliolo.bip39.entropy import Transformation
from tulliolo.bip39.mnemonic import Mnemonic, WORD_COUNT_ALL
from tulliolo.bip39.utils.common import normalize_string

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

@pytest.fixture
def random_passphrase() -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for i in range(12))


class TestStatic:
    @pytest.mark.parametrize("iter_transformation", enumerate([None, Transformation.NEGATIVE, Transformation.MIRROR]))
    @pytest.mark.parametrize("iter_data", enumerate(load_data("vector")))
    def test_static(self, iter_transformation, iter_data, passphrase):
        vcount, vector = iter_data
        tcount, transformation = iter_transformation
        vcount += 1

        if transformation:
            vector["transformation"] = transformation.value
        LOGGER.info(f"START test static {vcount}.{tcount}:\n{json.dumps(vector, indent=2)}")

        mnemonic_e = Mnemonic(vector["entropy"])
        LOGGER.info(f"generated mnemonic from entropy:\n{json.dumps(mnemonic_e.info, indent=2)}")

        mnemonic_w = Mnemonic.from_value(vector["mnemonic"])
        LOGGER.info(f"generated mnemonic from value:\n{json.dumps(mnemonic_w.info, indent=2)}")

        if transformation:
            for i in range(2):
                mnemonic_e = mnemonic_e.transform(transformation)
                LOGGER.info(
                    f"applied {'first' if i == 0 else 'second'} "
                    f"{transformation} transformation to mnemonic from entropy:\n"
                    f"{json.dumps(mnemonic_e.info, indent=2)}"
                )

                mnemonic_w = mnemonic_w.transform(transformation)
                LOGGER.info(
                    f"applied {'first' if i == 0 else 'second'} "
                    f"{transformation} transformation to mnemonic from value:\n"
                    f"{json.dumps(mnemonic_w.info, indent=2)}"
                )

        assert mnemonic_e == mnemonic_w, (
            "mnemonic objects mismatch",
            "mnemonics generated from entropy and from value does not match"
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

        LOGGER.info(f"STOP  test static {vcount}.{tcount}")


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


class TestDynamic:
    @pytest.mark.parametrize("iter_transformation", enumerate([None, Transformation.NEGATIVE, Transformation.MIRROR]))
    @pytest.mark.parametrize("iter_data", enumerate(WORD_COUNT_ALL))
    def test_dynamic(self, iter_transformation, iter_data, random_passphrase):
        scount, size = iter_data
        tcount, transformation = iter_transformation
        scount += 1

        LOGGER.info(
            f"START test dynamic {scount}.{tcount}: {size}.{transformation.value if transformation else 'none'}"
        )

        mnemonic = Mnemonic.generate(size)
        LOGGER.info(f"generated mnemonic:\n{json.dumps(mnemonic.info, indent=2)}")

        if transformation:
            mnemonic_t = mnemonic
            for i in range(2):
                mnemonic_t = mnemonic_t.transform(transformation)
                LOGGER.info(
                    f"applied {'first' if i == 0 else 'second'} "
                    f"{transformation} transformation to mnemonic from entropy:\n"
                    f"{json.dumps(mnemonic_t.info, indent=2)}"
                )

            assert mnemonic == mnemonic_t and mnemonic.info == mnemonic_t.info, (
                "mnemonic mismatch",
                f"expected: {mnemonic.value}"
                f"obtained: {mnemonic_t.value}"
            )

        seed = mnemonic.encode(random_passphrase).hex()
        LOGGER.info(f"encoded mnemonic with '{random_passphrase}' passphrase: {seed}")

        LOGGER.info(f"STOP  test dynamic {scount}.{tcount}")
