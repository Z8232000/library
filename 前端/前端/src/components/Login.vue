<template>
  <div class="login_container aaa">
    <div class="tip">欢迎使用图书馆信息管理系统，请先登录</div>
    <div class="login_box bbb">
      <div class="avatar_box">
        <img src="../assets/avatar.jpeg" />
      </div>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginFormRules"
        label-width="80px"
        class="login_form bbb"
      >
        <el-form-item label="账号" prop="uID">
          <el-input v-model="loginForm.uID"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password"></el-input>
        </el-form-item>
        <el-form-item class="btns">
          <el-button type="success" @click="Loginsuccess" class="btn_login">
            登录
          </el-button>
          <el-button type="primary" @click="Register" class="btn_register">
            注册
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    var checkuID = (rule, value, callback) => {
      const reguID = /^[1-2][0-9]{7}$/;
      if (reguID.test(value)) return callback();
      else callback(new Error("请输入合法的学号/工号"));
    };
    return {
      result: {},
      resultForm: {
        success: false,
        isManager: false,
        message: "",
      },
      loginForm: {
        uID: "",
        password: "",
      },
      loginFormRules: {
        uID: [
          { required: true, message: "请输入账号", trigger: "blur" },
         { validator: checkuID, trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "长度在 6 到 15 个字符",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    Loginsuccess() {
      this.$refs.loginFormRef.validate(async (valid) => {
        if (valid) {
          await new Promise((resolve) => {
            this.$http
              .post("/login/", JSON.stringify(this.loginForm))
              .then((res) => {
                console.log(res);
                if (res.data.message === "用户不存在") {
                  alert("用户不存在");
                  return console.log(res.data.message);
                }
                if (res.data.message === "密码错误") {
                  alert("用户名或密码错误！");
                  return console.log(res.data.message);
                }

                console.log("登录成功");
                this.$store.commit("login");
                window.sessionStorage.setItem("token", res.data.token);
                window.sessionStorage.setItem(
                  "uID",
                  JSON.stringify(res.data.UID)
                );
                window.sessionStorage.setItem(
                  "uName",
                  JSON.stringify(res.data.username)
                );
                console.log(this.$store.isLogin);
                if (res.data.isManager === true) {
                  this.$router.push("Welcome");
                } else {
                  this.$router.push("reader/Welcome");
                }
              });
            resolve();
          }).then((data) => {
            console.log("成功啦post啦");
          });
        } else {
          return;
        }
      });
    },
    Register() {
      window.sessionStorage.clear();
      this.$router.push("/Register");
    },
  },
};
</script>

<style Lang="less" scoped>
.login_form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.tip {
  font-size: x-large;
  position: absolute;
  left: 33%;
  top: 3%;
  color: #ffffff;
}
.btns {
  display: flex;
  justify-content: flex-end;
}

.login_container {
  background-color: #8696a7;
  height: 100%;
}
.login_box {
  width: 450px;
  height: 300px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 55%;
  transform: translate(-50%, -50%);
}
.avatar_box {
  height: 130px;
  width: 130px;
  border: 3px solid #eee;
  border-radius: 50%;
  padding: 5px;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
}
.avatar_box img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #eee;
}
.aaa {
  background-image: url(../assets/Login背景.jpeg);
  background-repeat: no-repeat;
  background-size: 100%;
  background-attachment: fixed;
}

.bbb {
  filter: alpha(Opacity=90);
  -moz-opacity: 0.9;
  opacity: 0.9;
}
</style>
