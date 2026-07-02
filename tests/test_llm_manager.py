from backend.core.llm import LLMManager


def main():

    llm = LLMManager()

    print()

    print(llm.health_check())

    print()

    answer = llm.invoke(

        "What is Artificial Intelligence?"

    )

    print()

    print(answer)


if __name__ == "__main__":

    main()