<template>
  <div class="recognition-page-container">
    <div class="page-title">Nhật ký nhận diện</div>
    <div class="recognition-history">
      <div class="table-action">
        <a-input-search
          placeholder="Tìm kiếm theo tên đăng nhập, thư điện tử và họ tên"
          style="width: 400px"
          @search="onSearch"
          @change="onSearchBoxChange"
        />
        <a-range-picker v-model:value="dateRange" :format="dateFormat" :locale="locale"  />
      </div>

      <a-table
        :columns="columns"
        :data-source="data"
        :pagination="pagination"
        :loading="loading"
        @change="handleTableChange"
        bordered
        size="middle"
      >
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'Action'"> </template>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script>
 import locale from 'ant-design-vue/es/date-picker/locale/vi_VN';
import {
  DeleteTwoTone,
  ExclamationCircleOutlined,
  FolderViewOutlined,
  SmileOutlined,
} from "@ant-design/icons-vue";
import { mask, unMask } from "@/utils";
import moment from 'moment';
import { httpClient } from '@/apis/httpclient';
export default {
  components: {
    DeleteTwoTone,
    FolderViewOutlined,
    SmileOutlined,
  },
  data() {
    return {
      locale:locale,
      dateFormat : 'YYYY/MM/DD',
      dateRange:  null, //[moment().startOf('day'), moment().endOf('day')],
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
          dataIndex: "LastName",
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
      ],
      data: [],
      searchValue:null,
      pagination: {
        total: 0,
        current: 1,
        pageSize: 20,
      },
    };
  },
  methods: {
    //Gọi api lần đầu
    async initvalue() {
      const me= this;
      mask();
      let skip = (me.pagination.current-1)*me.pagination.pageSize;
      let take = me.pagination.current*me.pagination.pageSize-1;
      // Lấy thời điểm bắt đầu của ngày hôm nay
      let startOfDay = moment().startOf('day').format('YYYY-MM-DDTHH:mm:ss');

      //Lấy thời điểm cuối ngày
      let endOfDay = moment().endOf('day').format('YYYY-MM-DDTHH:mm:ss');
      let params={
        skip:skip,
        take:take,
        fromDate:startOfDay,
        toDate:endOfDay
      }
      if(me.searchValue){
        params.searchValue=me.searchValue
      }
      let ans =  await httpClient.get(`recognition-history`,{params:params})
      console.log(ans)
      unMask();
    },
    /**
     * Buil object trả về từ elastic search
     * @param {*} res 
     */
    buildObject(res){

    }
  },
  created() {
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
}
</style>