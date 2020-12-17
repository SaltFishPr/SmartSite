<template>
  <div>
    <router-link to="/login">login</router-link> |
    <router-link to="/register">register</router-link>
    <div><input type="text" placeholder="account" v-model="account" /></div>
    <div>
      <input type="password" placeholder="password" v-model="password_1" />
    </div>
    <div>
      <input type="password" placeholder="password" v-model="password_2" />
    </div>
    <div><input type="button" value="注册" @click="register" /></div>
  </div>
</template>

<script>
import service from "../utils/request.js";

export default {
  data() {
    return {
      account: "",
      password_1: "",
      password_2: "",
    };
  },
  methods: {
    register() {
      if (this.password_1 !== this.password_2) {
        alert("两次密码不一致");
        return;
      }
      service({
        url: "/register",
        data: {
          account: this.account,
          password: this.password_1,
        },
      })
        .then(({ data }) => {
          if (data.flag) {
            alert(data.message);
            this.$router.push({ path: "/login" });
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