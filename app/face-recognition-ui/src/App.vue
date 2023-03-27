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
    // //Kiểm tra nếu chưa đăng nhập thì đưa đến trang đăng nhập
    // let token = localStorage.getItem("token");
    // if (token) {
    //   try {
    //     await httpClient.post("auth/authen");
    //   } catch (e) {
    //     this.$router.push({ name: "Login" });
    //   }
    // } else {
    //   this.$router.push({ name: "Login" });
    // }
    this.$router.push({name:'FaceRecognition'})
  },
};
</script>

<style>
#app {
  height: 100vh;
}
</style>
