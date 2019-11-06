<template>
  <div id="app">
    <Navbar current="Blog" />
    <router-view />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";

export default {
  components: {
    Navbar: Navbar
  }
};
</script>

<style>
</style>
