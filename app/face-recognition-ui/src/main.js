import '@/config/config'
import { createApp } from 'vue';
import router from '@/router/router'
import Antd from 'ant-design-vue/es';
import App from './App';
import 'ant-design-vue/dist/antd.css';

// import VueSocketIO from 'vue-3-socket.io'
// import SocketIO from 'socket.io-client'

const app = createApp(App);
// app.use(new VueSocketIO({
//     debug: true,
//     connection: SocketIO('http://localhost:8000', {
//         autoConnect: false,
//         path: "/ws/socket.io/",
//         transports: ["websocket","polling"],
//         auth:{
//             token:"anhyeuem"
//         },
      
//     }),
    
   
// }))
app.use(Antd)
app.use(router);
app.mount('#app');