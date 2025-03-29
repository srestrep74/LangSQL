<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import logo from './assets/logo.png';
import { userStore } from '@/store/userStore';
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  userStore.logout();
  router.push('/');
};
</script>

<template>
  <div id="content-wrapper" class="d-flex flex-column min-vh-100">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-light-gray shadow-sm py-3">
      <div class="container">
        <router-link to="/" class="navbar-brand d-flex align-items-center">
          <img :src="logo" alt="Logo" class="me-2" height="40" />
          <span class="fw-bold fs-3 text-custom-purple brand-text">LangSQL</span>
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto align-items-center">
            <!-- Always show Home -->
            <li class="nav-item">
              <router-link to="/" class="nav-link text-custom-purple">Home</router-link>
            </li>
            
            <!-- Show these only when authenticated -->
            <template v-if="userStore.isAuthenticated">
              <li class="nav-item">
                <router-link to="/query" class="nav-link text-custom-purple">Query</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/alerts" class="nav-link text-custom-purple">Alerts</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/reports" class="nav-link text-custom-purple">Reports</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/synthetic_data" class="nav-link text-custom-purple">Synthetic Data</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/configuration" class="nav-link text-custom-purple">Configuration</router-link>
              </li>
              
              <!-- User Dropdown -->
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="userDropdown" role="button" 
                   data-bs-toggle="dropdown" aria-expanded="false">
                  <div class="user-avatar me-2">
                    <i class="bi bi-person-circle"></i>
                  </div>
                </a>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                  <li><router-link to="/profile" class="dropdown-item">Profile</router-link></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><button class="dropdown-item" @click="logout">Logout</button></li>
                </ul>
              </li>
            </template>
            
            <!-- Show these only when NOT authenticated -->
            <template v-else>
              <li class="nav-item">
                <router-link to="/login" class="nav-link text-custom-purple">Login</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link text-custom-purple">Register</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
    <!-- Navbar -->

    <!-- Main Content -->
    <main class="flex-grow-1">
      <RouterView />
    </main>
    <!-- Main Content -->

    <!-- Footer -->
    <footer class="bg-light-gray text-custom-purple text-center p-4 mt-auto shadow-lg">
      <div class="container">
        <div class="footer-content">
          <p class="fw-bold fs-5">LangSQL - Powering Your Queries</p>
          <span>© 2025 LangSQL. All rights reserved.</span>
        </div>
      </div>
    </footer>
    <!-- Footer -->
  </div>
</template>

<style>
.bg-light-gray {
  background-color: #f4f4f4;
}

.text-custom-purple {
  color: #7b0779 !important;
}

.navbar-nav .nav-link {
  font-weight: 500;
  transition: all 0.3s ease-in-out;
  position: relative;
}

.navbar-nav .nav-link::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 100%;
  height: 2px;
  background-color: #7b0779;
  transform: scaleX(0);
  transition: transform 0.3s ease-in-out;
}

.navbar-nav .nav-link:hover::after {
  transform: scaleX(1);
}

.brand-text {
  font-family: 'Poppins', sans-serif;
  transition: transform 0.3s ease-in-out;
}

.brand-text:hover {
  transform: scale(1.1);
}

.footer-content {
  font-family: 'Poppins', sans-serif;
}

/* User avatar styles */
.user-avatar {
  color: #7b0779;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
}

bi-person-circle {  
  color: #7b0779 !important;
}

.user-name {
  font-weight: 500;
  color: #7b0779;
}

.dropdown-item {
  transition: all 0.2s ease;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f0e6ef;
  color: #7b0779;
}
</style>