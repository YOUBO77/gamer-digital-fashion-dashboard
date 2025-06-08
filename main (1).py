import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="🎮 Gamer Digital Fashion Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Questionnaire for Gamers & Digital-Fashion Consumers.csv")
    return df

df = load_data()

# Display column names for debugging (remove/comment after confirming)
# st.write("Columns:", df.columns.tolist())

# Clean column names (strip spaces)
df.columns = df.columns.str.strip()

# Sidebar filters
st.sidebar.title("🔍 Filters")
region_col = "Region:" if "Region:" in df.columns else df.columns[df.columns.str.contains("Region")][0]
age_col = "What is your age group?" if "What is your age group?" in df.columns else df.columns[df.columns.str.contains("age group")][0]

selected_region = st.sidebar.multiselect("Select Region", options=df[region_col].dropna().unique())
selected_age = st.sidebar.multiselect("Select Age Group", options=df[age_col].dropna().unique())

filtered_df = df.copy()
if selected_region:
    filtered_df = filtered_df[filtered_df[region_col].isin(selected_region)]
if selected_age:
    filtered_df = filtered_df[filtered_df[age_col].isin(selected_age)]

# Title
st.title("🎮 Gamer & Digital Fashion Survey Dashboard")
st.markdown("Explore how gamers interact with digital fashion and cultural identity.")

# Monthly Spending
st.subheader("💸 Monthly Spending on Digital Cosmetics")

spending_col = 'Approximate spent per month on digital cosmetics:'
if spending_col not in filtered_df.columns:
    spending_col = filtered_df.columns[filtered_df.columns.str.contains("spen", case=False)][0]

def clean_spending(val):
    if pd.isna(val): return 0
    val = str(val).lower()
    digits = ''.join(filter(str.isdigit, val))
    return int(digits) if digits else 0

try:
    filtered_df['cleaned_spending'] = filtered_df[spending_col].apply(clean_spending)
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['cleaned_spending'], bins=10, kde=True, ax=ax)
    plt.xlabel("Spending ($)")
    plt.ylabel("Frequency")
    plt.title("Monthly Spending on Digital Cosmetics")
    st.pyplot(fig)
except Exception as e:
    st.write(f"Unable to parse spending values. Error: {e}")

# Agreement Ratings
st.subheader("🧠 Agreement Analysis")

# Update these to match your exact column names!
rating_cols = [
    "Customizing my avatar's outfit helps me present my true self.",
    "Digital fashion lets me experiment with identities I couldn't explore in the real world.",
    "I'm concerned that many digital outfits borrow cultural motifs without credit."
]
# Try fuzzy matching if exact names aren't found
def find_col(target):
    for c in df.columns:
        if target.lower() in c.lower():
            return c
    return None

for raw_col in rating_cols:
    col = find_col(raw_col)
    if col is None:
        st.write(f"Column not found: {raw_col}")
        continue
    try:
        filtered_df[col] = pd.to_numeric(filtered_df[col], errors='coerce')
        avg = filtered_df[col].mean()
        st.write(f"**{col}** - Average Rating: {avg:.2f}")
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x=col, ax=ax)
        plt.xlabel("Rating (1–7)")
        plt.ylabel("Count")
        plt.title(col)
        st.pyplot(fig)
    except Exception as e:
        st.write(f"Error processing {col}: {e}")

# Cultural Recognition
st.subheader("🌏 Cultural Recognition")

# Try to find the column with a fuzzy match if not found
cultural_col = "Have you ever selected a skin or digital cosmetic because you recognized its cultural origin? "
if cultural_col not in filtered_df.columns:
    for c in filtered_df.columns:
        if "cultural origin" in c.lower():
            cultural_col = c
            break

try:
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x=cultural_col, ax=ax)
    plt.xlabel("Response")
    plt.ylabel("Count")
    plt.title("Selected Skin Based on Cultural Origin?")
    plt.xticks(rotation=45)
    st.pyplot(fig)
except Exception as e:
    st.write(f"Error with cultural recognition chart: {e}")

# Word Cloud from open responses
st.subheader("☁️ Words in Misrepresentation Examples")
text_col = "Describe an example of a digital garment that felt misrepresentative to you."
if text_col not in filtered_df.columns:
    for c in filtered_df.columns:
        if "misrepresent" in c.lower():
            text_col = c
            break

text_data = " ".join(filtered_df[text_col].dropna().astype(str))
if text_data.strip():
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    except Exception as e:
        st.write(f"Error generating word cloud: {e}")
else:
    st.write("No open responses found for word cloud.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io)")
