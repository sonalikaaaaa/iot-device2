import os
import openai
import tempfile
import streamlit as st
from gtts import gTTS  # Free Google TTS
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder

# Load OpenAI API Key (if still needed)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Optional if using alternatives

# Function for speech-to-text (using OpenAI Whisper, but can replace with Vosk)
def speech_to_text_conversion(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcription = openai.Audio.transcribe(model="whisper-1", file=audio_file)
        return transcription['text']
    except Exception as e:
        st.error(f"OpenAI Error: {e}. Check billing or use an alternative STT.")
        return None

# Function for text-to-speech (using gTTS instead of Google Cloud)
def text_to_speech_conversion(text):
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            return tmpfile.name
    except Exception as e:
        st.error(f"TTS Error: {e}")
        return None

# Streamlit UI
st.title("Voice Chatbot")
audio_bytes = audio_recorder(text="Click to record", pause_threshold=3.0)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name
    
    if st.button('Get Response'):
        user_text = speech_to_text_conversion(temp_audio_path)
        if user_text:
            st.write("You said:", user_text)
            
            # Get GPT response (if OpenAI is working)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_text}]
                )
                bot_text = response.choices[0].message.content
            except Exception as e:
                bot_text = "Sorry, I can't process this right now (OpenAI error)."
                st.error(f"GPT Error: {e}")
            
            st.write("Bot:", bot_text)
            
            # Convert to speech
            audio_file = text_to_speech_conversion(bot_text)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")