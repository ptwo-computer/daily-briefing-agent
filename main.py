from dotenv import load_dotenv

from weather import get_weather
from calendar_events import get_todays_events
from joke import get_dad_joke
from fact import get_nature_fact
from printer import generate_pdf, print_pdf

load_dotenv()


def main():
    print("Fetching data...")
    weather = get_weather()
    events = get_todays_events()
    joke = get_dad_joke()
    fact = get_nature_fact()

    print("Generating PDF...")
    pdf_path = generate_pdf(weather, events, joke, fact)
    print(f"PDF saved to {pdf_path}")

    print("Sending to printer...")
    print_pdf(pdf_path)
    print("Done — check your printer!")


if __name__ == "__main__":
    main()
