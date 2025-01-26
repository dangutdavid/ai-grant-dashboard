import spacy

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Sample grant text
grant_text = """
Apply for funding to:

explore the potential your organisation or department has to increase diversity of representation attracting a wider talent pool into NERC science

generate partnerships that identify, include and showcase a broad range of people and skillsets that contribute towards NERC science

You must be:

based at a UK research organisation eligible for NERC funding

in a role that meets the individual eligibility requirements

The full economic cost (FEC) of your project can be up to £62,500. We will fund 80% of the FEC.

Your project must start by July 2025 and end by March 2026.
"""

# Process the text with spaCy
doc = nlp(grant_text)

# Extract named entities
print("Extracted Entities:")
for ent in doc.ents:
    print(f"{ent.text} - {ent.label_}")

# Extract specific keywords (e.g., deadlines, funding amounts)
keywords = ["grants", "funding", "deadline", "applicants"]
print("\nKeyword Matches:")
for token in doc:
    if token.text.lower() in keywords:
        print(f"Keyword: {token.text}, Context: {token.sent.text.strip()}")
