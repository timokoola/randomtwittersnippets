from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import argparse  # requires 2.7
import json
import codecs
import pprint
import textwrap
import os.path
import os


class ImageGenerator(object):

    """Generates an image from the text"""

    def __init__(self, text, args):
        self.text = text["text"]
        self.image_name = "img_%s.png" % text["line"]
        self.args = args

    def generate(self):
        image = Image.new("RGB", (1024, 1024), "#bfb6aa")
        draw = ImageDraw.Draw(image)
        lines = textwrap.wrap(self.text, 40)
        fsize = 48
        font = ImageFont.truetype(self.args.fontfile, fsize)
        linew = 0
        while linew < 750:
            font = ImageFont.truetype(self.args.fontfile, fsize)
            linew = font.getsize(lines[0])[0]
            fsize = int(fsize * 1.25)

        offset = 10
        maxw = 10
        for l in lines:
            draw.text((10, offset), l, font=font, fill="#000")
            offset += int(font.getsize(l)[1] * 1.3)
            maxw = max(maxw, font.getsize(l)[0])

        self.image = Image.new(
            "RGB", (maxw + 20 + 100, offset + 20 + 100), "#bfb6aa")
        self.draw = ImageDraw.Draw(self.image)
        offset = 60
        for l in lines:
            self.draw.text((60, offset), l, font=font, fill="#000")
            offset += int(font.getsize(l)[1] * 1.3)

    def save(self):
        if not os.path.exists("images"):
            os.makedirs("images")
        self.file_name = "images/" + self.image_name
        self.image.save(self.file_name)


def handle_command_line():
    parser = argparse.ArgumentParser(
        description="Generates an image out of book part")
    parser.add_argument(
        "-i", "--id", help="Generates nth tweet",
        default="8")
    parser.add_argument("-f", "--fontfile",
                        help="fontfile location")
    parser.add_argument("-b", "--bookfile", help="Book to be read")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = handle_command_line()

    book = codecs.open(args.bookfile, "r", "utf-8")
    tweets = json.load(book)
    book.close()

    ig = ImageGenerator(tweets[args.id], args)
    ig.generate()
    ig.save()
