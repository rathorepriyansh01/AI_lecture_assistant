from backend.services.quiz_service import QuizService


def main():

    lecture_id = input(

        "Lecture ID : "

    ).strip()

    service = QuizService()

    print()

    print("=" * 80)

    print("HEALTH CHECK")

    print("=" * 80)

    print(

        service.health_check()

    )

    transcript = service.load_transcript(

        lecture_id

    )

    context = service.build_context(

        transcript

    )

    parts = service.split_context(

        context

    )

    print()

    print("=" * 80)
    print("GENERATE QUIZ")
    print("=" * 80)

    result = service.generate(

        lecture_id,

        difficulty="medium",

        total_questions=10

    )

    print()

    print(result["statistics"])

    print()

    print(result["quiz"][:2000])


if __name__ == "__main__":

    main()