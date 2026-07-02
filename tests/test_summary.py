from backend.services.summary_service import SummaryService


def main():

    lecture_id = input("Lecture ID : ")

    print()

    print("=" * 60)

    print("SUMMARY TYPES")

    print("=" * 60)

    print("1. Short")

    print("2. Detailed")

    print("3. Bullet")

    print("4. Keypoints")

    print("5. Chapter")

    print("6. Generate All")

    print()

    choice = input("Choose : ").strip()

    mapping = {

        "1": "short",

        "2": "detailed",

        "3": "bullet",

        "4": "keypoints",

        "5": "chapter",

        "6": "all"

    }

    summary_type = mapping.get(

        choice,

        "short"

    )

    service = SummaryService()

    result = service.generate_by_type(

        lecture_id=lecture_id,

        summary_type=summary_type,

        use_cache=False

    )

    print()

    print("=" * 80)

    print("RESULT")

    print("=" * 80)

    if summary_type == "all":

        for key, value in result.items():

            print()

            print("=" * 80)

            print(key.upper())

            print("=" * 80)

            print(value["summary"])

    else:

        print(result["summary"])


if __name__ == "__main__":

    main()