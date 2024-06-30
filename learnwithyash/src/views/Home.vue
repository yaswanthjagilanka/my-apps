<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/learnwithyash.jpg" />
    <HelloWorld msg="Welcome to LearnwithYash" />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Home",
  components: {
    HelloWorld
  }
};
</script>
