import streamlit as st
import json

# Function to calculate confidence score
def calculate_confidence(grant_keywords, researcher_expertise):
    grant_keywords = set(grant_keywords)
    expertise_keywords = set(researcher_expertise.split(", "))
    overlap = grant_keywords & expertise_keywords
    return len(overlap) / len(grant_keywords) * 100  # Percentage

# Example keywords for each grant
grant_keywords_map = {
    "Renewable Energy Research Grant": ["renewable energy", "research", "solar energy"],
    "Climate Change Policy Grant": ["climate change", "policy", "adaptation", "mitigation"],
    "AI for Public Health Grant": ["artificial intelligence", "public health", "AI", "health outcomes"],
}

# Load grants and researcher datasets
with open("grants.json", "r") as grant_file:
    grants = json.load(grant_file)

with open("researchers.json", "r") as researcher_file:
    researchers = json.load(researcher_file)

# Calculate recommendations with confidence scores
recommendations = []
for grant in grants:
    grant_title = grant["title"]
    grant_keywords = grant_keywords_map.get(grant_title, [])
    grant_recommendations = []

    for researcher in researchers:
        score = calculate_confidence(grant_keywords, researcher["expertise"])
        grant_recommendations.append({"name": researcher["name"], "score": score})

    # Sort recommendations by score
    grant_recommendations = sorted(grant_recommendations, key=lambda x: x["score"], reverse=True)
    recommendations.append({"grant": grant_title, "recommendations": grant_recommendations})

# Streamlit Dashboard
st.title("AI Grant Proposal Assistant Dashboard")

# Filters
min_score = st.slider("Minimum Confidence Score", 0, 100, 50)

# Display grants and filtered recommendations
for i, grant in enumerate(grants):
    st.header(f"Grant: {grant['title']}")
    st.write(f"**Description:** {grant['description']}")

    st.subheader("Recommendations:")
    for rec in recommendations[i]["recommendations"]:
        if rec["score"] >= min_score:
            st.write(f"- **{rec['name']}** with a confidence score of **{rec['score']:.2f}%**")

    st.write("---")
