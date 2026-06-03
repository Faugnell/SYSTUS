from waveshare_epd import epd4in2_V2

from PIL import Image
from PIL import ImageDraw


def show_setup():
    epd = epd4in2_V2.EPD()

    epd.init()

    image = Image.new("1", (400, 300), 255)
    draw = ImageDraw.Draw(image)

    draw.text((20, 20), "SETUP MODE", fill=0)

    epd.display(epd.getbuffer(image))


def show_running():
    epd = epd4in2_V2.EPD()

    epd.init()

    image = Image.new("1", (400, 300), 255)
    draw = ImageDraw.Draw(image)

    draw.text((20, 20), "RUNNING MODE", fill=0)

    epd.display(epd.getbuffer(image))