<template>
  <header class="app-header">
    <div class="header-inner">
      <router-link to="/" class="logo" aria-label="返回工作台">
        <span class="logo-icon">
          <svg width="25" height="25" viewBox="0 0 24 24" aria-hidden="true">
            <g class="sunflower-petals">
              <ellipse cx="12" cy="3.7" rx="1.55" ry="3.05"/>
              <ellipse cx="12" cy="20.3" rx="1.55" ry="3.05"/>
              <ellipse cx="3.7" cy="12" rx="3.05" ry="1.55"/>
              <ellipse cx="20.3" cy="12" rx="3.05" ry="1.55"/>
              <ellipse cx="6.15" cy="6.15" rx="1.45" ry="2.85" transform="rotate(-45 6.15 6.15)"/>
              <ellipse cx="17.85" cy="17.85" rx="1.45" ry="2.85" transform="rotate(-45 17.85 17.85)"/>
              <ellipse cx="17.85" cy="6.15" rx="1.45" ry="2.85" transform="rotate(45 17.85 6.15)"/>
              <ellipse cx="6.15" cy="17.85" rx="1.45" ry="2.85" transform="rotate(45 6.15 17.85)"/>
            </g>
            <circle class="sunflower-center" cx="12" cy="12" r="5.1"/>
            <circle class="sunflower-core" cx="12" cy="12" r="2.15"/>
          </svg>
        </span>
        <span class="logo-text">Agentic RAG 求职助手</span>
      </router-link>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: transparent;
  border-bottom: 0;
  backdrop-filter: none;
}

.header-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 13px 24px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 18px;
}

.logo {
  display: inline-flex;
  align-items: center;
  min-width: 0;
  gap: 10px;
  color: var(--color-text);
  text-decoration: none;
}

.logo-icon {
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #fff;
  background: linear-gradient(135deg, #ff9b25, #6d9b42);
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(244, 123, 18, 0.22);
}

.logo-icon svg {
  display: block;
}

.sunflower-petals {
  fill: #ffd65a;
}

.sunflower-center {
  fill: #7b4a16;
}

.sunflower-core {
  fill: #4e2c0d;
}

.logo-text {
  font-size: 17px;
  font-weight: 750;
  letter-spacing: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 640px) {
  .header-inner {
    padding: 12px 16px;
  }

  .logo-text {
    font-size: 15px;
  }
}
</style>
