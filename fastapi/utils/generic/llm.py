import openai
import os

openaikey = os.getenv("OPENAI_API_KEY")

def generate_suggestions(audio_transcript, emotion):
    prompt = "Generate a 2 line positive quote for the with given context and emotion. Context:{} Emotion:{}".format(audio_transcript, emotion)
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
    prompt = "Generate 200 words summary for the give personal journal. Journal:{}".format(audio_transcript)
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
