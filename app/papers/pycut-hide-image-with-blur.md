title : Pycut : hide an image and reveal it

date : 04-17-2014

----------

For my job I had to build a tool to hide (and ultimately reveal) an image step by step.

You can find it [here](https://github.com/ZebediahKillgrave/pycut).

For this project I used python with Pillow (a PIL fork).

The goal of the project is to be able to reveal an image square by square. The total number of square is given by the user and the tool must create an image for each step going from hidden to completely revealed.

First we have to completely "hide" or obfuscate the original image. In order to do this I chose to use the Gaussian Blur filter on the image. It takes more or less time to generate depending on the blur factor you want, for a 725x1087 image with a factor of 100 it takes about 10s~ on my computer.

    :::python
    >>> from PIL import Image, ImageFilter
    >>> image = Image.open("image.jpg")
    >>> blur = image.filter(ImageFilter.GaussianBlur(100))
    >>> blur.show()

I found it really easy to do what I wanted with Pillow, the library is very straightforward and the [documentation](http://pillow.readthedocs.org/en/latest/) is great.

Next step was to cut the image in parts and reveal each of them one by one, but in a random order.
I chose to represent the parts as a 1-dimensional list, it makes it easier to randomize and it's not so complicated when you want to find the equivalent 2-dimensional coordinate.

    :::python
    >>> from random import shuffle
    >>> width, height = 3, 2 # number of parts
    >>> pixelw, pixelh = image.size[0] / width, image.size[1] / height # size of one rectangle
    >>> parts = range(width * height)
    >>> shuffle(parts) # that will randomize the order of appearance
    >>> images = [blur.copy()] # that list will contain every steps
    >>> for i, part in enumerate(parts):
    ...    for x in xrange(pixelw):
    ...	       for y in xrange(pixelh):
    ...	       	   images[i].putpixel((x + pixelw * (part % width), y + pixelh * (part / width)),
    ...		   		      image.getpixel((x + pixelw * (part % width), y + pixelh * (part / width))))
    ...    images.append(images[i].copy())
    ...
    >>> for im in images:
    ...    im.show()
    ...
    >>>

That works and it looks nice, but sometimes the first revealed part will be the main subject of the picture. I haven't found a real solution to this yet but I will look into [cropy](https://github.com/mapado/cropy), it's a module that uses entropy information to identify the parts of the image with less informations.

It's not a real priority though so I might not dig deeper before some time.
