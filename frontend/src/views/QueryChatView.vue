<script setup lang="ts">
import { ref } from 'vue';

const userQuery = ref('');
</script>

<template>
  <main class="flex-grow-1 container py-5 d-flex flex-column align-items-center">
    
    <div class="chat-container w-100 d-flex flex-column" style="max-width: 600px; height: 400px; overflow-y: auto;">
      <div class="chat-message user-message">Hello! How can I help you?</div>
      <div class="chat-message bot-message">I'm looking for information on SQL queries.</div>
    </div>
    <div class="input-group mt-auto w-100 position-relative" style="max-width: 600px;">
      <input v-model="userQuery" type="text" class="form-control rounded-pill ps-4 pe-5" placeholder="Type your message..." style="border: 2px solid #7b0779; height: 50px;">
      <button class="btn btn-custom-purple position-absolute end-0 me-2 top-50 translate-middle-y px-4 rounded-pill">Send</button>
    </div>
  </main>
</template>

<style>
.bg-light-gray {
  background-color: #f4f4f4;
}

.text-custom-purple {
  color: #7b0779 !important;
}

.btn-custom-purple {
  background: linear-gradient(135deg, #7b0779, #5a055e);
  color: white;
  border: none;
  transition: all 0.3s ease-in-out;
}

.btn-custom-purple:hover {
  background: linear-gradient(135deg, #5a055e, #3a0340);
  transform: scale(1.05);
}

.input-group input {
  font-size: 1rem;
  transition: all 0.3s ease-in-out;
}

.input-group input:focus {
  border-color: #5a055e;
  box-shadow: 0px 0px 10px rgba(123, 7, 121, 0.5);
}

.chat-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  background-color: #fff;
  border-radius: 12px; border: none;
  
}

.chat-message {
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 80%;
  font-size: 1rem;
  line-height: 1.4;
}

.user-message {
  align-self: flex-end;
  background: linear-gradient(135deg, #7b0779, #5a055e);
  color: white;
}

.bot-message {
  align-self: flex-start;
  background: #eaeaea;
  color: #333;
}
</style>
