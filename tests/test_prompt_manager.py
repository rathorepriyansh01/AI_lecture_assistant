from backend.core.prompt_manager import PromptManager


def main():

    manager = PromptManager()

    prompt = manager.format_prompt(

        "chatbot",

        context="Machine Learning is a subset of AI.",

        question="What is Machine Learning?"

    )

    print()

    print("=" * 70)

    print(prompt)

    print("=" * 70)

    print()

    print("Available Prompts")

    print(manager.available_prompts())


if __name__ == "__main__":

    main()