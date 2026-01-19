import streamlit as st
import google.generativeai as genai

# १. एपको सेटअप
st.set_page_config(page_title="हेमन्तको AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. नयाँ साँचो Secrets बाट सुरक्षित रूपमा तान्ने
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("ओए हेमन्त, नयाँ Google Account को साँचो Secrets मा हाल मुजी!")
    st.stop()

# ३. बलियो मेमोरी सिस्टम (Session State)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ४. पुराना गफहरू देखाउने
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            # पुराना गफको सन्दर्भ सहित उत्तर माग्ने
            context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history[-5:]])
            response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। यो गफ सम्झेर नेपालीमा उत्तर दिनुहोस्: {context}\nहेमन्त: {prompt}")
            
            msg = response.text
            st.write(msg)
            st.session_state.chat_history.append({"role": "assistant", "content": msg})
        except Exception:
            st.error("गुगलले अझै टेरेन, १ मिनेट पछि 'Refresh' गर!")
