<template>
  <a-layout style="min-height: 100vh">
    <!-- sider bar -->
    <a-layout-sider v-model:collapsed="collapsed" collapsible>
      <side-bar-vue></side-bar-vue>
    </a-layout-sider>
    <a-layout>
      <!-- header -->
      <a-layout-header style="background: #fff; padding: 0">
        <top-nav-vue></top-nav-vue>
      </a-layout-header>
      <!-- content -->
      <a-layout-content style="margin: 0 16px">
        <router-view></router-view>
      </a-layout-content>
      <a-layout-footer style="text-align: center"> </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import {
  PieChartOutlined,
  DesktopOutlined,
  UserOutlined,
  TeamOutlined,
  FileOutlined,
  LaptopOutlined,
} from "@ant-design/icons-vue";
import { defineComponent, ref } from "vue";
import SideBarVue from "./SideBar.vue";
import TopNavVue from "./TopNav.vue";
export default defineComponent({
  components: {
    PieChartOutlined,
    DesktopOutlined,
    UserOutlined,
    TeamOutlined,
    FileOutlined,
    LaptopOutlined,
    TopNavVue,
    SideBarVue
  },
  data() {
    return {
      collapsed: ref(false),
     
    };
  },
});
</script>
<style>


.site-layout .site-layout-background {
  background: #fff;
}
[data-theme="dark"] .site-layout .site-layout-background {
  background: #141414;
}
</style>