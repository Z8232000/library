<template>
  <div>
    <div class="ccc">
      <!--    面包屑导航区-->
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/Reader/Welcome' }"
          >首页</el-breadcrumb-item
        >
        <el-breadcrumb-item>个人信息</el-breadcrumb-item>
      </el-breadcrumb>

      <!--    卡片视图区-->
      <el-card class="box-card">
        <div class="demo-basic--circle">
          <div class="block">
            <el-avatar :size="50" :src="circleUrl"></el-avatar>
          </div>
        </div>
        <div style="margin-bottom: 30px; margin-left: 10px">
          <h1>个人信息</h1>
        </div>

        <el-form ref="form" :model="userForm" label-width="80px">
          <el-form-item label="用户名称">
            <el-input v-model="userForm.uName" disabled></el-input>
          </el-form-item>
          <el-form-item label="用户ID">
            <el-input v-model="userForm.uID" disabled></el-input>
          </el-form-item>
        </el-form>
        <div class="boxdiv">
          管理密码<el-button plain @click="showEditDialog"
            >修改用户密码</el-button
          >
        </div>
        <div class="boxdiv">
          管理信息<el-button plain @click="showEdit_Dialog"
            >修改用户信息</el-button
          >
        </div>
        <div class="boxdiv">
          图书荐购<el-button plain @click="addDialogVisible = true"
            >编辑荐购图书表单</el-button
          >
        </div>
      </el-card>
    </div>
    <el-dialog
      title="图书荐购"
      :visible.sync="addDialogVisible"
      width="40%"
      @close="addDialogClosed"
    >
      <!--     对话框内容主体区-->
      <el-form
        :model="addForm"
        :rules="addRules"
        ref="addFormRef"
        label-width="120px"
      >
        <el-form-item label="图书名称" prop="bName">
          <el-input v-model="addForm.bName"></el-input>
        </el-form-item>
        <el-form-item label="图书作者" prop="bAuthor">
          <el-input v-model="addForm.bAuthor"></el-input>
        </el-form-item>
        <el-form-item label="图书出版年份" prop="bYear">
          <el-input v-model="addForm.bYear"></el-input>
        </el-form-item>
        <el-form-item label="荐购总量" prop="bTotal">
          <el-input v-model="addForm.bTotal"></el-input>
        </el-form-item>
        <el-form-item label="荐购理由" prop="bReason">
          <el-radio-group v-model="addForm.bReason">
            <el-radio label="课程需要"></el-radio>
            <el-radio label="自学需要"></el-radio>
            <el-radio label="个人兴趣"></el-radio>
            <el-radio label="其他"></el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <!--      对话框底部区域-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addBook">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="修改密码" :visible.sync="editDialogVisible" width="40%">
      <!--对话框主体区域-->
      <el-form
        :model="editForm"
        :rules="editRules"
        ref="editFormRef"
        label-width="120px"
      >
        <el-form-item label="用户名称" prop="uName">
          <el-input v-model="editForm.uName" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户ID" prop="uID">
          <el-input v-model="editForm.uID" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户新密码" prop="uPWD">
          <el-input v-model="editForm.uPWD"></el-input>
        </el-form-item>
        <el-form-item label="用户新密码确认" prop="ucheckPWD">
          <el-input v-model="editForm.ucheckPWD"></el-input>
        </el-form-item>
      </el-form>
      <!--      对话框底部-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false" @close="editDialogClosed"
          >取 消</el-button
        >
        <el-button type="primary" @click="editRecordInfo">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="修改个人信息"
      :visible.sync="edit_DialogVisible"
      width="40%"
    >
      <!--对话框主体区域-->
      <el-form
        :model="edit_Form"
        :rules="edit_Rules"
        ref="edit_FormRef"
        label-width="120px"
      >
        <el-form-item label="用户ID" prop="uID">
          <el-input v-model="edit_Form.uID" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户名称" prop="uName">
          <el-input v-model="edit_Form.uName"></el-input>
        </el-form-item>

        <el-form-item label="用户手机号" prop="uPhone">
          <el-input v-model="edit_Form.uPhone"></el-input>
        </el-form-item>
      </el-form>
      <!--      对话框底部-->
      <span slot="footer" class="dialog-footer">
        <el-button
          @click="edit_DialogVisible = false"
          @close="edit_DialogClosed"
          >取 消</el-button
        >
        <el-button type="primary" @click="edit_RecordInfo">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ReaderUsers",
  //页面测试数据
  data() {
    var u_checkPWD = (rule, value, callback) => {
      if (value !== this.editForm.uPWD)
        return callback(new Error("请保持两次密码一致"));
      else return callback();
    };
    var checkbTotal = (rule, value, callback) => {
      const regbTotal = /^[0-9]{1,3}$/;
      if (regbTotal.test(value)) return callback();
      else callback(new Error("请输入合法的库藏总量"));
    };
    var checkbYear = (rule, value, callback) => {
      const regbYear = /^[1-2][0-9]{3}$/;
      if (regbYear.test(value)) return callback();
      else callback(new Error("请输入合法的年份"));
    };
    var checkuID = (rule, value, callback) => {
      const reguID = /^[1-2][0-9]{7}$/;
      if (reguID.test(value)) return callback();
      else callback(new Error("请输入合法的学号/工号"));
    };
    var checkuPhone = (rule, value, callback) => {
      const regPhone = /^1[3-9][0-9]{9}$/;
      if (regPhone.test(value)) return callback();
      else callback(new Error("请输入合法的手机号"));
    };
    return {
      //验证用户名，学号/工号，手机号的规则
      circleUrl:
        "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
      userForm: {
        uName: "",
        uID: "",
      },

      addDialogVisible: false, //控制添加用户对话框的显示与隐藏
      addForm: {
        bName: "",
        bAuthor: "",
        bTotal: 0,
        bReason: "",
      },
      addRules: {
        bName: [
          { required: true, message: "请输入图书名称", trigger: "blur" },
          {
            min: 1,
            max: 20,
            message: "长度在 1 到 20 个字符",
            trigger: "blur",
          },
        ],
        bAuthor: [
          { required: true, message: "请输入图书作者", trigger: "blur" },
          {
            min: 2,
            max: 20,
            message: "长度在 2 到 20 个字符",
            trigger: "blur",
          },
        ],
        bYear: [
          { required: true, message: "请输入图书出版年份", trigger: "blur" },
          { validator: checkbYear, trigger: "blur" },
        ],

        bTotal: [
          { required: true, message: "请输入图书荐购量", trigger: "blur" },
          { validator: checkbTotal, trigger: "blur" },
        ],
        bReason: [
          { required: true, message: "请选择荐购理由", trigger: "blur" },
        ],
      },

      editDialogVisible: false, //控制修改用户对话框的显示与隐藏,rID为借阅单号
      editForm: {
        uName: "",
        uID: "",
        uPWD: "",
        ucheckPWD: "",
      },
      editRules: {
        uPWD: [
          { required: true, message: "请输入用户新密码", trigger: "blur" },
          { min: 6, max: 15, message: "长度在 6到 15 个字符", trigger: "blur" },
        ],
        ucheckPWD: [
          { required: true, message: "请确认用户新密码", trigger: "blur" },
          { min: 6, max: 15, message: "长度在 6到 15 个字符", trigger: "blur" },
          { validator: u_checkPWD, trigger: "blur" },
        ],
      },
      //修改用户密码表单验证规则对象

      edit_DialogVisible: false, //控制修改用户对话框的显示与隐藏,rID为借阅单号
      edit_Form: {
        uName: "",
        uID: "",
        uPhone: "",
      },
      edit_Rules: {
        uName: [
          { required: true, message: "请输入用户名称", trigger: "blur" },
          {
            min: 2,
            max: 10,
            message: "长度在 2 到 10 个字符",
            trigger: "blur",
          },
        ],
        uID: [
          { message: "请输入学号/工号", trigger: "blur" },
          { validator: checkuID, trigger: "blur" },
        ],
        uPhone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { validator: checkuPhone, trigger: "blur" },
        ],
      },
    };
  },

  created() {
    this.getNowUser();
  }, //生命周期函数，再次发起获取数据请求*/
  methods: {
    getNowUser() {
      var tmpuname = window.sessionStorage.getItem("uName");
      var tmpuid = window.sessionStorage.getItem("uID");
      this.userForm.uName = JSON.parse(tmpuname);
      this.userForm.uID = JSON.parse(tmpuid);
      this.editForm.uName = JSON.parse(tmpuname);
      this.editForm.uID = JSON.parse(tmpuid);
      this.edit_Form.uName = JSON.parse(tmpuname);
      this.edit_Form.uID = JSON.parse(tmpuid);
    }, //后面要改！！！

    addDialogClosed() {
      this.$refs.addFormRef.resetFields();
    }, //使得表单关闭以后就清空
    async addBook() {
      this.$refs.addFormRef.validate(
        //aync
        async (valid) => {
          if (!valid) return;
          //可以发起添加图书的请求
          else {
            await new Promise((resolve) => {
              this.$http
                .post("/users/buyBooks/", JSON.stringify(this.addForm))
                .then((res) => {
                  //别忘了保证addForm中的元素名和接口中要求的一致
                  //注意！！！要让后台给进行rID赋值
                  console.log(res);
                  if (res.data.success === false)
                    this.$message.error(res.data.message);
                  else this.$message.success("荐购成功！");

                  this.addDialogVisible = false;
                });
              resolve();
            });
          }
        }
      );
    }, //点击按钮添加图书荐购之前，进行表单预验证

    showEditDialog() {
      var tmpuname = window.sessionStorage.getItem("uName");
      var tmpuid = window.sessionStorage.getItem("uID");
      this.userForm.uName = JSON.parse(tmpuname);
      this.userForm.uID = JSON.parse(tmpuid);

      this.editDialogVisible = true;
    }, //点击修改按钮，弹出修改用户密码对话框
    editDialogClosed() {
      this.$refs.editFormRef.resetFields();
    }, //使得修改用户密码表单关闭以后就清空
    editRecordInfo() {
      this.$refs.editFormRef.validate(
        //aync
        async (valid) => {
          if (!valid) return;
          //可以发起修改用户密码的请求
          else {
            await new Promise((resolve) => {
              this.$http
                .post("/users/uPWD/", JSON.stringify(this.editForm))
                .then((res) => {
                  if (res.data.success === false)
                    this.$message.error(res.data.message);
                  else this.$message.success("密码修改成功！");
                  this.editDialogVisible = false;
                  this.getNowUser();
                });
              resolve();
            });
          }
        }
      );
    }, //修改用户密码
    showEdit_Dialog() {
      var tmpuname = window.sessionStorage.getItem("uName");
      var tmpuid = window.sessionStorage.getItem("uID");
      this.userForm.uName = JSON.parse(tmpuname);
      this.userForm.uID = JSON.parse(tmpuid);

      this.edit_DialogVisible = true;
    }, //点击修改按钮，弹出修改用户密码对话框
    edit_DialogClosed() {
      this.$refs.edit_FormRef.resetFields();
    }, //使得修改用户密码表单关闭以后就清空
    edit_RecordInfo() {
      this.$refs.edit_FormRef.validate(
        //aync
        async (valid) => {
          if (!valid) return;
          //可以发起修改用户密码的请求
          else {
            console.log(valid);
            await new Promise((resolve) => {
              this.$http
                .post("/users/uInform/", JSON.stringify(this.edit_Form))
                .then((res) => {
                  if (res.data.success === false)
                    this.$message.error(res.data.message);
                  else this.$message.success("个人信息修改成功！");
                  this.edit_DialogVisible = false;
                  this.getNowUser();
                });
              resolve();
            });
          }
        }
      );
    }, //修改用户密码
  },
};
</script>

<style  Lang="less" scoped>
.box-card {
  width: 1000px;
  margin: 0 auto;
}
.block {
  position: absolute;
  left: 50%;
  transform: translateX(150%) translateY(-100%);
}
.el-button {
  margin-left: 10px;
  height: 38px;
  text-align: center;
}
.boxdiv {
  margin-bottom: 20px;
  margin-left: 14px;
  font-size: 14px;
  color: #606266;
}
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
.ccc {
  filter: alpha(Opacity=85);
  -moz-opacity: 0.85;
  opacity: 0.85;
}
</style>
