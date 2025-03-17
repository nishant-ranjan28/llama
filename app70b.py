from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

st.title("Test Case Generator ")
CONTEXT="""
Test Case References:
test.describe("Integration test for schedule single day interview by office User", () => {
 test("C25264 - Verify if single day interview is scheduled successfully by Office user", async ({
   request
  }) => {
   const expectedFirstInterviewsData =
     schedulePayload.interviews[0].interviews[0];


   const expectedLocation = ${expectedFirstInterviewsData.conferencing[0].name }${expectedFirstInterviewsData.conferencing[0].type }: ${expectedFirstInterviewsData.conferencing[1].name };
   const expectedQuestionnaire =
     expectedFirstInterviewsData.skills[0].name.trim();
   const expectedCompetencies =
     expectedFirstInterviewsData.skills[1].name.trim();
   const expectedInterviewType =
     expectedFirstInterviewsData.conferencing[0].name;
   const expectedFirstInterviewerDetails = ${expectedFirstInterviewsData.interviewers[0].firstName } ${expectedFirstInterviewsData.interviewers[0].lastName };


   const modifiedSchedulePayload = modifySingleDaySchedulePayload(
     schedulePayload,
     interviewID
   );


   await scheduleOfficeInterview(request, modifiedSchedulePayload);
   await waitForSentStatusInInterviewDoc(interviewID);
   await waitForApplicationDocToLoad(applicationId);


   const modifiedCandidateInvitePayload = modifyCandidateInvitePayload(
     candidateInvitePayload,
     interviewID
   );


   await sendInterviewInviteToCandidateOffice(
     request,
     modifiedCandidateInvitePayload
   );


   await waitForSentStatusInInterviewDoc(interviewID);


   candidateInterviewDetailsSoapBody =
     getCandidateInterviewDetailsWorkDaySoapBody(candidateID, requisitionID);


   await waitForInterviewSessionReferenceIDsToLoadInWorkday(
     candidateInterviewDetailsSoapBody
   );

   candidateInterviewResponse = await getCandidateInterviewDetailsFromWorkDay(
     candidateInterviewDetailsSoapBody
   );

   expect(
     getCandidateLocationFromWorkDay(candidateInterviewResponse, 0)?.substring(
       2
     )
   ).toBe(expectedLocation);
   expect(
     getCandidateInterviewTypeFromWorkDay(candidateInterviewResponse, 0)
   ).toBe(expectedInterviewType);
   expect(
     getCandidateInterviewerDetailsFromWorkDay(candidateInterviewResponse, 0)
   ).toBe(expectedFirstInterviewerDetails);
   expect(
     getCandidateQuestionnaireFromWorkDay(candidateInterviewResponse, 0)
   ).toBe(expectedQuestionnaire);
   expect(
     getCandidateCompetenciesFromWorkDay(candidateInterviewResponse, 0)
   ).toBe(expectedCompetencies);
  });
 });
Helper Function References:
export async function scheduleOfficeInterview(request: any, data: any) {
 try {
   const response = await request.post(
     ${process.env.CLOUD_FUNCTIONS_BASE_URL }${BackendRoutes.MULTIDAY_SCHEDULE_INTERVIEWER_ROUTE },
     {
       data,
       headers: officeRestHeaders
      }
   );
   return response;
  } catch (error) {
   throw new ScheduleInterviewException(
     ManualInterviewExceptionMessages.SCHEDULE_INTERVIEW_EXCEPTION,
     error
   );
  }
 }
export async function cancelOfficeInterview(request: any, data: any) {
 try {
   const response = await request.post(
     ${process.env.CLOUD_FUNCTIONS_BASE_URL }${BackendRoutes.MULTIDAY_CANCEL_ROUTE },
     {
       data,
       headers: officeRestHeaders
      }
   );
   return response;
  } catch (error) {
   console.error(error);
   throw new ScheduleInterviewException(
     ManualInterviewExceptionMessages.SCHEDULE_INTERVIEW_EXCEPTION,
     error
   );
  }
 } """

template = """You are an expert in generating detailed TypeScript integration tests and helper functions. Based on the provided context, create:

1. Comprehensive integration test cases that:
   - Cover edge cases
   - Include clear comments explaining each step

2. Reusable helper functions that:
   - Support the test cases
   - Include comments explaining their purpose and usage

Context:
{CONTEXT}

Guidelines:
- Output executable TypeScript code only
- Do not include explanations outside of code comments
- Base your output on the provided context and instructions

Question: {question}
"""

#prompt = ChatPromptTemplate.from_template(template)
prompt = PromptTemplate(template = template, input_variables="CONTEXT")

model = OllamaLLM(model="llama3.1:70b", verbose=True)

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
