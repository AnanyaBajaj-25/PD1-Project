from agent import WikipediaAgent


SECTION_ORDER = [
    ("cultural_etiquette", "Cultural Etiquette"),
    ("language_communication", "Language & Communication"),
    ("food_dining_norms", "Food & Dining Norms"),
    ("festivals_holidays", "Festivals & Holidays"),
    ("spiritual_sites", "Religion & Spiritual Sites"),
    ("heritage_monuments", "Heritage & Monuments"),
    ("conversation_starters", "Conversation Starters"),
]


def main():
    agent = WikipediaAgent()
    print("Welcome to the Traveler Insight CLI! Ask about any destination.")
    while True:
        destination = input("Enter a country or city (or 'exit' to quit): ")
        if destination.lower() == "exit":
            break
        result = agent.forward(destination)
        if "error" in result:
            print(f"\nError: {result['error']}\n")
            continue

        print(f"\n=== {result['destination']} ===")

        for key, heading in SECTION_ORDER:
            text = result.get(key)
            if not text:
                continue
            print(f"{heading}:")
            print(text)
            print()
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()