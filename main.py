from flask import Flask, send_file, render_template, jsonify
from transformers import pipeline
from scipy.io import wavfile
import scipy
import torch
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import librosa

app = Flask(__name__)

if torch.cuda.is_available():
    device = 0
else:
    device = -1

# insert customizable toggles

description = "country music"
plot_filename = "spectrogram.png"
audio_file = "musicgen_out.wav"

def generate(description, plot_filename, audio_file):
    synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=device)

    music = synthesiser(description, forward_params={"do_sample": True})
    print(music["audio"])
    print(music["sampling_rate"])

    scipy.io.wavfile.write(audio_file, rate=music["sampling_rate"], data=music["audio"])

    samplerate, data = wavfile.read('./musicgen_out.wav')
    print(f'Samplerate: {samplerate}')
    print(f'Data: {data, type(data)}')
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

    return plot_filename
    

@app.route("/",  methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/music", methods=["GET"])
def music():
    generate(description, plot_filename, audio_file)
    data = wavfile.read(audio_file)
    print(data)
    return render_template("visual.html", spectrogram=plot_filename, data=data[1].tolist())

if __name__ == "__main__": 
    app.run(debug=True)