<template>
  <a-menu
    theme="dark"
    v-model:selectedKeys="selectedKeys"
    v-model:openKeys="openKeys"
    mode="inline"
  >
    <div style="height: 64px"></div>
    <div v-if="isMaster">
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
    </div>
    <div v-else>
      <a-sub-menu key="sub3">
        <template #title>
          <span>
            <laptop-outlined />
            Hệ thống
          </span>
        </template>

        <router-link :to="{ name: 'AccountRecognitionHistory' }">
          <a-menu-item key="4">Nhật ký nhận diện</a-menu-item>
        </router-link>
      </a-sub-menu>
    </div>
  </a-menu>
</template>

<script>
import { parseJwt } from "@/utils.js";
import {
  PieChartOutlined,
  DesktopOutlined,
  UserOutlined,
  TeamOutlined,
  FileOutlined,
  LaptopOutlined,
} from "@ant-design/icons-vue";
import {
  defineComponent,
  onMounted,
  ref,
  getCurrentInstance,
  computed,
} from "vue";
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
      selectedKeys: ref([]),
      openKeys: ref([]),
      isMaster: parseJwt()?.payload?.IsMasterAccount,
    };
  },
});
</script>
