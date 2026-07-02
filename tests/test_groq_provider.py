from config.settings import (

    GROQ_API_KEY,

    GROQ_MODEL

)

from backend.providers.groq_provider import GroqProvider


def main():

    provider = GroqProvider(

        api_key=GROQ_API_KEY,

        model=GROQ_MODEL

    )

    print()

    print(provider.provider_info())

    print()

    print(provider.health_check())

    print()

    answer = provider.invoke(

        "Say hello in one sentence."

    )

    print(answer)


if __name__ == "__main__":

    main()