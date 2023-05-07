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
import json
import secrets
import string
from pathlib import Path

import pytest


def load_data(section: str = "") -> dict:
    path = Path(__file__).parent

    with open(f"{path}/data/test_vectors.json") as file:
        data = json.load(file)

    if section:
        data = data[section]
    return data


@pytest.fixture
def random_password() -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for i in range(12))
