<template>
    <div>
        <el-row class="header">
            <el-col :span="16">
                <el-row type="flex" justify="start">
                    <div class="title">智能工地管理系统</div>
                    <el-menu
                        default-active="2"
                        class="el-menu-vertical-demo"
                        mode="horizontal"
                        background-color="#c0c0c0"
                        text-color="#fff"
                        active-text-color="#0080ff"
                        @select="handleSelect"
                    >
                        <el-menu-item index="/home/contract">
                            <i class="el-icon-document"></i>
                            <span slot="title">合同管理</span>
                        </el-menu-item>
                        <el-menu-item index="/home/client">
                            <i class="el-icon-school"></i>
                            <span slot="title">委托方管理</span>
                        </el-menu-item>
                        <el-menu-item index="/home/project">
                            <i class="el-icon-office-building"></i>
                            <span slot="title">项目管理</span>
                        </el-menu-item>
                        <el-submenu index="1">
                            <template slot="title">
                                <i class="el-icon-user"></i>
                                <span>员工管理</span>
                            </template>
                            <el-menu-item-group>
                                <el-menu-item index="/home/employee">人员管理</el-menu-item>
                                <el-menu-item index="/home/group">小组管理</el-menu-item>
                            </el-menu-item-group>
                        </el-submenu>

                        <el-menu-item index="/home/system">
                            <i class="el-icon-tickets"></i>
                            <span slot="title">检查体系管理</span>
                        </el-menu-item>
                    </el-menu>
                </el-row>
            </el-col>
            <el-col :span="6" class="search">
                <el-input type="text" placeholder="请输入内容" v-model="searchInput">
                    <el-button slot="append" icon="el-icon-search" @click="searchEvent" title="搜索"></el-button>
                    <el-button slot="append" icon="el-icon-refresh-left" @click="searchReset" title="重置"></el-button>
                </el-input>
            </el-col>

            <el-col :span="2">
                <el-row type="flex" justify="end">
                    <div class="quit" @click="quitSystem">退出</div>
                </el-row></el-col
            >
        </el-row>
        <el-col :span="24">
            <router-view ref="mainContent"> </router-view>
        </el-col>
    </div>
</template>

<script>
export default {
    data() {
        return {
            searchInput: ""
        };
    },
    methods: {
        searchEvent() {
            console.log(321);
            console.log(this.searchInput);
            this.$refs.mainContent.searchEvent(this.searchInput);
        },
        searchReset() {
            this.searchInput = "";
            this.$refs.mainContent.searchReset();
        },
        handleSelect(index) {
            console.log(index);
            this.$router.push({ path: index });
        },
        quitSystem() {
            console.log(123);
            new Promise((resolve, reject) => {
                if (confirm("您确定要退出系统吗吗？")) {
                    resolve();
                } else {
                    reject();
                }
            })
                .then(() => {
                    this.$store.commit("verificationGet", "jl");
                    sessionStorage.setItem("verification", "jl");
                    this.$router.push({ path: "/login" });
                })
                .catch(() => {
                    console.log("取消退出");
                });
        }
    }
};
</script>

<style>
.header {
    height: 60px;
    background-color: #c0c0c0;
}

.title {
    width: auto;
    cursor: pointer;
    line-height: 60px;
    font-size: 32px;
    padding-left: 20px;
    padding-right: 20px;
}

.quit {
    width: auto;
    cursor: pointer;
    line-height: 60px;
    font-size: 24px;
    padding-right: 20px;
    text-decoration: underline;
    color: #0080ff;
}

.search {
    line-height: 60px;
}
</style>
