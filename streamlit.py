import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

from config.shared_state import Shared_State as State
from graph import build

# Page config
st.set_page_config(
    page_title="StoryForge | AI Story & Image Generator",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0B0B0F 0%, #1A1A20 100%);
        color: #FFFFFF;
    }

    /* Hide default elements */
    #MainMenu, footer, header { display: none; }

    /* Custom container */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    /* Header section */
    .header {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeIn 0.8s ease-out;
    }

    .title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFE6B0 0%, #B5A1FF 50%, #FFB8B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #8A8F99;
        font-weight: 300;
    }

    /* Input section */
    .input-section {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
        animation: slideUp 0.6s ease-out;
    }

    /* Custom text input */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:hover {
        border-color: rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #B5A1FF !important;
        box-shadow: 0 0 0 4px rgba(181, 161, 255, 0.1) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #4A4F5A !important;
        font-weight: 300;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #B5A1FF 0%, #FFB8B8 100%) !important;
        color: #0B0B0F !important;
        border: none !important;
        border-radius: 16px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.875rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px -5px rgba(181, 161, 255, 0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Logs container */
    .logs-container {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.25rem;
        margin: 1.5rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        max-height: 200px;
        overflow-y: auto;
    }

    .log-entry {
        padding: 0.35rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        animation: slideIn 0.3s ease-out;
    }

    .log-entry:last-child {
        border-bottom: none;
    }

    .log-orch {
        color: #B5A1FF;
    }

    .log-story {
        color: #6CD4B3;
    }

    .log-image {
        color: #FFB8B8;
    }

    .log-error {
        color: #FF6B6B;
    }

    .timestamp {
        color: #4A4F5A;
        margin-right: 0.5rem;
        font-size: 0.75rem;
    }

    /* Story card */
    .story-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem 0;
        animation: scaleIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }

    .story-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #B5A1FF, #FFB8B8);
    }

    .story-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #B5A1FF;
        margin-bottom: 1rem;
    }

    .story-text {
        font-family: 'Inter', serif;
        font-size: 1.1rem;
        line-height: 1.8;
        color: #E0E0E0;
    }

    /* Image container */
    .image-container {
        margin: 2rem 0;
        animation: fadeIn 0.5s ease-out;
    }

    .image-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #FFB8B8;
        margin-bottom: 1rem;
    }

    .generated-image {
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    /* Error box */
    .error-box {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.3);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        color: #FFB8B8;
        font-family: 'Inter', sans-serif;
        margin: 1.5rem 0;
        animation: shake 0.5s ease-out;
    }

    /* Loading animation */
    .loading-dots {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        margin: 2rem 0;
    }

    .loading-dots div {
        width: 12px;
        height: 12px;
        background: #B5A1FF;
        border-radius: 50%;
        animation: bounce 0.5s infinite alternate;
    }

    .loading-dots div:nth-child(2) {
        animation-delay: 0.1s;
        background: #6CD4B3;
    }

    .loading-dots div:nth-child(3) {
        animation-delay: 0.2s;
        background: #FFB8B8;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes bounce {
        from { transform: translateY(0); }
        to { transform: translateY(-10px); }
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
        20%, 40%, 60%, 80% { transform: translateX(2px); }
    }

    /* Progress indicator */
    .progress-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #8A8F99;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        margin: 1rem 0;
    }

    .progress-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: currentColor;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }

    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 2rem 0;
    }

    /* Example prompts */
    .examples {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .example-tag {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 100px;
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
        color: #8A8F99;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .example-tag:hover {
        background: rgba(181, 161, 255, 0.1);
        border-color: #B5A1FF;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="title">StoryForge</div>
    <div class="subtitle">Transform your ideas into stories and images</div>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)

# Example prompts
example_prompts = [
    "a lonely lighthouse keeper discovers a message in a bottle",
    "a fox befriends a lost robot in the winter forest",
    "a city where buildings dream and streets remember",
    "a painter who brings emotions to life with colors"
]

# Create columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input(
        label="",
        placeholder="Enter your story idea...",
        label_visibility="collapsed",
        key="story_input"
    )

with col2:
    run = st.button("Generate →", use_container_width=True)

# Example prompts as clickable tags
if not user_input:
    st.markdown('<div class="examples">', unsafe_allow_html=True)
    for prompt in example_prompts:
        st.markdown(f'<span class="example-tag" onclick="navigator.clipboard.writeText(\'{prompt}\')">{prompt}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Main pipeline
if run and user_input.strip():
    logs = []
    app = build()

    # Placeholders for dynamic content
    log_placeholder = st.empty()
    progress_placeholder = st.empty()
    story_placeholder = st.empty()
    image_placeholder = st.empty()

    def add_log(log_type, message):
        timestamp = time.strftime("%H:%M:%S")
        logs.append((log_type, message, timestamp))
        
        # Render logs
        log_html = '<div class="logs-container">'
        for log_type, msg, ts in logs:
            log_html += f'<div class="log-entry {log_type}"><span class="timestamp">[{ts}]</span> {msg}</div>'
        log_html += '</div>'
        log_placeholder.markdown(log_html, unsafe_allow_html=True)

    # Initial log
    add_log("log-orch", f"✨ Received: \"{user_input[:50]}{'...' if len(user_input) > 50 else ''}\"")
    add_log("log-orch", "🔄 Routing to Story Agent")

    # Show progress indicator
    progress_placeholder.markdown("""
    <div class="progress-indicator">
        <span class="progress-dot"></span>
        <span>Crafting your story...</span>
    </div>
    """, unsafe_allow_html=True)

    # Run the pipeline
    with st.spinner(""):
        result = app.invoke(State(
            messages=[HumanMessage(content=user_input)],
            user_input=user_input,
            story=None,
            image_url=None,
            error=None,
        ))

    progress_placeholder.empty()

    if result.get("error"):
        add_log("log-error", f"❌ Error: {result['error']}")
        st.markdown(f'<div class="error-box">⚠️ {result["error"]}</div>', unsafe_allow_html=True)

    else:
        story = result.get("story", "")
        image_url = result.get("image_url", "")

        # Add logs
        add_log("log-story", f"📝 Story complete — {len(story.split())} words")
        add_log("log-orch", "🎨 Routing to Image Agent")
        
        if image_url:
            add_log("log-image", "🖼️ Image generated successfully")

        # Display story
        story_placeholder.markdown(f"""
        <div class="story-card">
            <div class="story-label">📖 Your Story</div>
            <div class="story-text">{story}</div>
        </div>
        """, unsafe_allow_html=True)

        # Display image
        if image_url:
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown('<div class="image-label">🎨 Generated Image</div>', unsafe_allow_html=True)
            
            if image_url.startswith("http"):
                st.image(image_url, use_container_width=True, output_format="auto")
            elif os.path.exists(image_url):
                st.image(image_url, use_container_width=True, output_format="auto")
            else:
                st.markdown(f'<div class="log-box"><span class="log-image">{image_url}</span></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

elif run and not user_input.strip():
    st.markdown("""
    <div class="error-box">
        ⚠️ Please enter a story idea to begin
    </div>
    """, unsafe_allow_html=True)