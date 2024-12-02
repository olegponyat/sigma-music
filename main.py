import os
from flask import Flask, send_file, jsonify, request, render_template
from flask_cors import CORS
from transformers import pipeline
from scipy.io import wavfile
import scipy
import torch
import librosa
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import uuid
import time
app = Flask(__name__)
CORS(app)
session_data = {}  # Global in-memory storage

STATIC_DIR = os.path.join(app.root_path, 'static')
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

device = 0 if torch.cuda.is_available() else -1

# Store session data for visualization
session_data = {}

def generate(description, plot_filename, audio_file):
    synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=device)
    music = synthesiser(description, forward_params={"do_sample": True})

    scipy.io.wavfile.write(audio_file, rate=music["sampling_rate"], data=music["audio"])
    display(audio_file, plot_filename)

def display(audio_file, plot_filename):
    y, sr = librosa.load(audio_file)
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 6))

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, y_axis='linear', x_axis='time', sr=sr, ax=ax[0])

    ax[0].set(title='Linear-frequency power spectrogram', ylabel='Frequency [Hz]')
    ax[0].label_outer()

    ax[1].plot(np.linspace(0., len(y) / sr, len(y)), y, color='tab:blue')
    ax[1].set(title='Waveform', xlabel='Time [s]', ylabel='Amplitude')
    ax[1].grid(True)

    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close(fig)

@app.route("/music", methods=["POST"])
def music():
    description = request.json.get('description', '')
    if not description:
        return jsonify({"error": "Description is required"}), 400

    unique_id = str(uuid.uuid4())
    audio_file = os.path.join(STATIC_DIR, f"musicgen_out_{unique_id}.wav")
    plot_filename = os.path.join(STATIC_DIR, f"spectrogram_{unique_id}.png")

    generate(description, plot_filename, audio_file)

    audio_url = f"/static/musicgen_out_{unique_id}.wav"
    spectrogram_url = f"/static/spectrogram_{unique_id}.png"

    # Store the data for later retrieval
    session_data[unique_id] = {
        "description": description,
        "audio_url": audio_url,
        "spectrogram_url": spectrogram_url
    }

    return jsonify({
        "audio_url": audio_url,
        "spectrogram_url": spectrogram_url,
        "visual_url": f"/visual/{unique_id}"  
    })


@app.route("/visual/<unique_id>")
def visual(unique_id):
    audio_file = os.path.join(STATIC_DIR, f"musicgen_out_{unique_id}.wav")
    sigma = wavfile.read(audio_file)

    # Extract audio data and pass to the template
    audio_data = sigma[1].tolist()



    return render_template(
        "visual.html", 
        data=audio_data,
        unique_id=unique_id,  # Pass unique_id to the template
    )