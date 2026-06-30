from backend.core.llm import LLMManager


def main():

    llm = LLMManager()

    response = llm.invoke(

        "Say hello in one sentence."

    )

    print()

    print("=" * 70)

    print(response)

    print("=" * 70)


if __name__ == "__main__":

    main()