from transformers import pipeline
from deep_translator import GoogleTranslator


summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)


def summarize_text(text):

    if not text:
        return "No content available."

    text = text[:2000]

    try:

        result = summarizer(
            text,
            max_length=120,
            min_length=40,
            do_sample=False
        )

        return result[0]["summary_text"]

    except:

        sentences = text.split(". ")
        return ". ".join(sentences[:4])


def translate_text(text, lang):

    if lang == "en":
        return text

    try:
        return GoogleTranslator(source="auto", target=lang).translate(text)
    except:
        return text