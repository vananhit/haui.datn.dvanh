<template>
  <div>
    <div class="page-title">Quản lý khuôn mặt</div>
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
            <div style="width:24px"></div>
            <a-tooltip>
              <template #title> Thiết lập dữ liệu khuôn mặt</template>
              <FolderViewOutlined  @click="viewDetail(record,text)"/>
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
     * Xem chi tiết tài khoản
     */
    viewDetail(record){
      this.$router.push({
        name:'FaceMangementDetatil',
        query:record
      })
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