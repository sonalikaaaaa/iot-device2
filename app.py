#!/usr/bin/env python
# coding: utf-8

import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import datetime
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import tempfile

# Loading the API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Maintain call history as a list
call_history = []

# Speech-to-text conversion with support for Hindi and English
def speech_to_text_conversion(file_path, language="en"):
    """Converts audio format message to text using OpenAI's Whisper model for multiple languages."""
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language=language  # Set the language to either 'en' (English) or 'hi' (Hindi)
    )
    return transcription.text

# Text-to-speech conversion with support for Hindi and English
def text_to_speech_conversion(text, language="en"):
    """Converts text to speech using OpenAI's TTS model, supporting Hindi and English."""
    if text:
        # You can choose a voice suitable for the language (e.g., 'fable' for general voices)
        speech_file_path = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_speech.webm"
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",  # Choose a voice suitable for the language
            input=text,
            language=language  # Set the language to either 'en' (English) or 'hi' (Hindi)
        )
        response.stream_to_file(speech_file_path)
        with open(speech_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        os.remove(speech_file_path)
        return audio_data

# Chat with GPT using text in either Hindi or English
def text_chat(text, language="en"):
    """Generates a response from GPT-3.5 in the specified language."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The LA Dodgers won the world series in 2020."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message['content']

# Function to make calls from voice input and save call history
def make_call(phone_number, call_duration):
    """Simulate making a call from voice input and save the call details in call history."""
    call_details = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phone_number": phone_number,
        "call_duration": call_duration
    }
    call_history.append(call_details)

# Streamlit interface for voice chatbot
st.title("Voice Chatbot")

# Add a dropdown to select the language (English or Hindi)
language_option = st.selectbox("Select Language", ["English", "Hindi"])

# Add a text input to accept phone number for making calls
phone_number = st.text_input("Enter Phone Number to Call")

# Record audio
audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="3x",
)

# Set the language based on user selection
language_code = "en" if language_option == "English" else "hi"

# If audio is recorded, process the input and provide a response
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name
    
    if st.button('Get Response'):
        # Convert speech to text (supports Hindi or English)
        converted_text_openai = speech_to_text_conversion(temp_audio_path, language=language_code)
        st.write("Transcription:", converted_text_openai)
        
        # Get response from GPT model (supports Hindi or English)
        textmodel_response = text_chat(converted_text_openai, language=language_code)
        
        # Convert the response to speech (supports Hindi or English)
        audio_data = text_to_speech_conversion(textmodel_response, language=language_code)
        
        # Play the response audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile.write(audio_data)
            tmpfile_path = tmpfile.name
            st.write("Response:", textmodel_response)
            st.audio(tmpfile_path)
        
        # If the user provided a phone number, simulate the call and save history
        if phone_number:
            # Simulate a call duration (in seconds)
            call_duration = 120  # For example, the call lasts for 2 minutes
            make_call(phone_number, call_duration)
            st.write(f"Call made to {phone_number}. Duration: {call_duration} seconds.")
    
# Display call history
if call_history:
    st.subheader("Call History")
    for call in call_history:
        st.write(f"Phone Number: {call['phone_number']}, Call Duration: {call['call_duration']} seconds, Time: {call['timestamp']}")
