import nltk
from youtube_transcript_api import YouTubeTranscriptApi
from config import collection

nltk.download("punkt",     quiet=True)
nltk.download("punkt_tab", quiet=True)


def getVideoId(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")


def fetchTranscript(videoId):
    transcript = YouTubeTranscriptApi.get_transcript(videoId)
    return " ".join([entry["text"] for entry in transcript])


def chunkText(text, maxWords=150, overlapSentences=1):
    sentences = nltk.sent_tokenize(text)
    chunks    = []
    current   = []
    wordCount = 0

    for sentence in sentences:
        words = len(sentence.split())
        if wordCount + words > maxWords and current:
            chunks.append(" ".join(current))
            current   = current[-overlapSentences:]
            wordCount = sum(len(s.split()) for s in current)
        current.append(sentence)
        wordCount += words

    if current:
        chunks.append(" ".join(current))

    return chunks


def indexVideo(url):
    videoId    = getVideoId(url)
    print(f"Fetching transcript for: {videoId}")

    text       = fetchTranscript(videoId)
    pageChunks = chunkText(text)
    chunks     = []
    ids        = []

    for i, chunk in enumerate(pageChunks):
        if len(chunk.split()) > 10:
            chunks.append(chunk)
            ids.append(f"{videoId}_chunk_{i+1}")

    collection.upsert(documents=chunks, ids=ids)
    print(f"Total chunks stored: {len(chunks)}")