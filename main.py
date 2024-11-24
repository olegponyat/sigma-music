from flask import Flask, send_file
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

def generate(description, plot_filename):
    synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=device)

    music = synthesiser(description, forward_params={"do_sample": True})
    print(music["audio"])
    print(music["sampling_rate"])

    audio_file = "musicgen_out4.wav"
    scipy.io.wavfile.write(audio_file, rate=music["sampling_rate"], data=music["audio"])

    samplerate, data = wavfile.read('./musicgen_out.wav')
    print(f'Samplerate: {samplerate}')
    print(f'Data: {data, data.shape}')
    display(audio_file, plot_filename)

def display(audio_file, plot_filename):
    """ length = 29
    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data, label="Amplitude")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
 """
    
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
    

@app.route("/")
def home():
    return "<p>Sigma Music Inc.</p>"

@app.route("/music", methods=["GET"])
def music():
    generate(description, plot_filename)
    return send_file(plot_filename, mimetype='image/png')

if __name__ == "__main__": 
    app.run(debug=True)