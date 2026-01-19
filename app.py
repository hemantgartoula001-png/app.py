import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. सुरक्षित चाबी (Secrets बाट तान्ने - कसैले चोर्न नसक्ने)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("ओए हेमन्त, Streamlit 'Secrets' मा साँचो हाल मुजी!")
    st.stop()

# ३. उपलब्ध मोडल खोज्ने (Gemini 1.5 Flash प्रयोग गर्नु उत्तम हुन्छ)
model = genai.GenerativeModel("gemini-1.5-flash")

# ४. च्याट मेमोरी (यो कहिल्यै हराउँदैन)
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना गफहरू देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # बलियो मेमोरीको लागि पुराना गफको सन्दर्भ दिने
            context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। यो गफ सम्झेर नेपालीमा उत्तर दिनुहोस्: {context}\nहेमन्त: {prompt}")
            
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगल रिसाएको छ, 'Secrets' मा साँचो चेक गर अनि १ मिनेट पछि 'Refresh' गर!")
