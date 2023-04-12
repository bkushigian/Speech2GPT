from ansi.color import fg, bg
import os
import sys
import openai
import speech_recognition as sr
from argparse import ArgumentParser


def speak_response(response):
    """
    This function takes in a response and uses the pyttsx3 library to speak it
    out loud using text-to-speech functionality.

    Args:
        response (str): A string containing the response that should be spoken.

    Returns:
        None
    """

    SPEECH_SYNTHESIZER = None
    try:
        import gtts
        from playsound import playsound

        SPEECH_SYNTHESIZER = "gtts"
    except ModuleNotFoundError as e:
        pass

    # if SPEECH_SYNTHESIZER is None:
    #     try:
    #         from TTS.api import TTS
    #         from playsound import playsound

    #         SPEECH_SYNTHESIZER = "TTS"
    #     except ModuleNotFoundError as e:
    #         pass

    if SPEECH_SYNTHESIZER is None:
        try:
            import pyttsx3

            SPEECH_SYNTHESIZER = "pyttsx3"
        except:
            pass

    print(fg.cyan("Synthesizer:"), SPEECH_SYNTHESIZER)

    if SPEECH_SYNTHESIZER == "gtts":
        tts = gtts.gTTS(response, lang="en", tld="com.au")
        tts.save("output.wav")
        print(fg.cyan("Saved as wav"), "output.wav")
        print(fg.cyan("Playing speech back..."))
        playsound("output.wav")

    # elif SPEECH_SYNTHESIZER == "TTS":
    #     print(SPEECH_SYNTHESIZER)
    #     tts = TTS(
    #         model_name="tts_models/en/ek1/tacotron2",
    #         progress_bar=False,
    #         gpu=False,
    #     )
    #     print("initialized tts")
    #     # wav = tts.tts("This is test")
    #     tts.tts_to_file(
    #         response,
    #         file_path="output.wav",
    #     )
    #     print("Wrote to file")
    #     # playsound("output.wav")
    #     # print("PLayed")
    #     pass

    elif SPEECH_SYNTHESIZER == "pyttsx3":
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()


def send_to_chatgpt(
    prompt, engine="text-davinci-003", max_tokens=500, n=1, stop=None, temperature=0.7
):
    """
    Send a chat prompt to OpenAI's GPT-3 language model and receive a generated text response.

    Parameters:
    ----------
    prompt : str
        The text prompt to send to the OpenAI API for generating a response.
    engine : str, optional
        The OpenAI GPT-3 language model engine to use. Default is
        `"text-davinci-003"`.
    max_tokens : int, optional
        The maximum number of tokens to include in the generated text response.
        Default is 500.
    n : int, optional
        The number of responses to generate. Default is 1.
    stop : str or None, optional
        An optional string that, when encountered during text generation, will
        stop the generation process. Default is `None`.
    temperature : float, optional
        Controls the level of randomness in the generated response. A higher
        value results in more random responses. Default is 0.7.

    Returns:
    -------
    str
        The generated text response from the OpenAI GPT-3 language model.

    Examples:
    ---------
    >>> send_to_chatgpt("Hello!")
    "Hi there, how can I assist you today?"

    >>> send_to_chatgpt("What is the meaning of life?", max_tokens=1000)
    "The answer to the ultimate question of life, the universe, and everything is 42."
    """

    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
    )

    return response.choices[0].text


def main():
    parser = ArgumentParser()
    parser.add_argument("--speak", action="store_true", help="Speak the response")
    parser.add_argument(
        "--engine",
        default="text-davinci-003",
        help="set the OpenAI GPT-3 language model engine",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=500,
        help="set the maximum number of tokens in chatGPT response",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.7, help="control the level of randomness"
    )
    parser.add_argument(
        "--api_key",
        default=None,
        help="your openai api key...if not provided, reads from OPENAI_API_KEY env variable",
    )
    parser.add_argument(
        "--org_id",
        default=None,
        help="your openai organization id...if not provided, reads from OPENAI_ORGANIZATION_ID env variable",
    )

    args = parser.parse_args()

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    # Set up OpenAI API
    if args.api_key is None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    else:
        openai.api_key = args.api_key

    if args.org_id is None:
        openai.organization = os.getenv("OPENAI_ORGANIZATION_ID")
    else:
        openai.organization = args.org_id

    if openai.organization is None:
        print(
            fg.red(
                "Error: Couldn't find an OPENAI_ORGANIZATION_ID environtment variable"
            )
        )
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

            # Send the text to ChatGPT and get a response
            chatgpt_response = send_to_chatgpt(
                prompt,
                engine=args.engine,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )

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
