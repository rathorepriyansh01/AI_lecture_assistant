from backend.providers.provider_factory import ProviderFactory


def main():

    factory = ProviderFactory()

    print()

    print(factory.health_check())

    print()

    result = factory.safe_invoke(

        "Explain Machine Learning in one sentence."

    )

    print()

    print("=" * 60)

    print("Provider Used")

    print("=" * 60)

    print(result["provider"])

    print()

    print("=" * 60)

    print("Response")

    print("=" * 60)

    print(result["response"])


if __name__ == "__main__":

    main()