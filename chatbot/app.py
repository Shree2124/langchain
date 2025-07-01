# from dotenv import load_dotenv
# import os
# from langchain_openai import ChatOpenAI

# load_dotenv()



# llm = ChatOpenAI(
#     model_name="mistralai/mistral-7b-instruct",
#     openai_api_base="https://openrouter.ai/api/v1",
#     openai_api_key=api
# )

# result = llm.invoke("What is the capital of France?")
# print(result)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

# os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

api=os.getenv("OPENROUTER_API_KEY")

## prompt template

prompt = ChatPromptTemplate.from_messages(
    {
        ("system", "You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    }
)

## streamlit framework

st.title("Langchain demo with openairouter api")
input_text = st.text_input("Search the topic you want ")

## openAI LLM

llm=ChatOpenAI(
    model_name="mistralai/mistral-7b-instruct",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api
)

output_parser = StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))