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
        <vxe-button icon="fa fa-plus" @click="employeeAdd()"
          >新增员工</vxe-button
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
      :data="employeeList"
    >
      <vxe-table-column type="seq" width="60"></vxe-table-column>
      <vxe-table-column field="employeeId" title="员工编号"></vxe-table-column>
      <vxe-table-column
        field="employeeName"
        title="员工姓名"
      ></vxe-table-column>
      <vxe-table-column field="employeeAge" title="员工年龄"></vxe-table-column>
      <vxe-table-column
        field="employeeGroup"
        title="员工组别"
      ></vxe-table-column>

      <vxe-table-column title="操作" width="100" show-overflow>
        <template v-slot="{ row }">
          <vxe-button
            type="text"
            title="编辑"
            icon="fa fa-edit"
            @click="employeeEdit(row)"
          ></vxe-button>

          <vxe-button
            type="text"
            title="删除"
            icon="fa fa-trash-o"
            @click="employeeDelete(row)"
          ></vxe-button>
        </template>
      </vxe-table-column>
    </vxe-table>

    <vxe-pager
      border
      size="medium"
      :loading="tableLoading"
      :current-page="employeePage.currentPage"
      :page-size="employeePage.pageSize"
      :total="employeePage.totalResult"
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
          :data="employee"
          :rules="formRules"
          title-align="right"
          title-width="100"
          @submit="submitEvent"
        >
          <vxe-form-item
            title="员工编号"
            field="employeeId"
            span="24"
            :visible="selectAction"
          >
            <template v-slot>
              <vxe-input
                v-model="employee.employeeId"
                placeholder="请输入员工编号"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item title="员工姓名" field="employeeName" span="24">
            <template v-slot>
              <vxe-input
                v-model="employee.employeeName"
                placeholder="请输入员工姓名"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item title="年龄" field="employeeAge" span="24">
            <template v-slot>
              <vxe-input
                v-model="employee.employeeAge"
                placeholder="请输入年龄"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item
            title="员工组别"
            field="employeeGroup"
            span="24"
            :visible="selectAction"
          >
            <template v-slot>
              <vxe-input
                v-model="employee.employeeGroup"
                placeholder="请输入员工组别"
                :disabled="selectAction"
                clearable
              ></vxe-input>
            </template>
          </vxe-form-item>

          <vxe-form-item align="center" span="24" titleAlign="left">
            <template v-slot>
              <vxe-button type="submit" status="primary">提交</vxe-button>
            </template>
          </vxe-form-item></vxe-form
        >
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
      employeeList: [], //员工列表
      employeePage: {
        //分页功能
        currentPage: 1,
        pageSize: 5,
        totalResult: 0,
        searchKey: "",
      },
      searchData: {
        name: "",
      },
      employee: {
        //员工
        employeeId: null,
        employeeName: null,
        employeeAge: null,
        employeeGroup: null,
      },
      formRules: {
        //表单规则
        employeeId: [{ required: true, message: "请输入员工编号" }],
        employeeName: [{ required: true, message: "请输入员工姓名" }],
      },
    };
  },

  mounted() {
    this.employeeListGet();
  },
  methods: {
    searchReset() {
      //重置搜索词
      this.employeePage.searchKey = "";
      this.employeePage.currentPage = 1;
      this.employeeListGet();
    },

    searchEvent() {
      //更新搜索词
      this.employeePage.currentPage = 1;
      this.employeePage.searchKey = this.searchData.name;
      this.employeeListGet();
    },
    handlePageChange({ currentPage, pageSize }) {
      //分页功能
      this.employeePage.currentPage = currentPage;
      this.employeePage.pageSize = pageSize;
      this.employeeListGet();
    },
    employeeListGet() {
      //更加当前页码和每页容纳员工数从服务器请求员工列表
      this.tableLoading = true; //使表格成为加载状态
      service({
        url: "/employee/getList",
        data: {
          page: this.employeePage.currentPage, //当前页码
          size: this.employeePage.pageSize, //每页size条数据
          searchKey: this.employeePage.searchKey,
          //searchKey为搜索词，searchKey为''时返回所有员工数据，不为空时返回符合条件的员工
        },
      })
        .then(({ data }) => {
          console.log(data);
          //resultTotal为总数据条数，resultList为数据列表
          this.employeeList = data.resultList;
          this.employeePage.totalResult = data.resultTotal;
          this.tableLoading = false;
        })
        .catch((e) => {
          this.tableLoading = false;
        });
    },
    submitEvent() {
      this.submitLoading = true;
      if (this.selectAction) {
        //编辑员工
        service({
          url: "/employee/update",
          data: {
            employeeId: this.employee.employeeId,
            employeeName: this.employee.employeeName,
            employeeAge: this.employee.employeeAge,
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
        //新增员工
        service({
          url: "/employee/create",
          data: {
            employeeName: this.employee.employeeName,
            employeeAge: this.employee.employeeAge,
          },
        })
          .then(({ data }) => {
            console.log(data);
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
    employeeAdd() {
      this.employee = {
        //新增员工，初始化员工数据为空
        employeeId: "",
        employeeName: "",
        employeeAge: "",
        employeeGroup: "",
      };
      this.selectAction = false; //新增员工
      this.showEdit = true; //显示编辑框
    },
    employeeEdit(row) {
      console.log(row);
      this.employee = {
        //编辑员工，填入待编辑员工的内容
        employeeId: row.employeeId,
        employeeName: row.employeeName,
        employeeAge: row.employeeAge,
        employeeGroup: row.employeeGroup,
      };
      this.selectAction = true; //编辑员工
      this.showEdit = true; //显示编辑框
    },
    employeeDelete(row) {
      new Promise((resolve, reject) => {
        if (confirm("您确定要删除吗？")) {
          resolve();
        } else {
          reject();
        }
      })
        .then(() => {
          //删除员工
          service({
            url: "/employee/delete",
            data: {
              employeeId: row.employeeId,
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
    employeeListGetLocal() {
      //本地模拟数据
      this.tableLoading = true;
      setTimeout(() => (this.tableLoading = false), 200);
      (this.employeeList = [
        {
          employeeId: 1, //员工ID
          employeeName: "李华", //员工姓名
          employeeGroup: 1, //员工组别
        },
        {
          employeeId: 2, //员工ID
          employeeName: "张三", //员工姓名
          employeeGroup: 1, //员工组别
        },
        {
          employeeId: 3, //员工ID
          employeeName: "李死", //员工姓名
          employeeGroup: 1, //员工组别
        },
        {
          employeeId: 4, //员工ID
          employeeName: "李华", //员工姓名
          employeeGroup: 1, //员工组别
        },
        {
          employeeId: 5, //员工ID
          employeeName: "李华", //员工姓名
          employeeGroup: 1, //员工组别
        },
        {
          employeeId: 6, //员工ID
          employeeName: "李华", //员工姓名
          employeeGroup: 1, //员工组别
        },
      ]),
        (this.employeePage = {
          currentPage: 1,
          pageSize: 5,
          totalResult: 36,
        });
    },
  },
};
</script>