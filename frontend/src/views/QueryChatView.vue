<script setup lang="ts">
import { ref } from 'vue';
import TextToSqlService from '@/services/TextToSqlService';
import type { QueryResults } from '@/interfaces/ApiResponse';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';

const userQuery = ref('');
const chatMessages = ref<Array<{ type: string; content: string }>>([]);
const isLoading = ref(false);

const sendQuery = async () => {
  if (!userQuery.value.trim()) return;

  if (!dbCredentialsStore.credentials) {
    chatMessages.value.push({
      type: 'bot',
      content: 'Database credentials are missing. Please configure the database connection first.'
    });
    return;
  }

  chatMessages.value.push({ type: 'user', content: userQuery.value });

  const loadingMessage = { type: 'bot', content: '<span class="loading-dots">Processing Query</span>' };
  chatMessages.value.push(loadingMessage);
  isLoading.value = true;

  try {
    const response: QueryResults = await TextToSqlService.processQuery(userQuery.value);

    if (!response || !response.header) {
      throw new Error('Invalid response from backend');
    }

    const index = chatMessages.value.indexOf(loadingMessage);
    if (index !== -1) {
      chatMessages.value.splice(index, 1);
    }

    const formattedHeader = response.header
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>');

    chatMessages.value.push({ type: 'bot', content: formattedHeader });

    if (response.sql_results) {
      try {
        const fixedJsonString = response.sql_results.replace(/'/g, '"');
        const sqlResults = JSON.parse(fixedJsonString);
        const columns = Object.keys(sqlResults[0]);

        const tableHeaders = columns.map(column => `<th>${column}</th>`).join('');
        const tableRows = sqlResults.map((row: Record<string, string|number|null>) => `<tr>${columns.map(column => `<td>${row[column]}</td>`).join('')}</tr>`).join('');

        const tableHTML = `
          <div class="sql-table-container">
            <table class="sql-table">
              <thead>
                <tr>${tableHeaders}</tr>
              </thead>
              <tbody>
                ${tableRows}
              </tbody>
            </table>
          </div>
        `;

        chatMessages.value.push({ type: 'bot', content: `SQL Results:<br>${tableHTML}` });
      } catch (error) {
        console.error(error);
        chatMessages.value.push({ type: 'bot', content: 'Error displaying SQL results.' });
      }
    }
  } catch (error) {
    console.error(error);
    const index = chatMessages.value.indexOf(loadingMessage);
    if (index !== -1) {
      chatMessages.value.splice(index, 1);
    }
    chatMessages.value.push({ type: 'bot', content: 'Error processing your query. Please try again.' });
  } finally {
    isLoading.value = false;
  }

  userQuery.value = '';
};
</script>

<template>
  <main class="container d-flex flex-column align-items-center" style="height: 90vh; margin-top: 20px;">
    <div class="chat-container w-100 d-flex flex-column" style="max-width: 800px; height: calc(90vh - 120px); overflow-y: auto;">
      <div v-for="(message, index) in chatMessages" :key="index" :class="['chat-message', message.type === 'user' ? 'user-message' : 'bot-message']">
        <div v-html="message.content"></div>
      </div>
    </div>

    <div class="input-group-container">
      <input v-model="userQuery" @keyup.enter="sendQuery" type="text" class="chat-input" placeholder="Type your message..." />
      <button @click="sendQuery" class="btn-custom-send">Send</button>
    </div>
  </main>
</template>

<style>
.chat-message {
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 80%;
  font-size: 1rem;
  line-height: 1.4;
  margin-bottom: 10px;
  position: relative;
  animation: fadeIn 0.3s ease-out;
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.sql-table-container {
  overflow-x: auto;
  margin-top: 10px;
}

.sql-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border: 1px solid #ddd;
}

.sql-table th,
.sql-table td {
  padding: 8px 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.sql-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.sql-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.sql-table tr:hover {
  background-color: #f1f1f1;
}

.chat-container::-webkit-scrollbar {
  width: 8px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #7b0779;
  border-radius: 4px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #5a055e;
}

.input-group-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 800px;
  margin-top: 20px;
  gap: 10px;
}

.chat-input {
  flex: 1;
  height: 50px;
  padding: 0 16px;
  border: 2px solid #7b0779;
  border-radius: 25px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.chat-input:focus {
  border-color: #a01fa0;
  outline: none;
}

.btn-custom-send {
  background: linear-gradient(135deg, #7b0779, #a01fa0);
  color: white;
  border: none;
  border-radius: 25px;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.3s;
}

.btn-custom-send:hover {
  background: linear-gradient(135deg, #a01fa0, #7b0779);
  transform: scale(1.05);
}

.btn-custom-send:active {
  transform: scale(0.95);
}

@keyframes dots {
  0% { content: '.'; }
  33% { content: '..'; }
  66% { content: '...'; }
}

.loading-dots::after {
  content: '...';
  display: inline-block;
  animation: dots 1.5s steps(3, end) infinite;
}

/* Modal de carga */
.loading-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
}
</style>
