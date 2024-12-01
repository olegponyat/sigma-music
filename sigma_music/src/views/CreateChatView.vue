<template>
  <div class="chat-container">
    <!-- Greeting -->
    <div class="greeting">What can I help with?</div>

    <!-- Chat Input Box -->
    <div class="chat-box">
      <input v-model="message" type="text" placeholder="Message ChatCBD" class="chat-input" />
      <button class="send-button" @click="sendMessage">↑</button>
    </div>

    <!-- Example Buttons -->
    <div class="example-inputs">
      <button class="example-btn" @click="setMessage('country music')">🤠 Country</button>
      <button class="example-btn" @click="setMessage('lo-fi music')">🎧 Lo-fi</button>
      <button class="example-btn" @click="setMessage('rock music')">🎸 Rock</button>
      <button class="example-btn" @click="setMessage('pop music')">🎤 Pop</button>
      <button class="example-btn" @click="setMessage('synth music')">🎹 Synth</button>
    </div>

    <!-- Display Spectrogram and Audio -->
    <div v-if="spectrogram">
      <img :src="spectrogram" alt="Spectrogram" />
      <audio :src="audioSrc" controls></audio>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatInterface',
  data() {
    return {
      message: '', // Current chat message
      spectrogram: null, // Spectrogram image filename
      audioSrc: null, // Audio file URL
    };
  },
  methods: {
    setMessage(description) {
      this.message = description;
    },
    sendMessage() {
      if (!this.message) return;

      // Send POST request to Flask
      axios.post('http://localhost:5000/music', { description: this.message })
        .then(response => {
          // Handle the response: get the audio file URL and spectrogram URL
          this.audioSrc = `http://localhost:5000${response.data.audio_url}`;
          this.spectrogram = `http://localhost:5000${response.data.spectrogram_url}`;
        })
        .catch(error => {
          console.error('Error generating music:', error);
        });
    }
  }
};
</script>
<style scoped>
/* Importing Inter Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.chat-container {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Vertical alignment */
  align-items: center; /* Horizontal alignment */
  height: 100vh; /* Full viewport height */
  background-color: #ffffff;
  padding: 2rem; /* Reduced padding */
  font-family: 'Inter', sans-serif;
  text-align: center; /* Center text alignment */
}

.greeting {
  font-size: 2.4rem; /* Slightly smaller font */
  font-weight: 700;
  margin-bottom: 1.8rem; /* Reduced spacing */
  color: #333;
}

.status-dot {
  color: #2ecc71;
  font-size: 1.2rem;
}

.chat-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 700px; /* Reduced max-width */
  border: 1px solid #ddd;
  border-radius: 22px; /* Slightly smaller radius */
  padding: 0.4rem 1rem; /* Reduced padding */
  background-color: #f7f7f8;
  margin-bottom: 2rem; /* Reduced spacing */
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Reduced shadow */
}

.chat-input {
  border: none;
  flex-grow: 1;
  outline: none;
  font-weight: lighter;
  background: transparent;
  font-size: 0.9rem; /* Slightly smaller font */
  font-family: 'Inter', sans-serif;
  color: #333;
}

.chat-input::placeholder {
  color: #aaa;
}

.send-button {
  background-color: #000;
  border: none;
  color: #fff;
  font-size: 1.4rem; /* Slightly smaller arrow size */
  cursor: pointer;
  padding: 0.4rem;
  border-radius: 50%; /* Circular button */
  font-family: 'Inter', sans-serif;
  width: 2.2rem; /* Slightly smaller button size */
  height: 2.2rem; /* Slightly smaller button size */
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover {
  background-color: #333;
}

.example-inputs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem; /* Slightly reduced button spacing */
  justify-content: center;
}

.example-btn {
  background-color: #f1f1f1;
  border: none;
  border-radius: 18px; /* Smaller button radius */
  padding: 0.6rem 1.1rem; /* Slightly smaller padding */
  font-size: 0.9rem; /* Slightly smaller text */
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  white-space: nowrap;
}

.example-btn:hover {
  background-color: #e0e0e0;
}
</style>
