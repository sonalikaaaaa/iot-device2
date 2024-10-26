import streamlit as st
!pip install audio_recorder_streamlit
from audio_recorder_streamlit import audio_recorder
import tempfile
import chatbot_function

st.title("Voice Chatbot")

audio_bytes = audio_recorder(
    text = "Click to record",
    recording_color = "#e8b62c",
    neutral_color = "#6aa36f",
    icon_name = "microphone",
    icon_size = "3x",
)

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