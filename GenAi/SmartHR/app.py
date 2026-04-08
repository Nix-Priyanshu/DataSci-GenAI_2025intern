from retriever_chain import qa_chain  

def chat():
    print("\n💬 Welcome to your HR Assistant Bot! Type 'exit' to quit.\n")
    print("Hi ... How can I Help You ? (0v0)/^")
    print("\n" + "="*50 + "\n")

    while True:
        user_query = input("You: ").strip()

        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye! 🥔🔥")
            break

        print("Processing your query...")

        try:
            answer = qa_chain(user_query)
        except Exception as e:
            answer = f"Error: {e}"

        print("\nBot:", answer, "\n" + "-"*50)


if __name__ == "__main__":
    chat()
