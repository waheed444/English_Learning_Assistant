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

# Initialize LLM model (ensure model name is valid)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["text"],
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
"""
)

# Create LangChain
translation_chain = LLMChain(llm=llm, prompt=prompt_template)

def process_text_with_model(text):
    """Process input text and return AI-generated response."""
    response = translation_chain.run(text=text)
    return response  # Returning plain text instead of JSON

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

def extract_section(response, section_title):
    """Extract a specific section from the response based on the section title."""
    sections = response.split("###")
    for section in sections:
        if section_title in section:
            return section.strip()
    return "Section not found."

# ─────────────────────────────
# 🎨 Streamlit UI Design
st.set_page_config(page_title="📚 AI English Learning Assistant", page_icon="📚", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput input {
        padding: 10px;
        font-size: 16px;
    }
    .stRadio div {
        flex-direction: row;
        gap: 10px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
    }
    .stSpinner div {
        color: #4CAF50;
    }
    .stSuccess {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    .stInfo {
        background-color: #2196F3;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    .stError {
        background-color: #f44336;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Main title and description
st.title("📚 AI English Learning Assistant")

st.markdown("""
Welcome to the AI-powered English Learning Assistant! This tool helps you learn English by providing translations, pronunciation guides, definitions, grammar analysis, and more. Enter a word or sentence below to get started.
""")

# Tabs for Functions and Quizzes & Exercises
tab1, tab2 = st.tabs(["Functions", "Practice Quiz"])

# ─────────────────────────────
# Functions Tab
with tab1:
    st.header("Functions")
    # Sidebar for function selection
    st.sidebar.header("Select any Function")
    options = ["Translation", "Pronunciation Guide", "Definition", "Grammar and Structure", "Vocabulary Analysis", "Corrections"]
    selected_option = st.sidebar.radio("Choose one:", options)

    # User input field
    user_input = st.text_input("✍️ Enter a word or sentence:", placeholder="Type here...")

    # Process input and display results
    if user_input:
        if user_input.lower() == "end":
            st.success("✅ Session Ended! Goodbye! 👋")
        else:
            with st.spinner("Processing your request..."):  # Add a loading spinner
                result = process_text_with_model(user_input)
            
            if selected_option == "Translation":
                st.markdown("### 🔍 Translation to Urdu:")
                translation_section = extract_section(result, "Translation")
                st.info(translation_section)
            elif selected_option == "Pronunciation Guide":
                st.markdown("### 🔊 Pronunciation Guide:")
                pronunciation_section = extract_section(result, "Pronunciation Guide")
                st.info(pronunciation_section)
                
                # Add speed control for pronunciation
                st.markdown("#### ⚙️ Pronunciation Speed")
                speed = st.radio("Select speed:", ["Normal", "Slow"], index=0)
                
                # Add voice functionality
                st.markdown("#### 🎤 Listen to the Pronunciation:")
                audio_file = text_to_speech(pronunciation_section, speed.lower())
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
            elif selected_option == "Definition":
                st.markdown("### 📚 Definition:")
                definition_section = extract_section(result, "Definition")
                st.info(definition_section)
            elif selected_option == "Vocabulary Analysis":
                st.markdown("### 🧠 Vocabulary and Phrase Analysis:")
                vocabulary_section = extract_section(result, "Vocabulary Analysis")
                st.info(vocabulary_section)
            elif selected_option == "Grammar and Structure":
                st.markdown("### 📏 Grammar and Structure:")
                grammar_section = extract_section(result, "Grammar and Structure")
                st.info(grammar_section)
            elif selected_option == "Corrections":
                st.markdown("### ✍️ Corrections:")
                corrections_section = extract_section(result, "Corrections")
                st.info(corrections_section)

# ─────────────────────────────
# Quizzes & Exercises Tab
with tab2:
    st.header("Practice Quiz")
    st.write("Test your knowledge with these randomly generated quizzes and exercises for your practice!")

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
        },
        {
            "question": "Identify the error in the sentence: 'She can sings very well.'",
            "answer": "Error: 'sings' should be 'sing'. Correct sentence: 'She can sing very well.'"
        },
        {
            "question": "Choose the correct preposition: 'She is good _____ playing chess.' (at, in, on)",
            "answer": "at"
        },
        {
            "question": "Fill in the blank with the correct article: '_____ apple a day keeps the doctor away.'",
            "answer": "An"
        },
        {
            "question": "What type of sentence is this: 'Do you want tea or coffee?'",
            "answer": "Interrogative sentence"
        },
        {
            "question": "Choose the correct sentence: 'He were going to the park' or 'He was going to the park.'",
            "answer": "He was going to the park."
        },
        {
            "question": "Which of the following is a compound sentence? 'I like pizza, and I like burgers.' or 'I like pizza.'",
            "answer": "I like pizza, and I like burgers."
        }
    ]

    # Store the current question in session_state
    if 'selected_quiz' not in st.session_state:
        st.session_state.selected_quiz = random.choice(quizzes)

    # Display the question
    selected_quiz = st.session_state.selected_quiz
    st.markdown(f"### {selected_quiz['question']}")

    # User input for answer
    user_answer = st.text_input("Your Answer:", placeholder="Type your answer here...")

    # Check the answer when the user submits it
    if user_answer:
        if user_answer.strip().lower() == selected_quiz["answer"].lower():
            st.success("✅ Correct! Well done!")
            # After a correct answer, pick a new random question
            st.session_state.selected_quiz = random.choice(quizzes)  # Change to a new quiz question
        else:
            st.error(f"❌ Incorrect. The correct answer is: {selected_quiz['answer']}")


# Footer
st.markdown("---")
st.markdown("**Built with LangChain,Google's Gemini API and Streamlit**")


# pip install -U streamlit python-dotenv gtts langchain langchain-google-genai pydantic requests