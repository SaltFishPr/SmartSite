<template>
  <div>
    <router-link to="/home/contract">合同管理</router-link> |
    <router-link to="/home/project">项目管理</router-link> |
    <router-link to="/home/employee">人员管理</router-link> |
    <router-link to="/home/group">小组管理</router-link> |
    <router-link to="/home/client">委托方管理</router-link>
    <router-view></router-view>
  </div>
</template>

<script>
export default {};
</script>
