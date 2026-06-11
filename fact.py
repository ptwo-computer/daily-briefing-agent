from anthropic import Anthropic
from datetime import datetime

CATEGORIES = [
    "deep sea creatures",
    "insects and arachnids",
    "plants and fungi",
    "birds",
    "mammals",
    "reptiles and amphibians",
    "ocean and marine life",
    "weather and atmosphere",
    "geology and earth science",
    "astronomy and space",
    "animal behavior and intelligence",
    "ecosystems and ecology",
    "prehistoric life and evolution",
    "microscopic life",
]


def get_nature_fact() -> str:
    client = Anthropic()
    today = datetime.now()
    category = CATEGORIES[today.timetuple().tm_yday % len(CATEGORIES)]

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        temperature=1.0,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today is {today.strftime('%B %d, %Y')}. "
                    f"Share one surprising, little-known fact about {category}. "
                    "1-2 sentences. Just the fact, no intro or label."
                ),
            }
        ],
    )
    return message.content[0].text
