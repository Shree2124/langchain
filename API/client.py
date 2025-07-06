import requests
import streamlit as st

def get_openrouter_res(input_text):
    try:
        response = requests.post(
            "http://localhost:8000/essay/invoke",
            json={'input': {'topic': input_text}}
        )
        response.raise_for_status()
        return response.json()['output']['content']
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e}\nResponse: {response.text}")
        return ""
    except Exception as e:
        st.error(f"Other Error: {e}")
        return ""
    

def get_groq_res(input_text):    
    try:
        response = requests.post(
            "http://localhost:8000/poem/invoke",
            json={'input': {'topic': input_text}}
        )
        response.raise_for_status()
        return response.json()['output']['content']
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e}\nResponse: {response.text}")
        return ""
    except Exception as e:
        st.error(f"Other Error: {e}")
        return ""
    
st.title("Langchain demo with openrouter and groq")
input_text = st.text_input("Write an essay on ")
input_text1 = st.text_input("Write an poem on ")

if st.button("Generate"):
    if input_text:
        st.write(get_openrouter_res(input_text))
    if input_text1:
        st.write(get_groq_res(input_text1))
