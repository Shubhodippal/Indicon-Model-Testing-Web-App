import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import io
import keras
import librosa
import joblib
import matplotlib.pyplot as plt
import plotly.express as px
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Set page title and icon
st.set_page_config(page_title="Result Analysis", page_icon="📊")
st.title("Result Analysis")

# Ensure user is logged in
if 'username' in st.session_state and 'email' in st.session_state:
    st.subheader(f"Hello, {st.session_state.username}!")
    st.write(f"Your email: {st.session_state.email}")

    # File uploader for feature CSV file
    uploaded_file = st.file_uploader("Upload a feature CSV file", type=["csv"], accept_multiple_files=False)

    if uploaded_file is not None:
        # Read the uploaded CSV file
        features_df = pd.read_csv(uploaded_file)
        #st.write("Uploaded feature file:")
        #st.write(features_df)

        MODEL_PATH = "audio_classification.hdf5"  # Update with the correct path
        SCALER_PATH = "scaler.pkl"  # Update with the correct path
        ENCODER_PATH = "onehot_encoder.pkl"  # Update with the correct path

        # Load model and preprocessing objects
        model = load_model(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoder = joblib.load(ENCODER_PATH)

        # Retrieve audio file length and clip length from session storage
        audio_file_length = st.session_state.get('audio_file_length', 2)
        clip_length = st.session_state.get('clip_length', 60)  # Default to 1 second if not set

        # Emotion labels mapping
        emotion_labels = {
            1: "ANGRY",
            2: "DISGUST",
            3: "FEAR",
            4: "HAPPY",
            5: "SAD",
            6: "SURPRISE",
            7: "NEUTRAL"
        }

        def predict_audio(features):
            """Predict emotion from an audio file."""
            features = scaler.transform(features)
            features = np.expand_dims(features, axis=2)  # Reshape for model input
            prediction = model.predict(features)
            predicted_label = encoder.inverse_transform(prediction)
            return predicted_label.flatten()[0]

        message_placeholder = st.empty()
        message_placeholder.text("Processing...")
        progress_bar = st.progress(0)
        predictions = []
        for i in range(0, len(features_df)):
            features = features_df.iloc[i].values
            features = features.reshape(1, -1)
            result = predict_audio(features)
            predictions.append(emotion_labels.get(result, "UNKNOWN"))
            progress_bar.progress((i + 1) / len(features_df))

        message_placeholder.empty()
        st.success("Prediction completed successfully!")

        st.write(predictions)
        print(predictions)
        result_df = pd.DataFrame(predictions, columns=["Predicted Emotion"])

        # Create a pie chart
        emotion_counts = result_df["Predicted Emotion"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(emotion_counts, labels=emotion_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

        # Create a timestamp-wise representation
        timestamps = pd.date_range(start='1/1/2022', periods=len(result_df), freq=f'{clip_length}S')
        result_df['Timestamp'] = timestamps
        fig = px.line(result_df, x='Timestamp', y='Predicted Emotion', title='Timestamp-wise Emotion Representation')
        st.plotly_chart(fig)

        csv_buffer = io.StringIO()
        result_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        st.download_button(
            label="Download Result Analysis CSV",
            data=csv_data,
            file_name=f"{st.session_state.username}_result_analysis.csv",
            mime="text/csv"
        )

else:
    st.warning("You are not logged in. Please go back to the login page.")

# Logout functionality
if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()