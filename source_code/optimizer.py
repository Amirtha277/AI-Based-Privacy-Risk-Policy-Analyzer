import re

def optimize_text(text):
    """
    Optimize privacy policy text before summarization
    """

    if not text:
        return ""

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # remove very short sentences
    sentences = text.split(".")

    filtered = []

    for s in sentences:
        s = s.strip()

        if len(s) > 40:
            filtered.append(s)

    optimized_text = ". ".join(filtered)

    return optimized_text