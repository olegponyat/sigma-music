<script setup>
import { ref } from 'vue';

const messages = ref([
  { sender: 'user', text: 'Hello!' },
  { sender: 'bot', text: 'Hi there! How can I help you today?' }
]);

const newMessage = ref('');
const addMessage = () => {
  if (newMessage.value.trim() !== '') {
    // Add user message
    messages.value.push({ sender: 'user', text: newMessage.value });

    // Add placeholder bot response
    setTimeout(() => {
      messages.value.push({ sender: 'bot', text: 'This is a placeholder response.' });
    }, 500); // Simulate a slight delay for the bot response

    newMessage.value = ''; // Clear input after sending
  }
};
</script>

<template>
  <div class="chat-container">
    <!-- Scrollable chat history -->
    <div class="chat-history">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="chat-bubble"
        :class="{ 'user-bubble': message.sender === 'user', 'bot-bubble': message.sender === 'bot' }"
      >
        {{ message.text }}
      </div>
    </div>

    <!-- Chat input box -->
    <div class="chat-box">
      <input
        type="text"
        v-model="newMessage"
        placeholder="Type a message"
        class="chat-input"
        @keydown.enter="addMessage"
      />
      <button class="send-button" @click="addMessage">↑</button>
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
  background-color: #f7f7f8; /* Matching color */
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