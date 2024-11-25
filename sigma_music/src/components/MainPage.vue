<template>
  <div class="centered-container">
    <div ><em class="quote">"The future of music is right here"</em></div>
    <div class="create-chat">
      <router-link to="/create-chat">click here</router-link>
      <span> to create your first chat</span>
    </div>
  </div>
</template>

<script>

</script>

<style scoped>
.centered-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  position: relative;
}

.quote {
  font-size: 5rem;
  font-weight: bolder;
  margin-bottom: 1rem;
  position: relative;
  top: -10%;
}

.create-chat {
  font-size: 1rem;
}

.create-chat a {
  color: #007bff;
  text-decoration: none;
}

.create-chat a:hover {
  text-decoration: underline;
}
</style>
