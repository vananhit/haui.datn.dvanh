<template>
  <div>
    <div class="page-title">Nhận diện khuôn mặt</div>
    <div class="face-deetction" >
        <face-dtector-vue></face-dtector-vue>
    </div>
  </div>
</template>

<script>
import FaceDtectorVue from "../../components/FaceDtector.vue";
export default {
  components: {
    FaceDtectorVue,
  },
  created() {},
  computed: {},
  data() {
    return {};
  },
  mounted() {},
};
</script>


<style scoped lang="scss">
.page-title{
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 24px;
    margin-top: 24px;
}
.face-deetction{
    width:700px;
    margin-left: auto;
    margin-right: auto;

}
</style>