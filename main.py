from flask import Flask
from transformers import pipeline
from scipy.io import wavfile
import scipy
import torch
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

if torch.cuda.is_available():
    device = 0
else:
    device = -1

# insert customizable toggles

description = 'country music'

def generate(description):
    synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=device)

    music = synthesiser(description, forward_params={"do_sample": True})
    print(music["audio"])
    print(music["sampling_rate"])

    scipy.io.wavfile.write("musicgen_out4.wav", rate=music["sampling_rate"], data=music["audio"])

    samplerate, data = wavfile.read('./musicgen_out.wav')
    print(f'Samplerate: {samplerate}')
    print(f'Data: {data, data.shape}')
    display(data)

def display(data):
    length = 29
    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data, label="Amplitude")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

@app.route("/")
def home():
    return "<p>Sigma Music Inc.</p>"

@app.route("/music", methods=["GET"])
def music():
    generate(description)
    return f"<p>Generating music for: {description}</p>"

if __name__ == "__main__": 
    app.run(debug=True)