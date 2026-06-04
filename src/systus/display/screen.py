from systus.display.waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw, ImageFont
import qrcode

W, H = 400, 300

# -------------------------
# INIT E-PAPER (1 seule fois)
# -------------------------
epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()


# -------------------------
# INTERNAL HELPERS
# -------------------------
def _center_text(draw, text, y, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    draw.text((x, y), text, font=font, fill=0)


def _render(image):
    epd.display(epd.getbuffer(image))


# -------------------------
# SETUP MODE
# -------------------------
def show_setup():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    _center_text(draw, "SETUP MODE", 30, font_big)
    _center_text(draw, "Scan to setup Wifi for SYSTUS:", 60, font_small)

    qr = qrcode.make("http://192.168.4.1")
    qr = qr.resize((140, 140))

    image.paste(qr, ((W - 140) // 2, 100))

    _render(image)


# -------------------------
# RUNNING MODE
# -------------------------
def show_idle():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    _center_text(draw, "SYSTUS", 80, font_big)
    _center_text(draw, "Press button to start detection.", 140, font_small)

    _render(image)


def show_listening():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    _center_text(draw, "Systus is listening...", 120, ImageFont.load_default())

    _render(image)


def show_thinking():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    _center_text(draw, "SYSTUS is thinking...", 120, ImageFont.load_default())

    _render(image)


def show_result_placeholder():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    _center_text(draw, "RESULT MODE", 120, ImageFont.load_default())

    _render(image)