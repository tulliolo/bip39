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

import pytest

from tests.common import get_vector_data
from tulliolo.bip39.entropy import ENTROPY_SIZE_RANGE, Entropy
from tulliolo.bip39.mnemonic import Mnemonic, WORD_COUNT_ALL
from tulliolo.bip39.seed import Seed

PASSPHRASE = "TREZOR"

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def random_passphrase():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    size = secrets.SystemRandom().randint(8, 25)
    yield "".join(secrets.choice(alphabet) for i in range(size))


class TestStatic:
    @pytest.mark.parametrize("iter_data", enumerate(get_vector_data()))
    def test_static(self, iter_data):
        count, vector = iter_data
        count += 1
        LOGGER.info(f"START test static {count}:\n{json.dumps(vector, indent=2)}")

        seed = Seed(Mnemonic.from_value(vector["mnemonic"]), PASSPHRASE)
        LOGGER.info(f"generated seed:\n{json.dumps(seed.info, indent=2)}")

        assert seed.value.hex() == vector["rootseed"], (
            "seed mismatch",
            f"expected: {vector['seed']}",
            f"obtained: {seed.value.hex()}"
        )

        LOGGER.info(f"STOP  test static {count}")


class TestDynamic:
    @pytest.mark.parametrize("iter_data", enumerate(ENTROPY_SIZE_RANGE))
    def test_dynamic(self, iter_data, random_passphrase):
        count, size = iter_data
        count += 1
        LOGGER.info(f"START test dynamic {count}: {WORD_COUNT_ALL[ENTROPY_SIZE_RANGE.index(size)]}")

        seed = Seed(Mnemonic.from_entropy(Entropy.generate(size)), random_passphrase)
        LOGGER.info(f"generated seed:\n{json.dumps(seed.info, indent=2)}")

        LOGGER.info(f"STOP  test dynamic {count}")
