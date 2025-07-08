import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import base64
import pdfkit
import time
from datetime import datetime
from ocr import extract_text_from_image
from ai import generate_response, detect_subject
from mpesa import process_payment, check_subscription_status

# Load environment variables
load_dotenv()

# App configuration
st.set_page_config(
    page_title="Homework Helper for Busy Parents",
    page_icon=":book:",
    layout="wide"
)

# CSS and JS injection
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def local_js(file_name):
    with open(file_name) as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'free_questions_used' not in st.session_state:
    st.session_state.free_questions_used = 0
if 'free_questions_limit' not in st.session_state:
    st.session_state.free_questions_limit = 3
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False

# Sidebar
def sidebar():
    with st.sidebar:
        st.image("static/images/logo.jpg", width=150)
        st.title("Homework Helper")
        st.subheader("Navigation")
        
        menu = st.radio("", ["Home", "History", "Plans", "Help", "Feedback"])
        
        st.markdown("---")
        st.subheader("Daily CBC Tip")
        tips = [
            "Encourage your child to explain concepts back to you in their own words.",
            "Connect homework topics to real-life situations in Kenya.",
            "Break study sessions into 20-minute chunks with short breaks.",
            "Use household items to demonstrate math and science concepts."
        ]
        st.info(tips[datetime.now().day % len(tips)])
        
        st.markdown("---")
        st.subheader("Settings")
        dark_mode = st.checkbox("Dark Mode", False)
        
        return menu

# Main chat interface
def chat_interface():
    st.title("Homework Helper for Busy Parents")
    st.subheader("Get child-friendly explanations for CBC homework questions")
    
    # Display free question counter
    if not st.session_state.is_subscribed:
        remaining = max(0, st.session_state.free_questions_limit - st.session_state.free_questions_used)
        st.warning(f"You've used {st.session_state.free_questions_used}/{st.session_state.free_questions_limit} free questions today.")
    
    # Input options
    input_option = st.radio("How would you like to ask your question?", 
                          ["Type your question", "Upload homework photo", "Voice input"])
    
    user_input = ""
    
    if input_option == "Type your question":
        user_input = st.text_area("Enter the homework question:", height=150)
    elif input_option == "Upload homework photo":
        uploaded_file = st.file_uploader("Upload homework image (JPEG, PNG)", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Homework', use_column_width=True)
            user_input = extract_text_from_image(image)
            st.text_area("Extracted text (you can edit):", value=user_input, height=150)
    else:  # Voice input
        st.warning("Voice input requires browser microphone access.")
        local_js("static/scripts.js")
        user_input = st.text_input("Voice input will appear here:", key="voice_input")
    
    # Additional options
    col1, col2 = st.columns(2)
    with col1:
        step_by_step = st.checkbox("Break it down step-by-step")
    with col2:
        simple_explanation = st.checkbox("Explain to a 10-year-old")
    
    if st.button("Get Explanation"):
        if user_input.strip():
            process_question(user_input, step_by_step, simple_explanation)
        else:
            st.error("Please enter or upload a homework question.")

# Process user question
def process_question(question, step_by_step, simple_explanation):
    # Check question limit
    if not st.session_state.is_subscribed and st.session_state.free_questions_used >= st.session_state.free_questions_limit:
        st.warning("You've used all your free questions for today.")
        show_payment_options()
        return
    
    with st.spinner("Analyzing your question..."):
        # Detect subject
        subject = detect_subject(question)
        st.session_state.conversation.append({"role": "user", "content": question})
        
        # Generate response
        response = generate_response(question, subject, step_by_step, simple_explanation)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        
        # Update question count
        if not st.session_state.is_subscribed:
            st.session_state.free_questions_used += 1
        
        # Display conversation
        display_conversation()

# Display conversation history
def display_conversation():
    for i, message in enumerate(st.session_state.conversation):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>Homework Helper:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback buttons
            col1, col2, col3 = st.columns([1, 1, 8])
            with col1:
                if st.button("👍", key=f"like_{i}"):
                    st.success("Thanks for your feedback!")
            with col2:
                if st.button("👎", key=f"dislike_{i}"):
                    st.error("We'll try to improve. Please tell us what was wrong.")
            
            st.markdown("---")

# Payment options
def show_payment_options():
    st.subheader("Unlock More Questions")
    plan = st.radio("Choose a plan:", 
                    ["Pay KES 10 for one more question", 
                     "Subscribe for KES 200/month (unlimited questions)"])
    
    if st.button("Continue with M-Pesa"):
        phone_number = st.text_input("Enter your M-Pesa phone number (e.g., 254712345678):")
        if phone_number and len(phone_number) == 12 and phone_number.startswith("254"):
            with st.spinner("Processing payment..."):
                success = process_payment(phone_number, plan)
                if success:
                    st.session_state.is_subscribed = True if "month" in plan else False
                    if "month" in plan:
                        st.session_state.free_questions_limit = float('inf')
                    else:
                        st.session_state.free_questions_limit += 1
                    st.success("Payment successful! You can now ask more questions.")
                else:
                    st.error("Payment failed. Please try again.")
        else:
            st.error("Please enter a valid Kenyan phone number starting with 254.")

# History page
def history_page():
    st.title("Your Question History")
    if st.session_state.conversation:
        display_conversation()
        
        # Export options
        if st.button("Download as PDF"):
            html_content = """
            <html>
                <head>
                    <title>Homework Helper Conversation</title>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        .user-message { margin-bottom: 15px; padding: 10px; background-color: #f0f0f0; border-radius: 5px; }
                        .assistant-message { margin-bottom: 15px; padding: 10px; background-color: #e6f7ff; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <h1>Homework Helper Conversation</h1>
            """
            
            for message in st.session_state.conversation:
                role = "You" if message["role"] == "user" else "Homework Helper"
                html_content += f"""
                <div class="{message['role']}-message">
                    <strong>{role}:</strong> {message["content"]}
                </div>
                """
            
            html_content += "</body></html>"
            
            pdf = pdfkit.from_string(html_content, False)
            st.download_button(
                label="Download PDF",
                data=pdf,
                file_name="homework_helper_conversation.pdf",
                mime="application/octet-stream"
            )
    else:
        st.info("No conversation history yet.")

# Main app flow
def main():
    local_css("static/style.css")
    
    menu = sidebar()
    
    if menu == "Home":
        chat_interface()
    elif menu == "History":
        history_page()
    elif menu == "Plans":
        show_payment_options()
    elif menu == "Help":
        st.title("Help & Support")
        st.markdown("""
        ### How to use Homework Helper
        1. **Type your question** in the text box
        2. **Upload a photo** of handwritten or printed homework
        3. Use **voice input** (requires microphone access)
        
        ### Tips for best results
        - Be as specific as possible with your questions
        - For math problems, include all given numbers and what's being asked
        - For essay questions, include the topic and any requirements
        
        ### Contact Support
        Email: support@homeworkhelper.co.ke
        Phone: +254 700 123 456
        """)
    elif menu == "Feedback":
        st.title("Feedback")
        feedback = st.text_area("Tell us how we can improve:")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")

    # Footer with disclaimers
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Disclaimer:</strong> This AI tool does not store homework content or personal data. Always review AI responses before sharing with your child.</p>
        <p>AI responses may not always be 100% accurate. Double-check when in doubt.</p>
        <p>Aligned with Kenyan CBC curriculum for Grades 4-9.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()