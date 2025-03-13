import pyaudio
import wave
from datetime import datetime
import keyboard
from faster_whisper import WhisperModel
import requests
import time
import os
import asyncio
import edge_tts
import langdetect
from dotenv import load_dotenv
import pygame
from pygame import mixer

# Initialize pygame mixer
pygame.init()
mixer.init()

# Load environment variables
load_dotenv()

def record_audio(filename, duration=10):
    # Audio recording parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def clean_markdown(text):
    # Remove markdown symbols
    cleaned = text.replace('*', '')  # Remove asterisks
    cleaned = cleaned.replace('**', '')  # Remove bold markers
    cleaned = cleaned.replace('##', '')  # Remove heading markers
    cleaned = cleaned.replace('`', '')   # Remove code markers
    cleaned = cleaned.replace('_', '')   # Remove underscores
    cleaned = cleaned.replace('>', '')   # Remove blockquote markers
    # Remove bullet points with spaces after them
    cleaned = cleaned.replace('* ', '')
    cleaned = cleaned.replace('- ', '')
    return cleaned

def get_gemini_response(text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": text}]
        }]
    }
    
    # Get API key from environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"{url}?key={api_key}"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print("Generating response:", flush=True)
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if 'candidates' in response_data:
                    text_response = response_data['candidates'][0]['content']['parts'][0]['text']
                    # Clean markdown before printing and returning
                    cleaned_response = clean_markdown(text_response)
                    print(cleaned_response, end='', flush=True)
                    return cleaned_response
            
            if attempt < max_retries - 1:
                print(f"\nRetrying... (attempt {attempt + 2}/{max_retries})")
                time.sleep(2)
                    
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"\nRequest timed out. Retrying... (attempt {attempt + 2}/{max_retries})")
                time.sleep(2)
            continue
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"\nError: {str(e)}\nRetrying... (attempt {attempt + 2}/{max_retries})")
                time.sleep(2)
            continue
    
    return "I apologize, but I'm having trouble generating a response. Please try again."

async def speak_text(text):
    try:
        # Detect the language
        lang = detect_language(text)
        print(f"\nDetected language: {lang}")
        
        # Map language codes to Edge TTS voices
        voice_map = {
            'en': 'en-US-ChristopherNeural',
            'fr': 'fr-FR-HenriNeural',
            'es': 'es-ES-AlvaroNeural',
            'de': 'de-DE-ConradNeural',
            'ar': 'ar-SA-HamedNeural'
        }
        
        # Get voice for detected language, default to English
        voice = voice_map.get(lang, 'en-US-ChristopherNeural')
        
        # Create output filename
        output_file = "temp_speech.mp3"
        
        print("Generating speech...")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # Play the audio using pygame
        print("Speaking response...")
        mixer.music.load(output_file)
        mixer.music.play()
        
        # Wait for the audio to finish
        while mixer.music.get_busy():
            time.sleep(0.1)
            
        # Clean up
        mixer.music.unload()
        os.remove(output_file)
        print("Finished speaking")
        
    except Exception as e:
        print(f"TTS Error: {str(e)}")

def detect_language(text):
    try:
        # Detect language of the text
        lang = langdetect.detect(text)
        
        # Map detected language to supported codes
        lang_map = {
            'ar': 'ar',  # Arabic
            'en': 'en',  # English
            'fr': 'fr',  # French
            'es': 'es',  # Spanish
            'de': 'de',  # German
            # Add more languages as needed
        }
        return lang_map.get(lang, 'en')  # Default to English if language not in map
    except:
        return 'en'  # Default to English if detection fails

def main():
    # Load the Whisper model
    print("Loading Whisper large-v2 model...")
    model = WhisperModel("large-v2", device="cpu", compute_type="int8", cpu_threads=8)
    print("Model loaded!")

    while True:
        print("\nPress and hold SPACE to record (or 'q' to quit)...")
        keyboard.wait('space')
        
        if keyboard.is_pressed('q'):
            break

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"recording_{timestamp}.wav"

        record_audio(audio_file)

        # Measure transcription time
        print("Transcribing...")
        transcription_start = time.time()
        segments, info = model.transcribe(audio_file)
        transcription_time = time.time() - transcription_start
        
        full_text = " ".join([segment.text for segment in segments])
        print(f"\nTranscription ({transcription_time:.2f}s):", full_text)
        
        # Measure response generation time
        print("\nGemini:", end=' ', flush=True)
        response_start = time.time()
        gemini_response = get_gemini_response(full_text)
        response_time = time.time() - response_start
        
        # Speak the response using Edge TTS
        asyncio.run(speak_text(gemini_response))
        
        print(f"\n\nProcessing times:")
        print(f"- Transcription: {transcription_time:.2f} seconds")
        print(f"- Response generation: {response_time:.2f} seconds")
        print(f"- Total processing: {(transcription_time + response_time):.2f} seconds")

if __name__ == "__main__":
    main() 