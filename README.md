Text-to-Bitmap

Text-to-Bitmap takes your text and encodes it as a bitmap image.

This project was partly inspired by GitHub's Identicons (https://github.com/blog/1586-identicons) and partly inspired by some of the challenges presented during the Hackathon Against Domestic Violence in January 2013 and FreedomHack to help journalists in conflict zones get sensitive information out safely in August 2013.

The lesson here: creativity flows from unexpected places.

Actual creation of the bitmap in Python is loosely based on http://pseentertainmentcorp.com/smf/index.php?topic=2034.0

Text-to-Bitmap now has two versions: ASCII (initial release) and Unicode.

-----------------------
Unicode Version Notes:
-----------------------

Text-to-Bitmap takes your text and encodes it as a bitmap image. The Unicode version of Text-to-Bitmap supports Unicode characters, and maps the code point of each character across five values: RGBRG for the first character; BRGBR for the second, and so on.

One value out of the five is randomly generated and subtracted from the code point of each character; the remaining four values are factors of that remaining value.

In other words, '\ua000' has a code point of 40960.  A random number between 1 and 255 is removed from this.  As an example, we'll use 211.  Factors for the number 40749 are generated (47 and 867), and those in turn are factored to bring their values lower than 256. (1, 47 and 17, 51).

Taken together, the four multiplier values plus the one adding value create the code point of the original character.

(1 * 47 * 17 * 51) + 211 = 40960

Essentially, five random numbers are generated that can be reconsituted to form the original number.  But it otherwise looks like noise.

Adding Value Position Scrambling

So the values (R 1, G 47, B 17) and (R 51, G211) are generated from that one character.  To delay a brute force attack, the adding value (211) can be moved to any position - and that position can change for each character throughout the whole message.  So it might be in position # 5 for the first character but in position # 2 for the next character, and depending on how secure you desire, may be in a different position for each character in your message.

RGB Scrambling

RGB seeds are also used as in the ASCII version, adding another layer of protection.  An improvement has been made to the security, allowing offset values to be mapped out of order: so instead of an R offset always being mapped to R, a G offset always being mapped to G, and a B offset always being mapped to B; it may map to R, B, and then G, or any combination.  Similar to the security measures around the adding value, this can also change per character and applied to the whole message.

Combining RGB Scrambling of six possible values and Adding Value Position Scrambling of 5 possible values with the RGB seed of 16,777,216 possible values and the Minimum Offset value (assuming your brute force attacker knew the language and character set range within 100 characters), your brute force attacker would be faced with:

6 * 5 * 16,777,216 * 100 = a 1 in 50,331,648,000 chance of getting the correct message.

Much higher if they didn't know which language or character set to go through.

In this example, only one set of Adding Value Position Scrambling is used, and only one set of RGB scrambling is used.  But multiples of each of these could be used, sharply increasing the amount of brute force attempts necessary.

---------------------
ASCII Version Notes:
---------------------

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

