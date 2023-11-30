#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import io
import streamlit as st
from st_audiorec import st_audiorec
import datetime
import tempfile


def main():
    
    load_dotenv('audio_test.env')  # This loads the variables from .env

    # Now you can use the environment variable
    speech_key = os.getenv("SUBSCRIPTION_KEY")
    service_region = os.getenv("SERVICE_REGION")
    
    st.title('streamlit audio recorder')

    # TUTORIAL: How to use STREAMLIT AUDIO RECORDER?
    # by calling this function an instance of the audio recorder is created
    # once a recording is completed, audio data will be saved to wav_audio_data

    wav_audio_data = st_audiorec() # tadaaaa! yes, that's it! :D

    # add some spacing and informative messages
    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer
        st.write('The .wav audio data, as received in the backend Python code,'
                 ' will be displayed below this message as soon as it has'
                 ' been processed. [This informative message is not part of'
                 ' the audio recorder and can be removed easily] 🎈')

    if wav_audio_data is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_file:
            audio_file.write(wav_audio_data)
            temp_file_name = audio_file.name
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            audio_stream = io.BytesIO(wav_audio_data)
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region) 
            audio_config = speechsdk.audio.AudioConfig(filename=temp_file_name)
            lang, text = speech_to_text(speech_config, audio_config)
            audio_output = text_to_speech(lang, text, speech_config, audio_config)
            st.audio(audio_output)
            



def speech_to_text(speech_config, audio_config):
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "zh-CN", "fr-FR", "es-ES"])
    speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            auto_detect_source_language_config=auto_detect_source_language_config, 
            audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(result)
    detected_language = auto_detect_source_language_result.language
    
    return detected_language, result.text


def text_to_speech(detected_language, text, speech_config, audio_config):
    if detected_language == 'fr-FR':
        speech_config.speech_synthesis_voice_name="fr-FR-DeniseNeural"
    elif detected_language == 'es-ES':
        speech_config.speech_synthesis_voice_name="es-ES-ElviraNeural"
    elif detected_language == 'zh-CN':
        speech_config.speech_synthesis_voice_name="zh-CN-XiaoxiaoNeural"
    else:
        speech_config.speech_synthesis_voice_name="en-US-JennyMultilingualV2Neural"
    
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text).get()
    return result.audio_data
    
if __name__=='__main__':
    main()


# In[3]:


# pip install azure-cognitiveservices-speech


# In[10]:


# pip install streamlit-audiorec

