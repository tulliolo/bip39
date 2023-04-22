# Mnemonic Transform

Turns a 12/15/18/21/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, useful for plausible deniability.
Transformation is reversible running the same tool, with the same parameters.

The original entropy can be encrypted with the following algorithms:

| ALGORITHM          | DESCRIPTION                                                                              |
|--------------------|------------------------------------------------------------------------------------------|
| NEGATIVE (DEFAULT) | Each bit is switched, like in a negative                                                 |
| REVERSAL           | All bits are swapped, the less significant bit becomes the most significant and so on... |

In order to rebuild the original mnemonic, take note of the new generated mnemonic, together with the encryption algorithm.

## Usage and Syntax
For production use, this tool is intended to run on an offline computer, with internet connection down.

```
$ python mnemonic_transform.py -h
usage: mnemonic_transform.py [-h] [-g GENERATE] [-e ENCRYPTION]

Turns a 12/15/18/21/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, useful for plausible deniability.
Transformation is reversible running the same tool, with the same parameters.

options:
  -h, --help            show this help message and exit
  -g GENERATE, --generate GENERATE
                        generate a new n words mnemonic (DEFAULT n = 0 -> NO GENERATION)
                        supported numbers of words are: 12, 15, 18, 21, 24
  -e ENCRYPTION, --encryption ENCRYPTION
                        encrypt the original entropy with different algorithms (enhance original seed obfuscation)
                        supported algorithms are:
                        0) NEGATIVE (DEFAULT): invert all bits
                        1) REVERSAL: swap all bits
```

## Usage Examples

Generate a 12 words mnemonic and apply NEGATIVE encryption.

```
$ python mnemonic_transform.py -g 12
************************
** mnemonic_transform **
************************
Turns a 12/15/18/21/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, useful for plausible deniability.
Transformation is reversible running the same tool, with the same parameters.

generating a 12 words mnemonic:
awesome path clarify staff mix gravity grocery below merry economy muscle page

Generating a new 12 words mnemonics for plausible deniability.
Please, take note of this mnemonics, together with the encryption algorithm, in order to rebuild the original mnemonic:

mnemonic: urge gallery stock cloud impose okay odor twenty inmate right hover genre
```

Insert a 12 words mnemonic and apply NEGATIVE encryption (rebuild the original mnemonic from previous example).

```
$ python mnemonic_transform.py
************************
** mnemonic_transform **
************************
Turns a 12/15/18/21/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, useful for plausible deniability.
Transformation is reversible running the same tool, with the same parameters.

insert a valid bip39 mnemonic:
mnemonic > urge gallery stock cloud impose okay odor twenty inmate right hover genre

Generating a new 12 words mnemonics for plausible deniability.
Please, take note of this mnemonics, together with the encryption algorithm, in order to rebuild the original mnemonic:

mnemonic: awesome path clarify staff mix gravity grocery below merry economy muscle page
```

Insert a 12 words mnemonic and apply REVERSAL encryption.

```
$ python mnemonic_transform.py -e 1
************************
** mnemonic_transform **
************************
Turns a 12/15/18/21/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, useful for plausible deniability.
Transformation is reversible running the same tool, with the same parameters.

insert a valid bip39 mnemonic:
mnemonic > awesome path clarify staff mix gravity grocery below merry economy muscle page

Generating a new 12 words mnemonics for plausible deniability.
Please, take note of this mnemonics, together with the encryption algorithm, in order to rebuild the original mnemonic:

mnemonic: venue basic shell people express slot slot tilt fitness clap apart away
```

Insert a 12 words mnemonic and apply REVERSAL encryption (rebuild the original mnemonic from previous example).

```
$ python mnemonic_transform.py -e 1
************************
** mnemonic_transform **
************************
Turns a 12/15/18/21/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, useful for plausible deniability.
Transformation is reversible running the same tool, with the same parameters.

insert a valid bip39 mnemonic:
mnemonic > venue basic shell people express slot slot tilt fitness clap apart away

Generating a new 12 words mnemonics for plausible deniability.
Please, take note of this mnemonics, together with the encryption algorithm, in order to rebuild the original mnemonic:

mnemonic: awesome path clarify staff mix gravity grocery below merry economy muscle page
```

Generate a 24 words mnemonic and apply NEGATIVE encryption.

```
$ python mnemonic_transform.py -g 24
************************
** mnemonic_transform **
************************
Turns a 12/15/18/21/24 words bip39 mnemonic into a new bip39 mnemonic of the same length, useful for plausible deniability.
Transformation is reversible running the same tool, with the same parameters.

generating a 24 words mnemonic:
response agent episode uphold clay autumn mind trouble metal pelican this limb aerobic dynamic mystery crumble oil embark rally gadget goose farm average spring

Generating a new 24 words mnemonics for plausible deniability.
Please, take note of this mnemonics, together with the encryption algorithm, in order to rebuild the original mnemonic:

mnemonic: embark wild reduce bachelor still utility indoor black initial frozen busy lawsuit wink robot horn sleep great response exchange pattern opinion proud usual clarify
```
