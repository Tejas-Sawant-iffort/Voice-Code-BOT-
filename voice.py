import os
import requests
import openai
import speech_recognition as sr
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, Voice, VoiceSettings, stream
from elevenlabs import play
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
import time

# Initialize Eleven Labs client with API key
client = ElevenLabs(
    api_key="key"
)

# Example text passage for generating speech
passage = """
 Welcome Everybody to IFFORT how may i help you ?
"""

# Generate the audio using Eleven Labs' TTS model
audio = client.generate(
    text=passage,
    model="eleven_multilingual_v2",
    voice=Voice(
        voice_id='3gsg3cxXyFLcGIfNbM6C',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.6)
    )
)

# Play the generated audio
play(audio)
# Load environment variables from .env file (API keys)
load_dotenv()

# Initialize ElevenLabs client
client = ElevenLabs(api_key="Key")

# Set OpenAI API key
openai.api_key = "Key"

# Define the system prompt (for OpenAI)
SYSTEM_PROMPT = """
You are Iffort, a helpful bot that provides information about Iffort and Fitze. Assist users with their queries in a friendly, professional, and conversational manner. Avoid repetitive introductions or unnecessary explanations about yourself. Respond naturally, providing helpful and concise answers.
"""


# Predefine ElevenLabs voice configuration (configure based on your preferred settings)
VOICE_ID = "3gsg3cxXyFLcGIfNbM6C"  # Replace with your desired voice ID from ElevenLabs
VOICE_SETTINGS = VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.6)


# Function to send text input to OpenAI and get a response
def openai_chat(message):
    try:
        start_time = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # GPT-4o mini model usage
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )
        elapsed_time = time.time() - start_time
        print(f"OpenAI execution time: {elapsed_time:.3f} seconds")
        return response.choices[0].message["content"]
    
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return None


# Function to convert text to speech and stream the audio (low-latency)
def text_to_speech_stream(openai_response):
    try:
    
        audio = client.generate(
        text=openai_response,
        model="eleven_multilingual_v2",
        voice=Voice(
            voice_id='3gsg3cxXyFLcGIfNbM6C',
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.6)
            )
        )
        
# Play the generated audio
        return audio
        

    except Exception as e:
        print(f"Error with ElevenLabs TTS: {e}")
        return None


# Function to recognize speech using your microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening...")

    with mic as source:
        print("mic on")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        start_time = time.time()
        print("Recognizing speech...")
        speech_text = recognizer.recognize_google(audio)
        print(f"You said: {speech_text}")
        elapsed_time = time.time() - start_time
        print(f"Speech Recognizing execution time: {elapsed_time:.3f} seconds")
        return speech_text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition; {e}")
        return None


# Main function to handle voice interaction
def voice_bot():
    start_time = time.time() 
    print("Voice bot is ready. Say something!")

    while True:
        # Step 1: Get user input through voice
        user_input = recognize_speech()

        if not user_input:
            print("I didn't catch that. Could you please repeat?")
            continue

        # Allow exit command
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        # Step 2: Send speech input to OpenAI for a response
        print("\nProcessing your request...")
        openai_response = openai_chat(user_input)
        if not openai_response:
            print("Error getting a response from OpenAI. Please try again.")
            continue

        # Print OpenAI response in text
        print(f"\nAI (text): {openai_response}")

        # Step 3: Convert the OpenAI response to speech and stream it
        print("\nAI (voice):")
        start_time = time.time()
        audio_stream = text_to_speech_stream(openai_response)
        elapsed_time = time.time() - start_time
        print(f"text to Speech execution time: {elapsed_time:.3f} seconds")
        if audio_stream:
            start = time.time()
            play(audio_stream)
            elapsed= time.time() - start
            print(f"Audio Speech execution time: {elapsed:.3f} seconds")
                
        else:
            print("Error generating speech. Please try again.")
        elapsed_time = time.time() - start_time
        print(f"Bot execution time: {elapsed_time:.3f} seconds")


if __name__ == "__main__":
    start_time = time.time()    
    voice_bot()
    elapsed_time = time.time() - start_time
    print(f"Bot execution time: {elapsed_time:.3f} seconds")

