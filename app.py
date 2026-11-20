import streamlit as st
from rag_engine import load_base, ask_rag
st.set_page_config(page_title = "SIET_Chatbot", layout = "centered")
st.title("Shridevi Institute of Engineering and Technology - Chatbot")
st.caption("Ask anythimg about the college information , courses, placements, FAQs, rules and regulation")
st.caption("RAG pipeline with multiple files")
st.caption("craated by J RISHAB BHARATHI")

mykey = st.secrets["GROQ_API_KEY"]

@st.cache_resource
def initiate_rag():
  return load_base("college_docs")
index, embed_model, chunks = initiate_rag()

if "chat_hist" not in st.session_state:
  st.session_state.chat_hist = []

for qa in st.session_state.chat_hist :
  with st.chat_message(qa["role"]):
    st.write(qa["content"])


question = st.chat_input("Ask anything SIET collage..... ")

if question:
  st.session_state.chat_hist.append(
    {"role" :"user" , "content" : question})
  with st.chat_message("user"):
    st.write(question)
  with st.chat_message("assistant"):
    with st.spinner("Asking RAG for answer........"):
      answer = ask_rag (question, embed_model, chunks, index, api_key = mykey )
      st.write(answer)
      st.session_state.chat_hist.append(
       {"role" :"assistant" , "content" : answer})

if st.button("Clear chat"):
  st.session_state.chat_hist = []
  st.rerun()
