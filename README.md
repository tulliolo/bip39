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

Transform and restore a mnemonic:
```
$ bip39-cli transform
******************
* bip39-cli v0.2 *
******************

enter a mnemonic
₿ view fresh drink impulse doctor wise another smoke license collect unaware hybrid

applying negative transformation...

transformation success!
army permit rude miss sausage adjust wait creek learn sponsor bean mixed

$ bip39-cli transform
******************
* bip39-cli v0.2 *
******************

enter a mnemonic
₿ army permit rude miss sausage adjust wait creek learn sponsor bean mixed

applying negative transformation...

transformation success!
view fresh drink impulse doctor wise another smoke license collect unaware hybrid
```

Hide a mnemonic in an image with steganography:
```
$ bip39-cli steganography encode -i tests/data/test_image.jpg -o tests/data/output/
******************
* bip39-cli v0.2 *
******************

enter a mnemonic:
₿ view fresh drink impulse doctor wise another smoke license collect unaware hybrid

enter a password to encrypt the mnemonic (or leave blank):
₿ 
insert again...:
₿ 
encrypting mnemonic...

encoding image...

encoding success!
tests/data/output/test_image_horizontal_20230510-120631.png
```

Reveal a mnemonic from an image with steganography:
```
$ bip39-cli steganography decode -i tests/data/output/test_image_horizontal_20230510-120631.png 
******************
* bip39-cli v0.2 *
******************

enter a password to decrypt the mnemonic (or leave blank):
₿ 
insert again...:
₿ 

decoding image...
decoding success!

decrypting mnemonic...
decrypting success!
view fresh drink impulse doctor wise another smoke license collect unaware hybrid
```

### Library
Generate a 12 words mnemonic:

```
from tulliolo.bip39.mnemonic import Mnemonic

mnemonic = Mnemonic.generate(12)
print(" ".join(mnemonic.value))

absent deny citizen next velvet where mixture glimpse deposit sentence hat manual
```

Import a mnemonic and fix the checksum:
```
from tulliolo.bip39.mnemonic import Mnemonic

mnemonic = Mnemonic.from_value("view fresh drink impulse doctor wise another smoke license collect unaware immense", fix_checksum=True)
print(mnemonic.info)

{'entropy': 'f3eb990c391405f8c266668125b3b1b8', 'checksum': '0', 'value': {1: 'view', 2: 'fresh', 3: 'drink', 4: 'impulse', 5: 'doctor', 6: 'wise', 7: 'another', 8: 'smoke', 9: 'license', 10: 'collect', 11: 'unaware', 12: 'hybrid'}}
```

Generate the seed, that can be later used to generate bip32 wallets:
```
from tulliolo.bip39.mnemonic import Mnemonic

seed = Mnemonic.generate(24).encode(passphrase="my_optional_passphrase")
print(seed.hex())

d24027e4b7dae545b95dca96a7b8e539e0a0d7ae2ef6cd2247e346907f7b842bb93d2268ee3bd28eede481b0ddab0b44f04ed49b4a4904ee7882677dd2677ac2
```

Transform and restore a mnemonic with a "mirror" transformation:
```
from tulliolo.bip39.mnemonic import Mnemonic
from tulliolo.bip39.utils.transformation import Transformation

mnemonic_o = Mnemonic.from_value("view fresh drink impulse doctor wise another smoke license collect unaware hybrid")
mnemonic_t = mnemonic_o.transform(Transformation.MIRROR)
print(mnemonic_t.value)

('budget', 'hover', 'hard', 'actress', 'grid', 'canoe', 'leader', 'agree', 'order', 'luggage', 'invest', 'paddle')

mnemonic_t = mnemonic_t.transform(Transformation.MIRROR)
assert mnemonic_o == mnemonic_t
print(mnemonic_t.value)

('view', 'fresh', 'drink', 'impulse', 'doctor', 'wise', 'another', 'smoke', 'license', 'collect', 'unaware', 'hybrid')
```


## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
