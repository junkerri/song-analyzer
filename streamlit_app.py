import streamlit as st
import essentia
import essentia.standard as es
import tempfile
import os

st.set_page_config(page_title="Song Analyzer", page_icon="🎸")

st.title("Song Analyzer")
st.write("Upload a mono WAV file of your guitar playing and get the detected key, scale, BPM, and loudness.")

uploaded_file = st.file_uploader("Choose a WAV file", type="wav")

if uploaded_file is not None:
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_filename = tmp_file.name

    st.audio(uploaded_file, format="audio/wav")

    st.info("Analyzing...")

    # Load audio
    audio = es.MonoLoader(filename=tmp_filename)()

    # Key and scale
    key, scale, strength = es.KeyExtractor()(audio)

    # BPM
    bpm, beats, _, _, _ = es.RhythmExtractor2013(method="multifeature")(audio)

    # Loudness
    loudness = es.Loudness()(audio)

    # Show results
    st.subheader("🎵 Results")
    st.write(f"**Detected Key:** {key} {scale}")
    st.write(f"**Strength:** {strength:.3f}")
    st.write(f"**BPM:** {bpm:.2f}")
    st.write(f"**Loudness:** {loudness:.2f}")

    # Clean up the temp file
    os.unlink(tmp_filename)
else:
    st.warning("Please upload a WAV file to begin.")
