<template>
  <div id="app">
    <!-- Navbar -->
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav class="align-items-center">
        <b-navbar-brand href="/" class="py-0">
          <img src="./assets/logo_v2.png" class="mw-95 logo ml-2" />
        </b-navbar-brand>
        <b-nav-item to="/">Smart Contracts</b-nav-item>
        <!-- <b-nav-item to="/archive">Download Archive</b-nav-item> -->
        <b-nav-item to="/about">About</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item
          href="https://www.tuhh.de/ide/homepage.html"
          target="_blank"
        >
          <img src="./assets/logo_ide_letters.png" class="mw-40 py-0" />
        </b-nav-item>
        <b-nav-item
          href="https://github.com/carl-egge/repo-smart-contracts"
          target="_blank"
        >
          <img src="./assets/GitHub-Mark-Light-64px.png" class="mw-35 py-0 mx-2" />
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

.mw-95 {
  max-width: 95px;
}
.mw-35 {
  max-width: 35px;
}
.mw-40 {
  max-width: 40px;
}
.logo {
  padding: 4px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.nav-link {
  padding: 0rem 0.5rem;
}
</style>
