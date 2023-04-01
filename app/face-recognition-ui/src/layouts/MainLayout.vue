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
        <div id="app-loading">
          <a-spin :spinning="true" :delay="500" :indicator="indicator">
          </a-spin>
        </div>
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
import { defineComponent, ref, h } from "vue";
import SideBarVue from "./SideBar.vue";
import TopNavVue from "./TopNav.vue";
import { LoadingOutlined } from '@ant-design/icons-vue';
export default defineComponent({
  components: {
    PieChartOutlined,
    DesktopOutlined,
    UserOutlined,
    TeamOutlined,
    FileOutlined,
    LaptopOutlined,
    TopNavVue,
    SideBarVue,
    LoadingOutlined
  },
  data() {
    return {
      collapsed: ref(false),
      indicator: h(LoadingOutlined, {
        style: {
          fontSize: "60px",
        },
        spin: true,
      }),
    };
  },
});
</script>
<style lang="scss">
#app-loading {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0px;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  visibility: hidden;
}
.site-layout .site-layout-background {
  background: #fff;
}
[data-theme="dark"] .site-layout .site-layout-background {
  background: #141414;
}
</style>