<template>
  <div>
    <!--    面包屑导航区-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>图书列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!--    卡片视图区-->
    <el-card class="box-card">
      <!--      引入栅格系统，方便布局-->
      <el-row :gutter="20">
        <!--      搜索框区域，span代表占几个格子，gutter控制间隙-->
        <el-col :span="8">
          <!--      搜索框-->
          <el-input placeholder="请输入图书名称/图书ID/作者名称" v-model="queryInfo.query"  @clear="getBooksList" clearable >
            <!--            @clear="getBooksList"应该加入上面标签中，以实现一清空，下面列表立刻刷新-->
            <el-select v-model="queryInfo.qparam" slot="prepend" placeholder="请选择" >
              <el-option label="图书名称" value="1" ></el-option>
              <el-option label="图书类ID" value="2"></el-option>
              <el-option label="作者名称" value="3" ></el-option>
            </el-select>
            <el-button slot="append" @click="getBooksList" icon="el-icon-search"></el-button>
            <!--@click="getBooksList"应该加入上面标签中，以实现搜索-->
          </el-input>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="addDialogVisible=true">添加图书</el-button>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="deleteDialogVisible=true">删除单本图书</el-button>
        </el-col>
      </el-row>
      <!--        借阅记录列表区-->
      <el-table :data="booksList"  @sort-change="onSortChange" border stripe >
        <!--最后一个属性为表格隔行变色-->
        <!--        index指定此列为索引列-->
        <el-table-column label="#" type="index"> </el-table-column>
        <el-table-column label="图书名称" prop="bName"  sortable="custom" :sort-orders="['ascending','descending']"> </el-table-column>
        <el-table-column label="图书编号" prop="bID" sortable="custom" :sort-orders="['ascending','descending']"> </el-table-column>
        <el-table-column label="图书作者" prop="bAuthor"> </el-table-column>
        <el-table-column label="图书出版年份" prop="bYear"  sortable="custom" :sort-orders="['ascending','descending']"> </el-table-column>
        <el-table-column label="库藏总量" prop="bTotal"></el-table-column>
        <el-table-column label="可借余量" prop="bLeft"  sortable="custom" :sort-orders="['ascending','descending']"></el-table-column>
        <!--        此处先只进行当前页内部排序，若要总体排序，后续修改-->
        <!--        在这里使用插槽作用域-->

        <el-table-column label="修改图书/删除图书" class="orderRow">
          <template slot-scope="scope">
            <!-- 修改按钮-->
            <el-tooltip effect="dark" content="修改" placement="top" :enterable="false">
              <el-button type="primary" icon="el-icon-edit" size="mini" @click="showEditDialog
              (scope.row.bName,scope.row.bID,scope.row.bAuthor,scope.row.bYear,
              scope.row.bTotal)">
              </el-button>
            </el-tooltip>

            <!-- 删除按钮-->
            <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
              <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeBookBybID(scope.row.bID)"></el-button>
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
    <!--    添加图书的对话框-->
    <el-dialog
        title="添加图书"
        :visible.sync="addDialogVisible"
        width="40%"
        @close="addDialogClosed">

      <!--     对话框内容主体区-->
      <el-form :model="addForm" :rules="addRules" ref="addFormRef" label-width="120px">
        <el-form-item label="图书名称" prop="bName">
          <el-input v-model="addForm.bName"></el-input>
        </el-form-item>
        <el-form-item label="图书作者" prop="bAuthor">
          <el-input v-model="addForm.bAuthor"></el-input>
        </el-form-item>
        <el-form-item label="图书出版年份" prop="bYear">
          <el-input v-model="addForm.bYear"></el-input>
        </el-form-item>
        <el-form-item label="图书库藏总量" prop="bTotal">
          <el-input v-model="addForm.bTotal"></el-input>
        </el-form-item>

      </el-form>
      <!--      对话框底部区域-->
      <span slot="footer" class="dialog-footer">
    <el-button @click="addDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addBook">确 定</el-button>
  </span>
    </el-dialog>

    <el-dialog
        title="删除单本图书"
        :visible.sync="deleteDialogVisible"
        width="40%"
        @close="deleteDialogClosed">

      <!--     对话框内容主体区-->
      <el-form :model="deleteForm" :rules="deleteRules" ref="deleteFormRef" label-width="120px">
        <el-form-item label="图书ID" prop="bID">
          <el-input v-model="deleteForm.bID"></el-input>
        </el-form-item>
        <el-form-item label="图书个体ID" prop="bSingleID">
          <el-input v-model="deleteForm.bSingleID"></el-input>
        </el-form-item>
      </el-form>
      <!--      对话框底部区域-->
      <span slot="footer" class="dialog-footer">
    <el-button @click="deleteDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="deleteBook()">确 定</el-button>
  </span>
    </el-dialog>

    <!--    修改图书的对话框-->
    <!--    对话框头部-->
    <el-dialog title="修改图书" :visible.sync="editDialogVisible" width="40%">
      <!--对话框主体区域-->
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="120px">
        <el-form-item label="图书ID" prop="bID">
          <el-input v-model="editForm.bID" disabled></el-input>
        </el-form-item>
        <el-form-item label="图书名称" prop="bName">
          <el-input v-model="editForm.bName"></el-input>
        </el-form-item>
        <el-form-item label="图书作者" prop="bAuthor">
          <el-input v-model="editForm.bAuthor"></el-input>
        </el-form-item>
        <el-form-item label="图书出版年份" prop="bYear">
          <el-input v-model="editForm.bYear"></el-input>
        </el-form-item>
        <el-form-item label="图书库藏总量（只可添加）" prop="bTotal">
          <el-input v-model="editForm.bTotal" ></el-input>
        </el-form-item>

      </el-form>
      <!--      对话框底部-->
      <span slot="footer" class="dialog-footer">
    <el-button @click="editDialogVisible = false" @close="editDialogClosed">取 消</el-button>
    <el-button type="primary" @click="editBookInfo">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "BookList",
  //页面测试数据
  data(){
    var checkbID=(rule,value,callback)=>{
      const regbID=/^[0-9]{8}$/
      if(regbID.test(value))
        return callback()
      else
        callback(new Error('输入图书ID号长度有误，应为8位'))
    }
    var checkbSingleID=(rule,value,callback)=>{
      const regbSingleID=/^[0-9]{11}$/
      if(regbSingleID.test(value))
        return callback()
      else
        callback(new Error('输入图书个体ID号长度有误，应为11位'))
    }
    var checkbYear=(rule,value,callback)=>{
      const regbYear=/^[1-2][0-9]{3}$/
      if(regbYear.test(value))
        return callback()
      else
        callback(new Error('请输入合法的年份'))
    }
    var checkbTotal = (rule, value, callback) => {
      const regbTotal = /^[0-9]{1,3}$/
      if (regbTotal.test(value))
        return callback()
      else
        callback(new Error('请输入合法的库藏总量,不可超过三位'))
    };
    var checkbLeft=(rule,value,callback)=>{
      const regbLeft=/^[0-9]{1,3}$/
      if(regbLeft.test(value))
        return callback()
      else
        callback(new Error('请输入合法的库藏余量，不可超过三位'))
    };
    var check_bTotal = (rule, value, callback) => {
      const regbTotal = /^[0-9]{1,3}$/
      if(parseInt(value)<this.editTmp)
        callback(new Error('请输入比原来库藏总量更大的数额'))
      if (regbTotal.test(value))
        return callback()
      else
        callback(new Error('请输入合法的库藏总量，不可超过三位'))
    };
    return{
      //验证图书ID，年份，库存总量，余量的规则

      queryInfo: {
        query: '', //搜索关键字
        qparam:1,//搜索图书选项参数
        qsort:11,//图书排序参数
        pagenum: 1,//当前页码
        pagesize: 10,//每页显示条数
      },
      booksList:[],
      total:3,//此为一共几条记录,现在定义死了，以后会随着API获取更改



      addDialogVisible:false,//控制添加用户对话框的显示与隐藏
      addForm: {
        bName:"",
        bAuthor:"",
        bYear:"",
        bTotal:0,
        bLeft:0
      },
      addRules: {
        bName: [
          { required: true, message: '请输入图书名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ],
        bAuthor: [
          { required: true, message: '请输入图书作者', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        bYear: [
          { required: true, message: '请输入图书出版年份', trigger: 'blur' },
          {validator:checkbYear,trigger:'blur'}
        ],
        bTotal: [
          { required: true, message: '请输入图书库藏总量', trigger: 'blur' },
          {validator:checkbTotal,trigger:'blur'}
        ],
        bLeft: [
          { required: true, message: '请输入图书库藏余量,不可超过三位', trigger: 'blur' },
          {validator:checkbLeft,trigger:'blur'}
        ],

      },
      //添加表单验证归规则对象


      editDialogVisible:false,//控制修改图书信息对话框的显示与隐藏
      editForm: {
        bName:"",
        bID:"",
        bAuthor:"",
        bYear:2000,
        bTotal:0,
        bLeft:0
      },
      editTmp:0,
      editRules: {
        bName: [
          { required: true, message: '请输入图书名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ],
        bID: [
          { required: true, message: '请输入8位图书ID号', trigger: 'blur' },
          {validator:checkbID,trigger:'blur'}
        ],
        bAuthor: [
          { required: true, message: '请输入图书作者', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        bYear: [
          { required: true, message: '请输入图书出版年份', trigger: 'blur' },
          {validator:checkbYear,trigger:'blur'}
        ],
        bTotal: [
          { required: true, message: '请输入图书库藏总量，不可超过三位', trigger: 'blur' },
          {validator:check_bTotal,trigger:'blur'}
        ],


      },
      //修改图书信息表单验证归规则对象

      deleteDialogVisible:false,//控制添加用户对话框的显示与隐藏
      deleteForm: {
        bID:"",
        bSingleID:"",
      },
      deleteRules: {

        bID: [
          { required: true, message: '请输入8位图书ID号', trigger: 'blur' },
          {validator:checkbID,trigger:'blur'}
        ],
        bSingleID: [
          { required: true, message: '请输入11位图书个体ID号', trigger: 'blur' },
          {validator:checkbSingleID,trigger:'blur'}
        ],

      },
      //添加表单验证归规则对象
    }




  },
  created(){
    this.getBooksList();
  },//生命周期函数，再次发起获取数据请求*/
  methods:{


    async getBooksList(){
      await new Promise((resolve)=>{
        this.$http.post('/users/booklist/', JSON.stringify(this.queryInfo)).then(res=>{
            console.log(res);
            if(res.status!==200)
                return this.$message.error('获取图书列表失败')
              else
              {
                this.$message.success('获取图书列表成功！')
                console.log(res);
                this.booksList=[];
                for(let i=0; i<res.data.bookInfo.length; i++)
                  this.booksList.push(res.data.bookInfo[i]);
                this.total=res.data.total;

              }

        })
        resolve();
      })



      },
    //获取图书信息列表函数
    handleSizeChange(newSize){
      this.queryInfo.pagesize=newSize;
      this.getBooksList();
    },//函数用来监听pagesize的改变情况
    handleCurrentChange(newPage){
      this.queryInfo.pagenum=newPage;
      this.getBooksList();
    },//函数用来监听页码值改变的事件

    onSortChange({ prop, order }) {
      if(prop==='bID'&&order==='ascending')
        this.queryInfo.qsort=11;
      else if(prop==='bID'&&order==='descending')
        this.queryInfo.qsort=10;
      else if(prop==='bName'&&order==='ascending')
        this.queryInfo.qsort=21;
      else if(prop==='bName'&&order==='descending')
        this.queryInfo.qsort=20;
      else if(prop==='bYear'&&order==='ascending')
        this.queryInfo.qsort=31;
      else if(prop==='bYear'&&order==='descending')
        this.queryInfo.qsort=30;
      else if(prop==='bLeft'&&order==='ascending')
        this.queryInfo.qsort=41;
      else if(prop==='bLeft'&&order==='descending')
        this.queryInfo.qsort=40;
      else
        this.queryInfo.qsort=11;

      this.getBooksList();
      //与后端连接后，解除此行注释
    },







    addDialogClosed(){
      this.$refs.addFormRef.resetFields()
    },//使得表单关闭以后就清空
    addBook(){
      this.$refs.addFormRef.validate(async valid=>{
            if(!valid)return
            //可以发起添加图书的请求
            else
            {
              console.log(valid)
              await new Promise(resolve=>{
                this.$http.post('/books/',JSON.stringify(this.addForm)).then(res=>{
                  console.log(res);
                  if(res.success===false)
                    this.$message.error(res.message)
                  else
                    this.$message.success('添加图书成功！')

                  this.addDialogVisible = false
                  this.getBooksList()//添加成功，重新获取图书列表
                })//别忘了保证addForm中的元素名称和接口中要求的一致
                resolve();
              })


            }

          })
    },//点击按钮添加新图书之前，进行表单预验证


    async showEditDialog(bName,bID,bAuthor,bYear,bTotal){
      //bID是以参数scope.row.bID的形式获取到的
      console.log(bID)
      this.editForm.bName=bName
      this.editForm.bID=bID
      this.editForm.bAuthor=bAuthor
      this.editForm.bYear=bYear
      this.editForm.bTotal=bTotal
      this.editTmp=bTotal
      this.editDialogVisible=true

    },//点击修改按钮，弹出修改图书对话框
    editDialogClosed(){
      this.$refs.editFormRef.resetFields()
    },//使得修改图书表单关闭以后就清空
    editBookInfo(){
      this.$refs.editFormRef.validate(//
          async valid=>{
            if(!valid)return
            //可以发起修改图书的请求
            else
            {
              console.log(valid)
              await new Promise(resolve => {
                this.$http.post('/books/bID/',JSON.stringify(this.editForm)).then(res=>{
                  if(res.success===false)
                    return this.$message.error(res.message)
                  else
                    this.$message.success('更新图书信息成功！')
                  this.editDialogVisible = false
                  this.getBooksList()//修改成功，重新获取图书列表
                })
                resolve();
              })


            }

          })

    },//修改图书列表

    async removeBookBybID(bID){
      //弹框询问用户是否删除数据
      console.log(bID)
      const confirmResult=await this.$confirm('此操作将永久删除该书籍, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err=>{return err})

      if(confirmResult!=='confirm')
        return this.$message.info('已取消删除。')

       await new Promise(resolve=>{
         this.$http.post('/books/del_bID/',JSON.stringify({bID})).then(res=>{
           if(res.success===false)
              this.$message.error(res.message)
           else
              this.$message.success('删除图书成功！')
           this.getBooksList()
         })
         resolve();
       })



      //进行删除书籍操作

    }, //根据bID删除对应书籍信息

    deleteDialogClosed(){
      this.$refs.deleteFormRef.resetFields()
    },//使得表单关闭以后就清空
    async deleteBook(){
      this.$refs.deleteFormRef.validate(
        async valid=>{
            if(!valid)return
            //可以发起删除单个图书的请求
            else
            {
              console.log(valid)
              const confirmResult=await this.$confirm('此操作将永久删除该单本书籍, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).catch(err=>{
                console.log('出错啦')
                return err})

              if(confirmResult!=='confirm')
                return this.$message.info('已取消删除。')

              console.log(this.deleteForm.bID,this.deleteForm.bSingleID)

              await new Promise(resolve=>{
                this.$http.post('/books/bID/bSingleID/', JSON.stringify(this.deleteForm)).then(res=>{
                  if(res.success===false)
                     this.$message.error(res.message)
                  else
                    this.$message.success('删除单本图书成功！')
                  this.deleteDialogVisible = false
                  this.getBooksList()//删除成功，重新获取图书列表
                })
                resolve();
              })

            }

          })
    },//点击按钮删除单本图书之前，进行表单预验证
/*
    removeBookBybSingleID(bID,bSingleID){
      //弹框询问用户是否删除数据
      const confirmResult=await this.$confirm('此操作将永久删除该单本书籍, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err=>{
        console.log('why?')
        return err})

      if(confirmResult!=='confirm')
        return this.$message.info('已取消删除。')

      console.log(bID,bSingleID)

      const {data:res}=await this.$http.post('/books/bID/bSingleID/', {bID,bSingleID})
       if(res.success===false)
         return this.$message.error(res.message)

       this.$message.success('删除单本图书成功！')
       this.getBooksList()

      //进行删除书籍操作

    }, //根据bID和bSingleID删除对应书籍信息
*/



  }

}
</script>

<style  Lang="less" scoped>


</style>
