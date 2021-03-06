<template>
  <div>
    <vxe-table
      border
      resizable
      row-key
      show-overflow
      highlight-hover-row
      ref="xTable"
      height="500"
      :loading="tableLoading"
      :data="clientList"
    >
      <vxe-table-column type="seq" width="60"></vxe-table-column>
      <vxe-table-column field="clientId" title="委托方编号"></vxe-table-column>
      <vxe-table-column
        field="clientName"
        title="委托方名称"
      ></vxe-table-column>
      <vxe-table-column
        field="clientDescription"
        title="委托方描述"
      ></vxe-table-column>
      <vxe-table-column title="操作" width="100" show-overflow>
        <template v-slot="{ row }">
          <vxe-button
            type="text"
            title="编辑"
            icon="fa fa-edit"
            @click="clientEdit(row)"
          ></vxe-button>

          <vxe-button
            type="text"
            title="删除"
            icon="fa fa-trash-o"
            @click="clientDelete(row)"
          ></vxe-button>
        </template>
      </vxe-table-column>
    </vxe-table>

    <el-row>
      <el-col :span="24">
        <el-row type="flex" justify="center">
          <vxe-pager
            border
            size="medium"
            :loading="tableLoading"
            :current-page="clientPage.currentPage"
            :page-size="clientPage.pageSize"
            :total="clientPage.totalResult"
            :layouts="[
              'PrevPage',
              'JumpNumber',
              'NextPage',
              'FullJump',
              'Sizes',
              'Total',
            ]"
            @page-change="handlePageChange"
          >
          </vxe-pager
        ></el-row>
      </el-col>
      <el-col :span="24">
        <el-row type="flex" justify="center">
          <vxe-toolbar>
            <template v-slot:buttons>
              <vxe-button icon="fa fa-plus" @click="clientAdd()"
                >新增委托方</vxe-button
              >
            </template>
          </vxe-toolbar>
        </el-row>
      </el-col>
    </el-row>

    <vxe-modal
      v-model="showEdit"
      :title="selectAction ? '编辑&保存' : '新增&保存'"
      width="800"
      min-width="600"
      min-height="300"
      :loading="submitLoading"
      resize
      destroy-on-close
    >
      <template v-slot>
        <vxe-form
          :data="client"
          :rules="formRules"
          title-align="right"
          title-width="100"
          @submit="submitEvent"
        >
          <vxe-form-item
            title="委托方编号"
            field="clientId"
            span="24"
            :visible="selectAction"
          >
            <template v-slot>
              <vxe-input
                v-model="client.clientId"
                placeholder="请输入委托方编号"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>
          <vxe-form-item title="委托方名称" field="clientName" span="24">
            <template v-slot>
              <vxe-input
                v-model="client.clientName"
                placeholder="请输入委托方名称"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>
          <vxe-form-item title="委托方描述" field="clientDescription" span="24">
            <template v-slot>
              <vxe-input
                v-model="client.clientDescription"
                placeholder="请输入委托方描述"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item align="center" span="24" titleAlign="left">
            <template v-slot>
              <vxe-button type="submit" status="primary">提交</vxe-button>
            </template></vxe-form-item
          >
        </vxe-form>
      </template>
    </vxe-modal>
  </div>
</template>
<script>
import service from "../utils/request.js";

export default {
  data() {
    return {
      submitLoading: false, //提交动画
      tableLoading: false,
      selectAction: false, //新增0or编辑1
      showEdit: false, //编辑框
      clientList: [], //合约列表
      clientPage: {
        //分页功能
        currentPage: 1,
        pageSize: 5,
        totalResult: 0,
        searchKey: "",
      },

      client: {
        //合约
        clientId: null,
        clientName: null,
        clientDescription: null,
      },
      formRules: {
        //表单规则
      },
    };
  },

  mounted() {
    this.clientListGet();
  },
  methods: {
    searchReset() {
      //重置搜索词
      this.clientPage.searchKey = "";
      this.clientPage.currentPage = 1;
      this.clientListGet();
    },

    searchEvent(searchInput) {
      //更新搜索词
      console.log(searchInput);
      this.contractPage.currentPage = 1;
      this.contractPage.searchKey = searchInput;
      this.clientListGet();
    },
    handlePageChange({ currentPage, pageSize }) {
      //分页功能
      this.clientPage.currentPage = currentPage;
      this.clientPage.pageSize = pageSize;
      this.clientListGet();
      // this.clientListGetLocal();
    },
    clientListGet() {
      //更加当前页码和每页容纳合约数从服务器请求合约列表
      this.tableLoading = true; //使表格成为加载状态
      service({
        url: "/client/getList",
        data: {
          page: this.clientPage.currentPage,
          size: this.clientPage.pageSize,
          searchKey: this.clientPage.searchKey,
          //searchKey为搜索词，searchKey为''时返回所有合约数据，不为空时返回符合条件的合约
        },
      })
        .then(({ data }) => {
          console.log(data);
          //resultTotal为总数据条数，resultList为数据列表
          this.clientList = data.resultList;
          this.clientPage.totalResult = data.resultTotal;
          this.tableLoading = false;
        })
        .catch((e) => {
          this.tableLoading = false;
        });
    },
    submitEvent() {
      this.submitLoading = true;
      if (this.selectAction) {
        //编辑合约
        service({
          url: "/client/update",
          data: {
            clientId: this.client.clientId,
            clientName: this.client.clientName,
            clientDescription: this.client.clientDescription,
          },
        })
          .then(({ data }) => {
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.clientListGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      } else {
        //新增合约
        service({
          url: "/client/create",
          data: {
            clientName: this.client.clientName,
            clientDescription: this.client.clientDescription,
          },
        })
          .then(({ data }) => {
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.clientListGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      }
    },
    clientAdd() {
      this.client = {
        //新增合约，初始化合约数据为空
        clientId: "",
        clientName: "",
        clientDescription: "",
      };
      this.selectAction = false; //新增合约
      this.showEdit = true; //显示编辑框
    },
    clientEdit(row) {
      this.client = {
        //编辑合约，填入待编辑合约的内容
        clientId: row.clientId,
        clientName: row.clientName,
        clientDescription: row.clientDescription,
      };
      this.selectAction = true; //编辑合约
      this.showEdit = true; //显示编辑框
    },
    clientDelete(row) {
      new Promise((resolve, reject) => {
        if (confirm("您确定要删除吗？")) {
          resolve();
        } else {
          reject();
        }
      })
        .then(() => {
          // 删除合约;
          service({
            url: "/client/delete",
            data: {
              clientId: row.clientId,
            },
          }).then(({ data }) => {
            console.log(data);
            alert(data.message);
            this.clientListGet();
          });
        })
        .catch(() => {
          console.log("删除失败");
        });
    },
    clientListGetLocal() {
      //本地模拟数据
      this.tableLoading = true;
      setTimeout(() => (this.tableLoading = false), 200);
      this.clientList = [
        {
          clientId: 1, //委托方ID
          clientName: 1, //委托方名称
          clientDescription: "合同描述1", //委托方描述
        },
        {
          clientId: 2,
          clientName: 2,
          clientDescription: "合同描述2",
        },
        {
          clientId: 3,
          clientName: 2,
          clientDescription: "合同描述3",
        },
        {
          clientId: 4,
          clientName: 6,
          clientDescription: "合同描述4",
        },
        {
          clientId: 5,
          clientName: 7,
          clientDescription: "合同描述5",
        },
        {
          clientId: 6,
          clientName: 2,
          clientDescription: "合同描述6",
        },
      ];
      this.clientPage = {
        currentPage: 1,
        pageSize: 5,
        totalResult: 36,
      };
    },
  },
};
</script>
