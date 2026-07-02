from config.settings import (

    NVIDIA_API_KEY,

    NVIDIA_MODEL

)

from backend.providers.nvidia_provider import NvidiaProvider


def main():

    provider = NvidiaProvider(

        api_key=NVIDIA_API_KEY,

        model=NVIDIA_MODEL

    )

    print()

    print(provider.provider_info())

    print()

    print(provider.health_check())

    print()

    answer = provider.invoke(

        "Introduce yourself in one sentence."

    )

    print(answer)


if __name__ == "__main__":

    main()