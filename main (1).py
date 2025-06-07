# main.py
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

# Clean column names
df.columns = df.columns.str.strip()

# Sidebar filters
st.sidebar.title("🔍 Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df["Region:"].dropna().unique())
selected_age = st.sidebar.multiselect("Select Age Group", options=df["What is your age group?"].dropna().unique())

filtered_df = df.copy()
if selected_region:
    filtered_df = filtered_df[filtered_df["Region:"].isin(selected_region)]
if selected_age:
    filtered_df = filtered_df[filtered_df["What is your age group?"].isin(selected_age)]

# Title
st.title("🎮 Gamer & Digital Fashion Survey Dashboard")
st.markdown("Explore how gamers interact with digital fashion and cultural identity.")

# Monthly Spending
st.subheader("💸 Monthly Spending on Digital Cosmetics")

def clean_spending(val):
    if pd.isna(val): return 0
    val = str(val).lower()
    digits = ''.join(filter(str.isdigit, val))
    return int(digits) if digits else 0

try:
    filtered_df['cleaned_spending'] = filtered_df['Approximate spent per month on digital cosmetics:'].apply(clean_spending)
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['cleaned_spending'], bins=10, kde=True, ax=ax)
    st.pyplot(fig)
except:
    st.write("Unable to parse spending values.")

# Agreement Ratings
st.subheader("🧠 Agreement Analysis")

rating_cols = [
    "“Customizing my avatar’s outfit helps me present my true self.”",
    "“Digital fashion lets me experiment with identities I couldn’t explore in the real world.”",
    "“I’m concerned that many digital outfits borrow cultural motifs without credit.”"
]

for col in rating_cols:
    try:
        filtered_df[col] = pd.to_numeric(filtered_df[col])
        avg = filtered_df[col].mean()
        st.write(f"**{col}** - Average Rating: {avg:.2f}")
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x=col, ax=ax)
        st.pyplot(fig)
    except:
        continue

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io)") 
    
