import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

st.title("🎬 YouTube Video Summary Generator")

def extract_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    return match.group(1) if match else None

url = st.text_input("Enter YouTube Video URL:")

if url:
    video_id = extract_video_id(url)
    if video_id:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([t['text'] for t in transcript])

            st.subheader("📜 Transcript:")
            st.write(full_text[:1000] + "...")

            st.subheader("🧠 Summary:")
            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
            summary = summarizer(full_text[:1024], max_length=120, min_length=30, do_sample=False)
            st.success(summary[0]['summary_text'])

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Invalid URL format.")
