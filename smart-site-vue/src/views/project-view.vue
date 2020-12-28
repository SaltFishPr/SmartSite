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
            :data="projectList"
        >
            <vxe-table-column type="seq" width="60"></vxe-table-column>
            <vxe-table-column field="projectId" title="项目ID"></vxe-table-column>
            <vxe-table-column field="clientId" title="委托方ID"></vxe-table-column>
            <vxe-table-column field="projectCheckSystemId" title="检查体系ID"></vxe-table-column>
            <vxe-table-column field="projectStatus" title="项目状态">
                <template v-slot="{ row }">
                    <el-link :type="row.projectStatus === '未完成' ? 'primary' : 'success'" @click="checksGet(row)">{{
                        row.projectStatus
                    }}</el-link>
                </template>
            </vxe-table-column>
            <vxe-table-column field="projectRiskValue" title="项目风险值"></vxe-table-column>
            <vxe-table-column field="projectCreationTime" title="项目创建时间"></vxe-table-column>
            <vxe-table-column field="projectDescription" title="项目描述"></vxe-table-column>
            <vxe-table-column field="projectManager" title="项目管理人"></vxe-table-column>
            <vxe-table-column field="projectCheckGroupId" title="检查小组ID"></vxe-table-column>

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
                    <vxe-button type="text" title="编辑" icon="fa fa-edit" @click="projectEdit(row)"></vxe-button>

                    <vxe-button type="text" title="删除" icon="fa fa-trash-o" @click="projectDelete(row)"></vxe-button>
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
                        :current-page="projectPage.currentPage"
                        :page-size="projectPage.pageSize"
                        :total="projectPage.totalResult"
                        :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
                        @page-change="handlePageChange"
                    >
                    </vxe-pager>
                </el-row>
            </el-col>
            <el-col :span="24">
                <el-row type="flex" justify="center">
                    <vxe-toolbar>
                        <template v-slot:buttons>
                            <vxe-button icon="fa fa-plus" @click="projectAdd()">新增项目</vxe-button>
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
                    :data="project"
                    :rules="formRules"
                    title-align="right"
                    title-width="120"
                    @submit="submitEvent"
                >
                    <vxe-form-item title="项目编号" field="projectId" span="24" :visible="selectAction">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectId"
                                placeholder="请输入项目编号"
                                :disabled="selectAction"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>

                    <vxe-form-item title="委托方编号" field="clientId" span="24">
                        <template v-slot>
                            <vxe-input
                                v-model="project.clientId"
                                placeholder="请输入委托方编号"
                                :disabled="selectAction"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>

                    <vxe-form-item title="检查体系" field="projectCheckSystemId" span="24">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectCheckSystemId"
                                placeholder="请输入检查体系"
                                :disabled="selectAction"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>

                    <vxe-form-item title="项目状态" field="projectStatus" span="24" :visible="selectAction">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectStatus"
                                placeholder="请输入项目状态"
                                :disabled="selectAction"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>
                    <vxe-form-item title="风险评估" field="projectRiskValue" span="24" :visible="selectAction">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectRiskValue"
                                placeholder="请输入风险评估"
                                :disabled="selectAction"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>
                    <vxe-form-item title="项目创建时间" field="projectCreationTime" span="24" :visible="selectAction">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectCreationTime"
                                placeholder="项目创建时间"
                                :disabled="selectAction"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>
                    <vxe-form-item title="项目描述" field="projectDescription" span="24">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectDescription"
                                placeholder="项目描述"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>
                    <vxe-form-item title="项目负责人" field="projectManager" span="24">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectManager"
                                placeholder="请输入项目负责人"
                                clearable
                            ></vxe-input>
                        </template>
                    </vxe-form-item>
                    <vxe-form-item title="检查小组" field="projectCheckGroupId" span="24">
                        <template v-slot>
                            <vxe-input
                                v-model="project.projectCheckGroupId"
                                placeholder="项目检查小组"
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

        <vxe-modal v-model="showCheck" width="600" min-height="200" resize>
            <template v-slot>
                <el-collapse v-model="checkNames" @change="handleChange">
                    <el-collapse-item
                        v-for="check in checks"
                        :key="check.title"
                        :title="check.title"
                        :name="check.title"
                    >
                        <div>{{ check.description }}</div>
                        <el-image style="width: 100%; height: auto" :src="check.pic"></el-image>
                        <div>
                            提交员工:<span>{{ check.employeeName }}</span>
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </template>
        </vxe-modal>
    </div>
</template>
<script>
import service from "../utils/request.js";

export default {
    data() {
        return {
            checks: [
                {
                    title: "12",
                    pic: "312",
                    employeeName: "123",
                    description: "2121"
                },
                {
                    title: "332",
                    pic: "12",
                    employeeName: "31",
                    description: "12312"
                }
            ],
            showCheck: false,
            checkNames: [],
            submitLoading: false, //提交动画
            tableLoading: false,
            selectAction: false, //新增0or编辑1
            showEdit: false, //编辑框
            projectList: [], //合约列表
            projectPage: {
                //分页功能
                currentPage: 1,
                pageSize: 5,
                totalResult: 0,
                searchKey: ""
            },

            project: {
                //项目
                projectId: null, //项目ID
                clientId: null, //委托方ID
                projectManager: null, //项目负责人
                projectCheckSystemId: null, //检查体系ID
                projectDescription: null, //项目描述
                projectCreationTime: null, //项目创建时间
                projectStatus: null, //项目状态
                projectRiskValue: null,
                projectCheckGroupId: null
            },
            formRules: {
                //表单规则

                projectCheckGroupId: [{ required: true, message: "请输入检查小组编号" }] //匹配001-001-003
            }
        };
    },

    mounted() {
        this.projectListGet();
    },
    methods: {
        handleChange(val) {
            console.log(val);
            console.log(this.checkNames);
        },
        checkStatusGet() {
            console.log(123);
        },

        checksGet(row) {
            this.showCheck = true;
            console.log(row);
            service({
                url: "/project/getCheckInfo",
                data: {
                    projectId: row.projectId,
                    systemId: row.projectCheckSystemId
                }
            })
                .then(({ data }) => {
                    console.log(data);
                    this.checks = data.checks;
                })
                .catch(e => {
                    console.log("数据加载失败");
                });
        },

        searchReset() {
            //重置搜索词
            this.projectPage.searchKey = "";
            this.projectPage.currentPage = 1;
            this.projectListGet();
        },

        searchEvent(searchInput) {
            //更新搜索词
            console.log(searchInput);
            this.contractPage.currentPage = 1;
            this.contractPage.searchKey = searchInput;
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
                    searchKey: this.projectPage.searchKey
                    //searchKey为搜索词，searchKey为''时返回所有合约数据，不为空时返回符合条件的合约
                }
            })
                .then(({ data }) => {
                    console.log(data);
                    //resultTotal为总数据条数，resultList为数据列表
                    this.projectList = data.resultList;
                    this.projectPage.totalResult = data.resultTotal;
                    this.tableLoading = false;
                })
                .catch(e => {
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
                        projectManager: this.project.projectManager,
                        projectCheckSystemId: this.project.projectCheckSystemId,
                        projectDescription: this.project.projectDescription,
                        projectCreationTime: this.project.projectCreationTime,
                        projectStatus: this.project.projectStatus,
                        projectRiskValue: this.project.projectRiskValue,
                        projectCheckGroupId: this.project.projectCheckGroupId
                    }
                })
                    .then(({ data }) => {
                        this.submitLoading = false;
                        this.showEdit = false;
                        alert(data.message);
                        this.projectListGet();
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
                        clientId: this.project.clientId,
                        projectManager: this.project.projectManager,
                        projectCheckSystemId: this.project.projectCheckSystemId,
                        projectDescription: this.project.projectDescription,
                        projectStatus: this.project.projectStatus,
                        projectRiskValue: this.project.projectRiskValue,
                        projectCheckGroupId: this.project.projectCheckGroupId
                    }
                })
                    .then(({ data }) => {
                        this.submitLoading = false;
                        this.showEdit = false;
                        alert(data.message);
                        this.projectListGet();
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
                projectId: "",
                clientId: "",
                projectManager: "",
                projectCheckSystemId: "",
                projectDescription: "",
                projectCreationTime: "",
                projectStatus: "",
                projectRiskValue: "",
                projectCheckGroupId: ""
            };
            this.selectAction = false; //新增合约
            this.showEdit = true; //显示编辑框
        },
        projectEdit(row) {
            console.log(row);
            this.project = {
                //编辑合约，填入待编辑合约的内容
                projectId: row.projectId,
                clientId: row.clientId,
                projectManager: row.projectManager,
                projectCheckSystemId: row.projectCheckSystemId,
                projectDescription: row.projectDescription,
                projectCreationTime: row.projectCreationTime,
                projectStatus: row.projectStatus,
                projectRiskValue: row.projectRiskValue,
                projectCheckGroupId: row.projectCheckGroupId
            };
            this.selectAction = true; //编辑合约
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
                            projectId: row.projectId
                        }
                    }).then(({ data }) => {
                        console.log(data);
                        alert(data.message);
                        this.projectListGet();
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
                    projectCheckSystemId: 1, //检查体系ID
                    projectDescription: "项目描述", //项目描述
                    projectCreationTime: "2020.12.2", //项目创建时间
                    projectStatus: "进行中", //项目状态
                    projectCheckGroupLeader: "001-002-003",
                    projectCheckGroupMember: "001-002-003",
                    projectCheckGroupId: 1
                },
                {
                    projectId: 2, //项目ID
                    clientId: 1, //委托方ID
                    projectManager: "王某", //项目负责人
                    projectCheckSystemId: 1, //检查体系ID
                    projectDescription: "项目描述", //项目描述
                    projectCreationTime: "2020.12.2", //项目创建时间
                    projectStatus: "已完成", //项目状态
                    projectCheckGroupLeader: "001-002-003",
                    projectCheckGroupMember: "001-002-003",
                    projectCheckGroupId: 1
                },
                {
                    projectId: 3, //项目ID
                    clientId: 1, //委托方ID
                    projectManager: "王某", //项目负责人
                    projectCheckSystemId: 1, //检查体系ID
                    projectDescription: "项目描述", //项目描述
                    projectCreationTime: "2020.12.2", //项目创建时间
                    projectStatus: "已完成", //项目状态
                    projectCheckGroupLeader: "001-002-003",
                    projectCheckGroupMember: "001-002-003",
                    projectCheckGroupId: 1
                },
                {
                    projectId: 4, //项目ID
                    clientId: 1, //委托方ID
                    projectManager: "王某", //项目负责人
                    projectCheckSystemId: 1, //检查体系ID
                    projectDescription: "项目描述", //项目描述
                    projectCreationTime: "2020.12.2", //项目创建时间
                    projectStatus: "已完成", //项目状态

                    projectCheckGroupLeader: "001-002-003",
                    projectCheckGroupMember: "001-002-003",
                    projectCheckGroupId: 1
                },
                {
                    projectId: 5, //项目ID
                    clientId: 1, //委托方ID
                    projectManager: "王某", //项目负责人
                    projectCheckSystemId: 1, //检查体系ID
                    projectDescription: "项目描述", //项目描述
                    projectCreationTime: "2020.12.2", //项目创建时间
                    projectStatus: "已完成", //项目状态
                    projectCheckGroupLeader: "001-002-003",
                    projectCheckGroupMember: "001-002-003",
                    projectCheckGroupId: 1
                }
            ]),
                (this.projectPage = {
                    currentPage: 1,
                    pageSize: 5,
                    totalResult: 36
                });
        }
    }
};
</script>
