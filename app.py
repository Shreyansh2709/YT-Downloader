import streamlit as st
import yt_dlp
import os
import uuid
import re

st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("🤖 YouTube Video Downloader")

url = st.text_input("Enter YouTube Video URL")

# Predefine containers so layout doesn't jump
loading_placeholder = st.empty()
thumbnail_placeholder = st.empty()
button_placeholder = st.empty()

loader_css = """
<style>
.loader {
    position: relative;
    width: 108px;
    height: 48px; /* Lock height to prevent layout jump */
    display: flex;
    justify-content: space-between;
    margin: 30px auto;
}
.loader::after, .loader::before {
    content: '';
    display: inline-block;
    width: 48px;
    height: 48px;
    background-color: #FFF;
    background-image: radial-gradient(circle 14px, #0d161b 100%, transparent 0);
    background-repeat: no-repeat;
    border-radius: 50%;
    animation: eyeMove 10s infinite, blink 10s infinite;
    transform-origin: center;
}
@keyframes eyeMove {
    0%, 10% { background-position: 0px 0px; }
    13%, 40% { background-position: -15px 0px; }
    43%, 70% { background-position: 15px 0px; }
    73%, 90% { background-position: 0px 15px; }
    93%, 100% { background-position: 0px 0px; }
}
@keyframes blink {
    0%, 10%, 12%, 20%, 22%, 40%, 42%, 60%, 62%, 70%, 72%, 90%, 92%, 98%, 100% {
        transform: scaleY(1);
    }
    11%, 21%, 41%, 61%, 71%, 91%, 99% {
        transform: scaleY(0.4); /* Simulate blinking without changing height */
    }
}
</style>
"""


loader_html = "<div class='loader'></div><p style='text-align:center;'>Your video is loading. This might take a moment...</p>"

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

if url:
    # Show loader immediately
    loading_placeholder.markdown(loader_css + loader_html, unsafe_allow_html=True)

    video_id = str(uuid.uuid4())
    output_path = f"{video_id}.mp4"

    ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'outtmpl': output_path,
    'merge_output_format': 'mp4',
    'quiet': True,
}


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'video')
            yt_id = info_dict.get('id', None)

        # Clean up loader once video is ready
        loading_placeholder.empty()

        st.success("✅ Download complete!")

        # Show thumbnail
        if yt_id:
            thumbnail_url = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg"
            thumbnail_placeholder.image(thumbnail_url, use_container_width=True)

        # Show download button
        with open(output_path, "rb") as file:
            button_placeholder.download_button(
                label="📥 Download Video",
                data=file,
                file_name=f"{title}.mp4",
                mime="video/mp4"
            )

        os.remove(output_path)

    except Exception as e:
        loading_placeholder.empty()
        st.error(f"❌ Error: {e}")