import os
from dotenv import load_dotenv
from anthropic import Anthropic

from weather import get_weather
from calendar_events import get_todays_events
from joke import get_dad_joke
from fact import get_nature_fact
from sms import send_sms

load_dotenv()


def format_brief(weather: str, events: list[str], joke: str, fact: str) -> str:
    client = Anthropic()

    events_text = "\n".join(f"  • {e}" for e in events) if events else "  No events today"

    prompt = f"""You are writing a warm, concise morning text message for a family.

Here is the data:
Weather (Bellevue, WA): {weather}
Today's Calendar:
{events_text}
Dad Joke: {joke}
Nature Fact: {fact}

Write a friendly morning briefing SMS. Format it exactly like this:

Good morning! ☀️

🌤 Weather: [weather summary]

📅 Today:
[list events, or "Nothing on the calendar"]

😄 [dad joke]

🌿 [nature fact]

Keep it warm and readable. Do not add extra commentary."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def main():
    print("Fetching data...")
    weather = get_weather()
    events = get_todays_events()
    joke = get_dad_joke()
    fact = get_nature_fact()

    print("Formatting brief...")
    brief = format_brief(weather, events, joke, fact)

    print("\n--- BRIEF PREVIEW ---")
    print(brief)
    print("---------------------\n")

    recipients = [
        os.getenv("PHONE_PAOLO"),
        os.getenv("PHONE_STEPHANIE"),
    ]

    for phone in recipients:
        if phone:
            send_sms(phone, brief)
            print(f"Sent to {phone}")

    print("Done!")


if __name__ == "__main__":
    main()
