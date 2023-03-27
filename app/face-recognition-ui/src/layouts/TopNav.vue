<template>
    <div class="top-nav-conatiner">
        <div class="logout" @click="logout"> <span>Đăng xuất</span> <LogoutOutlined/> </div>
    </div>
</template>

<script>
import {

  LogoutOutlined 
} from "@ant-design/icons-vue";

export default{
    components:{
        LogoutOutlined
    },
    methods:{
        logout(){
            this.$router.push({name:'Logout'})
        }
    }
}
</script>


<style scoped lang="scss">
.top-nav-conatiner{
    width: 100%;
    height: 100%;
    
    .logout{
        cursor: pointer;
        font-size: 16px;
        font-weight:    600;
        margin-left: auto;
        width: fit-content;
        height: fit-content;
        margin-right: 24px;
    }
}
</style>