<template>
  <div id="app">
    <div id="nav">
      <div class="row">
        <div class="col s3 left-align">
          <a id="brand">4Code</a>
        </div>
        <div class="col s6">
          <router-link to="/">Home</router-link>|
          <router-link to="/about">About</router-link>|
          <router-link to="/todo">Todo</router-link>
        </div>
        <div class="col s3">
          <div class="row">
            <div class="col s6 right-align">
              <i class="material-icons">search</i>
            </div>
            <div class="col s6 left-align">
              <span>Search</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#nav #brand {
  font-weight: bold;
  color: red;
}
</style>
