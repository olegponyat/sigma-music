import os
from flask import Flask, send_file, jsonify
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

app = Flask(__name__)
CORS(app)

# Static folder should be inside the project, accessible via /static URL
STATIC_DIR = os.path.join(app.root_path, 'static')
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

if torch.cuda.is_available():
    device = 0
else:
    device = -1

# Filenames for the music and spectrogram
description = "country music"
plot_filename = os.path.join(STATIC_DIR, "spectrogram.png")
audio_file = os.path.join(STATIC_DIR, "musicgen_out.wav")

def generate(description, plot_filename, audio_file):
    synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=device)

    music = synthesiser(description, forward_params={"do_sample": True})
    print(music["audio"])
    print(music["sampling_rate"])

    # Save audio file
    scipy.io.wavfile.write(audio_file, rate=music["sampling_rate"], data=music["audio"])

    # Generate spectrogram
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
    
    print(f"Saving spectrogram as: {plot_filename}")
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close(fig)

@app.route("/music", methods=["POST"])
def music():
    generate(description, plot_filename, audio_file)
    
    # Return audio file URL and spectrogram URL
    audio_url = f"/static/musicgen_out.wav"
    spectrogram_url = f"/static/spectrogram.png"
    return jsonify({"audio_url": audio_url, "spectrogram_url": spectrogram_url})

if __name__ == "__main__": 
    app.run(debug=True)
