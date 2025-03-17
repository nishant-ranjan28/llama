from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

st.title("Test Case Generator ")
CONTEXT="""
- WQL supports jobcustomData field
- jobcustomData field can now be separate fields in separate columns instead of one string of data
- In order for clients to separate their custom data fields, they will need to switch their CLAR file to v2.0 and utilize WQL as their integration method
- Update the UI to allow Rooster team to add the custom data fields and test that with using WQL it is returning the proper data
- This UI element will only show if WQL is toggled ON
- The custom job data field name can be edited (similar to reporting)
- The user provides the WQL
- A button to test that WQL is working as expected
- ***Clients will not have access to the Custom Field tab. This is only for Rooster team to add the custom fields***
- All custom fields that are pulled into Rooster should reflect under Analytics → Reporting
- All custom fields that are pulled into Rooster should reflect on the Dashboard if enabled by the user
- Custom fields should be brought in as placeholders in templates.
 """

template = """Generate concise manual test case scenarios based on the following context. Each scenario should:
1. Have a clear title
2. Include steps to execute
3. Specify expected results

Context:
{CONTEXT}

Provide 20 possible test scenarios covering key functionalities and potential edge cases.

Question: {question}
"""
question = "What are the possible test scenarios for the given context?"

#prompt = ChatPromptTemplate.from_template(template)
prompt = PromptTemplate(template = template, input_variables="CONTEXT")

model = OllamaLLM(model="llama3.1:70b", verbose=True)

chain = {"question": itemgetter("question")}| prompt.partial(CONTEXT=CONTEXT) | model
response = chain.invoke({"question": question })
print (response)

# # Initialize chat history in Streamlit session state if not already present
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# question = st.chat_input("Enter your question here")

# if question:
#     # Append new question to chat history
#     st.session_state.chat_history.append(f"User: {question }")

#     # Construct chat history string
#     chat_history_str = "\n".join(st.session_state.chat_history)
    
#     # Invoke the chain with the chat history and current question
#     response = chain.invoke({"chat_history": chat_history_str, "question": question })
    
#     # Append the response to chat history
#     st.session_state.chat_history.append(f"Assistant: {response }")

# # Display the chat history
# for message in st.session_state.chat_history:
#     if message.startswith("User:"):
#         st.markdown(f"**{message }**")
#     else:
#         st.markdown(message)
