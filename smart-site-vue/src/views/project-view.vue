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
        <vxe-button icon="fa fa-plus" @click="projectAdd()"
          >新增项目</vxe-button
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
      :data="projectList"
    >
      <vxe-table-column type="seq" width="60"></vxe-table-column>
      <vxe-table-column field="projectId" title="项目ID"></vxe-table-column>
      <vxe-table-column field="clientId" title="委托方ID"></vxe-table-column>
      <vxe-table-column
        field="projectManager"
        title="项目负责人"
      ></vxe-table-column>
      <vxe-table-column
        field="projectCheckSystemID"
        title="检查体系ID"
      ></vxe-table-column>
      <vxe-table-column
        field="projectDescription"
        title="项目描述"
      ></vxe-table-column>
      <vxe-table-column
        field="projectCreationTime"
        title="项目创建时间"
      ></vxe-table-column>
      <vxe-table-column field="projectStatus" title="项目状态">
        <template v-slot="{ row }">
          <el-link
            :type="row.projectStatus === '进行中' ? 'primary' : 'success'"
            @click="checkStatusGet()"
            >{{ row.projectStatus }}</el-link
          >
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="projectCheckGroupId"
        title="检查小组编号"
      ></vxe-table-column>
      <!-- <vxe-table-column
        field="projectCheckGroupLeader"
        title="检查小组组长"
      ></vxe-table-column>
      <vxe-table-column
        field="projectCheckGroupMember"
        title="检查小组组员"
      ></vxe-table-column> -->

      <vxe-table-column title="操作" width="100" show-overflow>
        <template v-slot="{ row }">
          <vxe-button
            type="text"
            title="编辑"
            icon="fa fa-edit"
            @click="projectEdit(row)"
          ></vxe-button>

          <vxe-button
            type="text"
            title="删除"
            icon="fa fa-trash-o"
            @click="projectDelete(row)"
          ></vxe-button>
        </template>
      </vxe-table-column>
    </vxe-table>

    <vxe-pager
      border
      size="medium"
      :loading="tableLoading"
      :current-page="projectPage.currentPage"
      :page-size="projectPage.pageSize"
      :total="projectPage.totalResult"
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
          :data="project"
          :items="formItems"
          :rules="formRules"
          title-align="right"
          title-width="120"
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
      projectList: [], //合约列表
      projectPage: {
        //分页功能
        currentPage: 1,
        pageSize: 5,
        totalResult: 0,
        searchKey: "",
      },
      searchData: {
        name: "",
      },
      project: {
        //项目
        projectId: null, //项目ID
        clientId: null, //委托方ID
        projectManager: null, //项目负责人
        projectCheckSystemID: null, //检查体系ID
        projectDescription: null, //项目描述
        projectCreationTime: null, //项目创建时间
        projectStatus: null, //项目状态
        // projectCheckGroupLeader: null,
        // projectCheckGroupMember: null,
        projectCheckGroupId: null,
      },
      formRules: {
        //表单规则
        projectId: [{ required: true, message: "请输入员工编号" }],
        projectName: [{ required: true, message: "请输入员工姓名" }],
        projectCheckGroupId: [
          { required: true, message: "请输入检查小组编号" },
        ], //匹配001-001-003
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
          field: "projectId",
          title: "项目ID",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入项目ID" },
          },
        },
        {
          field: "clientId",
          title: "委托方ID",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入委托方ID" },
          },
        },
        {
          field: "projectManager",
          title: "项目负责人",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入项目负责人" },
          },
        },
        {
          field: "projectCheckSystemID",
          title: "检查体系编号",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入检查体系编号" },
          },
        },
        {
          field: "projectDescription",
          title: "项目描述",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入项目描述" },
          },
        },
        {
          field: "projectCreationTime",
          title: "项目创建时间",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入项目创建时间" },
          },
        },
        {
          field: "projectStatus",
          title: "项目状态",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入项目状态" },
          },
        },
        {
          field: "projectCheckGroupId",
          title: "检查小组编号",
          span: 24,
          itemRender: {
            name: "$input",
            props: { placeholder: "请输入检查小组编号" },
          },
        },
        // {
        //   field: "projectCheckGroupLeader",
        //   title: "检查小组组长",
        //   span: 24,
        //   itemRender: {
        //     name: "$input",
        //     props: { placeholder: "请输入检查小组组长" },
        //   },
        // },
        // {
        //   field: "projectCheckGroupMember",
        //   title: "检查小组组员",
        //   span: 24,
        //   itemRender: {
        //     name: "$input",
        //     props: { placeholder: "请输入检查小组组员" },
        //   },
        // },
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
    this.projectListGetLocal();
  },
  methods: {
    checkStatusGet() {
      console.log(123);
    },
    searchReset() {
      //重置搜索词
      this.projectPage.searchKey = "";
      this.projectPage.currentPage = 1;
      this.projectListGet();
    },

    searchEvent() {
      //更新搜索词
      this.projectPage.currentPage = 1;
      this.projectPage.searchKey = this.searchData.name;
      this.projectListGet();
    },
    handlePageChange({ currentPage, pageSize }) {
      //分页功能
      this.projectPage.currentPage = currentPage;
      this.projectPage.pageSize = pageSize;
      this.projectListGet();
    },
    projectListGet() {
      //更加当前页码和每页容纳合约数从服务器请求合约列表
      this.tableLoading = true; //使表格成为加载状态
      service({
        url: "/project/getList",
        data: {
          page: this.projectPage.currentPage,
          size: this.projectPage.pageSize,
          searchKey: this.projectPage.searchKey,
          //searchKey为搜索词，searchKey为''时返回所有合约数据，不为空时返回符合条件的合约
        },
      })
        .then(({ data }) => {
          console.log(data);
          //resultTotal为总数据条数，resultList为数据列表
          this.projectList = data.resultList;
          this.projectPage.totalResult = data.resultTotal;
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
          url: "/project/update",
          data: {
            projectId: this.project.projectId,
            clientId: this.project.clientId,
            projectManager: this.project.projectDescription,
            projectCheckSystemID: this.project.projectCheckSystemID,
            projectDescription: this.project.projectDescription,
            projectCreationTime: this.project.projectCreationTime,
            // projectCheckGroupLeader: "", //项目状态
            // projectCheckGroupMember: "", //项目状态
            projectCheckGroupId: this.project.projectCheckGroupId,
          },
        })
          .then(({ data }) => {
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.employeeListGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      } else {
        //新增合约
        service({
          url: "/project/create",
          data: {
            projectId: this.project.projectId,
            clientId: this.project.clientId,
            projectManager: this.project.projectDescription,
            projectCheckSystemID: this.project.projectCheckSystemID,
            projectDescription: this.project.projectDescription,
            projectCreationTime: this.project.projectCreationTime,
            // projectCheckGroupLeader: "", //项目状态
            // projectCheckGroupMember: "", //项目状态
            projectCheckGroupId: this.project.projectCheckGroupId,
          },
        })
          .then(({ data }) => {
            this.submitLoading = false;
            this.showEdit = false;
            alert(data.message);
            this.employeeListGet();
          })
          .catch(() => {
            this.submitLoading = false;
            alert("失败");
          });
      }
    },
    projectAdd() {
      this.project = {
        //新增合约，初始化合约数据为空
        projectId: "", //项目ID
        clientId: "", //委托方ID
        projectManager: "", //项目负责人
        projectCheckSystemID: "", //检查体系ID
        projectDescription: "", //项目描述
        projectCreationTime: "", //项目创建时间
        // projectCheckGroupLeader: "", //项目状态
        // projectCheckGroupMember: "", //项目状态
        projectCheckGroupId: "",
      };
      this.selectAction = 0; //新增合约
      this.showEdit = true; //显示编辑框
    },
    projectEdit(row) {
      console.log(row);
      this.project = {
        //编辑合约，填入待编辑合约的内容
        projectId: row.projectId,
        clientId: row.clientId,
        projectManager: row.projectManager,
        projectCheckSystemID: row.projectCheckSystemID,
        projectDescription: row.projectDescription,
        projectCreationTime: row.projectCreationTime,
        projectStatus: row.projectStatus,
        // projectCheckGroupLeader: row.projectCheckGroupLeader,
        // projectCheckGroupMember: row.projectCheckGroupMember,
        projectCheckGroupId: row.projectCheckGroupId,
      };
      this.selectAction = 1; //编辑合约
      this.showEdit = true; //显示编辑框
    },
    projectDelete(row) {
      new Promise((resolve, reject) => {
        if (confirm("您确定要删除吗？")) {
          resolve();
        } else {
          reject();
        }
      })
        .then(() => {
          // 删除合约
          service({
            url: "/project/delete",
            data: {
              projectId: row.projectId,
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
    projectListGetLocal() {
      //本地模拟数据
      this.tableLoading = true;
      setTimeout(() => (this.tableLoading = false), 200);
      (this.projectList = [
        {
          projectId: 1, //项目ID
          clientId: 1, //委托方ID
          projectManager: "王某", //项目负责人
          projectCheckSystemID: 1, //检查体系ID
          projectDescription: "项目描述", //项目描述
          projectCreationTime: "2020.12.2", //项目创建时间
          projectStatus: "进行中", //项目状态
          projectCheckGroupLeader: "001-002-003",
          projectCheckGroupMember: "001-002-003",
          projectCheckGroupId: 1,
        },
        {
          projectId: 2, //项目ID
          clientId: 1, //委托方ID
          projectManager: "王某", //项目负责人
          projectCheckSystemID: 1, //检查体系ID
          projectDescription: "项目描述", //项目描述
          projectCreationTime: "2020.12.2", //项目创建时间
          projectStatus: "已完成", //项目状态
          projectCheckGroupLeader: "001-002-003",
          projectCheckGroupMember: "001-002-003",
          projectCheckGroupId: 1,
        },
        {
          projectId: 3, //项目ID
          clientId: 1, //委托方ID
          projectManager: "王某", //项目负责人
          projectCheckSystemID: 1, //检查体系ID
          projectDescription: "项目描述", //项目描述
          projectCreationTime: "2020.12.2", //项目创建时间
          projectStatus: "已完成", //项目状态
          projectCheckGroupLeader: "001-002-003",
          projectCheckGroupMember: "001-002-003",
          projectCheckGroupId: 1,
        },
        {
          projectId: 4, //项目ID
          clientId: 1, //委托方ID
          projectManager: "王某", //项目负责人
          projectCheckSystemID: 1, //检查体系ID
          projectDescription: "项目描述", //项目描述
          projectCreationTime: "2020.12.2", //项目创建时间
          projectStatus: "已完成", //项目状态

          projectCheckGroupLeader: "001-002-003",
          projectCheckGroupMember: "001-002-003",
          projectCheckGroupId: 1,
        },
        {
          projectId: 5, //项目ID
          clientId: 1, //委托方ID
          projectManager: "王某", //项目负责人
          projectCheckSystemID: 1, //检查体系ID
          projectDescription: "项目描述", //项目描述
          projectCreationTime: "2020.12.2", //项目创建时间
          projectStatus: "已完成", //项目状态
          projectCheckGroupLeader: "001-002-003",
          projectCheckGroupMember: "001-002-003",
          projectCheckGroupId: 1,
        },
      ]),
        (this.projectPage = {
          currentPage: 1,
          pageSize: 5,
          totalResult: 36,
        });
    },
  },
};
</script>