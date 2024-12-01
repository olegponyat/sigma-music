<script>
import axios from 'axios';

export default {
  name: 'ChatInterface',
  data() {
    return {
      message: '', // User's input message
      musicFiles: [], // Array to store audio and spectrogram URLs
      isLoading: false, // Loading state
    };
  },
  methods: {
    // Method to set the message text
    setMessage(description) {
      this.message = description;
    },

    // Method to send the message and fetch the audio file
    sendMessage() {
      if (!this.message) return;

      // Show loading state
      this.isLoading = true;

      // Send the request to the Flask server
      axios
        .post('http://localhost:5000/music', { description: this.message })
        .then((response) => {
          // Push the audio and spectrogram URLs to the musicFiles array
          this.musicFiles.push({
            audioSrc: `http://localhost:5000${response.data.audio_url}`, // Full audio URL
            spectrogram: `http://localhost:5000${response.data.spectrogram_url}`, // Full spectrogram URL
          });

          // Clear the message input after sending
          this.message = '';
        })
        .catch((error) => {
          console.error('Error generating music:', error);
        })
        .finally(() => {
          // Hide loading state
          this.isLoading = false;
        });
    }
  }
};
</script>

<template>
  <div class="chat-container">
    <div class="chat-history">
      <div
        v-for="(file, index) in musicFiles"
        :key="index"
        class="chat-bubble bot-bubble"
      >
        <!-- Audio player for the generated music -->
        <audio :src="file.audioSrc" controls></audio>
        
        <!-- Spectrogram image -->
        <img :src="file.spectrogram" alt="Spectrogram" />
      </div>
    </div>

    <div class="chat-box">
      <input
        type="text"
        v-model="message"
        placeholder="Type a description"
        class="chat-input"
        :disabled="isLoading"
        @keydown.enter="sendMessage"
      />
      <button
        class="send-button"
        @click="sendMessage"
        :disabled="isLoading"
      >
        ↑
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  height: 100vh;
  background-color: #ffffff;
  font-family: 'Inter', sans-serif;
  position: relative;
}

.chat-history {
  width: 100%;
  max-width: 700px;
  height: 80vh; /* Increased height for the chat history */
  overflow-y: auto; /* Enable scrolling */
  padding: 1rem;
  background-color: #f7f7f8;
  border-radius: 12px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.chat-bubble {
  padding: 10px;
  border-radius: 20px;
  font-size: 16px;
  margin-bottom: 15px;
  max-width: 60%;
  line-height: 1.5;
  word-wrap: break-word;
  background-color: #f1f1f1;
  color: #000;
}

.bot-bubble {
  margin-right: auto;
  background-color: #e1e2e1;
}

.chat-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 700px;
  border: 1px solid #ddd;
  border-radius: 22px;
  padding: 0.5rem 1rem;
  background-color: #ffffff;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chat-input {
  border: none;
  flex-grow: 1;
  outline: none;
  font-weight: lighter;
  background: transparent;
  font-size: 1rem;
  color: #333;
}

.chat-input::placeholder {
  color: #aaa;
}

.send-button {
  background-color: #000;
  border: none;
  color: #fff;
  font-size: 1.4rem;
  cursor: pointer;
  padding: 0.4rem;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover {
  background-color: #333;
}

@media (max-width: 768px) {
  .chat-box {
    max-width: 90%;
    padding: 0.4rem 0.8rem;
  }

  .chat-history {
    max-width: 90%;
    height: 60vh; /* Adjusted height for smaller screens */
  }
}
</style>
