from systus.display.waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw

# Init UNE seule fois
epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()

W, H = 400, 300


def _draw_text(text: str):
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    draw.text((20, 20), text, fill=0)

    epd.display(epd.getbuffer(image))


def show_setup():
    _draw_text("SETUP MODE")


def show_running():
    _draw_text("RUNNING MODE")