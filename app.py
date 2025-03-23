import os
import streamlit as st

# MUST call set_page_config as the very first Streamlit command!
st.set_page_config(
    page_title="Portfolio Chat & Navigation",
    page_icon="💬",
    layout="centered",
)

import logging
import openai  # This code is written for openai==0.28.0
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from the .env file for local development.
load_dotenv()

# Attempt to load the OpenAI API key from three sources:
# 1. Environment variable
# 2. Top-level of st.secrets
# 3. Nested under a [general] table in st.secrets
if "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.environ["OPENAI_API_KEY"]
elif "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
elif "general" in st.secrets and "OPENAI_API_KEY" in st.secrets["general"]:
    openai.api_key = st.secrets["general"]["OPENAI_API_KEY"]
else:
    st.error("No OpenAI API key provided. Please set it in your .env file or in your Streamlit Cloud secrets.")

# Set up logging to help debug issues.
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Adding custom CSS for a nicer look of chat messages and inputs.
st.markdown("""
<style>
.user-message {
    background-color: #e6f7ff;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.assistant-message {
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------- Helper Functions -----------------------

# Function to generate a response using the OpenAI Chat API while preserving conversation history.
def generate_response(prompt, conversation_history):
    # Always include a system message to set the context for my assistant.
    messages = [
        {"role": "system", "content": "You are a friendly portfolio assistant who answers questions about my work, experience, and projects."}
    ]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})
    
    try:
        # Using the old API interface from openai==0.28.0.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"Error: {e}"

# Function to display chat messages with custom CSS styling.
def display_chat_messages(messages):
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='assistant-message'><b>Assistant:</b> {msg['content']}</div>", unsafe_allow_html=True)

# ----------------------- Sidebar Navigation -----------------------

with st.sidebar:
    st.title("Navigation")
    app_mode = st.radio("Select Section:", [
        "Chatbot", "Portfolio Navigation", "FAQ & Experience", "Visuals & Multimedia"
    ])

# ----------------------- App Sections -----------------------

# Chatbot Section: Context-Aware Chat
if app_mode == "Chatbot":
    st.title("Interactive Portfolio Chatbot")
    st.write("Ask me anything about my projects, background, or data science in general!")
    
    # Initialize conversation history in session_state if not already present.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I'm your portfolio assistant! How can I help you today?"}
        ]
    
    # Display the conversation so far.
    display_chat_messages(st.session_state.messages)
    
    # Use st.chat_input for a modern chat-style input widget.
    user_input = st.chat_input("Type your message here:")
    if user_input:
        # Save the user's message and generate a response.
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = generate_response(user_input, st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Portfolio Navigation Section
elif app_mode == "Portfolio Navigation":
    st.title("My Portfolio Projects")
    st.write("Explore some of the projects I've worked on:")
    
    # Dictionary of portfolio projects; update with your own details.
    projects = {
        "Project Alpha": {
            "description": "A machine learning project using neural networks to predict stock prices.",
            "link": "https://github.com/yourusername/project-alpha"
        },
        "Project Beta": {
            "description": "A data visualization dashboard analyzing social media trends.",
            "link": "https://github.com/yourusername/project-beta"
        },
        "Project Gamma": {
            "description": "An NLP project for sentiment analysis on customer feedback.",
            "link": "https://github.com/yourusername/project-gamma"
        }
    }
    
    # Loop over each project and display its details.
    for project, details in projects.items():
        st.subheader(project)
        st.write(details["description"])
        st.markdown(f"[View Project]({details['link']})")
        st.markdown("---")

# FAQ & Experience Highlights Section
elif app_mode == "FAQ & Experience":
    st.title("FAQ & My Experience")
    st.write("Below are some frequently asked questions and highlights from my experience.")
    
    # FAQ content; update these as necessary.
    faq = {
        "What is your background in data science?": "I hold a Master's in Data Science and have over 5 years of experience in the field.",
        "Which programming languages do you use?": "I'm proficient in Python, R, SQL, and JavaScript.",
        "How do you approach solving data problems?": "I follow a systematic process: problem understanding, data collection/cleaning, exploratory data analysis, modeling, and insight communication."
    }
    
    for question, answer in faq.items():
        st.markdown(f"**Q: {question}**")
        st.markdown(f"A: {answer}")
        st.markdown("---")
    
    # Experience Timeline visualization.
    st.subheader("Experience Timeline")
    st.write("A quick look at my project milestones over the years.")
    timeline_data = pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022],
        "Projects Completed": [2, 3, 5, 4, 6]
    })
    fig, ax = plt.subplots()
    ax.plot(timeline_data["Year"], timeline_data["Projects Completed"], marker='o')
    ax.set_xlabel("Year")
    ax.set_ylabel("Projects Completed")
    ax.set_title("Experience Timeline")
    st.pyplot(fig)

# Visuals & Multimedia Section
elif app_mode == "Visuals & Multimedia":
    st.title("Interactive Visuals & Multimedia")
    st.write("Enjoy some interactive charts, images, and videos!")
    
    # Bar chart example showing project categories.
    st.subheader("Project Categories")
    df_bar = pd.DataFrame({
        "Category": ["ML", "Visualization", "NLP", "Data Engineering"],
        "Projects": [4, 3, 5, 2]
    })
    st.bar_chart(df_bar.set_index("Category"))
    
    # Display an image representing my journey.
    st.subheader("My Data Science Journey")
    st.image("https://via.placeholder.com/600x300.png?text=Data+Science+Journey", caption="Visualizing my path in data science")
    
    # Embed a video (update the URL to your relevant video).
    st.subheader("Introduction Video")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")