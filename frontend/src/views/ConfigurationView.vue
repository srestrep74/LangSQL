<script setup lang="ts">
</script>

<template>
  <main class="container-fluid d-flex justify-content-center align-items-center vh-100">
    <section class="config-panel p-5 rounded shadow-lg animate-fade-in">
      <h2 class="text-white text-center mb-4">Database Configuration</h2>
      <form>
        <div class="mb-3">
          <label for="dbType" class="form-label text-white">Database Type</label>
          <select class="form-select" id="dbType">
            <option value="mysql">MySQL</option>
            <option value="postgresql">PostgreSQL</option>
            <option value="sqlite">SQLite</option>
            <option value="mongodb">MongoDB</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="host" class="form-label text-white">Host</label>
          <input type="text" class="form-control" id="host" placeholder="e.g., localhost">
        </div>
        <div class="mb-3">
          <label for="port" class="form-label text-white">Port</label>
          <input type="number" class="form-control" id="port" placeholder="e.g., 5432">
        </div>
        <div class="mb-3">
          <label for="username" class="form-label text-white">Username</label>
          <input type="text" class="form-control" id="username" placeholder="Enter username">
        </div>
        <div class="mb-3">
          <label for="password" class="form-label text-white">Password</label>
          <input type="password" class="form-control" id="password" placeholder="Enter password">
        </div>
        <div class="mb-3">
          <label for="database" class="form-label text-white">Database Name</label>
          <input type="text" class="form-control" id="database" placeholder="Enter database name">
        </div>
        <div class="text-center">
          <button type="submit" class="btn btn-lg btn-outline-light animate-pulse">Save Configuration</button>
        </div>
      </form>
    </section>
  </main>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  background: linear-gradient(135deg, #a23dbf, #e289ff);
}

.config-panel {
  width: 50%;
  max-width: 600px;
  background: rgba(123, 7, 121, 0.9);
  border-radius: 12px;
  box-shadow: 0px 4px 15px rgba(123, 7, 121, 0.3);
}

h2 {
  font-weight: bold;
}

.form-control, .form-select {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
}
.form-control::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.form-select option {
    background: white;
    color: #7b0779; 
    font-weight: bold;
}

.btn-outline-light {
  border: 2px solid white;
  font-weight: bold;
  transition: all 0.3s ease;
}
.btn-outline-light:hover {
  background-color: white;
  color: #7b0779;
}

/* Animations */
.animate-fade-in {
  animation: fadeIn 1s ease-in-out;
}
.animate-pulse {
  animation: pulse 1.5s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
</style>