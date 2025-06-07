import matplotlib.pyplot as plt
import pandas as pd  # This line fixes the erro
# Load the CSV file into a DataFrame
df = pd.read_csv("Questionnaire for Gamers & Digital-Fashion Consumers.csv")

# Show the first few rows
df.head()
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 5])
plt.ylabel('some numbers')
plt.show()
df = pd.read_csv("Questionnaire for Gamers & Digital-Fashion Consumers.csv")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Set page title
st.set_page_config(page_title="🎮 Gamer Digital Fashion Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Questionnaire for Gamers & Digital-Fashion Consumers.csv")
    return df

df = load_data()

# Clean column names (remove leading/trailing spaces)
df.columns = df.columns.str.strip()

# Sidebar filters
st.sidebar.title("🔍 Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df["Region:"].dropna().unique())
selected_age = st.sidebar.multiselect("Select Age Group", options=df["What is your age group?"].dropna().unique())

# Filtered dataframe
filtered_df = df.copy()
if selected_region:
    filtered_df = filtered_df[filtered_df["Region:"].isin(selected_region)]
if selected_age:
    filtered_df = filtered_df[filtered_df["What is your age group?"].isin(selected_age)]

# Title
st.title("🎮 Gamer & Digital Fashion Survey Dashboard")
st.markdown("Explore how gamers interact with digital fashion and cultural identity.")

# Section 1: Monthly Spending
st.subheader("💸 Monthly Spending on Digital Cosmetics")

def clean_spending(val):
    if pd.isna(val):
        return 0
    val = str(val).lower()
    digits = ''.join(filter(str.isdigit, val.split()[0]))
    return int(digits) if digits else 0

try:
    filtered_df['cleaned_spending'] = filtered_df['Approximate spent per month on digital cosmetics:'].apply(clean_spending)
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['cleaned_spending'], bins=10, kde=True, ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.write("Unable to parse spending values.")

# Section 2: Agreement Ratings
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

# Section 3: Cultural Representation
st.subheader("🌍 Cultural Representation in Skins")

col_name = "Have you ever selected a skin or digital cosmetic because you recognized its cultural origin?"
response_counts = filtered_df[col_name].value_counts(dropna=False)

fig, ax = plt.subplots()
sns.barplot(x=response_counts.index, y=response_counts.values, ax=ax)
ax.set_xlabel("Response")
ax.set_ylabel("Count")
plt.xticks(rotation=45)
st.pyplot(fig)

# Section 4: Word Cloud from Open Responses
st.subheader("💬 Text Insights: Misrepresentative Garments")

text_col = "Describe an example of a digital garment that felt misrepresentative to you."
text_data = " ".join(filtered_df[text_col].dropna().str.lower())

if text_data:
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
else:
    st.write("No text responses available for analysis.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io)") 