from backend.core.embedding_model import EmbeddingModel


def main():

    model = EmbeddingModel()

    print()

    print("=" * 70)

    print("Embedding Dimension")

    print(model.embedding_dimension())

    print("=" * 70)

    vector = model.encode_query(

        "What is machine learning?"

    )

    print()

    print("Vector Length :", len(vector))

    print("First 10 Values")

    print(vector[:10])


if __name__ == "__main__":

    main()