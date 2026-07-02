from backend.services.ai_generator import AIGenerator


generator = AIGenerator(

    service_name="Summary",

    prompt_name="summary",

    cache_prefix="summary",

    supported_types=[

        "short",

        "detailed",

        "bullet",

        "keypoints",

        "chapter"

    ]

)

print(generator.health_check())

print()

print(generator.validate_type("bullet"))

print()

print(generator.get_cache_filename("bullet"))

generator = AIGenerator(

    service_name="Summary",

    prompt_name="summary",

    cache_prefix="summary",

    supported_types=[

        "short",

        "detailed"

    ]

)

print(

    generator.get_cache_filename(

        "short"

    )

)