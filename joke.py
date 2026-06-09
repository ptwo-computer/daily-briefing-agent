import requests


def get_dad_joke() -> str:
    response = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"},
    )
    return response.json()["joke"]
