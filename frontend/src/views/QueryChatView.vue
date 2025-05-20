<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router';
import TextToSqlService from '@/services/TextToSqlService';
import type { QueryResults, ChatData } from '@/interfaces/ApiResponse';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import { userStore } from '@/store/userStore';

const { t, locale } = useI18n()

const route = useRoute();
const router = useRouter();

const userQuery = ref('');
const chatMessages = ref<Array<{ type: string; content: string }>>([]);
const isLoading = ref(false);
const currentChatId = ref<string | null>(null);
const userChats = ref<any[]>([]);
const isEditingTitle = ref(false);
const editedTitle = ref('');
const editingChatId = ref<string | null>(null);
const showDeleteModal = ref(false);
const chatToDelete = ref<string | null>(null);

onMounted(async () => {
  if (route.params.chatId) {
    currentChatId.value = route.params.chatId as string;
    await loadChatHistory(currentChatId.value);
  } else {
    const shouldCreateNewChat = localStorage.getItem('createNewChat') === 'true';

    if (shouldCreateNewChat) {
      // Clear the flag
      localStorage.removeItem('createNewChat');
      // Leave currentChatId as null to create a new chat when user sends a query
    } else {
      // Load existing chats and select the most recent one
      await loadChats();
      if (userChats.value.length > 0) {
        const mostRecentChat = userChats.value[0];
        const chatId = mostRecentChat.chat_id || mostRecentChat.id;
        currentChatId.value = chatId;
        router.push(`/chat/${chatId}`);
        await loadChatHistory(chatId);
      }
    }
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

    const response = await TextToSqlService.processQuery('', chatData, 'list_only');

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
          let tableTitle = t('message.query.results');
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
      content: t('message.database.credentialsMissing')
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
        content: `${t('message.ui.errorLoadingChat')}: ${error.message || t('message.ui.unknownError')}`
      });
    }

  } catch (error) {
    chatMessages.value.push({
      type: 'bot',
      content: t('message.ui.errorLoadingHistory')
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

  // Set a flag to indicate we want to create a new chat
  localStorage.setItem('createNewChat', 'true');
}

async function deleteChat(chatId: string, event: Event) {
  event.stopPropagation();

  chatToDelete.value = chatId;
  showDeleteModal.value = true;
}

async function confirmDeleteChat() {
  if (!chatToDelete.value) return;

  try {
    isLoading.value = true;
    await TextToSqlService.deleteChat(chatToDelete.value);

    userChats.value = userChats.value.filter(chat =>
      (chat.chat_id || chat.id) !== chatToDelete.value
    );

    if (currentChatId.value === chatToDelete.value) {
      currentChatId.value = null;
      chatMessages.value = [];
      router.push('/chat');
    }
  } catch (error: any) {
    alert(`${t('message.ui.errorDeletingChat')}: ${error.message || t('message.ui.unknownError')}`);
  } finally {
    isLoading.value = false;
    showDeleteModal.value = false;
    chatToDelete.value = null;
  }
}

function cancelDeleteChat() {
  showDeleteModal.value = false;
  chatToDelete.value = null;
}

function startEditingTitle(chatId: string, currentTitle: string, event: Event) {
  event.stopPropagation();
  editingChatId.value = chatId;
  editedTitle.value = currentTitle.startsWith('Chat ') ? '' : currentTitle;
  isEditingTitle.value = true;

  setTimeout(() => {
    const input = document.getElementById('edit-title-input');
    if (input) {
      input.focus();
    }
  }, 50);
}

async function saveChatTitle(chatId: string, event: Event) {
  event.stopPropagation();

  if (!editedTitle.value.trim()) {
    cancelEditingTitle(event);
    return;
  }

  try {
    isLoading.value = true;
    await TextToSqlService.renameChat(chatId, editedTitle.value.trim());

    // Update chat title in the list
    const chatIndex = userChats.value.findIndex(chat =>
      (chat.chat_id || chat.id) === chatId
    );

    if (chatIndex !== -1) {
      userChats.value[chatIndex].title = editedTitle.value.trim();
    }

  } catch (error: any) {
    alert(`${t('message.ui.errorRenamingChat')}: ${error.message || t('message.ui.unknownError')}`);
  } finally {
    isEditingTitle.value = false;
    editingChatId.value = null;
    isLoading.value = false;
  }
}

function cancelEditingTitle(event: Event) {
  event.stopPropagation();
  isEditingTitle.value = false;
  editingChatId.value = null;
}

const sendQuery = async () => {
  if (!userQuery.value.trim()) return

  if (!dbCredentialsStore.credentials) {
    chatMessages.value.push({
      type: 'bot',
      content: t('message.database.credentialsMissing')
    })
    return
  }

  // If we don't have a chat ID and this is the first message, we should create a new chat
  const isFirstMessageInNewChat = !currentChatId.value && chatMessages.value.length === 0;

  chatMessages.value.push({ type: 'user', content: userQuery.value })

  const loadingMessage = {
    type: 'bot',
    content: `<span class="loading-dots">${t('message.query.processing')}</span>`
  }
  chatMessages.value.push(loadingMessage)
  isLoading.value = true

  try {
    const chatData: ChatData = {
      user_id: userStore.user?.id || '',
      messages: chatMessages.value.map(message => ({
        role: message.type === 'user' ? 1 : 0,
        message: message.content,
        timestamp: new Date().toISOString()
      }))
    };

    // If this is the first message in a new chat, let's create a chat
    const chatToUse = isFirstMessageInNewChat ? null : currentChatId.value;

    const response: QueryResults = await TextToSqlService.processQuery(
      userQuery.value,
      chatData,
      chatToUse
    );

    if (!currentChatId.value && response.chat_id) {
      currentChatId.value = response.chat_id;
      router.push(`/chat/${currentChatId.value}`);
    }

    if (!response || !response.header) {
      throw new Error('Invalid response from backend')
    }

    const index = chatMessages.value.indexOf(loadingMessage)
    if (index !== -1) {
      chatMessages.value.splice(index, 1)
    }

    await formatBotResponse(response);

    if (response.chats) {
      userChats.value = response.chats;
    }

  } catch (error) {
    console.error(error)
    const index = chatMessages.value.indexOf(loadingMessage)
    if (index !== -1) {
      chatMessages.value.splice(index, 1)
    }
    chatMessages.value.push({
      type: 'bot',
      content: t('message.query.error')
    })
  } finally {
    isLoading.value = false
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
          let tableTitle = t('message.query.results');
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
        let tableTitle = t('message.ui.queryResults');

        if (response.sql_query) {
          const queryMatch = response.sql_query.match(/SELECT\s+(.*?)\s+FROM/i);
          if (queryMatch && queryMatch[1]) {
            if (queryMatch[1].includes('*')) {
              const tableMatch = response.sql_query.match(/FROM\s+(\w+)/i);
              if (tableMatch && tableMatch[1]) {
                tableTitle = `${t('message.ui.dataFrom')} ${tableMatch[1]}`;
              }
            } else {
              const fields = queryMatch[1].split(',').map(f => f.trim());
              if (fields.length > 2) {
                tableTitle = `${t('message.ui.selectedFields')} (${fields.length})`;
              } else {
                tableTitle = queryMatch[1].substring(0, 40);
                if (queryMatch[1].length > 40) tableTitle += '...';
              }
            }
          }
        }

        addSqlResultsTable(sqlResults, tableTitle);
      } else {
        chatMessages.value.push({ type: 'bot', content: t('message.ui.noResultsFound') });
      }
    } catch (error) {
      chatMessages.value.push({ type: 'bot', content: t('message.ui.errorDisplayingResults') });
    }
  }
}

function addSqlResultsTable(data: any[], title: string = t('message.query.results')): void {
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
        formattedValue = `<span class="null-value">${t('message.ui.null')}</span>`;
      } else if (typeof value === 'number') {
        formattedValue = Number.isInteger(value)
          ? value.toLocaleString()
          : value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      } else if (typeof value === 'boolean') {
        formattedValue = value ? t('message.ui.true') : t('message.ui.false');
      } else {
        formattedValue = String(value);
      }

      return `<td>${formattedValue}</td>`;
    }).join('')}</tr>`
  ).join('');

  const rowCount = t('message.ui.rowReturned', data.length);

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
      <div class="sql-results-info">${data.length} ${rowCount}</div>
    </div>
  `;

  chatMessages.value.push({ type: 'bot', content: tableHTML });
}

// Language switcher function
const changeLanguage = (lang: 'en' | 'es') => {
  locale.value = lang
  localStorage.setItem('userLanguage', lang)
}
</script>

<template>
  <main class="container d-flex" style="height: 90vh; margin-top: 20px;">
    <div class="chat-sidebar">
      <div class="chat-sidebar-header">
        <h3>{{ t('message.ui.yourChats') }}</h3>
        <button @click="createNewChat" class="btn-new-chat">
          <i class="fas fa-plus"></i> {{ t('message.ui.newChat') }}
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
          <div class="chat-content">
            <div v-if="isEditingTitle && editingChatId === (chat.chat_id || chat.id)" class="chat-title-edit">
              <input
                id="edit-title-input"
                v-model="editedTitle"
                @keyup.enter="saveChatTitle(chat.chat_id || chat.id, $event)"
                @keyup.esc="cancelEditingTitle($event)"
                class="title-input"
                type="text"
                :placeholder="t('message.ui.enterTitle')"
              />
              <div class="edit-actions">
                <button class="btn-icon" @click="saveChatTitle(chat.chat_id || chat.id, $event)">
                  <i class="fas fa-check"></i>
                </button>
                <button class="btn-icon" @click="cancelEditingTitle($event)">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
            <div v-else>
              <div class="chat-title">
                {{ chat.title || t('message.ui.chatPrefix') + ' ' + (chat.chat_id || chat.id)?.substring(0, 8) }}
              </div>
              <div class="chat-preview">
                {{ chat.title ?
                  t('message.ui.clickToView') :
                  t('message.ui.untitledChat') }}
              </div>
            </div>
          </div>

          <div v-if="!isEditingTitle || editingChatId !== (chat.chat_id || chat.id)" class="chat-actions">
            <button class="btn-icon" @click="startEditingTitle(chat.chat_id || chat.id, chat.title || 'Chat ' + (chat.chat_id || chat.id)?.substring(0, 8), $event)">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon" @click="deleteChat(chat.chat_id || chat.id, $event)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>

        <div v-if="userChats.length === 0" class="no-chats">
          {{ t('message.ui.noChats') }}
        </div>
      </div>
    </div>

    <div class="chat-main">
      <div class="chat-container w-100 d-flex flex-column">
        <div v-if="isLoading && chatMessages.length === 0" class="loading-message">
          {{ t('message.ui.loadingHistory') }}
        </div>

        <div v-else-if="chatMessages.length === 0" class="empty-chat">
          <div class="empty-chat-message">
            {{ t('message.ui.startConversation') }}
          </div>
        </div>

        <div v-for="(message, index) in chatMessages" :key="index" :class="['chat-message', message.type === 'user' ? 'user-message' : 'bot-message']">
          <div v-html="message.content"></div>
        </div>
      </div>

      <div class="input-group-container">
        <input v-model="userQuery" @keyup.enter="sendQuery" type="text" class="chat-input" :placeholder="t('message.ui.placeholder')" />
        <button @click="sendQuery" class="btn-custom-send">{{ t('message.ui.send') }}</button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="delete-modal-overlay">
      <div class="delete-modal">
        <div class="delete-modal-header">
          <h4>{{ t('message.ui.confirmDelete') }}</h4>
        </div>
        <div class="delete-modal-body">
          <p>{{ t('message.ui.deleteConfirmation') }}</p>
          <p class="delete-warning">{{ t('message.ui.deleteWarning') }}</p>
        </div>
        <div class="delete-modal-footer">
          <button @click="cancelDeleteChat" class="btn-cancel">{{ t('message.ui.cancel') }}</button>
          <button @click="confirmDeleteChat" class="btn-delete">{{ t('message.ui.delete') }}</button>
        </div>
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

.language-switcher {
  display: flex;
  gap: 10px;
}

.language-switcher button {
  padding: 5px 10px;
  border: 1px solid #7b0779;
  border-radius: 5px;
  background: white;
  color: #7b0779;
  cursor: pointer;
  transition: all 0.3s;
}

.language-switcher button.active {
  background: #7b0779;
  color: white;
}

.language-switcher button:hover {
  background: #a01fa0;
  color: white;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-item:hover {
  background-color: #f5f5f5;
}

.chat-item.active {
  background-color: #f0e6f0;
  border-left: 3px solid #7b0779;
}

.chat-content {
  flex: 1;
  overflow: hidden;
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

.chat-actions {
  display: none;
  margin-left: 8px;
}

.chat-item:hover .chat-actions {
  display: flex;
}

.btn-icon {
  background: none;
  border: none;
  color: #666;
  font-size: 14px;
  padding: 2px 5px;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-icon:hover {
  color: #7b0779;
}

.chat-title-edit {
  display: flex;
  align-items: center;
  width: 100%;
}

.title-input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 14px;
  color: #333;
}

.edit-actions {
  display: flex;
  margin-left: 5px;
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

/* Delete Modal Styles */
.delete-modal-overlay {
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
  animation: fadeIn 0.2s ease-out;
}

.delete-modal {
  background: white;
  border-radius: 12px;
  width: 400px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: modalSlideIn 0.3s ease-out;
}

.delete-modal-header {
  background: linear-gradient(135deg, #7b0779, #a01fa0);
  color: white;
  padding: 15px 20px;
}

.delete-modal-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.delete-modal-body {
  padding: 20px;
  color: #333;
}

.delete-warning {
  color: #d9534f;
  font-size: 14px;
  margin-top: 10px;
}

.delete-modal-footer {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #eee;
}

.btn-cancel {
  background: #f5f5f5;
  color: #333;
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-cancel:hover {
  background: #e5e5e5;
}

.btn-delete {
  background: linear-gradient(135deg, #d9534f, #c9302c);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: 500;
  transition: transform 0.2s;
}

.btn-delete:hover {
  transform: scale(1.05);
}

@keyframes modalSlideIn {
  from { transform: translateY(-50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
