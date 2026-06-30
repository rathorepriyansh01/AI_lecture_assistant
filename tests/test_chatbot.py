from backend.services.chatbot_service import ChatbotService


def main():

    chatbot = ChatbotService()

    while True:

        question = input("\nQuestion : ")

        if question.lower() == "exit":
            break

        response = chatbot.ask(question)

        print()

        print("=" * 80)
        print("QUESTION")
        print("=" * 80)
        print(response["question"])

        print()

        print("=" * 80)
        print("ANSWER")
        print("=" * 80)
        print(response["answer"])

        print()

        print("=" * 80)
        print("SOURCES")
        print("=" * 80)

        for source in response["sources"]:
            print(source)

        print()

        print("=" * 80)
        print("STATISTICS")
        print("=" * 80)

        for k, v in response["statistics"].items():
            print(f"{k:20}: {v}")

        print("=" * 80)


if __name__ == "__main__":
    main()