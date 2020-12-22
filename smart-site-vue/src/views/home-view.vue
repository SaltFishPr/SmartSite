<template>
  <div>
    <el-col :span="4">
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        @select="handleSelect"
      >
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-location"></i>
            <span>员工管理</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="/home/employee">人员管理</el-menu-item>
            <el-menu-item index="/home/group">小组管理</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-menu-item index="/home/client">
          <i class="el-icon-menu"></i>
          <span slot="title">委托方管理</span>
        </el-menu-item>

        <el-menu-item index="/home/system">
          <i class="el-icon-document"></i>
          <span slot="title">检查体系管理</span>
        </el-menu-item>

        <el-menu-item index="/home/project">
          <i class="el-icon-setting"></i>
          <span slot="title">项目管理</span>
        </el-menu-item>

        <el-menu-item index="/home/contract">
          <i class="el-icon-setting"></i>
          <span slot="title">合同管理</span>
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="20">
      <router-view></router-view>
    </el-col>
  </div>
</template>

<script>
export default {
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    handleSelect(index) {
      console.log(index);
      this.$router.push({ path: index });
    },
  },
};
</script>
