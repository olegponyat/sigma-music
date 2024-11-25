<template>
  <div class="centered-container">
    <div class="quote">"The future of music is right here"</div>
    <div class="create-chat">
      <router-link to="/create-chat">click here to create your first chat</router-link>
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
  font-size: 1.5rem;
  margin-bottom: 1rem;
  position: relative;
  top: -10%;
}

.create-chat a {
  font-size: 1rem;
  color: #007bff;
  text-decoration: none;
}

.create-chat a:hover {
  text-decoration: underline;
}
</style>
