import streamlit as st
import json
from difflib import SequenceMatcher

class SupportAgent:
    def __init__(self, qa_data):
        self.qa_data = qa_data
        
    def calculate_similarity(self, str1, str2):
        """Calculate string similarity ratio"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def find_best_match(self, user_question, threshold=0.6):
        """Find the most similar question and its answer"""
        best_match = None
        highest_similarity = 0
        
        for qa_pair in self.qa_data["questions"]:
            similarity = self.calculate_similarity(user_question, qa_pair["question"])
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = qa_pair
                
        if highest_similarity >= threshold:
            return best_match
        return None
    
    def get_response(self, user_question):
        """Get response for user question"""
        best_match = self.find_best_match(user_question)
        if best_match:
            return best_match["answer"]
        return "I apologize, but I don't have specific information about that. Is there something else I can help you with regarding Thoughtful AI's agents?"

# Load QA data
qa_data = {
    "questions": [
        {
            "question": "What does the eligibility verification agent (EVA) do?",
            "answer": "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
        },
        {
            "question": "What does the claims processing agent (CAM) do?",
            "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
        },
        {
            "question": "How does the payment posting agent (PHIL) work?",
            "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
        },
        {
            "question": "Tell me about Thoughtful AI's Agents.",
            "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
        },
        {
            "question": "What are the benefits of using Thoughtful AI's agents?",
            "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
        }
    ]
}

# Initialize agent
agent = SupportAgent(qa_data)

# Streamlit UI
st.title("Thoughtful AI Support Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about Thoughtful AI's agents"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    response = agent.get_response(prompt)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)