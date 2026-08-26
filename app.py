import streamlit as st
import pandas as pd
from textblob import TextBlob

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Review Intelligence", layout="wide")

# ------------------ HEADER ------------------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
📊 Customer Review Intelligence System
</h1>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("📌 Menu")
option = st.sidebar.radio("Choose Input Type:", ["Upload File", "Manual Input"])
st.sidebar.info("Analyze customer sentiment using NLP")

# ------------------ SENTIMENT FUNCTION ------------------
# ------------------ SENTIMENT FUNCTION ------------------
def get_sentiment(text):
    text_lower = str(text).lower().strip()

    # Negative phrases
    negative_phrases = [
        "don't love",
        "do not love",
        "not love",
        "don't like",
        "do not like",
        "not good",
        "not happy",
        "not satisfied",
        "not worth",
        "very bad",
        "very poor",
        "damaged product",
        "product is damaged",
        "damaged",
        "broken",
        "defective",
        "worst",
        "terrible",
        "awful",
        "useless",
        "disappointed",
        "disappointing"
    ]

    # Positive phrases
    positive_phrases = [
        "love this",
        "love it",
        "really good",
        "very good",
        "excellent",
        "amazing",
        "awesome",
        "perfect",
        "highly recommend"
    ]

    # Check negative phrases FIRST
    if any(phrase in text_lower for phrase in negative_phrases):
        return "Negative"

    # Check positive phrases
    if any(phrase in text_lower for phrase in positive_phrases):
        return "Positive"

    # TextBlob sentiment for other reviews
    polarity = TextBlob(text_lower).sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# ------------------ EMPTY DATAFRAME ------------------
df = pd.DataFrame(columns=["review"])

# ------------------ SAMPLE DATA BUTTON ------------------
st.markdown("### 🚀 Get Started")

if st.button("📊 Try Sample Data"):
    sample_data = pd.DataFrame({
        "review": [
            "Great product",
            "Very bad experience",
            "Loved it!",
            "Not worth the price",
            "Amazing quality",
            "Terrible support"
        ]
    })
    sample_data["Sentiment"] = sample_data["review"].apply(get_sentiment)
    df = pd.concat([df, sample_data], ignore_index=True)
    st.success("✅ Sample data loaded!")

# ================== FILE UPLOAD ==================
if option == "Upload File":
    st.subheader("📂 Upload CSV File")

    uploaded_file = st.file_uploader("Upload your reviews file", type=["csv"])

    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)

        # Automatically detect review column
        possible_review_columns = [
            "review",
            "reviews",
            "customer review",
            "customer reviews",
            "customer_review",
            "customer_reviews",
            "feedback",
            "comment",
            "comments"
        ]

        # Create mapping with normalized column names
        column_mapping = {
            str(col).strip().lower().replace("_", " "): col
            for col in uploaded_df.columns
        }

        review_column = None

        # Find a matching review column
        for possible_column in possible_review_columns:
            if possible_column in column_mapping:
                review_column = column_mapping[possible_column]
                break

        if review_column is None:
            st.error(
                "⚠️ We couldn't identify a review column. "
                "Please upload a CSV containing customer review or feedback text."
            )
        else:
            # Rename detected column to 'review'
            uploaded_df = uploaded_df.rename(
                columns={review_column: "review"}
            )

            # Analyze sentiment
            uploaded_df["Sentiment"] = uploaded_df["review"].apply(get_sentiment)

            df = pd.concat([df, uploaded_df], ignore_index=True)

            st.success(
                f"✅ File uploaded and analyzed successfully! "
                f"Detected review column: '{review_column}'"
            )
# ================== MANUAL INPUT ==================
elif option == "Manual Input":
    st.subheader("✍️ Enter Reviews")

    user_input = st.text_area("Enter multiple reviews (one per line):")

    if user_input:
        reviews = user_input.split("\n")

        new_df = pd.DataFrame({"review": reviews})
        new_df["Sentiment"] = new_df["review"].apply(get_sentiment)

        df = pd.concat([df, new_df], ignore_index=True)

        st.success("✅ Reviews analyzed!")
        st.write("### 🆕 New Reviews")

        # Clean table
        new_df_display = new_df.copy()
        new_df_display["Sentiment"] = new_df_display["Sentiment"].map({
            "Positive": "😊 Positive",
            "Neutral": "😐 Neutral",
            "Negative": "😡 Negative"

        })

        st.dataframe(new_df_display, use_container_width=True, hide_index=True)

# ------------------ DASHBOARD ------------------
if not df.empty:

    if "Sentiment" not in df.columns:
        df["Sentiment"] = df["review"].apply(get_sentiment)

    total = len(df)
    positive = (df["Sentiment"] == "Positive").sum()
    negative = (df["Sentiment"] == "Negative").sum()
    neutral = (df["Sentiment"] == "Neutral").sum()

    st.markdown("## 📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Reviews", total)
    col2.metric("😊 Positive", positive)
    col3.metric("😐 Neutral", neutral)
    col4.metric("😡 Negative", negative)

    # ------------------ INSIGHT SUMMARY ------------------
    positive_ratio = positive / total if total > 0 else 0

    if positive_ratio > 0.8:
        overall = "🌟 Excellent!"
    elif positive_ratio > 0.6:
        overall = "👍 Good!"
    elif positive_ratio > 0.4:
        overall = "⚖️ Needs Improvement!"
    elif positive_ratio > 0.2:
        overall = "⚠️ Below Expectations!"
    else:
        overall = "🚨 Critical Attention Needed!"

    st.markdown("## 🧠 Overall Insight")
    st.info(f"Overall Product Feedback: {overall}")
    st.write(f"📈 {positive_ratio*100:.1f}% of reviews are positive")

    # ------------------ CHART ------------------
    st.markdown("### 📈 Sentiment Distribution")
    sentiment_counts = df["Sentiment"].value_counts()
    st.bar_chart(sentiment_counts)

    # ------------------ TABLE ------------------
    st.markdown("### 📋 Review Data")

    df_display = df.copy()
    df_display["Sentiment"] = df_display["Sentiment"].map({
        "Positive": "😊 Positive",
        "Neutral": "😐 Neutral",
        "Negative": "😡 Negative"
    })

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # ------------------ DOWNLOAD ------------------
    st.download_button(
        "📥 Download Results",
        df.to_csv(index=False),
        "analyzed_reviews.csv",
        "text/csv"
    )

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("<center>Made with ❤️ using Streamlit</center>", unsafe_allow_html=True)
