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

    <el-row>
      <el-col :span="24">
        <el-row type="flex" justify="center">
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
              'Total',
            ]"
            @page-change="handlePageChange"
          >
          </vxe-pager>
        </el-row>
      </el-col>
      <el-col :span="24">
        <el-row type="flex" justify="center">
          <vxe-toolbar>
            <template v-slot:buttons>
              <vxe-button icon="fa fa-plus" @click="groupAdd()"
                >新增小组</vxe-button
              >
            </template>
          </vxe-toolbar>
        </el-row>
      </el-col>
    </el-row>

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
          :rules="formRules"
          title-align="right"
          title-wIdth="100"
          @submit="submitEvent"
        >
          <vxe-form-item title="小组编号" field="groupId" span="24">
            <template v-slot>
              <vxe-input
                v-model="group.groupId"
                placeholder="请输入小组编号"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>
          <vxe-form-item title="小组成员" field="groupMember" span="24">
            <template v-slot>
              <vxe-input
                v-model="group.groupMember"
                placeholder="请输入小组成员"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>
          <vxe-form-item title="小组组长" field="groupLeader" span="24">
            <template v-slot>
              <vxe-input
                v-model="group.groupLeader"
                placeholder="请输入小组组长"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item align="center" span="24" titleAlign="left">
            <template v-slot>
              <vxe-button type="submit" status="primary">提交</vxe-button>
            </template>
          </vxe-form-item>
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
      groupList: [], //小组列表
      groupPage: {
        //分页功能
        currentPage: 1,
        pageSize: 5,
        totalResult: 0,
        searchKey: "",
      },

      group: {
        //小组
        groupId: null,
        groupLeader: null,
        groupMember: null,
      },
      formRules: {
        //表单规则

        groupLeader: [
          { required: true, message: "请输入小组组长" },
          {
            pattern: /^\d+(-\d*){0,2}$/,
            message: "请按员工编号-员工编号-员工编号进行输入",
          },
        ],
        groupMember: [
          { required: true, message: "请输入小组组员" },
          {
            pattern: /^\d+(-\d*){0,2}$/,
            message: "请按员工编号-员工编号-员工编号进行输入",
          },
        ],
      },
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

    searchEvent(searchInput) {
      //更新搜索词
      console.log(searchInput);
      this.contractPage.currentPage = 1;
      this.contractPage.searchKey = searchInput;
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
          this.groupList = data["resultList"];
          this.groupPage.totalResult = data["resultTotal"];
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
            groupLeader: this.group.groupLeader,
            groupMember: this.group.groupMember,
            groupId: this.group.groupId,
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
      this.selectAction = false; //新增小组
      this.showEdit = true; //显示编辑框
    },
    groupEdit(row) {
      this.group = {
        //编辑小组，填入待编辑小组的内容
        groupId: row.groupId,
        groupLeader: row.groupLeader,
        groupMember: row.groupMember,
      };
      this.selectAction = true; //编辑小组
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
          service({
            url: "/group/delete",
            data: {
              groupId: row.groupId,
            },
          }).then(({ data }) => {
            console.log(data);
            alert(data.message);
            this.groupListGet();
          });
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
