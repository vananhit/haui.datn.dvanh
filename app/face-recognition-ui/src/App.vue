<template>
  <MainLayout> </MainLayout>
</template>
<script>
import MainLayout from "@/layouts/MainLayout.vue";
import DemoVue from "./Demo.vue";
export default {
  name: "App",
  components: {
    MainLayout,
    DemoVue
  },
  async created() {
    
  },
  mounted(){
   
  }
};
</script>

<style>
#app {
  height: 100vh;
}
</style>
