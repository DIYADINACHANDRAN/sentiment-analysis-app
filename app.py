import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Sentiment AI 🧠", page_icon="💬", layout="centered")

# --- Beautiful Gradient Background & Custom Styles ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #d3cce3, #e9e4f0);
    }
    .main {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 2rem;
        box-shadow: 0px 0px 30px rgba(0, 0, 0, 0.15);
    }
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .button {
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        font-size: 16px;
        border-radius: 12px;
        cursor: pointer;
    }
    .analyze { background-color: #6c5ce7; }
    .clear { background-color: #d63031; }
    </style>
    <div class="main">
""", unsafe_allow_html=True)

# --- Heading ---
st.markdown('<div class="floating" style="text-align:center;font-size:50px;">🧠</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>Sentiment Analyzer AI</h1>", unsafe_allow_html=True)
st.write("Analyze how someone **feels** about anything — instantly!")

# --- Session State for text input ---
if "text" not in st.session_state:
    st.session_state.text = ""

# --- Input ---
text = st.text_area("💬 Enter your thoughts here:", value=st.session_state.text, height=150, placeholder="Type something like 'I love this app!'")

# --- Buttons ---
col1, col2 = st.columns([1, 1])
with col1:
    analyze = st.button("🔍 Analyze")
with col2:
    clear = st.button("🧹 Clear Text")

if clear:
    st.session_state.text = ""
    st.rerun()

# --- Analysis ---
if analyze:
    if text.strip():
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        st.session_state.text = text

        # Emoji Result
        if sentiment > 0:
            st.success("😊 Sentiment:wooww..You entered a Positive Sentence")
            icon = "🟢"
        elif sentiment == 0:
            st.info("😐 Sentiment:Hoo Its a Neutral Sentence")
            icon = "🟡"
        else:
            st.error("😢 Sentiment:OMG Its a Negative Sentence")
            icon = "🔴"

        # --- Bar Chart ---
        st.subheader("📊 Sentiment Score")
        fig, ax = plt.subplots()
        ax.bar(["Sentiment"], [sentiment], color="green" if sentiment > 0 else "red" if sentiment < 0 else "gray")
        ax.set_ylim(-1, 1)
        ax.axhline(0, color='black', linestyle='--', linewidth=0.5)
        ax.set_ylabel("Polarity Score")
        st.pyplot(fig)

        # --- Word Cloud ---
        st.subheader("🧠 See the Mind (Word Cloud)")
        wc = WordCloud(width=600, height=300, background_color='white').generate(text)
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wc, interpolation="bilinear")
        ax_wc.axis("off")
        st.pyplot(fig_wc)

        # --- History ---
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "text": text,
            "score": round(sentiment, 3),
            "label": icon,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        st.warning("⚠️ Please type something to analyze.")

# --- Rating Bar ---
st.markdown("### ⭐ Rate this App")
rating = st.slider("How do you like the app?", 1, 5, 4)
st.write(f"Thanks for rating us {rating} ⭐")

# --- Display Last 5 Inputs ---
if "history" in st.session_state and st.session_state.history:
    st.markdown("### 🕓 Recent Entries")
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"<div style='padding:8px;background:#f9f9f9;border-radius:10px;margin-bottom:6px;'><b>{item['time']}</b> — {item['label']}<br><i>{item['text']}</i></div>", unsafe_allow_html=True)

# --- Close div ---
st.markdown("</div>", unsafe_allow_html=True)
