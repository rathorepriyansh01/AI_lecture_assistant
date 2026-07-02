class MarkdownFormatter:

    @staticmethod
    def clean(text: str):

        text = text.strip()

        while "\n\n\n" in text:

            text = text.replace(

                "\n\n\n",

                "\n\n"

            )

        return text

final_summary = MarkdownFormatter.clean(

    final_summary

)