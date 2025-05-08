# Install requirements:
# pip install youtube-search-python youtube-transcript-api openai

from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import re
from pdb import set_trace

client = OpenAI(api_key = 'You API Key')


def extract_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    return match.group(1) if match else None

def search_youtube(query, limit=3):
    videos_search = VideosSearch(query, limit=limit)
    results = videos_search.result()['result']
    return [{'title': v['title'], 'link': v['link']} for v in results]

def get_transcript_text(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except:
        return None

def collect_context(query):
    context_blocks = []
    videos = search_youtube(query)
    for video in videos:
        video_id = extract_video_id(video['link'])
        transcript = get_transcript_text(video_id)
        if transcript:
            context_blocks.append(f"Video Title: {video['title']}\nTranscript:\n{transcript[:1500]}\n{video['link']}")  # Limit to keep prompt under token limit
    # set_trace()
    return "\n\n".join(context_blocks)

def ask_gpt(query, context):
    prompt = f"""
    You are an academic research assistant. 
    Based on the following video transcripts, find the most relevant content to the User's Question. 
    If the answer is not found in the transcripts, say "I don't know".
    If you find the context is not relevant to the question, say "I don't know".
    If you find the context is relevant to the question, provide a structured summary of the context as follows:

    1. **Motivation**: Explain the motivation behind the study.
    2. **Novelty**: Highlight the novel aspects of the study.
    3. **Main Findings**: Summarize the main findings of the study.
    4. **Video Title**: Provide the title of the video.
    5. **Video Link**: Provide the link to the video.

    Context:
    {context}

    User Question: {query}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def run_rag_youtube_search(query):
    print("🔍 Searching YouTube and collecting transcripts...")
    context = collect_context(query)
    print("🤖 Asking GPT for a grounded response...")
    answer = ask_gpt(query, context)
    return answer

if __name__ == "__main__":
    user_query = input("Enter your question: ")
    result = run_rag_youtube_search(user_query)
    print("\n🧠 GPT Response:\n", result)
    
