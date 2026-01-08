from io import BytesIO
import requests


def get_bunny_image() -> BytesIO:
    api = "https://rabbit-api-two.vercel.app/api/random"
    data = requests.get(api, timeout=10).json()
    image_url = data["url"]
    response = requests.get(image_url, timeout=10)

    image = BytesIO(response.content)
    image.seek(0)
    return image


def get_dog_image() -> BytesIO:
    api = "https://dog.ceo/api/breeds/image/random"
    data = requests.get(api, timeout=10).json()
    image_url = data["message"]
    response = requests.get(image_url, timeout=10)

    image = BytesIO(response.content)
    image.seek(0)
    return image


def get_cat_image() -> BytesIO:
    api = "https://cataas.com/cat"
    response = requests.get(api, timeout=10)

    image = BytesIO(response.content)
    image.seek(0)
    return image


def get_duck_image() -> BytesIO:
    api = "https://random-d.uk/api/random"
    data = requests.get(api, timeout=10).json()
    image_url = data["url"]
    response = requests.get(image_url, timeout=10)

    image = BytesIO(response.content)
    image.seek(0)
    return image


def get_fox_image() -> BytesIO:
    api = "https://randomfox.ca/floof/"
    data = requests.get(api, timeout=10).json()
    image_url = data["image"]
    response = requests.get(image_url, timeout=10)

    image = BytesIO(response.content)
    image.seek(0)
    return image
