import streamlit as st
import json

# Load grants and AI-generated recommendations
with open("grants.json", "r") as grant_file:
    grants = json.load(grant_file)

# Simulated recommendations (replace with actual AI results if needed)
recommendations = [
    "Dr. Alice Smith and Dr. John Doe are the best candidates for the Renewable Energy Research Grant due to their expertise in renewable energy and solar energy.",
    "Dr. Jane Lee is the ideal candidate for the Climate Change Policy Grant based on her focus on climate science and policy analysis.",
    "Dr. Mark White is highly suitable for the AI for Public Health Grant due to his expertise in artificial intelligence and public health applications."
]

# Streamlit Dashboard
st.title("AI Grant Proposal Assistant Dashboard")

# Loop through grants and display them
for i, grant in enumerate(grants):
    st.header(f"Grant: {grant['title']}")
    st.write(f"**Description:** {grant['description']}")
    st.write(f"**AI Recommendations:** {recommendations[i]}")
    st.write("---")
