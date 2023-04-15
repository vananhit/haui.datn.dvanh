<template>
  <div>
    <div class="page-title">
      <span>Quản lý khuôn mặt</span
      ><a-button @click="isShowAccountPopup = true" type="primary"
        >Thêm tài khoản</a-button
      >
    </div>
    <a-input-search
      class="search-box"
      placeholder="Tìm kiếm theo tên đăng nhập, thư điện tử họ và tên"
      style="width: 400px"
      @search="onSearch"
      @change="onSearchBoxChange"
    />
    <a-table
      :columns="columns"
      :data-source="data"
      :pagination="pagination"
      :loading="loading"
      @change="handleTableChange"
    >
      <template #bodyCell="{ column, text, record }">
        <template v-if="column.dataIndex === 'Action'">
          <div style="display: flex">
            <a-tooltip>
              <template #title> Xoá</template>
              <DeleteTwoTone @click="confirm(record)" />
            </a-tooltip>
            <div style="width: 24px"></div>
            <a-tooltip>
              <template #title> Thiết lập dữ liệu khuôn mặt</template>
              <FolderViewOutlined @click="viewDetail(record, text)" />
            </a-tooltip>
          </div>
        </template>
      </template>
    </a-table>
    <div class="create-account-popup-contatiner" v-if="isShowAccountPopup">
      <div class="create-account-container">
        <div class="popup-header">
          <span>Thêm tài khoản mới</span>
          <a-tooltip>
            <template #title>Đóng</template>
            <img
              src="@/assets/close-icon.svg"
              width="20"
              height="20"
              @click="isShowAccountPopup = false"
            />
          </a-tooltip>
        </div>
        <div class="popup-content">
          <a-form :layout="'vertical'" :rules="rules">
            <a-form-item label="Tên đăng nhập" name="UserName">
              <a-input
                v-model:value="formState.UserName"
                placeholder="Nhập tên đăng nhập"
              />
            </a-form-item>
            <a-form-item label="Thư điện tử" name="Email">
              <a-input
                v-model:value="formState.Email"
                placeholder="Nhập thư điện tử"
              />
            </a-form-item>
            <a-form-item label="Họ" name="LastName">
              <a-input
                v-model:value="formState.LastName"
                placeholder="Nhập họ"
              />
            </a-form-item>
            <a-form-item label="Tên" name="FirstName">
              <a-input
                v-model:value="formState.FirstName"
                placeholder="Nhập tên"
              />
            </a-form-item>
            <a-form-item label="Địa chỉ" name="Address">
              <a-input
                v-model:value="formState.Address"
                placeholder="Nhập địa chỉ"
              />
            </a-form-item>
            <div class="popup-action">
              <a-button @click="isShowAccountPopup = false"> Huỷ </a-button>
              <div style="width: 24px"></div>
              <a-button type="primary" @click="CreateAccout"> Tạo </a-button>
            </div>
          </a-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { httpClient } from "@/apis/httpclient";
import { unMask, mask } from "@/utils";
import {
  DeleteTwoTone,
  ExclamationCircleOutlined,
  FolderViewOutlined,
} from "@ant-design/icons-vue";
import { Modal } from "ant-design-vue";
import { createVNode } from "vue";
import { notification } from "ant-design-vue";
import { SmileOutlined } from "@ant-design/icons-vue";
import { h } from "vue";
export default {
  components: {
    DeleteTwoTone,
    FolderViewOutlined,
    SmileOutlined,
  },
  data() {
    return {
      formState: {
        Email: null,
        UserName: null,
        FirstName: null,
        LastName: null,
      },
      rules: {
        FirstName: [
          {
            required: true,
            validator: this.validateFirstName,
            trigger: "blur",
            message: "Tên không được để trống",
          },
        ],
        LastName: [
          {
            required: true,
            validator: this.validateLastName,
            trigger: "blur",
            message: "Họ không được để trống",
          },
        ],
        Email: [
          {
            required: true,
            validator: this.validateEmail,
            trigger: "blur",
            message: "Thư điện tử không được để trống",
          },
        ],
        UserName: [
          {
            required: true,
            validator: this.validateUserName,
            trigger: "blur",
            message: "Tên đăng nhập không được để trống",
          },
        ],
      },

      searchValue: null,
      isShowAccountPopup: false,
      columns: [
        {
          title: "Tên tài khoản",
          dataIndex: "UserName",
          key: "UserName",
        },
        {
          title: "Thư điện  tử",
          dataIndex: "Email",
          key: "Email",
        },
        {
          title: "Địa chỉ",
          dataIndex: "Address",
          key: "Address",
          ellipsis: true,
        },

        {
          title: "Họ",
          dataIndex: "LastName",
          key: "LastName",
          ellipsis: true,
        },
        {
          title: "Tên",
          dataIndex: "FirstName",
          key: "FirstName",
          ellipsis: true,
        },
        {
          title: "Hàng động",
          dataIndex: "Action",
          key: "Action",
          ellipsis: true,
        },
      ],
      data: [],
      pagination: {
        total: 0,
        current: 1,
        pageSize: 20,
      },
    };
  },

  async created() {
    let params = {
      skip: 0,
      take: 20,
    };

    let ans = await httpClient.get("customers/accounts", { params: params });
    this.data = ans.data.data.map((x) => {
      return {
        ...x,
        key: x.ID,
      };
    });
    this.pagination.total = ans.data.total;
  },
  methods: {
    /**
     * Tạo tài khoản
     */
    async CreateAccout() {
      mask();
      const me = this;
      try {
        await httpClient.post("accounts/account", {
          UserName: me.formState.UserName,
          Password: "",
          Email: me.formState.Email,
          FirstName: me.formState.FirstName,
          LastName: me.formState.LastName,
          Address: me.formState.Address,
        });
        await me.handleTableChange(me.pagination);
        notification.open({
          message: "Tạo tài khoản thành công",
          description:
            "Tên đăng nhâp, và mật khẩu đã được gửi tới mail đăng ký",
          icon: h(SmileOutlined, { style: "color: #108ee9" }),
        });
      } catch (e) {
        console.log(e);
        notification.open({
          message: "Tạo tài khoản không thành công",
          description:
            "Vui lòng liên hệ với quản trị hệ thống để biết thêm chi tiết",
          icon: h(SmileOutlined, { style: "color: #108ee9" }),
        });
      }
      me.isShowAccountPopup = false;
      unMask();
    },
    validateFirstName(rule) {
      if (!this.formState.FirstName) {
        return Promise.reject();
      } else {
        return Promise.resolve();
      }
    },
    validateLastName(rule) {
      if (!this.formState.LastName) {
        return Promise.reject();
      } else {
        return Promise.resolve();
      }
    },
    async validateEmail(rule) {
      if (!this.formState.Email) {
        return Promise.reject();
      } else {
        debugger;
        //Kiểm tra định dạng email

        if (
          //eslint-disable-next-line
          !/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(
            this.formState.Email
          )
        ) {
          rule.message = "Email sai định dạng!";
          return Promise.reject();
        }
        //Kiểm tra tồn tại email
        let exist = (
          await httpClient.get(
            `accounts/exits-email?email=${this.formState.Email}`
          )
        ).data;
        if (exist) {
          rule.message = "Thư điện tử đã tồn tại!";
          return Promise.reject();
        }
        return Promise.resolve();
      }
    },
    async validateUserName(rule, value) {
      const me = this;
      if (!this.formState.UserName) {
        return Promise.reject();
      } else {
        let isExist = (
          await httpClient.get(
            `accounts/exits?user_name=${me.formState.UserName}`
          )
        ).data;
        if (isExist) {
          rule.message = "Tên đăng nhập đã tồn tại!";
          return Promise.reject();
        } else {
          return Promise.resolve();
        }
      }
    },

    /**
     * Gọi lại api phân trang khi tìm kiếm
     * @param {*} e
     */
    onSearchBoxChange(e) {
      this.searchValue = e.target.value;
    },
    /**Khi nhấn vào ô tìm kiếm */
    async onSearch(e) {
      this.pagination = {
        total: 0,
        current: 1,
        pageSize: 20,
      };
      let params = {
        skip: 0,
        take: 20,
        search: this.searchValue,
      };

      let ans = await httpClient.get("customers/accounts", { params: params });
      this.data = ans.data.data.map((x) => {
        return {
          ...x,
          key: x.ID,
        };
      });
      this.pagination.total = ans.data.total;
    },
    /**
     * Xem chi tiết tài khoản
     */
    viewDetail(record) {
      this.$router.push({
        name: "FaceMangementDetatil",
        query: record,
      });
    },
    /**
     * Mở popup xác nhận xoá
     */
    confirm(record) {
      console.log(record);
      Modal.confirm({
        title: "Xác nhận xoá",
        icon: createVNode(ExclamationCircleOutlined),
        content: `Xoá tài khoản <${record.UserName}> và toàn bộ dữ liệu nhận dạng ra khỏi hệ thống`,
        okText: "Đồng ý",
        cancelText: "Huỷ bỏ",
        onOk: async () => {
          const me = this;
          mask();
          try {
            //Xoá
            await httpClient.delete(`accounts/account?account_id=${record.ID}`);
            //Lấy lại dữ liệu
            await me.handleTableChange(me.pagination);

            notification.open({
              message: "Xoá tài khoản thành công!",
              icon: h(SmileOutlined, { style: "color: #108ee9" }),
            });
          } catch (e) {
            console.log(e);
            if (e?.response?.status == 400) {
              notification.open({
                message: "Xoá tài khoản thất bại!",
                description:
                  e?.response?.data?.detail ||
                  "Vui lòng liên hệ với quản trị hệ thống để biết thêm chi tiết",
                icon: h(SmileOutlined, { style: "color: #108ee9" }),
              });
            } else {
              notification.open({
                message: "Xoá tài khoản thất bại!",
                description:
                  "Vui lòng liên hệ với quản trị hệ thống để biết thêm chi tiết",
                icon: h(SmileOutlined, { style: "color: #108ee9" }),
              });
            }
          }
          unMask();
        },
      });
    },

    /**
     * Xử lý sự kiện phân trang
     * @param {*} pag
     * @param {*} filters
     * @param {*} sorter
     */
    async handleTableChange(pag, filters, sorter) {
      this.pagination = pag;
      let ans = await httpClient.get("customers/accounts", {
        params: {
          skip: (pag.current - 1) * pag.pageSize,
          take: pag.pageSize,
          search: this.searchValue,
        },
      });
      this.data = ans.data.data.map((x) => {
        return {
          ...x,
          key: x.ID,
        };
      });
      this.pagination.total = ans.data.total;
    },
  },
  watch: {},
};
</script>

<style lang="scss">
.create-account-popup-contatiner {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;

  .create-account-container {
    width: 500px;
    min-height: 100px;
    background-color: #fff;
    border-radius: 8px;
    padding: 24px;

    .popup-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      span {
        font-size: 24px;
        font-weight: 600;
      }

      img {
        cursor: pointer;
      }
    }

    .popup-content {
      margin-bottom: 24pxpx;
    }

    .popup-action {
      display: flex;
      width: 100%;
      justify-content: flex-end;
    }
  }
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 24px;
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
}

.search-box {
  margin-bottom: 24px;
}
</style>