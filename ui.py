import streamlit as st
from rag_engine import ask_question

st.set_page_config(page_title="College Knowledge Chatbot")

st.title("🎓 College Knowledge Chatbot")
st.write("Ask questions about students, teachers, and courses.")

# Create chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
question = st.text_input("Ask a question")

if st.button("Ask"):

    if question:

        answer = ask_question(question)

        # Save conversation
        st.session_state.chat_history.append(("You", question))
        st.session_state.chat_history.append(("Bot", answer))

# Show chat history
for role, message in st.session_state.chat_history:

    if role == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")