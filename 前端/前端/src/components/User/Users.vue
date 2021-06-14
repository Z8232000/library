<template>
  <div>
    <!--    面包屑导航区-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!--    卡片视图区-->
    <el-card class="box-card">
      <!--      引入栅格系统，方便布局-->
      <el-row :gutter="20">
        <!--      搜索框区域，span代表占几个格子，gutter控制间隙-->
        <el-col :span="8">
          <!--      搜索框-->
          <el-input
            placeholder="请输入用户名或学号/工号"
            v-model="queryInfo.query"
            @clear="getUsersList"
            clearable
          >
            <!--            @clear="getUsersList"应该加入上面标签中，以实现一清空，下面列表立刻刷新-->
            <el-select
              v-model="queryInfo.qparam"
              slot="prepend"
              placeholder="请选择"
            >
              <el-option label="用户名" value="1"></el-option>
              <el-option label="学号/工号" value="2"></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getUsersList"
            ></el-button>
            <!--@click="getUsersList"应该加入上面标签中，以实现搜索-->
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addDialogVisible = true"
            >添加用户</el-button
          >
        </el-col>
      </el-row>
      <!--        用户列表区-->
      <el-table :data="usersList" border stripe
        ><!--最后一个属性为表格隔行变色-->
        <!--        index指定此列为索引列-->
        <el-table-column label="#" type="index"> </el-table-column>
        <el-table-column label="姓名" prop="uName"> </el-table-column>
        <el-table-column label="学号/工号" prop="uID"> </el-table-column>
        <el-table-column label="手机号" prop="uPhone"> </el-table-column>
        <el-table-column label="角色" prop="uCharacter"> </el-table-column>
        <!--        在这里使用插槽作用域-->
        <el-table-column label="修改用户/删除用户" class="orderRow">
          <template slot-scope="scope">
            <!-- 修改按钮-->
            <el-tooltip
              effect="dark"
              content="修改"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="
                  showEditDialog(
                    scope.row.uName,
                    scope.row.uID,
                    scope.row.uPhone,
                    scope.row.uCharacter
                  )
                "
              ></el-button>
            </el-tooltip>

            <!-- 删除按钮-->
            <el-tooltip
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="removeUserByuID(scope.row.uID)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!--      分页区-->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[10, 20, 30, 40]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>
    <!--    添加用户的对话框-->
    <el-dialog
      title="添加用户"
      :visible.sync="addDialogVisible"
      width="40%"
      @close="addDialogClosed"
    >
      <!--     对话框内容主体区-->
      <el-form
        :model="addForm"
        :rules="addRules"
        ref="addFormRef"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="uName">
          <el-input v-model="addForm.uName"></el-input>
        </el-form-item>

        <el-form-item label="学号/工号" prop="uID">
          <el-input v-model="addForm.uID"></el-input>
        </el-form-item>

        <el-form-item label="手机号" prop="uPhone">
          <el-input v-model="addForm.uPhone"></el-input>
        </el-form-item>

        <el-form-item label="用户密码" prop="uPWD">
          <el-input v-model="addForm.uPWD"></el-input>
        </el-form-item>
      </el-form>
      <!--      对话框底部区域-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addUser">确 定</el-button>
      </span>
    </el-dialog>

    <!--    修改用户的对话框-->
    <!--    对话框头部-->
    <el-dialog
      title="修改用户"
      :visible.sync="editDialogVisible"
      width="40%"
      :before-close="handleClose"
    >
      <!--对话框主体区域-->
      <el-form
        :model="editForm"
        :rules="editRules"
        ref="editFormRef"
        label-width="100px"
      >
        <el-form-item label="用户名">
          <el-input v-model="editForm.uName" disabled></el-input>
        </el-form-item>
        <el-form-item label="学号/工号">
          <el-input v-model="editForm.uID" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户角色">
          <el-input v-model="editForm.uCharacter" disabled></el-input>
        </el-form-item>

        <el-form-item label="修改手机号" prop="uPhone">
          <el-input v-model="editForm.uPhone"></el-input>
        </el-form-item>
      </el-form>
      <!--      对话框底部-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false" @close="editDialogClosed"
          >取 消</el-button
        >
        <el-button type="primary" @click="editUserInfo">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "Users",
  //页面测试数据
  data() {
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

      queryInfo: {
        query: "", //搜索关键字
        qparam: 1, //搜索参数
        pagenum: 1, //当前页码
        pagesize: 10, //每页显示条数
      },
      usersList: [],
      total: 4, //此为一共几条记录,现在定义死了，以后会随着API获取更改

      addDialogVisible: false, //控制添加用户对话框的显示与隐藏
      addForm: {
        uName: "",
        uID: "",
        uPhone: "",
        uCharacter: "",
        uPWD: "",
      },
      addRules: {
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
          { required: true, message: "请输入学号/工号", trigger: "blur" },
          { validator: checkuID, trigger: "blur" },
        ],
        uPhone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { validator: checkuPhone, trigger: "blur" },
        ],
        uPWD: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 15,
            message: "长度在 6 到 15 个字符",
            trigger: "blur",
          },
        ],
      },
      //添加表单验证归规则对象

      editDialogVisible: false, //控制修改用户对话框的显示与隐藏
      editForm: {
        uName: "",
        uID: "",
        uPhone: "",
        uCharacter: "",
      },
      editRules: {
        uPhone: [
          {
            required: true,
            message: "请输入手机号",
            trigger: ["blur", "change"],
          },
          { validator: checkuPhone, trigger: "blur" },
        ],
      },
      //修改用户表单验证归规则对象
    };
  },
  created() {
    this.getUsersList();
  }, //生命周期函数，再次发起获取数据请求*/
  methods: {
    async getUsersList() {
      await new Promise((resolve) => {
        this.$http
          .post("/users/", JSON.stringify(this.queryInfo))
          .then((res) => {
            console.log(res);
            if (res.status !== 200)
              return this.$message.error("获取用户列表失败");
            else {
              this.$message.success("获取用户列表成功！");
              console.log(res);
              this.usersList = [];
              for (let i = 0; i < res.data.userInfo.length; i++) {
                if (!res.data.userInfo[i].uCharacter) {
                  res.data.userInfo[i].uCharacter = "读者";
                  this.usersList.push(res.data.userInfo[i]);
                }
              }
              this.total = res.data.total;
            }
          });
        resolve();
      });
    },
    //获取用户列表函数
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getUsersList();
    }, //函数用来监听pagesize的改变情况
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage;
      this.getUsersList();
    }, //函数用来监听页码值改变的事件

    addDialogClosed() {
      this.$refs.addFormRef.resetFields();
    }, //使得表单关闭以后就清空
    async addUser() {
      this.$refs.addFormRef.validate(
        //aync
        async (valid) => {
          if (!valid) return;
          //可以发起添加用户的请求
          else {
            this.addForm.uCharacter = "读者";
            await new Promise((resolve) => {
              this.$http
                .post("/operator/addReader/", JSON.stringify(this.addForm))
                .then((res) => {
                  if (res.success === false) this.$message.error(res.message);
                  else this.$message.success("添加用户成功！");

                  this.addDialogVisible = false;
                  this.getUsersList(); //添加成功，重新获取用户列表
                });
              resolve();
            });
            //别忘了保证addForm中的元素名称和接口中要求的一致
          }
        }
      );
    }, //点击按钮添加新用户之前，进行表单预验证

    showEditDialog(uName, uID, uPhone, uCharacter) {
      //uID是以参数scope.row.uID的形式获取到的
      console.log(uID);
      this.editForm.uName = uName;
      this.editForm.uID = uID;
      this.editForm.uPhone = uPhone;
      this.editForm.uCharacter = uCharacter;

      this.editDialogVisible = true;
    }, //点击修改按钮，弹出修改用户对话框
    editDialogClosed() {
      this.$refs.editFormRef.resetFields();
    }, //使得修改用户表单关闭以后就清空
    async editUserInfo() {
      this.$refs.editFormRef.validate(
        //aync
        async (valid) => {
          if (!valid) return;
          //可以发起修改用户的请求
          else {
            console.log(valid);
            await new Promise((resolve) => {
              this.$http
                .post("/users/uID/", JSON.stringify(this.editForm))
                .then((res) => {
                  if (res.success === false)
                    this.$message.error("更新用户信息失败！");
                  else this.$message.success("更新用户信息成功！");
                  this.editDialogVisible = false;
                  this.getUsersList(); //修改成功，重新获取用户列表
                });
              resolve();
            });
          }
        }
      );
    }, //修改用户列表

    async removeUserByuID(uID) {
      //弹框询问用户是否删除数据
      console.log(uID);
      const confirmResult = await this.$confirm(
        "此操作将永久删除该用户, 是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      ).catch((err) => {
        return err;
      });

      if (confirmResult !== "confirm")
        return this.$message.info("已取消删除。");

      await new Promise((resolve) => {
        this.$http
          .post("/operator/delReader/", JSON.stringify({ uID }))
          .then((res) => {
            if (res.success === false) this.$message.error(res.message);
            else this.$message.success("删除用户成功！");
            this.getUsersList();

            //进行删除用户操作
          });
      });
    }, //根据uID删除对应用户信息
  },
};
</script>

<style  Lang="less" scoped>
.el-tooltip.el-button {
  margin-right: 40px;
}
</style>

