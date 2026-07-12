<template>
  <header class="app-header">
    <div class="header-inner">
      <router-link to="/" class="logo" aria-label="返回工作台">
        <span class="logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3l8 4.5-8 4.5-8-4.5L12 3z"/>
            <path d="M4 12l8 4.5 8-4.5"/>
            <path d="M4 16.5l8 4.5 8-4.5"/>
          </svg>
        </span>
        <span class="logo-text">Agentic RAG 求职助手</span>
      </router-link>

      <nav class="nav-links" aria-label="主导航">
        <router-link to="/" class="nav-link">工作台</router-link>
        <span class="header-status">AI 面试准备工作流</span>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.88);
  border-bottom: 1px solid rgba(226, 232, 240, 0.9);
  backdrop-filter: blur(16px);
}

.header-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 13px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
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
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  border-radius: 10px;
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.2);
}

.logo-text {
  font-size: 17px;
  font-weight: 750;
  letter-spacing: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.nav-links {
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  min-width: 0;
}

.nav-link,
.header-status {
  border: 1px solid var(--color-border);
  border-radius: 999px;
  padding: 6px 13px;
  font-size: 13px;
  font-weight: 650;
  line-height: 1.3;
  white-space: nowrap;
}

.nav-link {
  color: var(--color-primary);
  background: #fff;
  text-decoration: none;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--color-primary-dark);
  background: var(--color-primary-light);
  border-color: #bfdbfe;
}

.header-status {
  color: var(--color-accent);
  background: var(--color-accent-light);
  border-color: #99f6e4;
}

@media (max-width: 640px) {
  .header-inner {
    padding: 12px 16px;
  }

  .logo-text {
    font-size: 15px;
  }

  .header-status {
    display: none;
  }
}
</style>
