<template>
  <div>
    <router-link to="/login">login</router-link> |
    <router-link to="/register">register</router-link>
    <div><input type="text" placeholder="account" v-model="account" /></div>
    <div>
      <input type="password" placeholder="password" v-model="password" />
    </div>
    <div><input type="button" value="登录" @click="login" /></div>
  </div>
</template>

<script>
import service from "../utils/request.js";

export default {
  data() {
    return {
      account: "",
      password: "",
    };
  },
  methods: {
    login() {
      service({
        url: "/login",
        data: {
          account: this.account,
          password: this.password,
        },
      })
        .then(({ data }) => {
          if (data.flag) {
            alert(data.message);
            this.$router.push({ path: "/home" });
          } else {
            alert(data.message);
          }
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
};
</script>