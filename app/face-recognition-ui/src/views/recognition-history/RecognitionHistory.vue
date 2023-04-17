<template>
  <div class="recognition-page-container">
    <div class="page-title">Nhật ký nhận diện</div>
    <div class="recognition-history">
      <div class="table-action">
        <a-input-search
          placeholder="Tìm kiếm theo tên đăng nhập, thư điện tử và họ tên"
          style="width: 400px"
          @search="initvalue"
        />
        <a-range-picker
          v-model:value="dateRange"
          :locale="locale"
          @change="initvalue"
        />
      </div>

      <a-table
        :columns="columns"
        :data-source="data"
        :pagination="pagination"
        @change="handleTableChange"
        bordered
        size="middle"
      >
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'Status'">
            <div v-if="record.Status == 1" class="real-status">Thật</div>
            <div v-else>Giả mạo</div>
          </template>
          <template v-else-if="column.dataIndex === 'Score'">
            {{ Math.round(record.Score * 100) }}%
          </template>
          <template v-else-if="column.dataIndex === 'CreatedDate'">
            {{ formatDate(record.CreatedDate) }}
          </template>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script>
import locale from "ant-design-vue/es/date-picker/locale/vi_VN";
import {
  DeleteTwoTone,
  ExclamationCircleOutlined,
  FolderViewOutlined,
  SmileOutlined,
} from "@ant-design/icons-vue";
import { mask, unMask } from "@/utils";
import moment from "moment";
import { httpClient } from "@/apis/httpclient";
export default {
  components: {
    DeleteTwoTone,
    FolderViewOutlined,
    SmileOutlined,
  },
  data() {
    return {
      locale: locale,
      dateRange: null,
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
          title: "Họ Tên",
          dataIndex: "FullName",
          key: "FullName",
          ellipsis: true,
        },
        {
          title: "Tình trạng giả mạo",
          children: [
            {
              title: "Trạng thái",
              dataIndex: "Status",
              key: "Status",
              ellipsis: true,
            },
            {
              title: "Độ chính xác",
              dataIndex: "Score",
              key: "Score",
              ellipsis: true,
            },
          ],
        },
        {
          title: "Thời điểm",
          dataIndex: "CreatedDate",
          key: "CreatedDate",
          ellipsis: true,
        },
      ],
      data: [],
      searchValue: null,
      pagination: {
        total: 0,
        current: 1,
        pageSize: 20,
      },
    };
  },
  methods: {
    formatDate(date) {
      return moment(date, "YYYY-MM-DDTHH:mm:ss").format("DD/MM/YYYY HH:mm:ss");
    },
    async handleTableChange(pag, filters, sorter) {
      this.pagination = pag;
      await this.initvalue();
    },
    //Gọi api lần đầu
    async initvalue() {
      const me = this;
      mask();
      let skip = (me.pagination.current - 1) * me.pagination.pageSize;
      let take = me.pagination.current * me.pagination.pageSize - 1;
      let fromDate = moment().startOf("day").format("YYYY-MM-DDTHH:mm:ss");
      let toDate = moment().endOf("day").format("YYYY-MM-DDTHH:mm:ss");
      if (me.dateRange) {
        fromDate = me.dateRange[0].startOf("day").format("YYYY-MM-DDTHH:mm:ss");
        toDate = me.dateRange[1].endOf("day").format("YYYY-MM-DDTHH:mm:ss");
      }
      let params = {
        skip: skip,
        take: take,
        fromDate: fromDate,
        toDate: toDate,
      };
      if (me.searchValue) {
        params.searchValue = me.searchValue;
      }
      let ans = (
        await httpClient.get(`recognition-history`, { params: params })
      ).data;
      me.pagination.total = ans.hits.total.value;
      me.data = ans.hits.hits.map((x) => x._source);
      unMask();
    },
  },
  created() {
    // this.dateRange = [moment(), moment()];
    // console.log(this.dateRange)
    this.initvalue();
  },
};
</script>
<style lang="scss" scoped>
.recognition-page-container {
  // width: 90%;
  // height: 80vh;
  // background-color: #ffff;
  // border-radius: 12px;
  // margin: 24px auto;
  // padding: 24px;

  .page-title {
    display: flex;
    flex-direction: column;
    margin-bottom: 24px;
  }
  .recognition-history {
    .table-action {
      display: flex;
      width: 100%;
      justify-content: space-between;
      margin-bottom: 24px;
    }
  }
  .real-status {
    background-color: rgb(195, 236, 195);
    color: rgb(33, 156, 33);
    width: fit-content;
    padding: 0px 12px;
    border-radius: 4px;
    font-size: 16px;
    font-weight: 600;
  }
}
</style>