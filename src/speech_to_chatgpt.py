from ansi.color import fg, bg
import os
import sys
import openai
import speech_recognition as sr
from argparse import ArgumentParser

def speak_response(response):
    import pyttsx3

    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

def send_to_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text

def main():
    parser = ArgumentParser()
    parser.add_argument("--speak", action='store_true')
    parser.add_argument("--format", action='store_true')

    args = parser.parse_args()

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    # Set up OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORGANIZATION_ID")

    if openai.organization is None:
        print(fg.red("Error: Couldn't find an OPENAI_ORGANIZATION_ID environtment variable"))
        sys.exit(1)

    if openai.api_key is None:
        print(fg.red("Error: Couldn't find an OPENAI_API_KEY environtment variable"))
        sys.exit(1)

    with sr.Microphone() as source:
        print("Listening for speech...\n")

        # Record audio from the microphone
        audio = recognizer.listen(source)

        try:
            # Convert speech to text
            prompt = recognizer.recognize_google(audio)
            print(fg.green("Prompt:"))
            print(prompt)

            if args.format:
                prompt = f"Please punctuate and format the following text:\n\n{prompt}"

            # Send the text to ChatGPT and get a response
            chatgpt_response = send_to_chatgpt(prompt)

            print()
            print(fg.green("ChatGPT Response:"))
            print(chatgpt_response)

            if args.speak:
                speak_response(chatgpt_response)

        except sr.UnknownValueError:
            print("Could not understand the speech. Please try again.")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
