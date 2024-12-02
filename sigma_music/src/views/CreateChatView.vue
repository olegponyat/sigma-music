<template>
  <div class="chat-container">
    <div class="greeting">What can I help with?</div>
    
    <div class="chat-box">
      <input 
        type="text" 
        v-model="newMessage" 
        placeholder="Message ChatCBD" 
        class="chat-input" 
        @keydown.enter="navigateToChat" 
      />
      <button class="send-button" @click="navigateToChat">↑</button>
    </div>
    
    <div class="example-inputs">
      <button class="example-btn" @click="presetMessage('🤠 Country')">🤠 Country</button>
      <button class="example-btn" @click="presetMessage('🎧 Lo-fi')">🎧 Lo-fi</button>
      <button class="example-btn" @click="presetMessage('🎸 Rock')">🎸 Rock</button>
      <button class="example-btn" @click="presetMessage('🎤 Pop')">🎤 Pop</button>
      <button class="example-btn" @click="presetMessage('🎹 Synth')">🎹 Synth</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const newMessage = ref('');
const router = useRouter();

// Navigate to /chat with the message as a query parameter
const navigateToChat = () => {
  if (newMessage.value.trim()) {
    router.push({ name: 'chat', query: { message: newMessage.value } });
    newMessage.value = ''; // Clear the input field after navigating
  }
};

// Set a preset message and navigate to /chat
const presetMessage = (message) => {
  newMessage.value = message;
  navigateToChat();
};
</script>



<style scoped>
.example-btn:hover {
  background-color: #e0e0e0;
}
.example-inputs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  justify-content: center;
}
.greeting {
  font-size: 2.4rem;
  font-weight: 700;
  margin-bottom: 1.8rem;
  color: #333;
}
.status-dot {
  color: #2ecc71;
  font-size: 1.2rem;
}
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
.example-btn {
  background-color: #f1f1f1;
  border: none;
  border-radius: 18px;
  padding: 0.6rem 1.1rem;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  white-space: nowrap;
}
.chat-box {
  display: flex; /* Use flexbox to align items horizontally */
  align-items: center; /* Vertically center the elements */
  justify-content: space-between; /* Add space between the input and button */
  border: 1px solid #ddd;
  border-radius: 22px;
  padding: 0.5rem 1rem;
  background-color: #ffffff;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chat-input {
  flex-grow: 1; /* Make the input field take up remaining space */
  width: 700px;
  border: none;
  outline: none;
  font-weight: lighter;
  background: transparent;
  font-size: 1rem;
  font-family: 'Inter', sans-serif;
  color: #333;
  margin-right: 10px; /* Add some spacing between input and button */
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
  background-color: #555;
}

</style>
