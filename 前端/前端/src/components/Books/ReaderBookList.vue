<template>
  <div>
    <!--    面包屑导航区-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/Reader/Welcome' }"
        >首页</el-breadcrumb-item
      >
      <el-breadcrumb-item>图书列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!--    卡片视图区-->
    <el-card class="box-card">
      <!--      引入栅格系统，方便布局-->
      <el-row :gutter="20">
        <!--      搜索框区域，span代表占几个格子，gutter控制间隙-->
        <el-col :span="8">
          <!--      搜索框-->
          <el-input
            placeholder="请输入图书名称/图书ID/作者名称"
            v-model="queryInfo.query"
            clearable
          >
            <!--            @clear="getBooksList"应该加入上面标签中，以实现一清空，下面列表立刻刷新-->
            <el-select
              v-model="queryInfo.qparam"
              slot="prepend"
              placeholder="请选择"
            >
              <el-option label="图书名称" value="1"></el-option>
              <el-option label="图书ID" value="2"></el-option>
              <el-option label="作者名称" value="3"></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getBooksList"
            ></el-button>
            <!--@click="getBooksList"应该加入上面标签中，以实现搜索-->
          </el-input>
        </el-col>
      </el-row>
      <!--        书籍列表区-->
      <el-table :data="booksList" @sort-change="onSortChange" border stripe>
        <!--最后一个属性为表格隔行变色-->
        <!--        index指定此列为索引列-->
        <el-table-column label="#" type="index"> </el-table-column>
        <el-table-column
          label="图书名称"
          prop="bName"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
        >
        </el-table-column>
        <el-table-column
          label="图书类编号"
          prop="bID"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
        >
        </el-table-column>
        <el-table-column label="图书作者" prop="bAuthor"> </el-table-column>
        <el-table-column
          label="图书出版年份"
          prop="bYear"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
        >
        </el-table-column>
        <el-table-column label="库藏总量" prop="bTotal"></el-table-column>
        <el-table-column
          label="可借余量"
          prop="bLeft"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
        ></el-table-column>
        <!--        此处先只进行当前页内部排序，若要总体排序，后续修改-->
        <!--        在这里使用插槽作用域-->

        <el-table-column label="申请借书" class="orderRow">
          <template slot-scope="scope">
            <!-- 申请借书按钮-->
            <el-tooltip
              effect="dark"
              content="申请借书"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="editUserBorrowInfo(scope.row.bID)"
              >
              </el-button>
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

    <!--    借书的对话框-->
    <!--    对话框头部-->
    <el-dialog
      title="书籍申借信息确认"
      :visible.sync="editDialogVisible"
      width="40%"
      @close="editDialogClosed"
    >
      <!--     对话框内容主体区-->
      <el-form
        :model="editForm"
        :rules="editRules"
        ref="editFormRef"
        label-width="120px"
      >
        <el-form-item label="图书ID" prop="bID">
          <el-input v-model="editForm.bID" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户ID" prop="uID">
          <el-input v-model="editForm.uID" disabled></el-input>
        </el-form-item>
      </el-form>
      <!--      对话框底部区域-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editUserBorrowInfo">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ReaderBookList",
  //页面测试数据
  data() {
    var checkbID = (rule, value, callback) => {
      const regbID = /^[0-9]{8}$/;
      if (regbID.test(value)) return callback();
      else callback(new Error("请输入图书ID号长度有误"));
    };

    return {
      //验证图书ID，年份，库存总量，余量的规则

      queryInfo: {
        query: "", //搜索关键字
        qparam: 1, //搜索图书选项参数
        qsort: 11, //图书排序参数
        pagenum: 1, //当前页码
        pagesize: 10, //每页显示条数
      },
      booksList: [],
      total: 3, //此为一共几条记录,现在定义死了，以后会随着API获取更改

      editDialogVisible: false, //控制借书信息对话框的显示与隐藏
      editForm: {
        bID: "",
        uID: "",
        returnCondition: "未确认",
      },
      editRules: {
        bName: [
          { required: true, message: "请输入图书名称", trigger: "blur" },
          {
            min: 1,
            max: 20,
            message: "长度在 1 到 20 个字符",
            trigger: "blur",
          },
        ],
        bID: [
          { required: true, message: "请输入图书ID号", trigger: "blur" },
          { validator: checkbID, trigger: "blur" },
        ],
        uName: [
          { required: true, message: "请输入读者名称", trigger: "blur" },
          {
            min: 1,
            max: 20,
            message: "长度在 1 到 20 个字符",
            trigger: "blur",
          },
        ],
        uID: [{ required: true, message: "请输入读者ID号", trigger: "blur" }],
      },
      //修改图书信息表单验证归规则对象
    };
  },
  created() {
    this.getBooksList();
  }, //生命周期函数，再次发起获取数据请求*/
  methods: {
    async getBooksList() {
      await new Promise((resolve) => {
        this.$http
          .post("/users/booklist/", JSON.stringify(this.queryInfo))
          .then((res) => {
            console.log(res);
            if (res.status !== 200)
              return this.$message.error("获取图书列表失败");
            else {
              this.$message.success("获取图书列表成功！");
              console.log(res);
              this.booksList = [];
              for (let i = 0; i < res.data.bookInfo.length; i++)
                this.booksList.push(res.data.bookInfo[i]);
              this.total = res.data.total;
            }
          });
        resolve();
      });
    },
    //获取图书信息列表函数
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getBooksList();
    }, //函数用来监听pagesize的改变情况
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage;
      this.getBooksList();
    }, //函数用来监听页码值改变的事件
    onSortChange({ prop, order }) {
      if (prop === "bID" && order === "ascending") this.queryInfo.qsort = 11;
      else if (prop === "bID" && order === "descending")
        this.queryInfo.qsort = 10;
      else if (prop === "bName" && order === "ascending")
        this.queryInfo.qsort = 21;
      else if (prop === "bName" && order === "descending")
        this.queryInfo.qsort = 20;
      else if (prop === "bYear" && order === "ascending")
        this.queryInfo.qsort = 31;
      else if (prop === "bYear" && order === "descending")
        this.queryInfo.qsort = 30;
      else if (prop === "bLeft" && order === "ascending")
        this.queryInfo.qsort = 41;
      else if (prop === "bLeft" && order === "descending")
        this.queryInfo.qsort = 40;
      else this.queryInfo.qsort = 11;

      this.getBooksList();
      //与后端连接后，解除此行注释
    },

    async showEditDialog(bName, bID, bAuthor, bYear, bTotal, bLeft) {
      //bID是以参数scope.row.bID的形式获取到的

      console.log(bID);
      this.editForm.bName = bName;
      this.editForm.bID = bID;
      this.editForm.bAuthor = bAuthor;
      this.editForm.bYear = bYear;
      this.editForm.bTotal = bTotal;
      this.editForm.bLeft = bLeft;
      this.editDialogVisible = true;
      this.editForm.uName = JSON.parse(window.sessionStorage.getItem("uName"));
      this.editForm.uID = JSON.parse(window.sessionStorage.getItem("uID"));
    }, //点击修改按钮，弹出修改图书对话框
    editDialogClosed() {
      this.$refs.editFormRef.resetFields();
    }, //使得申借图书表单关闭以后就清空
    async editUserBorrowInfo(bID) {
      var tmpuid = window.sessionStorage.getItem("uID");
      this.editForm.uID = JSON.parse(tmpuid);
      this.editForm.bID = bID;
      await new Promise((resolve) => {
        this.$http
          .post("users/records/borrow/uID/", JSON.stringify(this.editForm))
          .then((res) => {
            //别忘了保证addForm中的元素名和接口中要求的一致
            //注意！！！要让后台给进行rID赋值
            console.log(res);
            if (res.data.success === false)
              this.$message.error(res.data.message);
            else this.$message.success("借书成功！");

            this.addDialogVisible = false;
            this.getBooksList(); //添加成功，重新获取借阅记录列表
          });
        resolve();
      });
    }, //申请借书
  },
};
</script>

<style  Lang="less" scoped>
</style>
