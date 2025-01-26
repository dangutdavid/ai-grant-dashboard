import openai

# Set your API key
openai.api_key = "your-openai-api-key"
# Test OpenAI with a simple prompt
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Use the newer model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short summary of a grant proposal for renewable energy research."}
    ],
    max_tokens=100
)

# Print the result
print(response['choices'][0]['message']['content'].strip())
