import openai
import os

openaikey = os.getenv("OPENAI_API_KEY")

def generate_suggestions(audio_transcript, emotion):
    prompt = """I want you to act as a motivational friend and generate a 2 line positive quote for the with given context and emotion. 
                Make it conversational to ensure that the mood is uplifted. 
                Context:{} Emotion:{}""".format(audio_transcript, emotion)
    print(prompt)
    openai.api_key = openaikey
    promptstr=prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=promptstr,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    return response.get("choices")[0]["text"]

def generate_summary(audio_transcript):
    prompt = """Can you provide a comprehensive summary of the given text? 
    The summary should cover all the key points and main ideas presented in the original text, 
    while also condensing the information into a concise and easy-to-understand format.
    Give the summary from the person's point of view.
    Please ensure that the summary includes relevant details and examples that support the main ideas, 
    while avoiding any unnecessary information or repetition. 
    The length of the summary should be appropriate for the length and complexity of the original text, 
    providing a clear and accurate overview without omitting any important information and completing the meaningful sentences.
    To ensure accuracy, please read the text carefully and pay attention to any nuances or complexities in the language.
    Text:{}""".format(audio_transcript)
    print(prompt)
    openai.api_key = openaikey
    promptstr=prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=promptstr,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    return response.get("choices")[0]["text"]
