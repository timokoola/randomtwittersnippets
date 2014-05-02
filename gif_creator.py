from images2gif import writeGif
from image_generator import ImageGenerator
from PIL import Image
import os


class Something(object):
    pass

if __name__ == '__main__':
    args = Something()
    args.fontfile = '/Users/timoeemelikoola/Downloads/Cardo/Cardo-Regular.ttf'
    imgs = []
    for i in xrange(20):
        ig = ImageGenerator({"text": str(i), "line": str(i)}, args)
        ig.generate()
        ig.save()
        imgs.append(Image.open(ig.file_name))

    size = (150, 150)
    for im in images:
        im.thumbnail(size, Image.ANTIALIAS)
    filename = "images/my_gif.GIF"
    writeGif(filename, images, duration=0.2)
