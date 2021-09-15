import openai

filename = "response.wav"

# SET THIS TO YOUR OPENAI API KEY!
openai.api_key = "your-api-key"

chat_log = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman:"""

def loop():
    
    question = input("Question: ")

    prompt1 = f"{chat_log}Human: {question}\nAI:"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt1,
        #prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman:",
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )

    idValue = response['choices'][0]['text']
    print("AI:" + idValue)


while True:
    loop()
