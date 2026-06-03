from systus.display.waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw, ImageFont
import qrcode

W, H = 400, 300

# Init UNE seule fois
epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()   # <- OK ici une seule fois au démarrage


def _center_text(draw, text, y, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    draw.text((x, y), text, font=font, fill=0)


def _make_qr(url: str, size: int = 140):
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(url)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white")
    return img_qr.resize((size, size))


def _render(image):
    epd.display(epd.getbuffer(image))


def show_setup():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    _center_text(draw, "SETUP MODE", 10, font_big)
    _center_text(draw, "Scan to setup Wifi for SYSTUS:", 40, font_small)

    qr = _make_qr("http://192.168.4.1")
    image.paste(qr, ((W - qr.size[0]) // 2, 80))

    _render(image)


def show_running():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    _center_text(draw, "RUNNING MODE", 120, font_big)

    _render(image)