# 📚 AI English Learning Assistant

This project is an **AI-powered English Learning Assistant** built using **Streamlit**, **LangChain**, **Google Gemini API**, and **gTTS** (Google Text-to-Speech). It helps users improve their English language skills by providing **translations**, **pronunciation guides**, **definitions**, **vocabulary analysis**, **grammar structures**, and **error corrections**.

---

## 🚀 Features

- **English-to-Urdu Translation**: Translate English words or sentences to Urdu with context-sensitive translations.
- **Pronunciation Guide**: Listen to the correct pronunciation of words.
- **Definitions**: Clear definitions with synonyms, antonyms, and example sentences.
- **Grammar and Structure Analysis**: Identify and explain grammatical structures in sentences.
- **Vocabulary Analysis**: In-depth analysis of words, including formality and difficulty levels.
- **Corrections**: Grammar and spelling corrections with suggested improvements.
- **Practice Quizzes**: Interactive quizzes to test English knowledge.

---

## ⚡️ Tech Stack

- **Streamlit**: Web framework to build interactive applications.
- **LangChain**: Framework to use large language models for tasks like text generation and processing.
- **Google Gemini API**: AI model for natural language processing and understanding.
- **gTTS**: Text-to-speech conversion for pronunciation guides.
- **python-dotenv**: Manage environment variables.

---

## 🛠️ Installation

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/waheed444/English_Learning_Assistant.git
cd AI-English-Learning-Assistant
```

## 2. Set Up Virtual Environment
### Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```
## 3. Install Dependencies
### Install all the required Python packages using pip:

```bash
 pip install -r requirements.txt
```
- If requirements.txt is not present, manually install the dependencies:

```bash
pip install streamlit python-dotenv gtts langchain langchain-google-genai pydantic requests
```

##  Set Up Google API Key
-  Create a .env file in the root of your project directory.
- Add the following line to the .env file:
```bash
GOOGLE_API_KEY=your-google-api-key
```
- Make sure to replace your-google-api-key with the actual API key you obtained from Google's API services.

## 🖥️ Running the Application
- After setting up the virtual environment and installing dependencies, run the app using Streamlit:
```bash
streamlit run app.py
```
- This will launch the application in your browser.

## 🎨 Project Structure

```bash
AI-English-Learning-Assistant/
│
├── app.py                 # Main Streamlit application file
├── .env                   # Environment variables file (API keys, etc.)
├── requirements.txt       # Python dependencies file
├── README.md              # Project overview and instructions
└── assets/                # Any additional assets like images, audio files 
```

# Language Learning Assistant

This is a language learning assistant application designed to help users enhance their English skills. It offers various functions, including translation, pronunciation guide, vocabulary analysis, and more. Follow the instructions below to get started.

## How to Use

1. **Open the Application**  
   Open the application in your browser (typically, Streamlit runs on [http://localhost:8501](http://localhost:8501)).

2. **Input the Text**  
   Enter a word or sentence into the text input box.

3. **Select the Function You Want to Use:**
   - **Translation:** Translate the text to Urdu.
   - **Pronunciation Guide:** Hear the pronunciation of the word or sentence.
   - **Definition:** Get the definition, synonyms, antonyms, and example sentences.
   - **Grammar and Structure:** Understand the grammatical structure of the input.
   - **Vocabulary Analysis:** Analyze the vocabulary.
   - **Corrections:** Get suggestions for grammatical corrections.

4. **Practice Quiz**  
   Use the **Practice Quiz** tab to test your English knowledge with randomly generated questions.

## Explore and Interact

Interact with the app and explore various functions to enhance your language learning experience.

# 🧑‍💻 Contributors

### Developer and Creator of this AI English Learning Assistant.

**[Waheed Ahmad](https://github.com/waheed444)** **|** **[Farhat Sattar](https://github.com/farhatsattar)** **|** **[Mudassar Hassan](https://github.com/MudassarHassan013)** **|** 
