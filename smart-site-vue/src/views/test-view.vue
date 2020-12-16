<template>
  <div>
    <vxe-form :data="searchData" @submit="searchEvent" @reset="searchReset">
      <vxe-form-item
        field="name"
        :item-render="{
          name: 'input',
          attrs: { placeholder: '请输入名称' },
        }"
      ></vxe-form-item>
      <vxe-form-item
        :item-render="{
          name: '$buttons',
          children: [
            {
              props: {
                type: 'submit',
                content: '查询',
                status: 'primary',
              },
            },
            { props: { type: 'reset', content: '重置' } },
          ],
        }"
      ></vxe-form-item>
    </vxe-form>
    <vxe-toolbar>
      <template v-slot:buttons>
        <vxe-button icon="fa fa-plus" @click="clientAdd()"
          >新增委托方</vxe-button
        >
      </template>
    </vxe-toolbar>

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
    </vxe-pager>

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
          :items="formItems"
          :rules="formRules"
          title-align="right"
          title-width="100"
          @submit="submitEvent"
        ></vxe-form>
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
      selectAction: 0, //新增0or编辑1
      showEdit: false, //编辑框
      clientList: [], //合约列表
      clientPage: {
        //分页功能
        currentPage: 1,
        pageSize: 5,
        totalResult: 0,
        searchKey: "",
      },
      searchData: {
        name: "",
      },
      client: {
        //合约
        clientId: null,
        clientName: null,
        clientDescription: null,
      },
      formRules: {
        //表单规则
        clientId: [
          { required: true, message: "请输入委托方编号" },
          { min: 1, max: 5, message: "长度在 3 到 5 个字符" },
        ],
      },
      formItems: [
        //表单项
        {
          title: "Basic information",
          span: 24,
          titleAlign: "left",
          titleWidth: 200,
          titlePrefix: { icon: "fa fa-address-card-o" },
        },
        {
          field: "clientId",
          title: "委托方编号",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入委托方编号" },
          },
        },
        {
          field: "clientName",
          title: "委托方名称",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入委托方名称号" },
          },
        },
        {
          field: "clientDescription",
          title: "委托方描述",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入委托方描述" },
          },
        },
        {
          align: "center",
          span: 24,
          titleAlign: "left",
          itemRender: {
            name: "$button",
            props: { type: "submit", content: "提交", status: "primary" },
          },
        },
      ],
    };
  },

  mounted() {
    this.clientListGetLocal();
  },
  methods: {
    searchReset() {
      //重置搜索词
      this.clientPage.searchKey = "";
      this.clientPage.currentPage = 1;
      this.clientListGet();
    },

    searchEvent() {
      //更新搜索词
      this.clientPage.currentPage = 1;
      this.clientPage.searchKey = this.searchData.name;
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
        .then(({ resultTotal, resultList }) => {
          //resultTotal为总数据条数，resultList为数据列表
          this.staffList = resultList;
          this.staffPage.totalResult = resultTotal;
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
          .catch(({ data }) => {
            this.submitLoading = false;
            alert(data.message);
          });
      } else {
        //新增合约
        service({
          url: "/client/create",
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
          .catch(({ data }) => {
            this.submitLoading = false;
            alert(data.message);
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
      this.selectAction = 0; //新增合约
      this.showEdit = true; //显示编辑框
    },
    clientEdit(row) {
      this.client = {
        //编辑合约，填入待编辑合约的内容
        clientId: row.clientId,
        clientName: row.clientName,
        clientDescription: row.clientDescription,
      };
      this.selectAction = 1; //编辑合约
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
          clientId: 1, //合同编号
          clientName: 1, //委托方ID
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