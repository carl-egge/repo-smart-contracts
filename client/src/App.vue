<template>
  <div id="app">
    <!-- Navbar -->
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav class="align-items-center">
        <b-navbar-brand href="/">
          <img src="./assets/logo.png" class="mw-65 logo" />
        </b-navbar-brand>
        <b-nav-item to="/">Smart Contracts List</b-nav-item>
        <b-nav-item to="/add">Add Smart Contract</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item
          href="https://www.tuhh.de/ide/homepage.html"
          target="_blank"
        >
          <img src="./assets/logo_ide_letters.png" class="mw-45" />
        </b-nav-item>
        <b-nav-item
          href="https://github.com/carl-egge/repo-smart-contracts"
          target="_blank"
        >
          <img src="./assets/GitHub-Mark-Light-64px.png" class="mw-40" />
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <!-- Main Container -->
    <div class="m-3">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  methods: {
    makeToast(title, msg, variant = null) {
      this.toastCount++;
      this.$bvToast.toast(msg, {
        title: title,
        variant: variant,
        autoHideDelay: 5000,
      });
    },
  },
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
