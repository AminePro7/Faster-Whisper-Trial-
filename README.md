# 🎙️ Faster Whisper with Gemini AI and Edge TTS

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Faster Whisper](https://img.shields.io/badge/Faster%20Whisper-0.10.0-green.svg)](https://github.com/guillaumekln/faster-whisper)
[![Gemini AI](https://img.shields.io/badge/Gemini%20AI-2.0-purple.svg)](https://ai.google.dev/docs/gemini_api_overview)
[![Edge TTS](https://img.shields.io/badge/Edge%20TTS-6.1.9-orange.svg)](https://github.com/rany2/edge-tts)

## 📝 Description

This project combines the power of OpenAI's Whisper (via Faster Whisper) for speech recognition, Google's Gemini AI for natural language processing, and Microsoft's Edge TTS for speech synthesis. It creates an interactive voice assistant that can:

- 🎤 Record your voice input
- 📝 Transcribe speech to text using Faster Whisper
- 🤖 Process the text using Gemini AI
- 🔊 Respond using natural-sounding Edge TTS voices

## ✨ Features

- **Real-time Voice Recording**: Press and hold SPACE to record your voice
- **Multilingual Support**: Works with multiple languages including:
  - 🇺🇸 English
  - 🇫🇷 French
  - 🇪🇸 Spanish
  - 🇩🇪 German
  - 🇸🇦 Arabic
- **High-Quality Speech Recognition**: Uses Whisper large-v2 model
- **Natural Language Processing**: Powered by Gemini 2.0 Flash
- **Neural Text-to-Speech**: High-quality voices from Microsoft Edge TTS
- **Performance Metrics**: Shows processing times for each step

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AminePro7/Faster-Whisper-Trial-.git
   cd Faster-Whisper-Trial-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**
   - Create a `.env` file in the project root
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## 💻 Usage

1. **Start the program**
   ```bash
   python faster-whisper-large-v3-tts.py
   ```

2. **Using the program**
   - Press and hold SPACE to start recording
   - Speak your message
   - Release SPACE to stop recording
   - Wait for the response
   - Press 'q' to quit

## ⚙️ System Requirements

- Python 3.8 or higher
- FFmpeg installed on your system
- Microphone for voice input
- Speakers for audio output
- Sufficient RAM for Whisper model (recommended 8GB+)

## 🔧 Technical Details

### Components

- **Voice Recording**: PyAudio for audio capture
- **Speech Recognition**: Faster Whisper (large-v2 model)
- **AI Processing**: Gemini 2.0 Flash API
- **Text-to-Speech**: Microsoft Edge TTS
- **Audio Playback**: Pygame mixer

### Voice Models

| Language | TTS Voice |
|----------|-----------|
| English | en-US-ChristopherNeural |
| French | fr-FR-HenriNeural |
| Spanish | es-ES-AlvaroNeural |
| German | de-DE-ConradNeural |
| Arabic | ar-SA-HamedNeural |

## ⏱️ Performance

The system provides timing information for:
- Transcription time
- Response generation time
- Total processing time

## 🤝 Contributing

Feel free to:
- 🐛 Report bugs
- 💡 Suggest enhancements
- 🔧 Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for the Whisper model
- Google for Gemini AI
- Microsoft for Edge TTS
- The Faster Whisper team
- All other open-source contributors

## 📞 Contact

- GitHub: [@AminePro7](https://github.com/AminePro7)

## 🔍 Troubleshooting

### Common Issues

1. **Audio Recording Issues**
   - Ensure microphone permissions are granted
   - Check if PyAudio is properly installed
   - Verify microphone is set as default input device

2. **TTS Issues**
   - Check internet connection for Edge TTS
   - Ensure audio output device is working
   - Verify pygame mixer is initialized correctly

3. **API Issues**
   - Verify Gemini API key is correct
   - Check internet connection
   - Ensure API quota is not exceeded 