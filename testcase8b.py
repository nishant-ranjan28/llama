from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

st.title("Manual Test Case Generator ")
CONTEXT="""
- As a user, I want to be able to download the Rooster browser extension from the webstore for Microsoft Edge, and Chrome so that I can easily install and use it on my preferred browser.
- As a user, I want to be able to access Rooster without navigating away from the candidate page in Workday so that I can perform all necessary actions more efficiently.
- As a user, I want to see the interviewer’s invite status in the Workday interview schedule so that I can quickly understand the availability and commitment of interviewers.
- As a user, I want documentation surrounding the plugin that I can provide to my IT teams when requesting approval so that they can understand its functionality, security, and installation requirements.
 """

template = """Generate concise manual test case scenarios based on the following context. Each scenario should:
1. Have a clear title
2. Include steps to execute
3. Specify expected results

Context:
{CONTEXT}

Provide 25 possible test scenarios covering key functionalities and potential edge cases.

Question: {question}
"""

#prompt = ChatPromptTemplate.from_template(template)
prompt = PromptTemplate(template = template, input_variables="CONTEXT")

model = OllamaLLM(model="llama3.1", verbose=True)

chain = prompt.partial(CONTEXT=CONTEXT) | model

# Initialize chat history in Streamlit session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.chat_input("Enter your question here")

if question:
    # Append new question to chat history
    st.session_state.chat_history.append(f"User: {question }")

    # Construct chat history string
    chat_history_str = "\n".join(st.session_state.chat_history)
    
    # Invoke the chain with the chat history and current question
    response = chain.invoke({"chat_history": chat_history_str, "question": question })
    
    # Append the response to chat history
    st.session_state.chat_history.append(f"Assistant: {response }")

# Display the chat history
for message in st.session_state.chat_history:
    if message.startswith("User:"):
        st.markdown(f"**{message }**")
    else:
        st.markdown(message)
