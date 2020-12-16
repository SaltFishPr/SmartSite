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
        <vxe-button icon="fa fa-plus" @click="groupAdd()">新增小组</vxe-button>
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
      :data="groupList"
    >
      <vxe-table-column type="seq" wIdth="60"></vxe-table-column>
      <vxe-table-column field="groupId" title="小组编号"></vxe-table-column>
      <vxe-table-column field="groupLeader" title="小组组长"></vxe-table-column>
      <vxe-table-column field="groupMember" title="小组组员"></vxe-table-column>

      <vxe-table-column title="操作" wIdth="100" show-overflow>
        <template v-slot="{ row }">
          <vxe-button
            type="text"
            title="编辑"
            icon="fa fa-edit"
            @click="groupEdit(row)"
          ></vxe-button>

          <vxe-button
            type="text"
            title="删除"
            icon="fa fa-trash-o"
            @click="groupDelete(row)"
          ></vxe-button>
        </template>
      </vxe-table-column>
    </vxe-table>

    <vxe-pager
      border
      size="medium"
      :loading="tableLoading"
      :current-page="groupPage.currentPage"
      :page-size="groupPage.pageSize"
      :total="groupPage.totalResult"
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
      wIdth="800"
      min-wIdth="600"
      min-height="300"
      :loading="submitLoading"
      resize
      destroy-on-close
    >
      <template v-slot>
        <vxe-form
          :data="group"
          :items="formItems"
          :rules="formRules"
          title-align="right"
          title-wIdth="100"
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
      groupList: [], //小组列表
      groupPage: {
        //分页功能
        currentPage: 1,
        pageSize: 5,
        totalResult: 0,
        searchKey: "",
      },
      searchData: {
        name: "",
      },
      group: {
        //小组
        groupId: null,
        groupLeader: null,
        groupMember: null,
      },
      formRules: {
        //表单规则
        groupId: [
          { required: true, message: "请输入小组编号" },
          { min: 1, max: 5, message: "长度在 3 到 5 个字符" },
        ],
        groupLeader: [
          { required: true, message: "请输入小组组长" },
          {
            pattern: /^\d+(-\d*){0,2}$/,
            message: "请输入员工编号-员工编号-员工编号进行输入",
          },
        ],
        groupMember: [
          { required: true, message: "请输入小组组员" },
          {
            pattern: /^\d+(-\d*){0,2}$/,
            message: "请输入员工编号-员工编号-员工编号进行输入",
          },
        ],
      },
      formItems: [
        //表单项
        {
          title: "Basic information",
          span: 24,
          titleAlign: "left",
          titleWIdth: 200,
          titlePrefix: { icon: "fa fa-address-card-o" },
        },
        {
          field: "groupId",
          title: "小组编号",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入小组编号" },
          },
        },
        {
          field: "groupLeader",
          title: "小组组长",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入小组组长" },
          },
        },
        {
          field: "groupMember",
          title: "小组组员",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入小组组员" },
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
    this.groupListGet();
  },
  methods: {
    searchReset() {
      //重置搜索词
      this.groupPage.searchKey = "";
      this.groupPage.currentPage = 1;
      this.groupListGet();
    },

    searchEvent() {
      //更新搜索词
      this.groupPage.currentPage = 1;
      this.groupPage.searchKey = this.searchData.name;
      this.groupListGet();
    },
    handlePageChange({ currentPage, pageSize }) {
      //分页功能
      this.groupPage.currentPage = currentPage;
      this.groupPage.pageSize = pageSize;
      this.groupListGet();
    },
    groupListGet() {
      //更加当前页码和每页容纳小组数从服务器请求小组列表
      this.tableLoading = true; //使表格成为加载状态
      service({
        url: "/group/getList",
        data: {
          page: this.groupPage.currentPage,
          size: this.groupPage.pageSize,
          searchKey: this.groupPage.searchKey,
          //searchKey为搜索词，searchKey为''时返回所有小组数据，不为空时返回符合条件的小组
        },
      })
        .then(({ data }) => {
          console.log(data);
          //resultTotal为总数据条数，resultList为数据列表
          this.groupList = data.resultList;
          this.groupPage.totalResult = data.resultTotal;
          this.tableLoading = false;
        })
        .catch((e) => {
          this.tableLoading = false;
        });
    },
    submitEvent() {
      this.submitLoading = true;
      console.log(this.group);
      if (this.selectAction) {
        //编辑小组
        service({
          url: "/group/update",
          data: {
            groupId: this.group.groupId,
            groupLeader: this.group.groupLeader,
            groupMember: this.group.groupMember,
          },
        })
          .then(({ data }) => {
            console.log(data);
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.groupListGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      } else {
        //新增小组
        service({
          url: "/group/create",
          data: {
            groupId: this.group.groupId,
            groupLeader: this.group.groupLeader,
            groupMember: this.group.groupMember,
          },
        })
          .then(({ data }) => {
            console.log(data);
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.groupListGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      }
    },
    groupAdd() {
      this.group = {
        //新增小组，初始化小组数据为空
        groupId: "", //合同编号
        groupLeader: "", //合同编号
        groupMember: "", //合同编号
      };
      this.selectAction = 0; //新增小组
      this.showEdit = true; //显示编辑框
    },
    groupEdit(row) {
      this.group = {
        //编辑小组，填入待编辑小组的内容
        groupId: row.groupId,
        groupLeader: row.groupLeader,
        groupMember: row.groupMember,
      };
      this.selectAction = 1; //编辑小组
      this.showEdit = true; //显示编辑框
    },
    groupDelete(row) {
      new Promise((resolve, reject) => {
        if (confirm("您确定要删除吗？")) {
          resolve();
        } else {
          reject();
        }
      })
        .then(() => {
          //删除小组
          // service({
          //   url: "/group/delete",
          //   data: {
          //     groupId: row.groupId,
          //   },
          // });
        })
        .catch(() => {
          console.log("删除失败");
        });
    },
    groupListGetLocal() {
      //本地模拟数据
      this.tableLoading = true;
      setTimeout(() => (this.tableLoading = false), 200);
      this.groupList = [
        {
          groupId: 1, //合同编号
          groupLeader: "001-002", //委托方Id
          groupMember: "003-004", //委托方描述
        },
        {
          groupId: 1, //合同编号
          groupLeader: "001-002", //委托方Id
          groupMember: "003-004", //委托方描述
        },
        {
          groupId: 1, //合同编号
          groupLeader: "001-002", //委托方Id
          groupMember: "003-004", //委托方描述
        },
        {
          groupId: 1, //合同编号
          groupLeader: "001-002", //委托方Id
          groupMember: "003-004", //委托方描述
        },
        {
          groupId: 1, //合同编号
          groupLeader: "001-002", //委托方Id
          groupMember: "003-004", //委托方描述
        },
      ];
      this.groupPage = {
        currentPage: 1,
        pageSize: 5,
        totalResult: 36,
      };
    },
  },
};
</script>