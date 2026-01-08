from PIL import Image, ImageTk
import requests
from io import BytesIO

def stat_color(value):
    if value >= 80:
        return "green"
    elif value >= 50:
        return "orange"
    else:
        return "red"


def load_image_from_url(url, size=(150, 150)):
    """
    Download image from URL and prepare it for Tkinter.
    """
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image = image.resize(size)
    return ImageTk.PhotoImage(image)
