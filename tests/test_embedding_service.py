from backend.services.embedding_service import EmbeddingService


def main():

    lecture_id = input(

        "Enter Lecture ID : "

    ).strip()

    service = EmbeddingService()

    metadata = service.process(

        lecture_id

    )

    print()

    print("=" * 70)

    print("EMBEDDING SUMMARY")

    print("=" * 70)

    print()

    print(

        f"Lecture : {metadata['lecture']['lecture_name']}"

    )

    print(

        f"Stage : {metadata['processing']['current_stage']}"

    )

    print(

        f"Embedded Chunks : {metadata['statistics']['embedded_chunks']}"

    )

    print(

        f"Embedding Model : {metadata['models']['embedding_model']}"

    )

    print()

    print("=" * 70)


if __name__ == "__main__":

    main()