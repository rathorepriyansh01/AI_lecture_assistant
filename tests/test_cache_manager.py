from backend.utils.cache_manager import CacheManager


def main():

    lecture_id = input("Lecture ID : ")

    cache = CacheManager()

    cache.save_text(

        lecture_id,

        "summary_short.md",

        "This is a sample summary."

    )

    print(

        cache.exists(

            lecture_id,

            "summary_short.md"

        )

    )

    print()

    print(

        cache.load_text(

            lecture_id,

            "summary_short.md"

        )

    )


if __name__ == "__main__":

    main()