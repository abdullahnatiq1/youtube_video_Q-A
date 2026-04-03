from dotenv import load_dotenv
from selfrag import selfRagRetrieve, selfRagVerify
from config import client, collection
from chunking import indexVideo

load_dotenv()

URL = input("Enter your URL: ")

if collection.count() == 0:
    indexVideo(URL)
else:
    print("Already Indexed")

history = []
lastContext = ""

while True:
    query = input("You: ")
    if query.lower == "exit":
        break

    if any(word in query.lower()for word in ["further", "explain", "more", "describe", "elaborate"]):
        retrievedContext = lastContext
    else:
        retrievedContext = selfRagRetrieve(query)
        lastContext = retrievedContext

    prompt = f"""
    Answer the following based on the context provided
    Context : {retrievedContext}
    Question : {query}
"""
    history.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        stream = True,
        messages = history,
        temperature= 0.5
    )

    print("Assistant: ", end="", flush = True)
    fullResponse = ""

    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content , end="", flush = True)
            fullResponse += content
            
    history.append({"role": "assistant", "content": fullResponse})
    selfRagVerify(fullResponse, retrievedContext)