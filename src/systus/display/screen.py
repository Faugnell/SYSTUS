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
# HELPERS
# -------------------------
def _center_text(draw, text, y, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    draw.text((x, y), text, font=font, fill=0)


def _render(image):
    epd.display(epd.getbuffer(image))

def _make_qr(url, size=120):
    qr = qrcode.make(url)
    qr = qr.resize((size, size))
    return qr


# -------------------------
# SETUP MODE
# -------------------------
def show_setup():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    _center_text(draw, "SETUP MODE", 40, font_big)
    _center_text(draw, "Scan to setup Wifi for SYSTUS:", 70, font_small)

    qr = qrcode.make("http://10.0.0.32:5000")
    qr = qr.resize((140, 140))

    image.paste(qr, ((W - 140) // 2, 110))

    _render(image)

def show_setup_connected():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    _center_text(draw, "SETUP MODE", 40, font_big)
    _center_text(draw, "Scan to change WiFi for SYSTUS", 80, font_small)

    qr = qrcode.make("http://10.0.0.32:5000")
    qr = qr.resize((140, 140))
    image.paste(qr, ((W - 140) // 2, 110))

    _render(image)


def show_setup_hotspot():
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    _center_text(draw, "SETUP MODE", 40, font_big)
    _center_text(draw, "Not connected to network.", 75, font_small)
    _center_text(draw, "Scan to setup WiFi for SYSTUS", 100, font_small)

    qr = qrcode.make("http://192.168.4.1:5000")  # hotspot IP typical
    qr = qr.resize((140, 140))
    image.paste(qr, ((W - 140) // 2, 120))

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


def show_result(result: dict):
    image = Image.new("1", (W, H), 255)
    draw = ImageDraw.Draw(image)

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    # safety
    if not result:
        _center_text(draw, "No result", 120, font_big)
        _render(image)
        return

    title = result.get("title", "Unknown title")
    artist = result.get("artist", "Unknown artist")
    album = result.get("album", "Unknown album")

    release_date = result.get("release_date", "")
    year = release_date.split("-")[0] if release_date else "?"

    link = result.get("song_link")

    # TEXT
    _center_text(draw, title, 10, font_big)
    _center_text(draw, artist, 45, font_small)
    _center_text(draw, album, 75, font_small)
    _center_text(draw, f"{year}", 105, font_small)

    # QR
    if link:
        qr = _make_qr(link, size=120)
        image.paste(qr, ((W - 120) // 2, 135))
    else:
        _center_text(draw, "No link available", 150, font_small)

    _render(image)