<template>
    <div class="login">
        <div class="box">
            <i class="el-icon-close" @click="close_login"></i>
            <div class="content">
                <div class="nav">
                    <span :class="{active: login_method === 'is_pwd'}"
                          @click="change_login_method('is_pwd')">密码登录</span>
                    <span :class="{active: login_method === 'is_sms'}"
                          @click="change_login_method('is_sms')">短信登录</span>
                </div>
                <el-form v-if="login_method === 'is_pwd'">
                    <el-input
                            placeholder="用户名/手机号/邮箱"
                            prefix-icon="el-icon-user"
                            v-model="username"
                            clearable>
                    </el-input>
                    <el-input
                            placeholder="密码"
                            prefix-icon="el-icon-key"
                            v-model="password"
                            clearable
                            show-password>
                    </el-input>
                    <el-button type="primary" @click="login">登录</el-button>
                </el-form>
                <el-form v-if="login_method === 'is_sms'">
                    <el-input
                            placeholder="手机号"
                            prefix-icon="el-icon-phone-outline"
                            v-model="mobile"
                            clearable
                            @blur="check_mobile">
                    </el-input>
                    <el-input
                            placeholder="验证码"
                            prefix-icon="el-icon-chat-line-round"
                            v-model="sms"
                            clearable>
                        <template slot="append">
                            <span class="sms" @click="send_sms">{{ sms_interval }}</span>
                        </template>
                    </el-input>
                    <el-button type="primary" @click="login_mobile">登录</el-button>
                </el-form>
                <div class="foot">
                    <span @click="go_register">立即注册</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Login",
        data() {
            return {
                username: '',
                password: '',
                mobile: '',
                sms: '',
                login_method: 'is_pwd',
                sms_interval: '获取验证码',
                is_send: false,
            }
        },
        methods: {
            close_login() {
                this.$emit('close')
            },
            go_register() {
                this.$emit('go')
            },
            change_login_method(method) {
                this.login_method = method;
            },
            // 校验手机对应用户是否存在
            check_mobile() {
                // 前台校验手机格式
                if (!this.mobile) return;
                if (!this.mobile.match(/^1[3-9][0-9]{9}$/)) {
                    this.$message({
                        message: '手机号有误',
                        type: 'warning',
                        duration: 1000,
                        onClose: () => {
                            this.mobile = '';
                        }
                    });
                    return false;
                }
                // 访问后台校验手机号对应用户是否存在
                this.$axios({
                    url: this.$settings.base_url + '/user/mobile/',
                    method: 'get',
                    params: {
                        mobile: this.mobile
                    }
                }).then(response => {
                    if (response.data.status === 0) {
                        this.$message({
                            message: response.data.msg,
                            type: 'warning',
                            duration: 1000,
                        })
                    } else {
                        // 注册过的手机才允许发送验证码
                        this.is_send = true;
                    }
                }).catch(error => {
                    this.$message({
                        message: error.response.data.msg,
                        type: 'error'
                    })
                });
            },
            // 发送验证码
            send_sms() {
                if (!this.is_send) return;
                this.is_send = false;
                this.sms_interval = "发送中...";

                // 倒计时
                let sms_interval_time = 60;
                let timer = setInterval(() => {
                    if (sms_interval_time <= 1) {
                        clearInterval(timer);
                        this.sms_interval = "获取验证码";
                        this.is_send = true; // 重新回复点击发送功能的条件
                    } else {
                        sms_interval_time -= 1;
                        this.sms_interval = `${sms_interval_time}秒后再发`;
                    }
                }, 1000);

                this.$axios({
                    url: this.$settings.base_url + '/user/sms/',
                    method: 'post',
                    data: {
                        mobile: this.mobile
                    }
                }).then(response => {
                    if (response.data.status === 0) {
                        // 成功
                        this.$message({
                            message: '验证码发送成功',
                            type: 'success',
                        })
                    } else {
                        // 失败
                        this.$message({
                            message: '验证码发送失败',
                            type: 'error',
                        })
                    }
                }).catch(() => {
                    // 异常
                    this.$message({
                        message: '获取验证码异常',
                        type: 'error',
                    })
                });
            },
            // 验证码登录
            login_mobile() {
                if (!this.mobile || !this.sms) return false;

                this.$axios({
                    url: this.$settings.base_url + '/user/login/mobile/',
                    method: 'post',
                    data: {
                        mobile: this.mobile,
                        code: this.sms,
                    }
                }).then(response => {
                    // 要将响应的用户信息和token存储到cookies中
                    this.$cookies.set('token', response.data.results.token, '1d');
                    this.$cookies.set('username', response.data.results.username, '1d');

                    // 弹出框提示后，关闭登录界面
                    this.$message({
                        message: '登录成功',
                        type: 'success',
                        duration: 1500,
                        onClose: () => {
                            this.$emit('success')
                        }
                    });
                }).catch(() => {
                    // 异常
                    this.$message({
                        message: '登录失败',
                        type: 'error',
                        duration: 1500,
                        onClose: () => {
                            this.mobile = '';
                            this.sms = '';
                        }
                    })
                });
            },
            // 密码登录
            login() {
                if (!this.username || !this.password) return false;
                this.$axios({
                    url: this.$settings.base_url + '/user/login/',
                    method: 'post',
                    data: {
                        username: this.username,
                        password: this.password,
                    }
                }).then(response => {
                    // 要将响应的用户信息和token存储到cookies中
                    this.$cookies.set('token', response.data.results.token, '1d');
                    this.$cookies.set('username', response.data.results.username, '1d');

                    // 弹出框提示后，关闭登录界面
                    this.$message({
                        message: '登录成功',
                        type: 'success',
                        duration: 1500,
                        onClose: () => {
                            this.$emit('success')
                        }
                    });
                }).catch(() => {
                    // 异常
                    this.$message({
                        message: '登录失败',
                        type: 'error',
                        duration: 1500,
                        onClose: () => {
                            this.username = '';
                            this.password = '';
                        }
                    })
                });
            },
        }
    }
</script>

<style scoped>
    .login {
        width: 100vw;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 10;
        background-color: rgba(0, 0, 0, 0.3);
    }

    .box {
        width: 400px;
        height: 420px;
        background-color: white;
        border-radius: 10px;
        position: relative;
        top: calc(50vh - 210px);
        left: calc(50vw - 200px);
    }

    .el-icon-close {
        position: absolute;
        font-weight: bold;
        font-size: 20px;
        top: 10px;
        right: 10px;
        cursor: pointer;
    }

    .el-icon-close:hover {
        color: darkred;
    }

    .content {
        position: absolute;
        top: 40px;
        width: 280px;
        left: 60px;
    }

    .nav {
        font-size: 20px;
        height: 38px;
        border-bottom: 2px solid darkgrey;
    }

    .nav > span {
        margin: 0 20px 0 35px;
        color: darkgrey;
        user-select: none;
        cursor: pointer;
        padding-bottom: 10px;
        border-bottom: 2px solid darkgrey;
    }

    .nav > span.active {
        color: black;
        border-bottom: 3px solid black;
        padding-bottom: 9px;
    }

    .el-input, .el-button {
        margin-top: 40px;
    }

    .el-button {
        width: 100%;
        font-size: 18px;
    }

    .foot > span {
        float: right;
        margin-top: 20px;
        color: orange;
        cursor: pointer;
    }

    .sms {
        color: orange;
        cursor: pointer;
        display: inline-block;
        width: 70px;
        text-align: center;
        user-select: none;
    }
</style>