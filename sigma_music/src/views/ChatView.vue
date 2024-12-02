<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const messages = ref([]);
const newMessage = ref('');
const isLoading = ref(false);
const route = useRoute();

const sendBotResponse = (userInput) => {
  messages.value.push({ sender: 'bot', text: 'Bot is typing...' });

  axios
    .post('http://localhost:5000/music', { description: userInput })
    .then((response) => {
      messages.value.pop();

      messages.value.push({
        sender: 'bot',
        audioUrl: `http://localhost:5000${response.data.audio_url}`,
        spectrogramUrl: `http://localhost:5000${response.data.spectrogram_url}`,
        visualLink: `http://localhost:5000${response.data.visual_url}`,
      });
    })
    .catch((error) => {
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
};


const addMessage = (initial = false) => {
  const userInput = initial ? newMessage.value : newMessage.value.trim();
  if (userInput !== '') {
    // Add user message
    messages.value.push({ sender: 'user', text: userInput });

    // Reset input if not initial message
    if (!initial) newMessage.value = '';

    // Set loading state and send bot response
    isLoading.value = true;
    sendBotResponse(userInput);
  }
};

onMounted(() => {
  // Check if there's a message in the query
  if (route.query.message) {
    newMessage.value = route.query.message;
    addMessage(true); // Auto-trigger with initial query
  }
});
</script>

<template>
  <div class="chat-container">
    <div class="chat-history">
    <div
      v-for="(message, index) in messages"
      :key="index"
      class="chat-bubble"
      :class="{
        'user-bubble': message.sender === 'user',
        'bot-bubble': message.sender === 'bot',
      }"
    >
      <template v-if="!message.audioUrl">
        {{ message.text }}
      </template>
      <template v-else>
        <audio :src="message.audioUrl" controls></audio>
        <img :src="message.spectrogramUrl" alt="Spectrogram" />
        <a v-if="message.visualLink" :href="message.visualLink" target="_blank">View Visualization</a>
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
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #ffffff;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  text-align: center;
}

.chat-history {
  width: 100%;
  max-width: 1200px;
  height: 85vh;
  overflow-y: auto;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.chat-bubble {
  padding: 10px 15px;
  border-radius: 20px;
  font-size: 16px;
  margin-bottom: 15px;
  max-width: fit-content; /* Ensure bubble width adjusts to content */
  min-width: 100px; /* Prevent very narrow bubbles */
  line-height: 1.5;
  word-wrap: break-word;
  color: #000;
}

.user-bubble {
  margin-left: auto;
  background-color: #e1e2e1;
}

.bot-bubble {
  margin-right: auto;
  background-color: #d4f1f4; /* Light blue color for distinction */
  color: #002333; /* Dark text for better readability */
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
  flex-grow: 1;
  width: 700px;
  border: none;
  outline: none;
  background: transparent;
  font-size: 1rem;
  color: #333;
  margin-right: 10px;
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
  background-color: #555;
}

@media (max-width: 768px) {
  .chat-box {
    max-width: 90%;
    padding: 0.4rem 0.8rem;
  }

  .chat-history {
    max-width: 90%;
    height: 60vh;
  }
}
</style>
