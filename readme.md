Voice Chatbot
Overview
This project implements a voice-activated chatbot using OpenAI's API. It leverages speech recognition to convert audio messages into text, processes the text using OpenAI's language models, and generates speech responses. The application is built using Streamlit for a user-friendly interface.

Features
Speech-to-Text Conversion: Converts recorded audio messages into text using OpenAI's Whisper model.
Text Processing: Engages with users through text using the GPT-3.5 model.
Text-to-Speech Conversion: Converts the chatbot's text responses back into audio using a TTS model.
Interactive User Interface: Streamlit provides an easy-to-use interface for recording and playing audio.
Requirements
Python 3.7+
Streamlit
OpenAI Python client
dotenv
audio_recorder_streamlit
Installation
Clone the repository:

bash
Copy code
git clone <repository_url>
cd <repository_directory>
Create a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables: Create a .env file in the root directory of the project and add your OpenAI API key:

makefile
Copy code
OPENAI_API_KEY=your_openai_api_key
Usage
Run the Streamlit application:

bash
Copy code
streamlit run main.py
Open your web browser and go to http://localhost:8501.

Click the record button to start recording your message.

Once you finish recording, the app will transcribe your audio, generate a response, and provide an audio playback of the response.

Code Structure
main.py: Main application file containing the Streamlit interface and functionality.
requirements.txt: List of required Python packages.
.env: Environment variables for sensitive information (like API keys).

Acknowledgements
OpenAI for providing the API.
Streamlit for the interactive web application framework.
Whisper model for speech recognition and TTS for text-to-speech capabilities.