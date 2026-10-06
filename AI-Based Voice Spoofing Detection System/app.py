import streamlit as st
import textwrap
import tempfile
import os

# Uncomment these when your backend folder is ready
# from backend.feature_extraction import extract_features
# from backend.detector import VoiceSpoofDetector


# ============================================================
# HTML HELPER (FIXED)
# ============================================================

def html(content):
    """Render HTML without Streamlit turning it into a code block.

    Removes all indentation and blank lines, which Markdown would
    otherwise treat as code blocks / end of the HTML block.
    """
    cleaned = "\n".join(
        line.strip()
        for line in textwrap.dedent(content).splitlines()
        if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VoxShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD CSS
# ============================================================

try:
    with open("frontend/styles.css", "r", encoding="utf-8") as f:
        css = f.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )

except FileNotFoundError:
    st.warning(
        "⚠️ styles.css not found. "
        "Make sure frontend/styles.css exists."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html("""
    <div class="logo-container">
        <div class="logo-icon">🛡️</div>

        <div>
            <h2>VoxShield AI</h2>
            <p>Authenticity Lab</p>
        </div>
    </div>
    """)

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎙️ Voice Detection",
            "🎥 Video Detection",
            "📊 Analysis History",
            "ℹ️ About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    html("""
    <div class="sidebar-status">
        <span class="status-dot"></span>
        System Ready
    </div>
    """)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    html("""
    <div class="hero">

        <div class="hero-badge">
            🛡️ AI-POWERED AUTHENTICITY DETECTION
        </div>

        <h1>
            Detect
            <span>AI-Generated</span>
            <br>
            Voices &amp; Videos
        </h1>

        <p>
            Analyze suspicious audio and video content
            to estimate whether the voice is likely
            human-generated or AI-generated.
        </p>

    </div>
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        html("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3>Voice Detection</h3>
            <p>
                Analyze voice recordings and detect
                potential AI-generated speech.
            </p>
        </div>
        """)

    with col2:
        html("""
        <div class="feature-card">
            <div class="feature-icon">🎥</div>
            <h3>Video Analysis</h3>
            <p>
                Upload videos and analyze their
                speech audio for synthetic voices.
            </p>
        </div>
        """)

    with col3:
        html("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Smart Results</h3>
            <p>
                Get an easy-to-understand authenticity
                score and analysis.
            </p>
        </div>
        """)

    html("""
    <div class="section-title">
        <h2>Start an Analysis</h2>
        <p>Choose an audio or video file to begin.</p>
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:

        html("""
        <div class="upload-card">
            <div class="upload-icon">🎙️</div>
            <h3>Analyze Voice</h3>
            <p>Upload an audio recording</p>
        </div>
        """)

        st.file_uploader(
            "Upload Audio",
            type=["wav", "mp3", "m4a", "ogg"],
            key="dashboard_audio",
            label_visibility="collapsed"
        )

    with col2:

        html("""
        <div class="upload-card">
            <div class="upload-icon">🎥</div>
            <h3>Analyze Video</h3>
            <p>Upload a video containing speech</p>
        </div>
        """)

        st.file_uploader(
            "Upload Video",
            type=["mp4", "mov", "avi", "mkv"],
            key="dashboard_video",
            label_visibility="collapsed"
        )


# ============================================================
# VOICE DETECTION
# ============================================================

elif page == "🎙️ Voice Detection":

    html("""
    <div class="page-header">

        <div class="page-icon">🎙️</div>

        <div>
            <h1>Voice Detection</h1>

            <p>
                Analyze a voice recording for
                potential AI-generated speech.
            </p>
        </div>

    </div>
    """)

    tab1, tab2 = st.tabs(
        ["📁 Upload Voice", "🎤 Record Voice"]
    )

    # --------------------------------------------------------
    # UPLOAD VOICE
    # --------------------------------------------------------

    with tab1:

        html("""
        <div class="big-upload">

            <div class="big-upload-icon">🎙️</div>

            <h2>Upload your voice recording</h2>

            <p>
                Supported formats:
                WAV • MP3 • M4A • OGG
            </p>

        </div>
        """)

        audio = st.file_uploader(
            "Choose audio file",
            type=["wav", "mp3", "m4a", "ogg"],
            label_visibility="collapsed"
        )

        if audio is not None:

            st.audio(audio)

            html("""
            <div class="file-info">
                <b>File uploaded successfully</b>
                <br>
                Ready for analysis.
            </div>
            """)

            if st.button(
                "🔍 Analyze Voice",
                use_container_width=True
            ):
                st.info(
                    "AI detection backend will be connected next."
                )

    # --------------------------------------------------------
    # RECORD VOICE
    # --------------------------------------------------------

    with tab2:

        html("""
        <div class="record-card">

            <div class="record-icon">🎤</div>

            <h2>Record Your Voice</h2>

            <p>
                Record a short voice sample
                directly from your microphone.
            </p>

        </div>
        """)

        recorded_audio = st.audio_input(
            "Click the mic to start recording",
            label_visibility="collapsed"
        )

        if recorded_audio is not None:

            st.audio(recorded_audio)

            html("""
            <div class="file-info">
                <b>Recording captured successfully</b>
                <br>
                Ready for analysis.
            </div>
            """)

            if st.button(
                "🔍 Analyze Recording",
                use_container_width=True,
                key="analyze_recording"
            ):
                # Save the recording to a temporary WAV file
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".wav"
                ) as tmp:
                    tmp.write(recorded_audio.getvalue())
                    temp_path = tmp.name

                st.info(f"Recording saved at: {temp_path}")

                # Later, connect your detector here:
                # features = extract_features(temp_path)
                # result = detector.predict(features)

                os.remove(temp_path)


# ============================================================
# VIDEO DETECTION
# ============================================================

elif page == "🎥 Video Detection":

    html("""
    <div class="page-header">

        <div class="page-icon">🎥</div>

        <div>
            <h1>Video Detection</h1>

            <p>
                Analyze the voice contained inside a video.
            </p>
        </div>

    </div>
    """)

    html("""
    <div class="big-upload">

        <div class="big-upload-icon">🎥</div>

        <h2>Upload a Video</h2>

        <p>
            Upload a video containing speech.
        </p>

    </div>
    """)

    video = st.file_uploader(
        "Choose video file",
        type=["mp4", "mov", "avi", "mkv"],
        label_visibility="collapsed"
    )

    if video is not None:

        st.video(video)

        html("""
        <div class="file-info">

            <b>Video uploaded successfully</b>

            <br>

            Ready for analysis.

        </div>
        """)

        if st.button(
            "🔍 Analyze Video",
            use_container_width=True
        ):

            st.info(
                "🎥 Video analysis backend will be connected "
                "after audio extraction is added."
            )


# ============================================================
# ANALYSIS HISTORY
# ============================================================

elif page == "📊 Analysis History":

    html("""
    <div class="page-header">

        <div class="page-icon">📊</div>

        <div>
            <h1>Analysis History</h1>

            <p>
                View your previous voice and video
                authenticity analyses.
            </p>
        </div>

    </div>
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        html("""
        <div class="feature-card">
            <div class="feature-icon">📁</div>
            <h3>Total Analyses</h3>
            <h2>0</h2>
            <p>No analyses yet</p>
        </div>
        """)

    with col2:
        html("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3>Voice Analyses</h3>
            <h2>0</h2>
            <p>No voice files analyzed</p>
        </div>
        """)

    with col3:
        html("""
        <div class="feature-card">
            <div class="feature-icon">🎥</div>
            <h3>Video Analyses</h3>
            <h2>0</h2>
            <p>No video files analyzed</p>
        </div>
        """)

    st.markdown("### 📋 Recent Analysis")

    html("""
    <div class="empty-state">

        <div class="empty-icon">📂</div>

        <h2>No Analyses Yet</h2>

        <p>
            Your previous analysis results
            will appear here after you analyze
            a voice or video.
        </p>

    </div>
    """)


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    html("""
    <div class="page-header">

        <div class="page-icon">🛡️</div>

        <div>
            <h1>About VoxShield AI</h1>

            <p>
                Voice &amp; Video Authenticity Detection System
            </p>
        </div>

    </div>
    """)

    html("""
    <div class="about-card">

        <h2>What is VoxShield AI?</h2>

        <p>
            VoxShield AI is an AI-based voice spoofing
            detection system designed to analyze audio
            and video content and estimate whether
            speech is likely human-generated or
            AI-generated.
        </p>

        <h3>🔬 How It Works</h3>

        <div class="process">

            <div>
                <b>01</b>
                <span>Upload</span>
            </div>

            <div>
                <b>02</b>
                <span>Extract</span>
            </div>

            <div>
                <b>03</b>
                <span>Analyze</span>
            </div>

            <div>
                <b>04</b>
                <span>Detect</span>
            </div>

        </div>

    </div>
    """)
 