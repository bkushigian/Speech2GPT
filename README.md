# Speech-to-Text ChatGPT

This Python program allows you to interact with ChatGPT using your voice. It
records audio from your microphone, converts it to text using Google's Speech
Recognition API, and sends the transcribed text to ChatGPT. The program then
displays the transcribed text and ChatGPT's response in the terminal.

This program and README were written by ChatGPT.

## Prerequisites

* Python 3.6 or higher
* A working microphone
* An internet connection
* OpenAI API key (you can get one from https://beta.openai.com/signup/)

## Installation

1. Clone this repository or download the speech_to_chatgpt.py file.

2. Install the required packages:

    ```bash
    pip install ansi
    pip install gtts
    pip install openai
    pip install playsound
    pip install pyaudio
    pip install SpeechRecognition
    ```

3. Set up your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY='your-api-key'
    ```

    Replace `'your-api-key'` with your actual API key.

## Usage

1. Run the script from the terminal:

    ```bash
    python speech_to_chatgpt.py
    ```

2. When prompted, start speaking into your microphone. The program will
   automatically record your speech, convert it to text, and send it to ChatGPT.

6. The transcribed text and ChatGPT's response will be displayed in the
   terminal.

## Troubleshooting

If you encounter any issues with the microphone or speech recognition, ensure
that your microphone is properly connected and configured on your system.
Additionally, check your internet connection, as both Google's Speech
Recognition API and OpenAI API require an active connection.

## License

This project is provided under the MIT License. See the LICENSE file for more
information.