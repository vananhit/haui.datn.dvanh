<template>
  <a-menu
    theme="dark"
    v-model:selectedKeys="selectedKeys"
    v-model:openKeys="openKeys"
    mode="inline"
  >
    <div style="height: 64px"></div>
    <a-sub-menu key="sub1">
      <template #title>
        <span>
          <user-outlined />
          Quản lý người dùng
        </span>
      </template>
      <router-link :to="{ name: 'FaceRecognition' }">
        <a-menu-item key="1">Nhận diện khuôn mặt</a-menu-item>
      </router-link>
      <router-link :to="{ name: 'FaceMangement' }">
        <a-menu-item key="2">Quản lý khuôn mặt </a-menu-item>
      </router-link>
    </a-sub-menu>
    <a-sub-menu key="sub2">
      <template #title>
        <span>
          <laptop-outlined />
          Hệ thống
        </span>
      </template>

      <router-link :to="{ name: 'RecognitionHistory' }">
        <a-menu-item key="3">Nhật ký nhận diện</a-menu-item>
      </router-link>
    </a-sub-menu>
  </a-menu>
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
import { defineComponent, onMounted, ref, getCurrentInstance } from "vue";
export default defineComponent({
  components: {
    PieChartOutlined,
    DesktopOutlined,
    UserOutlined,
    TeamOutlined,
    FileOutlined,
    LaptopOutlined,
  },
  setup() {
    
    return {
      selectedKeys: ref(["1"]),
      openKeys: ref(["sub1"]),
    };
  },
});
</script>
