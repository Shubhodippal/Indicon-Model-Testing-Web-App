import streamlit as st
from pydub import AudioSegment
import io
import pandas as pd
import librosa
import numpy as np
import time

# Set page title and icon
st.set_page_config(page_title="Home", page_icon="🏠")
st.title("Welcome to the Home Page")


def extract_features(clip):
    """Extracts features from the given audio clip."""
    data, sample_rate = librosa.load(clip, sr=None)
    result = np.array([])

    # Feature Extraction
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result = np.hstack((result, zcr))

    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft))

    chroma_cqt = np.mean(librosa.feature.chroma_cqt(y=data, sr=sample_rate))
    result = np.hstack((result, chroma_cqt))

    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc))

    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms))

    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel))

    return result


# Ensure user is logged in
if 'username' in st.session_state and 'email' in st.session_state:
    st.subheader(f"Hello, {st.session_state.username}!")
    st.write(f"Your email: {st.session_state.email}")

    # Dropdown for selecting clip length
    clip_length = st.selectbox("Select chunk length (in milliseconds)", [500, 1000, 1500, 2000, 2500, 3000], index=2)

    uploaded_file = st.file_uploader("Upload a .wav file", type=["wav"], accept_multiple_files=False)

    if uploaded_file is not None:
        audio = AudioSegment.from_file(io.BytesIO(uploaded_file.read()), format="wav")
        duration_in_seconds = len(audio) / 1000

        if duration_in_seconds <= 180:
            st.audio(uploaded_file, format='audio/wav')

            # Check if features are already extracted for this session
            if "features_df" not in st.session_state:
                st.session_state.features_df = None

            if st.session_state.features_df is None:
                clips = [audio[i:i+clip_length] for i in range(0, len(audio), clip_length)]
                features_list = []

                progress_bar = st.progress(0)
                total_clips = len(clips)

                with st.spinner("Extracting features..."):
                    for idx, clip in enumerate(clips):
                        clip_io = io.BytesIO()
                        clip.export(clip_io, format="wav")
                        clip_io.seek(0)
                        clip_features = extract_features(clip_io)
                        features_list.append(clip_features)

                        # Update progress bar
                        progress = (idx + 1) / total_clips
                        progress_bar.progress(progress)

                # Store the extracted features in session state
                st.session_state.features_df = pd.DataFrame(features_list)
                #st.toast("Feature extraction completed successfully!", icon="✅")

            # Provide download link for the CSV file using in-memory storage
            csv_buffer = io.StringIO()
            st.session_state.features_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            st.write("Download the csv file and go to the next page for result analysis")
            st.write(st.session_state.features_df)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{st.session_state.username}_features.csv",
                mime="text/csv"
            )
            st.write("Go to the result page from the left side")

        else:
            st.error("The uploaded file exceeds the 3-minute length limit. Please upload a shorter file.")
else:
    st.warning("You are not logged in. Please go back to the login page.")

# Logout functionality
if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()
