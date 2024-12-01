<script setup>
import { ref } from 'vue';
import axios from 'axios';

const messages = ref([]);
const newMessage = ref('');
const isLoading = ref(false);

const addMessage = () => {
  const userInput = newMessage.value.trim();
  if (userInput !== '') {
    // Add user message
    messages.value.push({ sender: 'user', text: userInput });

    // Clear input and set loading state
    newMessage.value = '';
    isLoading.value = true;

    // Add "bot is typing" indicator
    messages.value.push({ sender: 'bot', text: 'Bot is typing...' });

    // Send the message to Flask server
    axios
      .post('http://localhost:5000/music', { description: userInput })
      .then((response) => {
        // Remove "bot is typing" message
        messages.value.pop();
        console.log(response.data)

        // Add bot's audio response only after both URLs are available
        messages.value.push({
          sender: 'bot',
          audioUrl: response.data.audio_url, // Add audio URL as a message
          spectrogramUrl: response.data.spectrogram_url, // Add spectrogram URL as a message
        });

      })
      .catch((error) => {
        // Remove "bot is typing" message
        messages.value.pop();

        messages.value.push({
          sender: 'bot',
          text: `Error generating music. ${error.response?.data?.message || 'Please try again.'}`,
        });
        console.error('Error:', error);
      })
      .finally(() => {
        isLoading.value = false;
      });
  }
};
</script>

<template>
  <div class="chat-container">
    <div class="chat-history">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="chat-bubble"
        :class="{ 'user-bubble': message.sender === 'user', 'bot-bubble': message.sender === 'bot' }"
      >
        <!-- Display message text if no audio URL -->
        <template v-if="!message.audioUrl">
          {{ message.text }}
        </template>

        <!-- Render audio player and spectrogram if URLs exist -->
        <template v-else>
          <audio :src="message.audioUrl" controls></audio>
          <img :src="message.spectrogramUrl" alt="Spectrogram" />
        </template>
      </div>
    </div>

    <div class="chat-box">
      <input
        type="text"
        v-model="newMessage"
        placeholder="Type a message"
        class="chat-input"
        :disabled="isLoading"
        @keydown.enter="addMessage"
      />
      <button class="send-button" @click="addMessage" :disabled="isLoading">
        ↑
      </button>
    </div>
  </div>
</template>

<style>
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
  background-color: #f7f7f8; /* Matching color to chat box */
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
  background-color: #f1f1f1; /* Neutral background color */
  color: #000; /* Black font color */
}

.user-bubble {
  margin-left: auto; /* Align user messages to the right */
  background-color: #e1e2e1; /* Light blue for user messages */
}

.bot-bubble {
  margin-right: auto; /* Align bot messages to the left */
  background-color: #e1e2e1; /* Light gray for bot messages */
}

.chat-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 700px; /* Same width as chat history */
  border: 1px solid #ddd;
  border-radius: 22px;
  padding: 0.5rem 1rem;
  background-color: #ffffff; /* Matching color */
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px
}

.chat-input {
  border: none;
  flex-grow: 1;
  outline: none;
  font-weight: lighter;
  background: transparent;
  font-size: 1rem;
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
  font-size: 1.4rem;
  cursor: pointer;
  padding: 0.4rem;
  border-radius: 50%;
  font-family: 'Inter', sans-serif;
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
