from backend.core.chroma_client import ChromaClient


def main():

    chroma = ChromaClient()

    print()

    print("=" * 60)

    print("Collection Name")

    print(chroma.collection.name)

    print()

    print("Documents")

    print(chroma.count())

    print("=" * 60)


if __name__ == "__main__":

    main()