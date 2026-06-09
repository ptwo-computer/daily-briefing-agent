from anthropic import Anthropic


def get_nature_fact() -> str:
    client = Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": (
                    "Share one fascinating, specific nature or wildlife fact that most people don't know. "
                    "1-2 sentences max. Just the fact, no intro or label."
                ),
            }
        ],
    )
    return message.content[0].text
