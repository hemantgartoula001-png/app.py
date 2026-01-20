import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="हेमन्तको AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# १. सेक्रेट साँचो तान्ने
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # यहाँ हामीले मोडेललाई अझ स्थिर (Stable) बनायौं
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
            # सर्भरलाई छिटो रेस्पोन्स दिन लगाउने सेटिङ
            response = model.generate_content(
                f"You are Hemant's best friend. Answer in short Nepali. Question: {prompt}",
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=500,
                    temperature=0.7,
                ),
            )
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error("सर्भर अझै अलि अल्छी छ, रिफ्रेस गरेर १ पटक फेरि प्रयास गर!")
