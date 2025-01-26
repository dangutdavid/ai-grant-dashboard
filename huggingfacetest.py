from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")
result = generator("Write an abstract for a policy brief on climate change.", max_length=100)
print(result[0]['generated_text'])
