<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark p-3">
      <router-link to="/" class="navbar-brand">
        <img src="./assets/logo.png" class="mw-65 logo" />
      </router-link>
      <div class="navbar-nav mr-auto">
        <li class="nav-item m-2">
          <router-link to="/contracts" class="nav-link">
            Smart Contracts List
          </router-link>
        </li>
        <li class="nav-item m-2">
          <router-link to="/add" class="nav-link">
            Add Smart Contract
          </router-link>
        </li>
        <!-- Just for testing -->
        <li class="nav-item m-2">
          <router-link
            to="/contracts/62a0a039e0d82ba44f875573"
            class="nav-link"
          >
            One Smart Contract
          </router-link>
        </li>
      </div>
      <div class="navbar-nav ms-auto me-3 align-items-center">
        <a
          href="https://www.tuhh.de/ide/homepage.html"
          target="_blank"
          class="me-3"
        >
          <img src="./assets/logo_ide_letters.png" class="mw-45" />
        </a>
        <a
          href="https://github.com/carl-egge/repo-smart-contracts-v2"
          target="_blank"
        >
          <img src="./assets/GitHub-Mark-Light-64px.png" class="mw-40" />
        </a>
      </div>
    </nav>
    <div class="m-3">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.mw-65 {
  max-width: 65px;
}
.mw-40 {
  max-width: 40px;
}
.mw-45 {
  max-width: 45px;
}
.logo {
  padding: 4px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>
