# Bip39
A Bip39 library, with a CLI and collection of tools.

This project provides a full implementation of the [Bip39 specs](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), along with a CLI that offers some mnemonic key management tools such as:
- **generate** and **validate** mnemonics;
- **correct** the last word according to the checksum (e.g. when a mnemonic is generated by rolling dices);
- **transform** (and restore) mnemonics, e.g. to create side-wallets hiding the original;
- **hide/reveal** a mnemonic in an image file, with a steganography algorithm.

For further details, please refer to the [documentation folder](https://github.com/tulliolo/bip39/wiki).

**For security reasons, it is highly recommended to run the CLI on an offline system, without any Internet or LAN connection.**

## Requirements
python 3.10+

## Installation
This project is distributed on [PyPI](https://pypi.org/):
```
pip install tulliolo.bip39
```

## Usage Examples
Here are some examples of using the library and CLI.

### CLI
Generate a new 24 words mnemonic:
```
$ bip39-cli generate -s 24
******************
* bip39-cli v0.2 *
******************

generating a 24 words mnemonic...

generate success!
view fresh drink impulse doctor wise another smoke license collect unaware immense normal trick second owner subway bright chaos upper ribbon kite debris quote
```

Validate a mnemonic, correcting the checksum:
```
$ bip39-cli validate -f
******************
* bip39-cli v0.2 *
******************

enter a mnemonic:
₿ view fresh drink impulse doctor wise another smoke license collect unaware immense
invalid checksum | expected: 0 | obtained: c

validation success... with fixed checksum:
view fresh drink impulse doctor wise another smoke license collect unaware hybrid
```

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
