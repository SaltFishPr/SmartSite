<template>
  <div>
    <router-link to="/login">login</router-link> |
    <router-link to="/register">register</router-link>
    <div><input type="text" placeholder="account" /></div>
    <div><input type="password" placeholder="password" /></div>
    <div><input type="button" value="登录" @click="login" /></div>
  </div>
</template>

<script>
export default {
  methods: {
    login() {
      this.$router.push({ path: "/home" });
    },
  },
};
</script>