from agent import WikipediaAgent

def main():
    agent = WikipediaAgent()
    print("Welcome to the Travel Agent! Give me a country and I'll give you a summary of the country's culture, history, and tourist attractions.")
    while True:
        question = input("Enter a destination: ")
        if question.lower() == "exit":
            break
        answer = agent.forward(question)
        print("\nAnswer: ", answer)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()