<template>
    <div class="login">
        <div class="content">
            <div class="content_input">
                <div class="title">
                    <p>{{ selectAction ? "注册" : "管理员登录" }}</p>
                </div>
                <el-input v-model="account" clearable placeholder="用户名"></el-input>
                <el-input v-model="password" clearable show-password placeholder="密码"></el-input>
                <el-input
                    v-model="passwordConfirm"
                    clearable
                    show-password
                    placeholder="确认密码"
                    v-show="selectAction"
                ></el-input>
                <div class="content_button">
                    <el-button type="primary" @click="submit">{{ selectAction ? "注册" : "登录" }}</el-button>
                </div>
                <div class="help" @click="actionChange">
                    {{ selectAction ? "去登录" : "去注册" }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import service from "../utils/request.js";

export default {
    mounted() {
        let x = document.querySelector(".login");
        let y = document.createElement("script");
        y.setAttribute("src", "/external/ribbon.js");
        x.appendChild(y);
        console.log(x);
    },

    destroyed() {
        document.body.removeChild(document.querySelector("#bgCanvas"));
    },
    data() {
        return {
            account: "",
            password: "",
            passwordConfirm: "",
            selectAction: false //true为注册,false为登录
        };
    },
    methods: {
        actionChange() {
            this.account = "";
            this.password = "";
            this.passwordConfirm = "";
            this.selectAction = !this.selectAction;
        },

        submit() {
            if (this.selectAction) this.register();
            else this.login();
        },

        login() {
            service({
                url: "/auth/login",
                data: {
                    account: this.account,
                    password: this.password
                }
            })
                .then(({ data }) => {
                    if (data.flag) {
                        alert(data.message);
                        this.$store.commit("verificationGet", data.verification);
                        sessionStorage.setItem("verification", data.verification);
                        this.$router.push({ path: "/home/contract" });
                    } else {
                        alert(data.message);
                    }
                })
                .catch(e => {
                    console.log(e);
                });
        },
        register() {
            if (this.password !== this.passwordConfirm) {
                alert("两次密码不一致");
                return;
            }
            service({
                url: "/auth/register",
                data: {
                    account: this.account,
                    password: this.password,
                    identity: "admin"
                }
            })
                .then(({ data }) => {
                    if (data.flag) {
                        alert(data.message);
                    } else {
                        alert(data.message);
                    }
                })
                .catch(e => {
                    console.log(e);
                });
        }
    }
};
</script>

<style>
@charset "utf-8";
* {
    padding: 0;
    margin: 0;
}

.content {
    width: 500px;
    height: 400px;
    box-sizing: border-box;
    padding: 0 50px;
    border-radius: 5px;
    box-shadow: 0px 2px 12px 0px rgba(105, 105, 105, 0.07);
    background: rgba(255, 255, 255, 0.5);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: mymove 1s ease-in-out alternate;
    overflow: hidden;
    transition: 1.5s;
}

@keyframes mymove {
    0% {
        width: 0px;
        height: 5px;
    }

    10% {
        width: 50px;
        height: 5px;
    }

    15% {
        width: 100px;
        height: 5px;
    }

    20% {
        width: 150px;
        height: 5px;
    }

    25% {
        width: 200px;
        height: 5px;
    }

    30% {
        width: 250px;
        height: 5px;
    }

    35% {
        width: 300px;
        height: 5px;
    }

    40% {
        width: 350px;
        height: 5px;
    }

    45% {
        width: 450px;
        height: 5px;
    }

    50% {
        width: 500px;
        height: 5px;
    }

    55% {
        height: 30px;
    }

    60% {
        height: 60px;
    }

    65% {
        height: 90px;
    }

    70% {
        height: 120px;
    }

    75% {
        height: 150px;
    }

    80% {
        height: 180px;
    }

    85% {
        height: 210px;
    }

    90% {
        height: 240px;
    }

    95% {
        height: 240px;
    }

    100% {
        height: 300px;
    }
}

.content_input {
    width: 300px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.content_button {
    margin-top: 10px;
}

.el-input {
    margin-bottom: 25px;
}

.title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 30px;
    font-weight: bold;
    color: #606266;
}

.el-button--primary {
    width: 100%;
}

.help {
    text-align: end;
    font-size: 16px;
    margin-top: 20px;
    font-weight: bold;
    color: #0080ff;
    text-decoration: underline;
    cursor: pointer;
}
</style>
