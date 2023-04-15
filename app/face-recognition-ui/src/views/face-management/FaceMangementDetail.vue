<template>
  <div class="page-container">
    <div class="page-title">
      <span class="title">Thông tin tài khoản</span>
      <span class="note">Thông tin của tài khoản người dùng &lt;{{ userName }}></span>
    </div>
    <div class="account-infor">
      <img src="@/assets/user-icon.svg" class="account-infor__avatar" />
      <div class="account-infor__content">
        <div class="full-name">{{ fullName }}</div>
        <div>{{ email }}</div>
        <div>{{ phone }}</div>
      </div>
    </div>
    <div class="decorator"></div>
    <div class="page-title">
      <span class="title">Thêm dữ liệu nhận dạng</span>
      <span class="note">Vui lòng chụp 8 ảnh với các góc khác nhau để nhận diện chính xác
        nhất</span>
    </div>
    <div class="image-conatiner">
      <Image @delete="deleteImage(1)" @takePhoto="($event) => takePhoto($event, 1)"
        :placeholder="require('@/assets/front_1.svg')" :src="faces[1]?.src"></Image>
      <Image @delete="deleteImage(2)" @takePhoto="($event) => takePhoto($event, 2)"
        :placeholder="require('@/assets/front_2.svg')" :src="faces[2]?.src"></Image>
      <Image @delete="deleteImage(3)" @takePhoto="($event) => takePhoto($event, 3)"
        :placeholder="require('@/assets/front_3.svg')" :src="faces[3]?.src"></Image>
      <Image @delete="deleteImage(4)" @takePhoto="($event) => takePhoto($event, 4)"
        :placeholder="require('@/assets/front_4.svg')" :src="faces[4]?.src"></Image>
      <Image @delete="deleteImage(5)" @takePhoto="($event) => takePhoto($event, 5)"
        :placeholder="require('@/assets/left-to-right.svg')" :src="faces[5]?.src"></Image>
      <Image @delete="deleteImage(6)" @takePhoto="($event) => takePhoto($event, 6)"
        :placeholder="require('@/assets/right-to-left.svg')" :src="faces[6]?.src"></Image>
      <Image @delete="deleteImage(7)" @takePhoto="($event) => takePhoto($event, 7)"
        :placeholder="require('@/assets/top-down.svg')" :src="faces[7]?.src"></Image>
      <Image @delete="deleteImage(8)" @takePhoto="($event) => takePhoto($event, 8)"
        :placeholder="require('@/assets/bottom-up.svg')" :src="faces[8]?.src"></Image>
    </div>
  </div>
</template>

<script>
import Image from "@/components/Image.vue";
import { httpClient } from "@/apis/httpclient";
import { mask, unMask, parseJwt } from "@/utils";
import { notification } from "ant-design-vue";
import { SmileOutlined } from "@ant-design/icons-vue";
import { h } from "vue";
export default {
  components: {
    Image,
    SmileOutlined
  },
  computed: {
    fullName: {
      get() {
        return this.$route.query.LastName + ' ' +this.$route.query.FirstName;
      },
    },
    email: {
      get() {
        return this.$route.query.Email;
      },
    },
    phone: {
      get() {
        return this.$route.query.Phone;
      },
    },
    userName: {
      get() {
        return this.$route.query.UserName;
      },
    },
  },
  created() {
    this.initData();
  },
  data() {
    return {
      faces: [],
    };
  },
  methods: {
    /**
     * Xoá dữ liệu nhận dạng
     * @param {*} type 
     */
    async deleteImage(type) {

      mask()
      try {
        await httpClient.delete(`faces?face_id=${this.faces[type].ID}`)
        await this.initData();
      } catch (e) {

        console.log(e);
      }

      unMask()
    },
    async initData() {
      
      mask();
      const me = this;
      me.faces.splice(0, me.faces.length)
      let facesResponse = (
        await httpClient.get(`faces?account_id=${this.$route.query.ID}`)
      )?.data;
      let customerID = parseJwt().payload.CustomerID;
      facesResponse.forEach((face) => {
        while (me.faces.length - 1 < face.Type) {
          me.faces.push({});
        }
        me.faces[face.Type] = face
        me.faces[
          face.Type
        ].src = `${window.__config.static_file}/${customerID}/${this.$route.query.ID}/${face.ID}${face.Extension}`;
      });
      unMask();
    },
    /**
     * Chụp ảnh và gửi lên server
     */
    async takePhoto(image, type) {
      mask();
      try {
        image.append("type", type);
        image.append("account_id", this.$route.query.ID);

        await httpClient.post(
          `faces?account_id=${this.$route.query.ID}&type=${type}`,
          image
        );
        await this.initData();

      } catch (e) {
        console.log(e);
        notification.open({
          message: 'Thêm dữ liệu nhận dạng thất bại!',
          description:
            "Vui lòng liên hệ với quản trị hệ thống để biết thêm chi tiết",
          icon: h(SmileOutlined, { style: "color: #108ee9" }),
        });
      }

      unMask();
    },
  },
};
</script>

<style lang="scss">

.page-container {
  width: 90%;
  height: 80vh;
  background-color: #ffff;
  border-radius: 12px;
  margin: 24px auto;
  padding: 24px;

  .page-title {
    display: flex;
    flex-direction: column;
    margin-bottom: 24px;

    .title {
      font-size: 24px;
      font-weight: bold;
    }

    .note {
      color: #464646;
      font-size: 14px;
    }
  }

  .account-infor {
    display: flex;

    &__avatar {
      width: 86px;
      height: 86px;
      border-radius: 50%;
    }

    &__content {
      margin-left: 24px;

      div {
        color: #464646;
        font-size: 14px;
      }

      .full-name {
        font-size: 16px;
        font-weight: bold;
      }
    }
  }

  .decorator {
    height: 1px;
    background-color: #f1f1f1;
    width: 90%;
    margin: 24px auto;
  }

  .image-conatiner {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
  }
}
</style>

