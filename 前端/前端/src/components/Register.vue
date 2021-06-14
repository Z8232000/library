<template>
  <div class="register_container aaa">
    <div class="register_box bbb">
      <div class="avatar_box">
        <img src="../assets/avatar.jpeg" />
      </div>
      <el-form
        :model="registerForm"
        :rules="registerFormRules"
        label-width="80px"
        class="register_form"
        ref="registerFormRef"
      >
        <el-form-item label="账号" prop="uID">
          <el-input v-model="registerForm.uID"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username"></el-input>
        </el-form-item>
        <el-form-item label="手机号码" prop="phonenum">
          <el-input v-model="registerForm.phonenum"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="repassword">
          <el-input
            v-model="registerForm.repassword"
            type="repassword"
          ></el-input>
        </el-form-item>
        <el-form-item class="btns">
          <el-button type="primary" plain @click="Registersuccess">
            注册
          </el-button>
          <el-button type="plain" plain @click="back"> 返回 </el-button>
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
    var u_checkPWD = (rule, value, callback) => {
      if (value !== this.registerForm.password)
        return callback(new Error("请保持两次密码一致"));
      else return callback();
    };
    var checkuPhone = (rule, value, callback) => {
      const regPhone = /^1[3-9][0-9]{9}$/;
      if (regPhone.test(value)) return callback();
      else callback(new Error("请输入合法的手机号"));
    };
    return {
      registerForm: {
        uID: "",
        username: "",
        phonenum: "",
        password: "",
        repassword: "",
      },
      radio: "1",
      registerFormRules: {
        uID: [
          { required: true, message: "请输入账号", trigger: "blur" },
          {
            min: 8,
            max: 8,
            message: "长度为8个字符",
            trigger: "blur",
          },
          { validator: checkuID, trigger: "blur" },
        ],
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 2,
            max: 10,
            message: "长度在 2 到 10 个字符",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "长度在 6到 15 个字符",
            trigger: "blur",
          },
        ],
        repassword: [
          { required: true, message: "请确认密码", trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "长度在 5 到 10 个字符",
            trigger: "blur",
          },
          { validator: u_checkPWD, trigger: "blur" },
        ],
        phonenum: [
          { required: true, message: "请输入手机号码", trigger: "blur" },
          {
            min: 11,
            max: 11,
            message: "长度必须为11个字符",
            trigger: "blur",
          },
          { validator: checkuPhone, trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    Registersuccess() {
      this.$refs.registerFormRef.validate(async (valid) => {
        if (valid) {
          await new Promise((resolve) => {
            this.$http
              .post("/register/", JSON.stringify(this.registerForm))
              .then((res) => {
                console.log(res);
                if (res.data.success === false) {
                  if (res.data.message === "账号已存在") {
                    alert("账号已存在");
                  } else if (res.data.message === "两次密码不一致") {
                    alert("两次密码不一致");
                  }
                  return console.log(res.data.message);
                }

                console.log("注册成功");
                alert("注册成功");
                this.$router.push("/Login");
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
    back() {
      this.$router.push("/Login");
    },
  },
};
</script>

<style Lang="less" scoped>
.register_form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.tip {
  font-size: x-large;
}
.btns {
  display: flex;
  justify-content: flex-end;
}

.register_container {
  background-color: #8696a7;
  height: 100%;
}
.register_box {
  width: 450px;
  height: 400px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 60%;
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
  transform: translate(-50%, -85%);
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