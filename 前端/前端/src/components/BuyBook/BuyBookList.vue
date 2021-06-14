<template>
  <div>
    <!--    面包屑导航区-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>图书荐购</el-breadcrumb-item>
    </el-breadcrumb>

    <!--    卡片视图区-->
    <el-card class="box-card">
      <!--      引入栅格系统，方便布局-->
      <el-row :gutter="20">
        <!--      搜索框区域，span代表占几个格子，gutter控制间隙-->
        <el-col :span="8">
          <!--      搜索框-->
          <el-input placeholder="请输入图书名称/作者名称" v-model="queryInfo.query"  @clear="getBuyBooksList" clearable >
            <!--            @clear="getBuyBooksList"应该加入上面标签中，以实现一清空，下面列表立刻刷新-->
            <el-select v-model="queryInfo.qparam" slot="prepend" placeholder="请选择" >
              <el-option label="图书名称" value="1" ></el-option>
              <el-option label="作者名称" value="2" ></el-option>
            </el-select>
            <el-button slot="append" icon="el-icon-search" @click="getBuyBooksList"></el-button>
            <!--@click="getBuyBooksList"应该加入上面标签中，以实现搜索-->
          </el-input>
        </el-col>

      </el-row>
      <!--        借阅记录列表区-->
      <el-table :data="buyBooksList"  border stripe><!--最后一个属性为表格隔行变色-->
        <!--        index指定此列为索引列-->
        <el-table-column label="#" type="index"> </el-table-column>
        <el-table-column label="图书类ID" prop="bID"> </el-table-column>
        <el-table-column label="图书名称" prop="bName"> </el-table-column>
        <el-table-column label="图书作者" prop="bAuthor"> </el-table-column>
        <el-table-column label="图书出版年份" prop="bYear"> </el-table-column>
        <el-table-column label="荐购总量" prop="bTotal"></el-table-column>
        <el-table-column label="荐购理由" prop="bReason" ></el-table-column>
        <!--        此处先只进行当前页内部排序，若要总体排序，后续修改-->
        <!--        在这里使用插槽作用域-->
        <el-table-column label="删除图书" class="orderRow">
          <template slot-scope="scope">
            <!-- 删除按钮-->
            <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeBuyBookBybID(scope.row.bID)"></el-button>
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
          :total="total">
      </el-pagination>

    </el-card>




  </div>
</template>

<script>
export default {
  name: "BuyBookList",
  //页面测试数据
  data(){

    return {
      //验证图书ID，年份，库存总量，余量的规则

      queryInfo: {
        query: '', //搜索关键字
        qparam: 1,//搜索图书选项参数
        pagenum: 1,//当前页码
        pagesize: 10,//每页显示条数
      },
      buyBooksList: [],
      total: 3,//此为一共几条记录,现在定义死了，以后会随着API获取更改



    }

  },
  created(){
    this.getBuyBooksList();
  },//生命周期函数，再次发起获取数据请求*/
  methods:{

    async getBuyBooksList() {
      await new Promise(resolve => {
        this.$http.post('/operator/buyBooks/', JSON.stringify(this.queryInfo)).then(res => {
          console.log(res)
          if (res.status !== 200)
            this.$message.error('获取荐购记录列表失败！')
          else {
            this.$message.success('获取荐购记录列表成功！')
            console.log(res);
            this.buyBooksList = [];
            for (let i = 0; i < res.data.recordInfo.length; i++)
              this.buyBooksList.push(res.data.recordInfo[i]);

            this.total = res.data.total;

          }
        })
        resolve();
      })

    },
    //获取图书信息列表函数
    handleSizeChange(newSize){
      this.queryInfo.pagesize=newSize;
      //this.getBooksList();
    },//函数用来监听pagesize的改变情况
    handleCurrentChange(newPage){
      this.queryInfo.pagenum=newPage;
      //this.getBooksList();
    },//函数用来监听页码值改变的事件
    async removeBuyBookBybID(bID){
      //弹框询问用户是否删除数据
      const confirmResult=await this.$confirm('此操作将永久删除该记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err=>{return err})

      if(confirmResult!=='confirm')
        return this.$message.info('已取消删除。')

      console.log(bID)
      await new Promise(resolve => {
        this.$http.post('/operator/buyBooks/bID/', JSON.stringify({bID})).then(res => {
          console.log(res);
          if (res.data.success === false)
            this.$message.error('删除借阅记录失败！')
          else
            this.$message.success('删除借阅记录成功！')
          this.getBuyBooksList()

          //进行删除借阅记录操作
        })
      })

    }, //根据bID删除对应书籍信息




  }

}
</script>

<style  Lang="scss" scoped>
.el-tooltip.el-button{
  margin-left:40px;
}
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}

</style>
