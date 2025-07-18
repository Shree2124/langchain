import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import CohereEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import time

from dotenv import load_dotenv

load_dotenv()

# load apis
groq = os.getenv("GROQ_API_KEY")
cohere = os.getenv("COHERE_API")

# embedding:-
# embeddings = CohereEmbeddings(

# )

if "vector" not in st.session_state:
    st.session_state.embeddings = CohereEmbeddings(
        cohere_api_key=cohere, model="embed-english-v3.0", user_agent="MyApp/1.0"
    )
    st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs = st.session_state.loader.load()

    st.session_state.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(
        st.session_state.docs
    )
    st.session_state.vectors = FAISS.from_documents(
        st.session_state.final_documents, st.session_state.embeddings
    )


st.title("CHAT GROQ DEMO")
llm = ChatGroq(groq_api_key=groq, model_name="llama3-8b-8192")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the questions based on the provided context only. Please provide the most accurate response based on the question."),
    ("human", "Context:\n{context}\n\nQuestion: {input}")
])

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = st.session_state.vectors.as_retriever()
retriever_chain = create_retrieval_chain(retriever, document_chain)

prompt = st.text_input("Input your prompt here", placeholder="Ask a question...")

if prompt:
    start = time.process_time()
    response = retriever_chain.invoke({"input": prompt})
    print("Response time: ", time.process_time() - start)
    st.write(response["answer"])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")
