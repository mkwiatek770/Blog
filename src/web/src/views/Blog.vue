<template>
  <div class="blog">
    <img alt="Vue logo" src="../assets/logo.png" />
    <h1>Articles:</h1>
    <hr />
  </div>
</template>

<script>
// @ is an alias to /src

import axios from "axios";

export default {
  name: "blog",
  components: {},
  data() {
    return {};
  },
  mounted() {
    axios
      .get("http://localhost:5000/api/v1/articles", { useCredentials: true })
      .then(response => console.log(response));
  }
};
</script>
