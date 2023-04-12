import os
import openai
import speech_recognition as sr

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")


def send_to_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


def main():
    with sr.Microphone() as source:
        print("Listening for speech...")

        # Record audio from the microphone
        audio = recognizer.listen(source)

        try:
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"Transcribed text: {text}")

            # Send the text to ChatGPT and get a response
            chatgpt_response = send_to_chatgpt(text)
            print(f"ChatGPT Response: {chatgpt_response}")

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
