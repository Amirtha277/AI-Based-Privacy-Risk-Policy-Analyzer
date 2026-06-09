import re


def detect_risks(text):

    sentences = re.split(r'[.!?]', text)

    risks = []

    for s in sentences:

        s_low = s.lower()

        if "third party" in s_low or "share" in s_low:
            risks.append((s.strip(), "High Risk"))

        elif "personal data" in s_low or "information we collect" in s_low:
            risks.append((s.strip(), "Sensitive"))

        elif "location" in s_low or "gps" in s_low:
            risks.append((s.strip(), "Medium Risk"))

        elif "cookies" in s_low:
            risks.append((s.strip(), "Medium Risk"))

        elif "advertising" in s_low or "ads" in s_low:
            risks.append((s.strip(), "Medium Risk"))

        elif "retain" in s_low or "storage" in s_low:
            risks.append((s.strip(), "Low Risk"))

    if len(risks) < 3:

        risks.append(("User activity may be monitored", "Medium Risk"))
        risks.append(("Policy terms may change without notice", "Low Risk"))

    return risks[:6]

def extract_risky_sentences(text):

    keywords = [
        "third party",
        "share",
        "tracking",
        "cookies",
        "advertising",
        "collect personal"
    ]

    sentences = text.split(".")

    risky = []

    for s in sentences:

        for k in keywords:

            if k in s.lower():
                risky.append(s.strip())
                break

    return risky[:5]