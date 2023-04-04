<template>
  <div>
    <div class="page-title">
      <span>Quản lý khuôn mặt</span
      ><a-button @click="OpenCreateAccountPopup" type="primary"
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
            <a-form-item label="Thư điện tử" name="Email">
              <a-input
                v-model:value="formState.Email"
                placeholder="Nhập thư điện tử"
              />
            </a-form-item>
            <a-form-item label="Tên đăng nhập" name="UserName">
              <a-input
                v-model:value="formState.UserName"
                placeholder="Nhập tên đăng nhập"
              />
            </a-form-item>
            <div class="popup-action">
              <a-button @click="isShowAccountPopup = false"> Huỷ </a-button>
              <div style="width: 24px"></div>
              <a-button type="primary"> Tạo </a-button>
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
export default {
  components: {
    DeleteTwoTone,
    FolderViewOutlined,
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
            trigger: "change",
            message: "Tên không được để trống",
          },
        ],
        LastName: [
          {
            required: true,
            validator: this.validateLastName,
            trigger: "change",
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
    debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
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
    validateEmail(rule) {
      if (!this.formState.Email) {
        return Promise.reject();
      } else {
        /**
         * kiểm tra định dạng email
         */

        //eslint-disable-next-line
        if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.formState.Email))) {
          rule.message="Email sai định dạng!"
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
     * Bật popup thêm tài khoản mới
     */
    OpenCreateAccountPopup() {
      mask();
      this.isShowAccountPopup = true;
      unMask();
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
      Modal.confirm({
        title: "Xác nhận xoá",
        icon: createVNode(ExclamationCircleOutlined),
        content: `Xoá tài khoản <${record.UserName}> ra khỏi hệ thống`,
        okText: "Đồng ý",
        cancelText: "Huỷ bỏ",
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
  z-index: 999;
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