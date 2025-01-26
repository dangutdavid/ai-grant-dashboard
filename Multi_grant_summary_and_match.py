import spacy
import openai
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# OpenAI API Key
openai.api_key = "your-openai-api-key"

# Load grants and researcher datasets
with open("grants.json", "r") as grant_file:
    grants = json.load(grant_file)

with open("researchers.json", "r") as researcher_file:
    researchers = json.load(researcher_file)

# Process each grant
for grant in grants:
    print(f"Processing Grant: {grant['title']}")
    
    # Extract key details with spaCy
    doc = nlp(grant["description"])
    extracted_info = [f"{ent.text} ({ent.label_})" for ent in doc.ents]
    
    # Pass extracted details to OpenAI for recommendations
    prompt = f"""
    Match the following grant description to researchers based on their expertise:

    Grant Title:
    {grant['title']}

    Grant Description:
    {grant['description']}

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
    print("\n")
