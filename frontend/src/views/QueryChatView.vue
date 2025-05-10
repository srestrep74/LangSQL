<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TextToSqlService from '@/services/TextToSqlService';
import type { QueryResults, ChatData } from '@/interfaces/ApiResponse';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import { userStore } from '@/store/userStore';

const route = useRoute();
const router = useRouter();

const userQuery = ref('');
const chatMessages = ref<Array<{ type: string; content: string }>>([]);
const isLoading = ref(false);
const currentChatId = ref<string | null>(null);
const userChats = ref<any[]>([]);

onMounted(async () => {
  if (route.params.chatId) {
    currentChatId.value = route.params.chatId as string;
    await loadChatHistory(currentChatId.value);
  } else {
    await loadChats();
  }
});

watch(() => route.params.chatId, async (newChatId) => {
  if (newChatId) {
    currentChatId.value = newChatId as string;
    await loadChatHistory(currentChatId.value);
  }
});

async function loadChats() {
  if (!dbCredentialsStore.credentials) return;

  try {
    const chatData: ChatData = {
      user_id: userStore.user?.id || '',
      messages: []
    };

    const response = await TextToSqlService.processQuery('', chatData);

    if (response && response.chats) {
      userChats.value = response.chats;
    } else {
      userChats.value = [];
    }
  } catch (error) {
    userChats.value = [];
  }
}

function processBotMessage(message: string): void {
  if (message.includes('[{') && message.includes('}]')) {
    const parts = message.split(/(\[{.*}\])/);
    if (parts.length >= 3) {
      const headerText = parts[0].trim();
      if (headerText) {
        chatMessages.value.push({
          type: 'bot',
          content: headerText.replace(/\n/g, '<br>')
        });
      }

      try {
        const jsonText = parts[1];
        const extractedData = JSON.parse(jsonText.replace(/'/g, '"'));
        if (Array.isArray(extractedData) && extractedData.length > 0) {
          let tableTitle = 'SQL Results';
          if (headerText) {
            tableTitle = headerText.replace(/\:$/, '').trim();
          }
          addSqlResultsTable(extractedData, tableTitle);
        }
      } catch (parseError) {
        chatMessages.value.push({
          type: 'bot',
          content: message.replace(/\n/g, '<br>')
        });
      }
    } else {
      chatMessages.value.push({
        type: 'bot',
        content: message.replace(/\n/g, '<br>')
      });
    }
  } else {
    chatMessages.value.push({
      type: 'bot',
      content: message.replace(/\n/g, '<br>')
    });
  }
}

async function loadChatHistory(chatId: string) {
  if (!dbCredentialsStore.credentials) {
    chatMessages.value = [{
      type: 'bot',
      content: 'Database credentials are missing. Please configure the database connection first.'
    }];
    return;
  }

  try {
    isLoading.value = true;
    chatMessages.value = [];

    const chatData: ChatData = {
      user_id: userStore.user?.id || '',
      messages: []
    };

    try {
      const response = await TextToSqlService.processQuery('', chatData, chatId);

      if (response && response.messages) {
        for (const msg of response.messages) {
          if (msg.role === 1) {
            chatMessages.value.push({
              type: 'user',
              content: msg.message
            });
          } else {
            processBotMessage(msg.message);
          }
        }

        if (response.chats) {
          userChats.value = response.chats;
        }
      } else {
        chatMessages.value = [];
      }
    } catch (error: any) {
      if (error.message && error.message.includes("no attribute 'messages'")) {
        currentChatId.value = null;
        chatMessages.value = [];
        router.push('/chat');
        return;
      }

      chatMessages.value.push({
        type: 'bot',
        content: `Error loading chat: ${error.message || 'Unknown error'}`
      });
    }

  } catch (error) {
    chatMessages.value.push({
      type: 'bot',
      content: 'Error loading chat history. Please try again.'
    });
  } finally {
    isLoading.value = false;
  }
}

function selectChat(chatId: string) {
  router.push(`/chat/${chatId}`);
}

function createNewChat() {
  currentChatId.value = null;
  chatMessages.value = [];
  router.push('/chat');
}

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
    const chatData: ChatData = {
      user_id: userStore.user?.id || '',
      messages: chatMessages.value.map(message => ({
        role: message.type === 'user' ? 1 : 0,
        message: message.content,
        timestamp: new Date().toISOString()
      }))
    };

    const response: QueryResults = await TextToSqlService.processQuery(
      userQuery.value,
      chatData,
      currentChatId.value
    );

    if (!currentChatId.value && response.chat_id) {
      currentChatId.value = response.chat_id;
      router.push(`/chat/${currentChatId.value}`);
    }

    if (!response || !response.header) {
      throw new Error('Invalid response from backend');
    }

    const index = chatMessages.value.indexOf(loadingMessage);
    if (index !== -1) {
      chatMessages.value.splice(index, 1);
    }

    await formatBotResponse(response);

    if (response.chats) {
      userChats.value = response.chats;
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

async function formatBotResponse(response: QueryResults): Promise<void> {
  if (response.header) {
    const formattedHeader = response.header
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>');

    const arrayPattern = /\[(.*)\]/;
    const match = formattedHeader.match(arrayPattern);

    if (match && match[0].includes('{') && match[0].includes('}')) {
      try {
        let jsonText = match[0];
        const extractedData = JSON.parse(jsonText.replace(/'/g, '"'));

        if (Array.isArray(extractedData) && extractedData.length > 0) {
          const cleanHeader = formattedHeader.replace(jsonText, '').trim();
          let tableTitle = 'SQL Results';
          if (cleanHeader) {
            tableTitle = cleanHeader.replace(/\:$/, '').trim();
          }
          if (cleanHeader && !cleanHeader.endsWith('<br>')) {
            chatMessages.value.push({ type: 'bot', content: cleanHeader });
          }
          addSqlResultsTable(extractedData, tableTitle);
          return;
        }
      } catch (error) {}
    }

    chatMessages.value.push({ type: 'bot', content: formattedHeader });
  }

  if (response.sql_results) {
    try {
      let sqlResults;

      if (typeof response.sql_results === 'string') {
        try {
          const fixedJsonString = response.sql_results.replace(/'/g, '"');
          sqlResults = JSON.parse(fixedJsonString);
        } catch (parseError) {
          sqlResults = [];
        }
      } else if (Array.isArray(response.sql_results)) {
        sqlResults = response.sql_results;
      } else {
        sqlResults = [];
      }

      if (Array.isArray(sqlResults) && sqlResults.length > 0) {
        let tableTitle = 'Query Results';

        if (response.sql_query) {
          const queryMatch = response.sql_query.match(/SELECT\s+(.*?)\s+FROM/i);
          if (queryMatch && queryMatch[1]) {
            if (queryMatch[1].includes('*')) {
              const tableMatch = response.sql_query.match(/FROM\s+(\w+)/i);
              if (tableMatch && tableMatch[1]) {
                tableTitle = `Data from ${tableMatch[1]}`;
              }
            } else {
              const fields = queryMatch[1].split(',').map(f => f.trim());
              if (fields.length > 2) {
                tableTitle = `Selected Fields (${fields.length})`;
              } else {
                tableTitle = queryMatch[1].substring(0, 40);
                if (queryMatch[1].length > 40) tableTitle += '...';
              }
            }
          }
        }

        addSqlResultsTable(sqlResults, tableTitle);
      } else {
        chatMessages.value.push({ type: 'bot', content: 'No results found in the query.' });
      }
    } catch (error) {
      chatMessages.value.push({ type: 'bot', content: 'Error displaying SQL results.' });
    }
  }
}

function addSqlResultsTable(data: any[], title: string = 'SQL Results'): void {
  if (!Array.isArray(data) || data.length === 0) return;

  const columns = Object.keys(data[0]);

  const tableHeaders = columns.map(column => {
    const formattedHeader = column
      .replace(/_/g, ' ')
      .replace(/\b\w/g, char => char.toUpperCase());
    return `<th>${formattedHeader}</th>`;
  }).join('');

  const tableRows = data.map((row: Record<string, any>) =>
    `<tr>${columns.map(column => {
      const value = row[column];
      let formattedValue: string;

      if (value === null) {
        formattedValue = '<span class="null-value">NULL</span>';
      } else if (typeof value === 'number') {
        formattedValue = Number.isInteger(value)
          ? value.toLocaleString()
          : value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      } else if (typeof value === 'boolean') {
        formattedValue = value ? 'True' : 'False';
      } else {
        formattedValue = String(value);
      }

      return `<td>${formattedValue}</td>`;
    }).join('')}</tr>`
  ).join('');

  const tableHTML = `
    <div class="sql-results-section">
      <div class="sql-results-title">${title}</div>
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
      <div class="sql-results-info">${data.length} row${data.length !== 1 ? 's' : ''} returned</div>
    </div>
  `;

  chatMessages.value.push({ type: 'bot', content: tableHTML });
}
</script>

<template>
  <main class="container d-flex" style="height: 90vh; margin-top: 20px;">
    <div class="chat-sidebar">
      <div class="chat-sidebar-header">
        <h3>Your Chats</h3>
        <button @click="createNewChat" class="btn-new-chat">
          <i class="fas fa-plus"></i> New Chat
        </button>
      </div>

      <div class="chat-list">
        <div
          v-for="chat in userChats"
          :key="chat.chat_id || chat.id"
          class="chat-item"
          :class="{ 'active': currentChatId === (chat.chat_id || chat.id) }"
          @click="selectChat(chat.chat_id || chat.id)"
        >
          <div class="chat-title">
            {{ chat.title || 'Chat ' + (chat.chat_id || chat.id)?.substring(0, 8) }}
          </div>
          <div class="chat-preview">
            {{ chat.messages && chat.messages.length > 0 ?
               chat.messages[chat.messages.length - 1].message.substring(0, 30) + '...' :
               'No messages' }}
          </div>
        </div>

        <div v-if="userChats.length === 0" class="no-chats">
          No chats yet. Start a new conversation!
        </div>
      </div>
    </div>

    <div class="chat-main">
      <div class="chat-container w-100 d-flex flex-column">
        <div v-if="isLoading && chatMessages.length === 0" class="loading-message">
          Loading chat history...
        </div>

        <div v-else-if="chatMessages.length === 0" class="empty-chat">
          <div class="empty-chat-message">
            Start a new conversation by typing a question below
          </div>
        </div>

        <div v-for="(message, index) in chatMessages" :key="index" :class="['chat-message', message.type === 'user' ? 'user-message' : 'bot-message']">
          <div v-html="message.content"></div>
        </div>
      </div>

      <div class="input-group-container">
        <input v-model="userQuery" @keyup.enter="sendQuery" type="text" class="chat-input" placeholder="Type your message..." />
        <button @click="sendQuery" class="btn-custom-send">Send</button>
      </div>
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

.container {
  gap: 20px;
  padding: 0 15px;
  max-width: 1400px;
}

.chat-sidebar {
  width: 280px;
  border-right: 1px solid #ddd;
  padding-right: 15px;
  display: flex;
  flex-direction: column;
}

.chat-sidebar-header {
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.btn-new-chat {
  background: #7b0779;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 5px 10px;
  font-size: 12px;
  cursor: pointer;
}

.chat-list {
  overflow-y: auto;
  flex: 1;
}

.chat-item {
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-item:hover {
  background-color: #f5f5f5;
}

.chat-item.active {
  background-color: #f0e6f0;
  border-left: 3px solid #7b0779;
}

.chat-title {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.chat-preview {
  font-size: 12px;
  color: #777;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-chats {
  text-align: center;
  color: #777;
  padding: 20px 0;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: calc(100% - 300px);
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

.empty-chat {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.empty-chat-message {
  color: #777;
  text-align: center;
  font-size: 18px;
}

.loading-message {
  text-align: center;
  color: #777;
  padding: 20px;
}

.sql-table-container {
  overflow-x: auto;
  margin-top: 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.sql-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
  border-radius: 8px;
  overflow: hidden;
}

.sql-table th {
  background: linear-gradient(135deg, #7b0779, #a01fa0);
  color: white;
  font-weight: 600;
  text-align: left;
  padding: 12px 15px;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
}

.sql-table th:first-child {
  border-top-left-radius: 8px;
}

.sql-table th:last-child {
  border-top-right-radius: 8px;
}

.sql-table td {
  padding: 10px 15px;
  border-bottom: 1px solid #efefef;
  color: #333;
}

.sql-table tr:nth-child(even) {
  background-color: #f9f4f9;
}

.sql-table tr:hover {
  background-color: #f0e6f0;
  transition: background-color 0.2s ease;
}

.sql-table tr:last-child td {
  border-bottom: none;
}

.sql-table tr:last-child td:first-child {
  border-bottom-left-radius: 8px;
}

.sql-table tr:last-child td:last-child {
  border-bottom-right-radius: 8px;
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
  margin-top: 20px;
  margin-bottom: 20px;
  gap: 10px;
  padding: 0 15px;
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

.sql-results-section {
  margin: 20px 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.sql-results-title {
  background: linear-gradient(135deg, #7b0779, #a01fa0);
  color: white;
  padding: 12px 16px;
  font-weight: bold;
  font-size: 16px;
  letter-spacing: 0.5px;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  display: flex;
  align-items: center;
}

.sql-results-title::before {
  content: '📊';
  margin-right: 10px;
  font-size: 18px;
}

.sql-results-info {
  padding: 8px 16px;
  color: #666;
  font-size: 12px;
  text-align: right;
  background-color: #f9f4f9;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.null-value {
  color: #999;
  font-style: italic;
}
</style>