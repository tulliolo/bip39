# Bip39
A bip39 library, with a collection of tools.

This project provides a full implementation of the [bip39 specs](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), toghether with a CLI and
some useful tools to:
- generate and validate mnemonics;
- transform (and recreate) mnemonics (e.g. to create plausible deniability wallets)
- hide/reveal a mnemonic in an image file, with a steganography algorithm

**For better safety, we strongly suggest using the CLI in an offline system, without any Internet or LAN connection.**

## Requirements
python 3.10+

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND **NONINFINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.