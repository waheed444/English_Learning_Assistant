import os
import random
import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Ensure API key is available
if not GOOGLE_API_KEY:
    st.error("🚨 GOOGLE_API_KEY is missing! Please check your .env file.")
    st.stop()

# Initialize LLM model
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["text", "function"],
    template="""
You are an English language translation expert. Your goal is to provide accurate, context-sensitive Urdu translation of English words and sentences while helping learners understand and apply the content effectively. Follow these detailed steps for translation:

### 1. *Translation*:
   - Translate the following text into Urdu:
     "{text}"
   - Ensure the translation is:
     - *Accurate*: Retain the original meaning and context of the text.
     - *Culturally Appropriate*: Use expressions and terms that align with Urdu language norms and cultural sensibilities.
     - *Intention*: Adjust the tone to match the intent of the original text (e.g., conversational, formal, poetic, etc.).

### 2. *Pronunciation Guide*:
   - Provide pronunciation of the input word to help learners unfamiliar with English.

### 3. *Definition*:
   If the input is in the form of text, provide:
   - A clear and simple definition with *Urdu meanings*.
   - Two or Three relevant synonyms and antonyms of the words in English with *Urdu meanings*.
   - An example sentence to demonstrate proper usage in context.
   - Translation in Roman Urdu to help learners unfamiliar with the Urdu script.

### 4. *Vocabulary Analysis*:
   - Analyze the *input word* and provide:
     - Details on usage, formality, and difficulty level (beginner, intermediate, advanced).

### 5. *Grammar and Structure*:
   - Identify notable grammatical structures in the text (e.g., verb tenses, clauses, sentence types) and explain how they are represented in Urdu.

### 6. *Corrections*:
    - Check for any grammar, spelling, or sentence structure errors in the input and suggest improvements.

### Response Formatting:
   - Organize your response into clear sections with headings (e.g., Translation, Pronunciation, Vocabulary, etc.).
   - Use simple and concise language to ensure clarity.
   - Adopt an encouraging tone to motivate learners in their English language journey.

IMPORTANT: Only provide the response for the selected function: {function}. Do not include information for other functions.
"""
)

# Create LangChain
translation_chain = LLMChain(llm=llm, prompt=prompt_template)

def process_text_with_model(text, function):
    """Process input text and return AI-generated response for the specific function."""
    response = translation_chain.run(text=text, function=function)
    return response

def text_to_speech(text, speed="normal"):
    """Convert text to speech using gTTS and return the audio file path."""
    try:
        clean_text = " ".join(text.split())  # Remove extra spaces
        clean_text = clean_text.replace("*", "").replace("#", "")  # Remove markdown symbols
        
        slow = True if speed == "slow" else False
        tts = gTTS(text=clean_text, lang='en', slow=slow)
        audio_path = "pronunciation.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        st.error(f"Failed to generate audio: {e}")
        return None

# ─────────────────────────────
# 🎨 Streamlit UI Design
st.set_page_config(page_title="📚 AI English Learning Assistant", page_icon="📚", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        background-color: #f0f8ff;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #1e90ff;
    }
    .stButton > button {
        background-color: #1e90ff;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0066cc;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTextInput > div > div > input {
        background-color: white;
        color: #333;
        border: 1px solid #1e90ff;
        padding: 0.5rem;
        font-size: 1rem;
        border-radius: 5px;
    }
    .stRadio > div {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stTabs > div > div > div {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        padding: 1rem;
    }
    .stMarkdown a {
        color: #1e90ff;
        text-decoration: none;
    }
    .stMarkdown a:hover {
        text-decoration: underline;
    }
    .title-container {
        background-color: #1e90ff;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .title-container h1 {
        color: white;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title at the top
st.markdown('<div class="title-container"><h1>📚 AI English Learning Assistant</h1></div>', unsafe_allow_html=True)

# Description
st.markdown("""
Welcome to your personal AI-powered English Learning Assistant! This tool is designed to help you improve your English skills through interactive learning experiences. Whether you're looking for translations, pronunciation guides, or want to test your knowledge with quizzes, we've got you covered.

Let's embark on this exciting journey to enhance your English proficiency!
""")

# Tabs for Functions and Quizzes & Exercises
tab1, tab2 = st.tabs(["🔍 Learning Functions", "🏆 Practice Quiz"])

# ─────────────────────────────
# Learning Functions Tab
with tab1:
    st.header("🚀 Learning Functions")
    
    # Function selection
    st.sidebar.header("📊 Select a Function")
    options = ["Translation", "Pronunciation Guide", "Definition", "Grammar and Structure", "Vocabulary Analysis", "Corrections"]
    selected_option = st.sidebar.selectbox("Choose one:", options)

    # User input field
    user_input = st.text_area("✍️ Enter a word or sentence:", placeholder="Type here...", height=100)

    # Process button
    if st.button("🔮 Process", key="process_button"):
        if user_input:
            with st.spinner("🧠 AI is working its magic..."):
                result = process_text_with_model(user_input, selected_option)
            
            st.success("✨ Analysis complete! Here's what I found:")
            
            if selected_option == "Translation":
                st.markdown("### 🌐 Translation to Urdu:")
                st.info(result)
            elif selected_option == "Pronunciation Guide":
                st.markdown("### 🔊 Pronunciation Guide:")
                st.info(result)
                
                st.markdown("#### ⚙️ Pronunciation Speed")
                speed = st.radio("Select speed:", ["Normal", "Slow"], index=0)
                
                st.markdown("#### 🎤 Listen to the Pronunciation:")
                audio_file = text_to_speech(result, speed.lower())
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
            elif selected_option == "Definition":
                st.markdown("### 📚 Definition:")
                st.info(result)
            elif selected_option == "Vocabulary Analysis":
                st.markdown("### 🧠 Vocabulary and Phrase Analysis:")
                st.info(result)
            elif selected_option == "Grammar and Structure":
                st.markdown("### 📏 Grammar and Structure:")
                st.info(result)
            elif selected_option == "Corrections":
                st.markdown("### ✍️ Corrections:")
                st.info(result)
        else:
            st.warning("Please enter some text to analyze.")

# ─────────────────────────────
# Quizzes & Exercises Tab
with tab2:
    st.header("🏆 Practice Quiz")
    st.write("Test your knowledge with these randomly generated quizzes!")

    # Sample quizzes and exercises
    quizzes = [
        {
            "question": "Identify the verb tense in the sentence: 'She has been working all day.'",
            "answer": "Present Perfect Continuous"
        },
        {
            "question": "Choose the correct sentence: 'She don't like ice cream' or 'She doesn't like ice cream.'",
            "answer": "She doesn't like ice cream."
        },
        {
            "question": "What is the opposite of the word 'strong'?",
            "answer": "weak"
        },
        {
            "question": "Identify the subject in the sentence: 'The dog barked loudly.'",
            "answer": "The dog"
        },
        {
            "question": "Choose the correct form of the verb: 'He _____ to the store yesterday.' (go, goes, went)",
            "answer": "went"
        },
        {
            "question": "What is the correct plural form of 'mouse'?",
            "answer": "mice"
        }
    ]

    # Store the current question in session_state
    if 'selected_quiz' not in st.session_state:
        st.session_state.selected_quiz = random.choice(quizzes)

    # Display the question
    selected_quiz = st.session_state.selected_quiz
    st.markdown(f"### 🤔 {selected_quiz['question']}")

    # User input for answer
    user_answer = st.text_input("Your Answer:", placeholder="Type your answer here...")

    # Check answer button
    if st.button("📝 Check Answer", key="check_answer_button"):
        if user_answer:
            if user_answer.strip().lower() == selected_quiz["answer"].lower():
                st.success("✅ Correct! Well done! You're making great progress.")
                st.balloons()
                # After a correct answer, pick a new random question
                st.session_state.selected_quiz = random.choice(quizzes)
            else:
                st.error(f"❌ Not quite. The correct answer is: {selected_quiz['answer']}")
                st.markdown("Don't worry! Learning from mistakes is part of the process. Keep practicing!")
        else:
            st.warning("Please enter an answer before checking.")

    # Next question button
    if st.button("➡️ Next Question", key="next_question_button"):
        st.session_state.selected_quiz = random.choice(quizzes)
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h4>📚 Keep Learning, Keep Growing! 🌱</h4>
    <p>Built with ❤️ using LangChain, Google's Gemini API, and Streamlit</p>
    <p><a href="https://github.com/yourusername/english-learning-assistant" target="_blank">View on GitHub</a> | <a href="mailto:your.email@example.com">Contact Us</a></p>
</div>
""", unsafe_allow_html=True)