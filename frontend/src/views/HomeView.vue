<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { locale, t } = useI18n()
</script>

<template>
  <main class="container-fluid">
    <section class="hero text-center text-white d-flex flex-column justify-content-center align-items-center">
      <h1 class="display-3 fw-bold animate-zoom-in text-white">{{ t('message.landing.hero.title') }}</h1>
      <p class="lead animate-slide-up text-white">{{ t('message.landing.hero.subtitle') }}</p>
    </section>

    <section class="container my-5">
      <div class="row text-center">
        <div class="col-md-4 animate-fade-in">
          <i class="bi bi-lightning-fill feature-icon"></i>
          <h3 class="mt-3 feature-text">{{ t('message.landing.features.fast.title') }}</h3>
          <p class="feature-text">{{ t('message.landing.features.fast.description') }}</p>
        </div>
        <div class="col-md-4 animate-fade-in" style="animation-delay: 0.2s;">
          <i class="bi bi-chat-left-text-fill feature-icon"></i>
          <h3 class="mt-3 feature-text">{{ t('message.landing.features.effortless.title') }}</h3>
          <p class="feature-text">{{ t('message.landing.features.effortless.description') }}</p>
        </div>
        <div class="col-md-4 animate-fade-in" style="animation-delay: 0.4s;">
          <i class="bi bi-database-fill-check feature-icon"></i>
          <h3 class="mt-3 feature-text">{{ t('message.landing.features.versatile.title') }}</h3>
          <p class="feature-text">{{ t('message.landing.features.versatile.description') }}</p>
        </div>
      </div>
    </section>

    <section class="how-it-works text-white text-center py-5">
      <h2 class="display-4 animate-slide-up text-white">{{ t('message.landing.howItWorks.title') }}</h2>
      <p class="lead animate-fade-in text-white">{{ t('message.landing.howItWorks.subtitle') }}</p>
      <div class="container mt-4">
        <div class="row">
          <div class="col-md-4 animate-scale-up">
            <i class="bi bi-pencil-square feature-icon"></i>
            <h4 class="text-white">{{ t('message.landing.howItWorks.step1.title') }}</h4>
            <p class="text-white">{{ t('message.landing.howItWorks.step1.description') }}</p>
          </div>
          <div class="col-md-4 animate-scale-up" style="animation-delay: 0.2s;">
            <i class="bi bi-chat-dots feature-icon"></i>
            <h4 class="text-white">{{ t('message.landing.howItWorks.step2.title') }}</h4>
            <p class="text-white">{{ t('message.landing.howItWorks.step2.description') }}</p>
          </div>
          <div class="col-md-4 animate-scale-up" style="animation-delay: 0.4s;">
            <i class="bi bi-bar-chart-line feature-icon"></i>
            <h4 class="text-white">{{ t('message.landing.howItWorks.step3.title') }}</h4>
            <p class="text-white">{{ t('message.landing.howItWorks.step3.description') }}</p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  color: #f5f5f5;
}

.hero {
  height: 80vh;
  background: linear-gradient(135deg, #a23dbf, #e289ff);
  padding: 3rem;
}

.how-it-works {
  background: linear-gradient(135deg, #a23dbf, #e289ff);
  padding: 4rem 2rem;
}

.hero-btn {
  background-color: transparent;
  color: #7b0779;
  font-weight: bold;
  border: 2px solid #7b0779;
  padding: 0.75rem 2rem;
  transition: all 0.3s ease;
  box-shadow: 0px 4px 15px rgba(123, 7, 121, 0.3);
}
.hero-btn:hover {
  background-color: #7b0779;
  color: #fff;
  transform: scale(1.1);
}

.feature-icon {
  font-size: 3rem;
  color: #ffcc00;
}

.feature-text {
  color: #7b0779 !important;
  font-weight: bold;
}

h1, h2, h3, h4, p {
  color: #ffffff !important;
}

.animate-fade-in {
  animation: fadeIn 1s ease-in-out;
}
.animate-slide-up {
  animation: slideUp 1s ease-in-out;
}
.animate-scale-up {
  animation: scaleUp 1s ease-in-out;
}
.animate-zoom-in {
  animation: zoomIn 1.2s ease-in-out;
}
.animate-pulse {
  animation: pulse 1.5s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes scaleUp {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes zoomIn {
  from { transform: scale(0.5); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
</style>