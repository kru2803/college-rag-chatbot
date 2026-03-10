import streamlit as st
from rag_engine import load_documents, ask_question

st.set_page_config(page_title="EduRAG", layout="wide")

st.title("🎓 EduRAG: AI-powered Education Knowledge Assistant")

# load knowledge only once
@st.cache_resource
def initialize_rag():
    load_documents()

initialize_rag()

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask something about students, teachers or courses...")

if question:

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    answer = ask_question(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
