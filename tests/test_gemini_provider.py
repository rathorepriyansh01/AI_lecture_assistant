from config.settings import (

    GEMINI_API_KEY,

    GEMINI_MODEL

)

from backend.providers.gemini_provider import GeminiProvider


def main():

    provider = GeminiProvider(

        api_key=GEMINI_API_KEY,

        model=GEMINI_MODEL

    )

    print()

    print(provider.health_check())

    print()

    response = provider.invoke(

        "Introduce yourself in one sentence."

    )

    print(response)


if __name__ == "__main__":

    main()