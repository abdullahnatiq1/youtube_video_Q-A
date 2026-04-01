from config import client, collection

def llm(prompt):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[{"role" : "user", "content" : prompt}]
    )
    return response.choices[0].message.content.strip()

def filterChunksBatch(query, chunks):
    numbered = "\n".join([f"{i+1}. {c[:300]}" for i, c in enumerate(chunks)])
    prompt = f"""
give the following question : "{query}"
which of these chunks are useful to answer it? {numbered}
Reply with only the number of useful chunks, comma seperated. Example: 1,3,5
If none are useful reply: NONE
"""
    result = llm(prompt)

    if "NONE" in result.upper():
        return[]
    
    try:
        indices = [int(x.strip()) - 1 for x in result.split(",") if x.split() .isdigit()]
        return [chunks[i] for i in indices if 0 <= i < len(chunks)]
    except:
        return chunks
    
def isAnswerRelevant(answer, context):
    return "YES" in llm(
        f"Is this answer based on te context? \n Context : {context} \n Answer: {answer} \n Reply YES or NO only"
    ).upper()

def selfRagRetrieve(query):
    results = collection.query(query_texts=[query],n_results=5)
    chunks = results["documents"][0]
    usefulChunks = filterChunksBatch(query, chunks)
    print(f"Total: {len(chunks)}, USeful: {len(usefulChunks)}")
    return "\n\n".join(usefulChunks) if usefulChunks else "\n\n".join(chunks)

def selfRagVerify(answer, context):
    if isAnswerRelevant(answer, context):
        print("Answer is Relevant")
    else:
        print("Answer is Irrelevant")


