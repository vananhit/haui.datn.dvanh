<template>
  <MainLayout> </MainLayout>
</template>
<script>
import MainLayout from "@/layouts/MainLayout.vue";
import { httpClient } from "@/apis/httpclient";
export default {
  name: "App",
  components: {
    MainLayout,
  },
  async created() {
    this.$router.push({name:'FaceRecognition'})
  },
  mounted(){
    console.log(this.$socket)
   
  }
};
</script>

<style>
#app {
  height: 100vh;
}
</style>
