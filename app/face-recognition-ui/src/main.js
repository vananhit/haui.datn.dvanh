import { createApp } from 'vue';
import router   from '@/router/router'
import Antd from 'ant-design-vue/es';
import App from './App';
import 'ant-design-vue/dist/antd.css';
const app = createApp(App);

app.use(Antd)
app.use(router);
app.config.productionTip = false;
app.mount('#app');