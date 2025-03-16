import streamlit as st
import requests
import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# Hugging Face API Key (replace with yours)
HF_API_KEY = "your_huggingface_api_key"

# Function to generate story using Hugging Face
def generate_story(title):
    API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-1.3B"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    prompt = f"Write a short story based on this title: {title}"
    payload = {"inputs": prompt, "parameters": {"max_length": 200}}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return "Error generating story."

# Function to convert text to voiceover
def text_to_speech(text):
    tts = gTTS(text, lang="en")
    tts.save("story.mp3")

# Function to add background music
def add_background_music():
    story_audio = AudioSegment.from_mp3("story.mp3")
    music = AudioSegment.from_mp3("background_music.mp3").set_frame_rate(44100)

    # Adjust volume levels
    music = music - 20  # Lower music volume
    combined = story_audio.overlay(music, loop=True)

    combined.export("final_story.mp3", format="mp3")

# Streamlit UI
st.title("Title to Story Generator with Voiceover & Music")
st.write("Enter a story title and get a generated story with voiceover and background music.")

title = st.text_input("Enter Story Title")

if st.button("Generate Story"):
    with st.spinner("Generating story..."):
        story = generate_story(title)
    
    st.subheader("Generated Story")
    st.write(story)
    
    # Convert story to speech
    text_to_speech(story)

    # Add background music
    add_background_music()

    # Play final audio
    st.audio("final_story.mp3", format="audio/mp3")
