import { createRouter, createWebHistory } from 'vue-router';

import routerFaceRecognition from './router-face-recognition';
import routerRecognitionHistory from './router-recognition-history';
import routerFaceMangement from './router-face-mangement';
import Login from "@/views/login/Login"
import { httpClient } from "@/apis/httpclient"

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/logout',
    name: 'Logout',
   
  },
  ...routerFaceRecognition,
  ...routerRecognitionHistory,
  ...routerFaceMangement

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {

  if(to.fullPath=="/"){
    next({name:'FaceMangement'})
  }
  //xoá token nếu đăng xuất
  if(to.fullPath=="/logout"){
    localStorage.removeItem("token")
    router.push({name:'Login'})
  }
  //nếu router có yêu cầu authen
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    //Kiểm tra xem đã đăng nhập hay chưa nếu chưa thì đưa về trang đăng nhập
    try {

      await httpClient.post('auth/authen')
      next()
    } catch (e) {
      console.log(e)
      //Đưa tới trang login
      next({
        name: "Login"
      })
    }

  }
  next()
});

export default router;