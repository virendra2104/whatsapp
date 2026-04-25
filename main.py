from llm import ask_question
if __name__ == "__main__":
    while True:
        q = input("You: ")

        if q == "exit":
            break

        print("AI:", ask_question(q))