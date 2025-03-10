<script setup lang="ts">
import { ref } from 'vue';
import TextToSqlService from '@/services/TextToSqlService';

const userQuery = ref('');
const chatMessages = ref<Array<{ type: string; content: string }>>([]);

const sendQuery = async () => {
  if (!userQuery.value.trim()) return;

  chatMessages.value.push({ type: 'user', content: userQuery.value });

  try {
    const response = await TextToSqlService.proccessQuery(userQuery.value);

    if (!response || !response.header) {
      throw new Error('Invalid response from backend');
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
        const tableRows = sqlResults.map((row: Record<string, any>) => `<tr>${columns.map(column => `<td>${row[column]}</td>`).join('')}</tr>`).join('');

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
        chatMessages.value.push({ type: 'bot', content: 'Error displaying SQL results.' });
      }
    }
  } catch (error) {
    chatMessages.value.push({ type: 'bot', content: 'Error processing your query. Please try again.' });
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
    <div class="input-group w-100 position-relative" style="max-width: 800px; margin-top: 20px;">
      <input v-model="userQuery" @keyup.enter="sendQuery" type="text" class="form-control rounded-pill ps-4 pe-5" placeholder="Type your message..." style="border: 2px solid #7b0779; height: 50px;">
      <button @click="sendQuery" class="btn btn-custom-purple position-absolute end-0 me-2 top-50 translate-middle-y px-4 rounded-pill">Send</button>
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
</style>