import streamlit as st
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

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
st.title("AI Grant Proposal Assistant Dashboard with Multi-Grant Comparison")

# Filters
min_score = st.slider("Minimum Confidence Score", 0, 100, 50)
compare_grants = st.multiselect(
    "Select Grants to Compare", [grant["title"] for grant in grants]
)

# Multi-Grant Comparison Visualization
if compare_grants:
    st.header("Multi-Grant Comparison")

    # Prepare data for comparison
    comparison_data = []
    for grant in grants:
        if grant["title"] in compare_grants:
            total_recommendations = len(
                [rec for rec in recommendations if rec["grant"] == grant["title"]]
            )
            funding = grant.get("funding", "N/A")
            deadline = grant.get("deadline", "N/A")
            comparison_data.append({
                "Grant": grant["title"],
                "Funding": funding,
                "Deadline": deadline,
                "Total Recommendations": total_recommendations,
            })

    # Create a dataframe for the comparison
    df_comparison = pd.DataFrame(comparison_data)

    # Display the comparison table
    st.dataframe(df_comparison)

    # Bar chart for total recommendations
    plt.figure(figsize=(8, 4))
    plt.bar(df_comparison["Grant"], df_comparison["Total Recommendations"], color="skyblue")
    plt.xlabel("Grant")
    plt.ylabel("Total Recommendations")
    plt.title("Comparison of Total Recommendations for Selected Grants")
    st.pyplot(plt)
else:
    st.write("Select grants to compare using the dropdown above.")

# Display grants and filtered recommendations with visualizations
for i, grant in enumerate(grants):
    st.header(f"Grant: {grant['title']}")
    st.write(f"**Description:** {grant['description']}")

    # Calculate days left to apply
    if "deadline" in grant:
        try:
            deadline = datetime.strptime(grant["deadline"], "%Y-%m-%d")
            days_left = (deadline - datetime.now()).days
            st.write(f"**Days Left to Apply:** {days_left} days")
        except Exception as e:
            st.write("**Deadline:** N/A")

    st.subheader("Recommendations:")
    grant_recommendations = recommendations[i]["recommendations"]

    # Apply minimum score filter
    filtered_recommendations = [rec for rec in grant_recommendations if rec["score"] >= min_score]
    for rec in filtered_recommendations:
        st.write(f"- **{rec['name']}** with a confidence score of **{rec['score']:.2f}%**")

    # Visualization: Bar chart of confidence scores
    st.subheader("Confidence Scores Visualization")
    if filtered_recommendations:
        names = [rec["name"] for rec in filtered_recommendations]
        scores = [rec["score"] for rec in filtered_recommendations]

        plt.figure(figsize=(8, 4))
        plt.bar(names, scores, color="lightgreen")
        plt.xlabel("Researchers")
        plt.ylabel("Confidence Score")
        plt.title(f"Confidence Scores for {grant['title']}")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt)
    else:
        st.write("No recommendations meet the minimum confidence score.")

    st.write("---")
