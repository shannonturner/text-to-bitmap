Text-to-Bitmap

Text-to-Bitmap takes your text and encodes it as a bitmap image.

This project was partly inspired by GitHub's Identicons (https://github.com/blog/1586-identicons) and partly inspired by some of the challenges presented during the Hackathon Against Domestic Violence in January 2013 and FreedomHack to help journalists in conflict zones get sensitive information out safely in August 2013.

The lesson here: creativity flows from unexpected places.

Actual creation of the bitmap in Python is loosely based on http://pseentertainmentcorp.com/smf/index.php?topic=2034.0

Text-to-Bitmap takes your text and encodes it as a bitmap image.  Text-to-Bitmap uses ASCII characters only; mapping each character to one R, G, or B value, offset by the R, G, or B seed as a small layer of security.

This means that without your RGB seed or 'password', your message is protected against casual intrusion.  Using a seed means that your message will only be decoded correctly every 1 in 256^3 times. That said, 1 in 256^3 (1 in 16,777,216) is trivial to brute-force for anyone determined to decode your message.

When combined with other methods, Text-to-Bitmap may be more successful in hiding your message.

By default, Text-to-Bitmap will create an image with a minimum height of 4 pixels.  The image itself looks like random static or noise.

A test text file with 2153 characters generated a bitmap file 180 pixels wide and 4 pixels high.  This is fairly small, and would easily fit inside an innocuous image and simply look like image corruption or distortion -- if it is noticed at all.  In other words, steganography may render your encoded message undetected, even moreso when the encoded message is small.

Combining methods of security may improve Text-to-Bitmap's success, such as encoding a garbled, misspelled, or otherwise deliberately obfuscated message.  Essentially, anything that would increase the number of potential matches a brute-force decoder would then have to verify is good practice.  Longer unobfuscated messages are less secure than shorter messages, as shorter messages would conceivably have several potential matches - and longer messages would probably only have one or a few.

Since there are only 16,777,216 ways your message can be re-arranged (and because of how the ASCII character set is arranged, an even narrower range of valid values), it is better to encode short, obfuscated messages.

For example, encoding the text "R(48in$2na-q" is likely to look like garbage no matter which of the 256^3 ways it's decoded.

As another example, encoding the text "508940198412392231381939102" will produce many false leads for your brute-force decoder to trip over.

BOTTOM LINE: Text-to-Bitmap should not be considered to be in the same class of security measures as cryptography, and is not secure from determined decoders.  Do not use Text-to-Bitmap in any situation where actual cryptography would be required.  As stated in the license, Text-to-Bitmap IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.