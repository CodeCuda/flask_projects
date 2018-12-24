#module for pillow photo magic

from PIL import Image, ImageDraw


def create_thumbnail(img_url):
    size = (640, 640)
    try:
        image = Image.open(img_url)

    except IOError:
        print("Unable to load image")
    print(img_url)
    image.thumbnail(size)
    image.save(img_url)
    return img_url


def mouth_magic(image_url, coordinates):

    image = Image.open(image_url)

    x_left = int(round(coordinates['mouthLeft'].get('x')))
    y_left = int(round(coordinates['noseLeftBottom'].get('y'))) + int(round(coordinates['noseLeftBottom'].get('y')/20))
   # x_right = int(round(coordinates['mouthRight'].get('x')))
   # y_right = int(round(coordinates['noseBottom'].get('y')))

    moustache = Image.open('app/static/pillow_magic_stuff/moustache.png')
    x_size = int(round(coordinates['mouthRight'].get('x'))) - int(round(coordinates['mouthLeft'].get('x')))
    y_size = int(round(coordinates['lipTop'].get('y'))) - int(round(coordinates['noseLeftBottom'].get('y')))

    size = (x_size, y_size)
    print(size)
    moustache.thumbnail(size)
    moustache = moustache.rotate(-coordinates['faceAngle'].get('roll'), expand=True)
    moustache.save('app/static/pillow_magic_stuff/mous1.png')
    image_copy = image.copy()

    position = (x_left, y_left)


    image_copy.paste(moustache, position, moustache)
    new_filename = image_url.replace('temp', 'moustache')
    image_copy.save(new_filename)
    return new_filename

def eyes_magic(image_url, coordinates):
    image = Image.open(image_url)
    print(coordinates)
    x_left = int(round(coordinates['leftBrow'].get('x')))
    y_left = int(round(coordinates['leftBrow'].get('y')))

    glasses = Image.open('app/static/pillow_magic_stuff/glasses.png')
    x_size = int(round(coordinates['rightBrow'].get('x'))) - int(round(coordinates['leftBrow'].get('x')))
    y_size = int(round(coordinates['noseTop'].get('y'))) - int(round(coordinates['rightBrow'].get('y')))

    size = (x_size, y_size)
    print(size)
    glasses.thumbnail(size)
    glasses = glasses.rotate(-coordinates['faceAngle'].get('roll'), expand = True)
    glasses.save('app/static/pillow_magic_stuff/glasses1.png')

    image_copy = image.copy()

    position = (x_left, y_left)

    image_copy.paste(glasses, position, glasses)
    new_filename = image_url.replace('temp', 'glasses')
    image_copy.save(new_filename)
    return new_filename

