<template>
  <div>
    <!--    面包屑导航区-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>待还记录</el-breadcrumb-item>
    </el-breadcrumb>

    <!--    卡片视图区-->
    <el-card class="box-card">
      <!--      引入栅格系统，方便布局-->
      <el-row :gutter="20">
        <!--      搜索框区域，span代表占几个格子，gutter控制间隙-->
        <el-col :span="8">
          <!--      搜索框-->
          <el-input placeholder="请输入待还记录ID/图书ID/读者ID" v-model="queryInfo.query" @clear="getReturnList" clearable >
            <!--            @clear="getReturnList"应该加入上面标签中，以实现一清空，下面列表立刻刷新-->
            <el-select v-model="queryInfo.qparam" slot="prepend" placeholder="请选择" >
              <el-option label="待还记录ID" value="1"></el-option>
              <el-option label="图书ID" value="2" ></el-option>
              <el-option label="读者ID" value="3"></el-option>
              <el-option label="图书名称" value="4"></el-option>
            </el-select>
            <el-button slot="append" icon="el-icon-search" @click="getReturnList"></el-button>
            <!--@click="getReturnList"应该加入上面标签中，以实现搜索-->
          </el-input>

        </el-col>
      </el-row>
      <!--        待还记录列表区-->
      <el-table :data="ReturnList" @sort-change="onSortChange" border stripe><!--最后一个属性为表格隔行变色-->
        <!--        index指定此列为索引列-->
        <el-table-column label="#" type="index"> </el-table-column>
        <el-table-column label="待借记录ID" prop="rID" sortable="custom" :sort-orders="['ascending','descending']"> </el-table-column>
        <el-table-column label="图书名称" prop="bName"> </el-table-column>
        <el-table-column label="图书ID" prop="bSingleID" sortable="custom" :sort-orders="['ascending','descending']"> </el-table-column>
        <el-table-column label="用户ID" prop="uID" sortable="custom" :sort-orders="['ascending','descending']"> </el-table-column>
        <el-table-column label="借书日期" prop="borrowDate"> </el-table-column>
        <el-table-column label="规定还书日期" prop="presetDate"> </el-table-column>
        <el-table-column label="此书籍状态" prop="returnCondition"> </el-table-column>

        <!--        此处先只进行当前页内部排序，若要总体排序，后续修改-->
        <!--        在这里使用插槽作用域-->

        <el-table-column label="还书" class="orderRow">
          <template slot-scope="scope">
            <!-- 还书按钮-->
            <el-tooltip effect="dark" content="还书" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="editReturnInfo
              (scope.row.rID)">
              </el-button>
            </el-tooltip>
<!--            只能删已还书的记录-->
<!--            &lt;!&ndash; 删除按钮&ndash;&gt;-->
<!--            <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">-->
<!--              <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeReturnByrID(scope.row.rID)"></el-button>-->
<!--            </el-tooltip>-->


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

    <!--    修改待还记录即确认借阅的对话框-->
    <!--    对话框头部-->
    <el-dialog title="还书确认" :visible.sync="editDialogVisible" width="40%">
      <!--对话框主体区域-->
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="120px">
        <el-form-item label="待还记录ID" prop="rID">
          <el-input v-model="editForm.rID" disabled></el-input>
        </el-form-item>
        <el-form-item label="图书名称" prop="bName">
          <el-input v-model="editForm.bName" disabled></el-input>
        </el-form-item>
        <el-form-item label="图书ID" prop="bSingleID">
          <el-input v-model="editForm.bSingleID" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户名称" prop="uName">
          <el-input v-model="editForm.uName" disabled></el-input>
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
        <el-form-item label="还书日期" prop="returnDate">
          <el-col :span="11">
            <el-date-picker type="date" placeholder="选择日期" v-model="editForm.returnDate" style="width: 100%;">
            </el-date-picker>
          </el-col>
        </el-form-item>

      </el-form>
      <!--      对话框底部-->
      <span slot="footer" class="dialog-footer">
    <el-button @click="editDialogVisible = false" @close="editDialogClosed">取 消</el-button>
    <el-button type="primary" @click="editReturnInfo">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "BorrowList",
  //页面测试数据
  data(){
    var checkbSingleID=(rule,value,callback)=>{
      const regbSingleID=/^[0-9]{10}$/
      if(regbSingleID.test(value))
        return callback()
      else
        callback(new Error('输入图书ID号长度有误'))
    }
    var checkuID=(rule,value,callback)=>{
      const reguID=/^[1-2][0-9]{7}$/
      if(reguID.test(value))
        return callback()
      else
        callback(new Error('请输入合法的学号/工号'))
    }

    return{
      //验证图书ID，年份，库存总量，余量的规则

      queryInfo: {
        query: '', //搜索关键字
        qparam:1,//搜索待借记录选项参数
        qsort:11,//记录排序参数
        pagenum: 1,//当前页码
        pagesize: 10,//每页显示条数
      },
      ReturnList:[],
      total:3,//此为一共几条记录,现在定义死了，以后会随着API获取更改


      editDialogVisible:false,//控制还书确认对话框的显示与隐藏,rID为待还单号
      editForm: {
        rID:"",
        bName:"",
        bSingleID:"",
        uName:"",
        uID:"",
        applyDate:"",
        borrowDate:"",
        presetDate:"",
        returnCondition:"借阅未还",
      },
      editRules: {
        rID: [
          { required: true },
        ],
        bName: [
          { required: true, message: '请输入图书名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ],
        bSingleID: [
          { required: true, message: '请输入图书ID号', trigger: 'blur' },
          {validator:checkbSingleID,trigger:'blur'}
        ],
        uName: [
          { required: true, message: '请输入用户名称', trigger: 'blur' },
          { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
        ],
        uID: [
          { required: true, message: '请输入学号/工号', trigger: 'blur' },
          { validator:checkuID, trigger:'blur' }
        ],
        borrowDate: [
          { required: true, message: '请输入图书借阅日期', trigger: 'blur' },
        ],
        presetDate: [
          { required: true, message: '请输入图书规定归还日期', trigger: 'blur' },
        ],
        returnDate: [
          { required: true, message: '请输入图书归还日期', trigger: 'blur' },
        ],
        returnCondition: [
          { required: true, message: '请修改该记录图书归还状态', trigger: 'blur' },
        ],

      }
      //修改图书待还记录表单验证规则对象
    }
  },
  created(){
    this.getReturnList();
  },//生命周期函数，再次发起获取数据请求*/
  methods:{
    async getReturnList() {
      await new Promise(resolve => {
        this.$http.post('/operator/records/', JSON.stringify(this.queryInfo)).then(res => {
          console.log(res)
          if (res.status !== 200)
            this.$message.error('获取待还记录列表失败！')
          else {
            this.$message.success('获取待还列表成功！')
            console.log(res);
            this.ReturnList = [];
            for (let i = 0; i < res.data.recordInfo.length; i++) {
              if (res.data.recordInfo[i].returnCondition == 0)
                res.data.recordInfo[i].returnCondition = "未确认"
              else if (res.data.recordInfo[i].returnCondition == 1)
                res.data.recordInfo[i].returnCondition = "借阅未还"
              else if (res.data.recordInfo[i].returnCondition == 2)
                res.data.recordInfo[i].returnCondition = "借阅已还"
              else if (res.data.recordInfo[i].returnCondition == 3)
                res.data.recordInfo[i].returnCondition = "过期未还"

              this.ReturnList.push(res.data.recordInfo[i]);
            }
            this.total = res.data.total;

          }
        })
        resolve();
      })


    },
    handleSizeChange(newSize){
      this.queryInfo.pagesize=newSize;
      this.getReturnList();
    },//函数用来监听pagesize的改变情况
    handleCurrentChange(newPage){
      this.queryInfo.pagenum=newPage;
      this.getReturnList();
    },//函数用来监听页码值改变的事件
    onSortChange({ prop, order }) {
      if(prop==='rID'&&order==='ascending')
        this.queryInfo.qsort=11;
      else if(prop==='rID'&&order==='descending')
        this.queryInfo.qsort=10;
      else if(prop==='bSingleID'&&order==='ascending')
        this.queryInfo.qsort=21;
      else if(prop==='bSingleID'&&order==='descending')
        this.queryInfo.qsort=20;
      else if(prop==='uID'&&order==='ascending')
        this.queryInfo.qsort=31;
      else if(prop==='uID'&&order==='descending')
        this.queryInfo.qsort=30;
      else
        this.queryInfo.qsort=11;

      this.getReturnList();
      //与后端连接后，解除此行注释
    },





    async showEditDialog(rID,bName,bSingleID,uName,uID,borrowDate,presetDate,returnCondition){
      //aID是以参数scope.row.rID的形式获取到的
      console.log(rID)
      this.editForm.rID=rID
      this.editForm.bSingleID=bSingleID
      this.editForm.bName=bName
      this.editForm.uID=uID
      this.editForm.uName=uName
      this.editForm.borrowDate=borrowDate
      this.editForm.presetDate=presetDate
      this.editForm.returnCondition=returnCondition

      this.editDialogVisible=true

    },//点击修改按钮，弹出修改待还记录即还书对话框
    editDialogClosed(){
      this.$refs.editFormRef.resetFields()
    },//使得修改待还记录表单关闭以后就清空
    async editReturnInfo(rID){
      await new Promise(resolve => {
        this.$http.post('/operator/return/rID/', JSON.stringify({rID})).then(res => {
          if (res.data.success === false)
            this.$message.error(res.data.message)
          else
            this.$message.success('还书成功！')
          this.getReturnList()//修改成功，重新获取借阅记录列表
        })
        resolve();
      })

    },//修改待还记录列表

    // async removeReturnByrID(rID){
    //   console.log(rID)
    //   const confirmResult = await this.$confirm('此操作将永久删除该记录, 是否继续?', '提示', {
    //     confirmButtonText: '确定',
    //     cancelButtonText: '取消',
    //     type: 'warning'
    //   }).catch(err => {
    //     return err
    //   })
    //
    //   if (confirmResult !== 'confirm')
    //     return this.$message.info('已取消删除。')
    //
    //   await new Promise(resolve => {
    //     this.$http.post('/records/del/', JSON.stringify({rID})).then(res => {
    //       if (res.status !== 200)
    //         this.$message.error('删除借阅记录失败！')
    //       else
    //         this.$message.success('删除借阅记录成功！')
    //       this.getReturnList()
    //
    //       //进行删除借阅记录操作
    //     })
    //   })
    //
    // } //根据rID删除对应待借记录信息








  }

}
</script>

<style  Lang="less" scoped>
.el-button{
  margin-left:2px !important;
}

</style>
