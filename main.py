from flask import Flask
from transformers import pipeline
import scipy
import torch

app = Flask(__name__)

if torch.cuda.is_available():
    device = 0
else:
    device = -1

synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=device)

music = synthesiser("country music", forward_params={"do_sample": True})
print(music["audio"])
print(music["sampling_rate"])

scipy.io.wavfile.write("musicgen_out1.wav", rate=music["sampling_rate"], data=music["audio"])

@app.route("/")
def hello_world():
    return "<p>Sigma Music Inc.</p>"

if __name__ == "__main__": 
    app.run(debug=True)