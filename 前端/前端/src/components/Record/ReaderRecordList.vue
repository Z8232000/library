<template>
  <div>
    <!--    面包屑导航区-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/Reader/Welcome' }"
        >首页</el-breadcrumb-item
      >
      <el-breadcrumb-item>个人借阅记录</el-breadcrumb-item>
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
      </el-row>
      <!--        借阅记录列表区-->

      <el-table
        :data="recordsList"
        :default-sort="{ prop: 'rID', order: 'ascending' }"
        border
        :row-class-name="tableRowClassName"
        ><!--最后一个属性为表格隔行变色-->
        <!--        index指定此列为索引列-->
        <template slot-scope="scope">
          <el-table-column label="#" type="index"> </el-table-column>
          <el-table-column label="借阅记录ID" prop="rID" sortable>
          </el-table-column>
          <el-table-column label="图书名称" prop="bName"> </el-table-column>
          <el-table-column label="图书ID" prop="bSingleID" sortable>
          </el-table-column>
          <el-table-column label="用户ID" prop="uID" sortable>
          </el-table-column>
          <el-table-column label="申借日期" prop="applyDate"> </el-table-column>
          <el-table-column label="借书日期" prop="borrowDate">
          </el-table-column>
          <el-table-column label="规定还书日期" prop="presetDate">
          </el-table-column>
          <el-table-column label="还书日期" prop="returnDate">
          </el-table-column>
          <el-table-column label="此书籍状态" prop="returnCondition">
          </el-table-column>
        </template>
        <!--        此处先只进行当前页内部排序，若要总体排序，后续修改-->
        <!--        在这里使用插槽作用域-->
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
  </div>
</template>

<script>
export default {
  name: "ReaderRecordList",
  //页面测试数据
  data() {
    return {
      //验证图书ID，年份，库存总量，余量的规则

      queryInfo: {
        query: "", //搜索关键字
        qparam: 1, //搜索借阅记录选项参数
        pagenum: 1, //当前页码
        pagesize: 10, //每页显示条数
        uID: "",
      },
      recordsList: [],
      total: 3, //此为一共几条记录,现在定义死了，以后会随着API获取更改
    };
  },
  created() {
    this.getRecordsList();
  }, //生命周期函数，再次发起获取数据请求*/
  methods: {
    async getRecordsList() {
      var tmpuid = window.sessionStorage.getItem("uID");
      this.queryInfo.uID = JSON.parse(tmpuid);
      await new Promise((resolve) => {
        this.$http
          .post("/users/records/all/uID/", JSON.stringify(this.queryInfo))
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
</style>
