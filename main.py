#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
from dotenv import load_dotenv
load_dotenv()
#get_ipython().system('pip install openai')
from openai import OpenAI


# In[3]:


openai_api_key = os.getenv("OPENAI_API_KEY")


# In[4]:


client = OpenAI()


# In[5]:


def speech_to_text_conversion(file_path):
    """Converts audio format message to text using OpenAI's Whisper model."""
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model = "whisper-1",
        file = audio_file
    )
    return transcription.text


# In[6]:


def text_chat(text):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system", "content":"You are a helpful assistant"},
            {"role":"user", "content":"Who won the world series in 2020?"},
            {"role":"assistant", "content":"The LA Dodgers won the world series in 2020."},
            {"role":"user", "content": text}
        ]
    )
    return response.choice[0].messages


# In[8]:


import tempfile
import datetime
def text_to_speech_conversion(text):
    if text:
        speech_file_path = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_speech.webm"
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "fable",
            input = text
        )
        response.stream_to_file(speech_file_path)
        with open(speech_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        os.remove(speech_file_path)
        return audio_data


# In[14]:


import streamlit as st
#get_ipython().system('pip install audio_recorder_streamlit')
from audio_recorder_streamlit import audio_recorder
import tempfile
#import chatbot_function


# In[15]:


st.title("Voice Chatbot")

audio_bytes = audio_recorder(
    text = "Click to record",
    recording_color = "#e8b62c",
    neutral_color = "#6aa36f",
    icon_name = "microphone",
    icon_size = "3x",
)


# In[16]:


if audio_bytes:
    st.audio(audio_bytes, format = "audio/wav")
    with tempfile.NamedTemporaryFile(suffix = ".wav", delete = False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name
    if st.button('Get Response'):
        converted_text_openai = speech_to_text_conversion(temp_audio_path)
        st.write("Transcription:", converted_text_openai)
        textmodel_response = text_chat(converted_text_openai)
        audio_data = text_to_speech_conversion(textmodel_response)
        with tempfile.NamedTemporaryFile(delete = False, suffix = ".mp3") as tmpfile:
            tmpfile.write(audio_data)
            tmpfile_path = tmpfile.name
            st.write("Response:", textmodel_response)
            st.audio(tmpfile_path)


# In[26]:


# Save the current notebook as a .py file


# In[ ]:




