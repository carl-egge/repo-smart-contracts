<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark p-3">
      <router-link to="/" class="navbar-brand">
        <img src="./assets/logo_ide_letters.png" class="logo" />
      </router-link>
      <div class="navbar-nav mr-auto">
        <li class="nav-item m-2">
          <router-link to="/contracts" class="nav-link">
            Smart Contracts List
          </router-link>
        </li>
        <li class="nav-item m-2">
          <router-link to="/add" class="nav-link"
            >Add Smart Contract</router-link
          >
        </li>
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

.logo {
  max-width: 60px;
}
</style>
