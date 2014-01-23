#Text-to-Bitmap

(psst ... a bitmap is a type of image)

#####Problem this Solves
Journalists, activists, and others who need to pass secret messages to prevent interception and decoding by third parties can use Text-to-bitmap to create images that look like random static. The images created are small and can often be hidden in plain sight as part of a larger image (steganography.)

#####How this project solves this problem
Text-to-Bitmap turns regular text into a scrambled-looking image that can only be decoded with the correct password. Decoding with the incorrect password gives garbage data or false positives.

#####How to use the tool
Text-to-Bitmap has an API and a command-line tool, both of which can encode text and decode images.

For a demo of the API (no programming necessary), see **http://shannonturner.github.io/text-to-bitmap/api.html** 

For the command line tool, run **python uni_text_to_bitmap.py** at the terminal to see the full usage details.

#####How the tool works
Text-to-Bitmap is primarily used to encode a message into a small scrambled-looking image. Text-to-Bitmap can encode messages in any language.

**Alice** will encode her secret message and send the scrambled image to **Bob**.  They can use a pre-agreed-upon password, or Text-to-Bitmap can automatically create a secure new password for each image.

Either way, when **Bob** has both the scrambled image and password from **Alice**, he can use Text-to-Bitmap to decode the image and receive the message.

If **Eve** intercepts the image, she might attempt to crack the code -- but will most likely be frustrated; each image created by the API has **7,132,766,847,673,865,645,550,849,603,057,000,000** possible passwords. Attempting to decode the image with an incorrect password will either fail outright or worse for **Eve**, give a false positive result.

Beyond simple messages, Text-to-Bitmap can also encode photos, videos, documents, or any other type of file and turn it into a scrambled image. 

#####Text-to-Bitmap Code breaker
Included with Text-to-Bitmap is a command-line tool to test the strength of the encoded images by systematically trying to break the code.

Using the tool, even running **100 trillion attempts per second** would take **22,602,374,222,608,400 years** to crack the code.

If you'd like to try to crack the code, see **http://shannonturner.github.io/text-to-bitmap/challenges.html** for challenges.

#####Text-to-Smiley (in active development, NOT PRODUCTION READY)
Text-to-Smiley hides a short message in an existing small image of an emoticon by altering the colors imperceptibly. Because the emoticons look identical to the original identicons, Text-to-Smiley's strength is in hiding messages in plain sight (steganography).

Text-to-Smiley is limited to encoding very short messages.

Text-to-Smiley is in the early stages of development and should not yet be used for protecting secret messages.

#####License
Text-to-Bitmap is free software available under the MIT license; see LICENSE for full details.
