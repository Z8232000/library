<template>
  <div>
    <!--    面包屑导航区-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>借阅记录</el-breadcrumb-item>
    </el-breadcrumb>

    <!--    卡片视图区-->
    <el-card class="box-card">
      <!--      引入栅格系统，方便布局-->
      <el-row :gutter="20">
        <!--      搜索框区域，span代表占几个格子，gutter控制间隙-->
        <el-col :span="8">
          <!--      搜索框-->
          <el-input
            placeholder="请输入借阅记录ID/图书ID/读者ID"
            v-model="queryInfo.query"
            @clear="getRecordsList"
            clearable
          >
            <!--            @clear="getRecordsList"应该加入上面标签中，以实现一清空，下面列表立刻刷新-->
            <el-select
              v-model="queryInfo.qparam"
              slot="prepend"
              placeholder="请选择"
            >
              <el-option label="借阅记录ID" value="1"></el-option>
              <el-option label="图书ID" value="2"></el-option>
              <el-option label="读者ID" value="3"></el-option>
              <el-option label="图书名称" value="4"></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getRecordsList"
            ></el-button>
            <!--@click="getRecordsList"应该加入上面标签中，以实现搜索-->
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addDialogVisible = true"
            >现场借书</el-button
          >
        </el-col>
      </el-row>
      <!--        借阅记录列表区-->
      <el-table
        :data="recordsList"
        @sort-change="onSortChange"
        border
        :row-class-name="tableRowClassName"
        ><!--最后一个属性为表格隔行变色-->
        <!--        index指定此列为索引列-->
        <el-table-column label="#" type="index"> </el-table-column>
        <el-table-column
          label="借阅记录ID"
          prop="rID"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
        >
        </el-table-column>
        <el-table-column label="图书名称" prop="bName"> </el-table-column>
        <el-table-column
          label="图书个体ID"
          prop="bSingleID"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
        >
        </el-table-column>
        <el-table-column
          label="用户ID"
          prop="uID"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
        >
        </el-table-column>
        <el-table-column label="借书日期" prop="borrowDate"> </el-table-column>
        <el-table-column label="规定还书日期" prop="presetDate">
        </el-table-column>
        <el-table-column label="还书日期" prop="returnDate"> </el-table-column>
        <el-table-column label="此记录状态" prop="returnCondition">
        </el-table-column>

        <!--        此处先只进行当前页内部排序，若要总体排序，后续修改-->
        <!--        在这里使用插槽作用域-->

        <el-table-column label="还书/删除记录" class="orderRow">
          <template slot-scope="scope">
            <!-- 修改按钮-->
            <el-tooltip
              effect="dark"
              content="还书"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="
                  editRecordInfo(scope.row.rID, scope.row.returnCondition)
                "
              >
              </el-button>
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
                @click="
                  removeRecordByrID(scope.row.rID, scope.row.returnCondition)
                "
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
    <!--    添加借阅记录即借书的对话框-->
    <el-dialog
      title="现场借书"
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
        <el-form-item label="图书ID" prop="bID">
          <el-input v-model="addForm.bID"></el-input>
        </el-form-item>
        <el-form-item label="图书个体ID" prop="bSingleID">
          <el-input v-model="addForm.bSingleID"></el-input>
        </el-form-item>
        <el-form-item label="用户ID" prop="uID">
          <el-input v-model="addForm.uID"></el-input>
        </el-form-item>
      </el-form>
      <!--      对话框底部区域-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addRecord">确 定</el-button>
      </span>
    </el-dialog>

    <!--    修改借阅记录即还书的对话框-->
    <!--    对话框头部-->
    <el-dialog title="还书" :visible.sync="editDialogVisible" width="40%">
      <!--对话框主体区域-->
      <el-form
        :model="editForm"
        :rules="editRules"
        ref="editFormRef"
        label-width="120px"
      >
        <el-form-item label="借阅记录ID" prop="rID">
          <el-input v-model="editForm.rID" disabled></el-input>
        </el-form-item>
        <el-form-item label="图书名称" prop="bName">
          <el-input v-model="editForm.bName" disabled></el-input>
        </el-form-item>
        <el-form-item label="图书ID" prop="bSingleID">
          <el-input v-model="editForm.bSingleID" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户ID" prop="uID">
          <el-input v-model="editForm.uID" disabled></el-input>
        </el-form-item>
        <el-form-item label="借书日期" prop="borrowDate">
          <el-input v-model="editForm.borrowDate" disabled></el-input>
        </el-form-item>
        <el-form-item label="规定还书日期" prop="presetDate">
          <el-input v-model="editForm.presetDate" disabled></el-input>
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
  </div>
</template>

<script>
export default {
  name: "RecordList",
  //页面测试数据
  data() {
    var checkbID = (rule, value, callback) => {
      const regbID = /^[0-9]{8}$/;
      if (regbID.test(value)) return callback();
      else callback(new Error("输入图书ID号长度有误，应为8位"));
    };
    var checkbSingleID = (rule, value, callback) => {
      const regbSingleID = /^[0-9]{11}$/;
      if (regbSingleID.test(value)) return callback();
      else callback(new Error("输入图书个体ID号长度有误，应为11位"));
    };
    var checkuID = (rule, value, callback) => {
      const reguID = /^[1-2][0-9]{7}$/;
      if (reguID.test(value)) return callback();
      else callback(new Error("请输入合法的学号/工号"));
    };

    return {
      //验证图书ID，年份，库存总量，余量的规则

      queryInfo: {
        query: "", //搜索关键字
        qparam: 1, //搜索借阅记录选项参数
        qsort: 11, //记录排序参数
        pagenum: 1, //当前页码
        pagesize: 10, //每页显示条数
      },
      recordsList: [],
      total: 3, //此为一共几条记录,现在定义死了，以后会随着API获取更改

      addDialogVisible: false, //控制添加用户对话框的显示与隐藏
      addForm: {
        bSingleID: "",
        uID: "",
      },
      addRules: {
        bID: [
          { required: true, message: "请输入8位图书ID号", trigger: "blur" },
          { validator: checkbID, trigger: "blur" },
        ],
        bSingleID: [
          {
            required: true,
            message: "请输入11位图书个体ID号",
            trigger: "blur",
          },
          { validator: checkbSingleID, trigger: "blur" },
        ],
        uID: [
          { required: true, message: "请输入学号/工号", trigger: "blur" },
          { validator: checkuID, trigger: "blur" },
        ],
      },
      //添加图书借阅记录验证归规则对象

      editCondition: "借阅未还",
      editDialogVisible: false, //控制修改用户对话框的显示与隐藏,rID为借阅单号
      editForm: {
        rID: "",
        bName: "",
        bSingleID: "",
        uID: "",
        borrowDate: "",
        presetDate: "",
        returnDate: "",
      },
      editRules: {
        rID: [{ required: true }],
        bName: [
          { required: true, message: "请输入图书名称", trigger: "blur" },
          {
            min: 1,
            max: 20,
            message: "长度在 1 到 20 个字符",
            trigger: "blur",
          },
        ],
        bSingleID: [
          { required: true, message: "请输入图书ID号", trigger: "blur" },
          { validator: checkbSingleID, trigger: "blur" },
        ],
        uID: [
          { required: true, message: "请输入学号/工号", trigger: "blur" },
          { validator: checkuID, trigger: "blur" },
        ],
        borrowDate: [
          { required: true, message: "请输入图书借阅日期", trigger: "blur" },
        ],
        presetDate: [
          {
            required: true,
            message: "请输入图书规定归还日期",
            trigger: "blur",
          },
        ],
        returnDate: [
          {
            required: true,
            message: "请输入用户归还图书日期",
            trigger: "blur",
          },
        ],
      },
      //修改图书借阅记录表单验证规则对象
    };
  },
  created() {
    this.getRecordsList();
  }, //生命周期函数，再次发起获取数据请求
  methods: {
    async getRecordsList() {
      await new Promise((resolve) => {
        this.$http
          .post("/records/", JSON.stringify(this.queryInfo))
          .then((res) => {
            console.log(res);
            if (res.status !== 200)
              this.$message.error("获取借阅记录列表失败！");
            else {
              this.$message.success("获取借阅列表成功！");
              console.log(res);
              this.recordsList = [];
              for (let i = 0; i < res.data.userINFO.length; i++) {
                if (res.data.userINFO[i].returnCondition == 0)
                  res.data.userINFO[i].returnCondition = "未确认";
                else if (res.data.userINFO[i].returnCondition == 1)
                  res.data.userINFO[i].returnCondition = "借阅未还";
                else if (res.data.userINFO[i].returnCondition == 2)
                  res.data.userINFO[i].returnCondition = "借阅已还";
                else if (res.data.userINFO[i].returnCondition == 3)
                  res.data.userINFO[i].returnCondition = "过期未还";

                this.recordsList.push(res.data.userINFO[i]);
              }
              this.total = res.data.total;
            }
          });
        resolve();
      });
    },
    //获取借阅记录列表函数
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getRecordsList();
    }, //函数用来监听pagesize的改变情况
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage;
      this.getRecordsList();
    }, //函数用来监听页码值改变的事件
    onSortChange({ prop, order }) {
      if (prop === "rID" && order === "ascending") this.queryInfo.qsort = 11;
      else if (prop === "rID" && order === "descending")
        this.queryInfo.qsort = 10;
      else if (prop === "bSingleID" && order === "ascending")
        this.queryInfo.qsort = 21;
      else if (prop === "bSingleID" && order === "descending")
        this.queryInfo.qsort = 20;
      else if (prop === "uID" && order === "ascending")
        this.queryInfo.qsort = 31;
      else if (prop === "uID" && order === "descending")
        this.queryInfo.qsort = 30;
      else this.queryInfo.qsort = 11;

      this.getRecordsList();
      //与后端连接后，解除此行注释
    },

    addDialogClosed() {
      this.$refs.addFormRef.resetFields();
    }, //使得表单关闭以后就清空
    async addRecord() {
      this.$refs.addFormRef.validate(
        //aync
        async (valid) => {
          if (!valid) return;
          //可以发起添加借阅记录即借书的请求
          else {
            await new Promise((resolve) => {
              this.$http
                .post("/records/addnow/", JSON.stringify(this.addForm))
                .then((res) => {
                  //别忘了保证addForm中的元素名和接口中要求的一致
                  //注意！！！要让后台给进行rID赋值
                  console.log(res);
                  if (res.data.success === false)
                    this.$message.error(res.data.message);
                  else this.$message.success("借书成功！");

                  this.addDialogVisible = false;
                  this.getRecordsList(); //添加成功，重新获取借阅记录列表
                });
              resolve();
            });
          }
        }
      );
    }, //点击按钮添加新借阅记录之前，进行表单预验证

    async showEditDialog(
      rID,
      bName,
      bSingleID,
      uID,
      borrowDate,
      presetDate,
      returnDate,
      returnCondition
    ) {
      //rID是以参数scope.row.rID的形式获取到的
      console.log(rID);
      this.editForm.rID = rID;
      this.editForm.bSingleID = bSingleID;
      this.editForm.bName = bName;
      this.editForm.uID = uID;
      this.editForm.borrowDate = borrowDate;
      this.editForm.presetDate = presetDate;
      this.editForm.returnDate = returnDate;
      this.editForm.returnCondition = returnCondition;
      this.editCondition = returnCondition;

      if (returnCondition === "借阅未还" || returnCondition === "过期未还")
        this.editDialogVisible = true;
      else {
        this.editDialogVisible = false;
        alert("此书已还，不必再进行还书操作！");
      }
    }, //点击修改按钮，弹出修改借阅记录即还书对话框
    editDialogClosed() {
      this.$refs.editFormRef.resetFields();
    }, //使得修改借阅记录表单关闭以后就清空
    async editRecordInfo(rID, returnCondition) {
      if (returnCondition === "借阅已还") {
        alert("此书已还！无需再进行还书操作！");
        return;
      }
      await new Promise((resolve) => {
        this.$http
          .post("/records/rID/", JSON.stringify({ rID }))
          .then((res) => {
            if (res.data.success === false) this.$message.error("还书失败！");
            else this.$message.success("还书成功！");
            this.editDialogVisible = false;
            this.getRecordsList(); //修改成功，重新获取借阅记录列表
          });
        resolve();
      });
    },

    async removeRecordByrID(rID, rCondition) {
      //弹框询问用户是否删除这条借阅记录
      console.log(rID);
      if (rCondition !== "借阅已还") {
        alert("只能删除已还记录！");
        return;
      }

      const confirmResult = await this.$confirm(
        "此操作将永久删除该记录, 是否继续?",
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
          .post("/records/del/", JSON.stringify({ rID }))
          .then((res) => {
            if (res.status !== 200) this.$message.error("删除借阅记录失败！");
            else this.$message.success("删除借阅记录成功！");
            this.getRecordsList();

            //进行删除借阅记录操作
          });
      });
    }, //根据rID删除对应借阅记录信息

    tableRowClassName(obj) {
      if (obj.row.returnCondition === "过期未还") {
        return "warning-row";
      } else if (obj.row.returnCondition === "借阅已还") {
        return "success-row";
      }
      return "";
    },
  },
};
</script>

<style  Lang="less" scoped>
>>> .el-table .warning-row {
  background: oldlace;
}
>>> .el-table .success-row {
  background: #f0f9eb;
}
.el-table .success-row :hover {
  background: red;
}
.el-tooltip.el-button {
  margin-right: 0px !important;
}
</style>
