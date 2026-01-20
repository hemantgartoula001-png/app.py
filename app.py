import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. सुरक्षित साँचो तान्ने (Secrets बाट मात्र)
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("ओए हेमन्त, Streamlit Secrets मा साँचो हाल मुजी!")
    st.stop()

# ३. मेमोरी (पुराना गफ सम्झिने)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ४. गफगाफ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"You are Hemant's best friend. Answer in Nepali. Question: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलको सर्भरमा जाम भयो, १ मिनेट पछि 'Refresh' गर!")
