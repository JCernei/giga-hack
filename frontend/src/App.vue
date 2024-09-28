<template>
  <div id="app">
    <TransformContract />
  </div>
</template>

<script>
import TransformContract from './components/TransformContract.vue';

export default {
  name: "App",
  components: {
    TransformContract,
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>