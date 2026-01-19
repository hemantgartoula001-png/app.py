import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="हेमन्तको AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# १. सेक्रेट साँचो तान्ने पक्का तरिका
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("हेमन्त, Streamlit Secrets मा साँचो हाल मुजी!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # एआईलाई कडा निर्देशन
            response = model.generate_content(f"You are Hemant's best friend. Answer in Nepali. Question: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलको सर्भर व्यस्त भयो, ५ मिनेट पछि 'Refresh' गर!")
