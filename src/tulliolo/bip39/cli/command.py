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
import sys
from functools import wraps


def command(name):
    """
    A decorator wrapping commands in a try/except block with result codes.
    :param name:
    :return:
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            code = 0
            try:

                func(*args, **kwargs)

            except TypeError as e:
                print(f"\n{name} failure!\n{str(e)}", file=sys.stderr)
                code = -1
            except ValueError as e:
                print(f"\n{name} failure!\n{str(e)}", file=sys.stderr)
                code = -2
            except OSError as e:
                print(f"\n{name} failure!\n{str(e)}", file=sys.stderr)
                code = -3
            except Exception as e:
                print(f"\n{name} failure!\n{str(e)}", file=sys.stderr)
                code = -4
            finally:
                return code

        return wrapper
    return decorate
