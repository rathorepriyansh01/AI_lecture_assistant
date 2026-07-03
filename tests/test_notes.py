from backend.services.notes_service import NotesService


def main():

    lecture_id = input("Lecture ID : ")

    notes_type = input(

        "Notes Type (short/detailed/exam/revision/cheatsheet): "

    ).strip().lower()

    service = NotesService()

    result = service.generate(

    lecture_id,

    notes_type,

    use_cache=False

)
    service = NotesService()

    print(

    service.health_check()

    )
    print()

    print("=" * 80)

    print("NOTES")

    print("=" * 80)

    print(result["notes"])

    print()

    print("=" * 80)

    print("STATISTICS")

    print("=" * 80)

    print(result["statistics"])

if __name__ == "__main__":

    main()