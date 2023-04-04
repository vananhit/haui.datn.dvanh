<template>
  <div>
    <div class="page-title">
      <span>Quản lý khuôn mặt</span><a-button type="primary">Thêm tài khoản</a-button>
    </div>
    <a-input-search class="search-box" placeholder="Tìm kiếm theo tên đăng nhập, thư điện tử họ và tên"
      style="width: 400px" @search="onSearch" @change="onSearchBoxChange" />
    <a-table :columns="columns" :data-source="data" :pagination="pagination" :loading="loading"
      @change="handleTableChange">
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
  </div>
</template>

<script>
import { httpClient } from "@/apis/httpclient";
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
      searchValue: null,

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
};
</script>

<style>
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