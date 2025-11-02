from agent import WikipediaAgent

def main():
    agent = WikipediaAgent()
    print("Welcome to the Wikipedia Agent! Ask me anything")
    while True:
        question = input("Enter a question: ")
        if question.lower() == "exit":
            break
        answer = agent.forward(question)
        print("\nAnswer: ", answer)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()