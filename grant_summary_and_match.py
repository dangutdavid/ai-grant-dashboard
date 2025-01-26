import spacy
import openai
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# OpenAI API Key
openai.api_key = "your-openai-api-key"

# Sample grant text
grant_text = """
The International Development Fund is providing grants of up to $500,000 for research projects in renewable energy.
Eligible applicants include universities and research institutions. The deadline for applications is March 15, 2025.
"""

# Load researcher dataset
with open("researchers.json", "r") as file:
    researchers = json.load(file)

# Step 1: Extract key details with spaCy
doc = nlp(grant_text)
extracted_info = []
for ent in doc.ents:
    extracted_info.append(f"{ent.text} ({ent.label_})")

# Step 2: Match grants to researchers using OpenAI
prompt = f"""
Match the following grant description to researchers based on their expertise:

Grant Description:
{grant_text}

Extracted Information:
{', '.join(extracted_info)}

Researchers and Their Expertise:
{', '.join([f"{r['name']} - {r['expertise']}" for r in researchers])}

Recommend the most suitable researchers for this grant and explain why.
"""

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for grant proposal tasks."},
        {"role": "user", "content": prompt},
    ],
    max_tokens=300
)

# Print the AI-generated recommendations
print("AI-Generated Recommendations:")
print(response['choices'][0]['message']['content'].strip())