<template>
  <nav id="nav">
    <div class="nav-wrapper">
      <div class="hide-on-small-only">
        <a href="#" class="brand-logo left">4Code</a>
      </div>
      <div class="hide-on-med-and-up">
        <a href="#" class="brand-logo left">4Code | {{ current }}</a>
      </div>

      <div class="brand-logo center">
        <ul id="nav-mobile" class="hide-on-small-only">
          <li>
            <a href>Blog</a>
          </li>
          <li>
            <a href>Snippets</a>
          </li>
          <li>
            <a href>About</a>
          </li>
        </ul>
      </div>

      <div class="hide-on-med-and-down">
        <div class="right">
          <div class="center row">
            <div class="col s12">
              <div class="row" id="topbarsearch">
                <div class="input-field col s6 s12 red-text">
                  <i class="red-text material-icons prefix">search</i>
                  <input
                    type="text"
                    placeholder="search"
                    id="autocomplete-input"
                    class="autocomplete red-text"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <ul class="right hide-on-large-only">
        <li>
          <a href="sass.html">
            <i class="material-icons">search</i>
          </a>
        </li>
        <li>
          <a href="badges.html">
            <i class="material-icons">menu</i>
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  props: ["current"]
};
</script>

<style>
</style>