from gtts import gTTS


def generate_audio(text, lang="en"):

    if isinstance(text, list):
        text = " ".join(str(t) for t in text)

    if not text or not text.strip():
        text = "No summary available."

    try:

        tts = gTTS(text=text, lang=lang,slow=False)

        tts.save("static/output.mp3")

    except:

        tts = gTTS(text="Audio generation failed.", lang="en")

        tts.save("static/output.mp3")