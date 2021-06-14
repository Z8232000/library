<template>
  <el-container class="home_container">
    <el-header>
      <div>
        <img src="../assets/bookLOGO.png"  alt="">
        <span>图书管理系统</span>
      </div>
      <el-button type="info" @click="logout">退出</el-button>
    </el-header>
    <el-container>
      <el-aside :width="isCollapse?'64px':'200px'">
        <!--侧边栏菜单区  -->
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <!--  侧边栏收缩按钮      -->
        <el-menu
            background-color="#333744"
            text-color="#fff"
            active-text-color="#409EFF"
            unique-opened :collapse="isCollapse"
            :collapse-transition="false"
            router
            :default-active="this.$route.path.substring(1,length)"
        >
          <!--一级菜单-->

          <el-menu-item index="1">
            <!--一级菜单模板区-->
            <!--图标-->
            <i class="el-icon-tickets"></i>
            <!-- 文本-->
            <span slot="title">图书信息</span>
          </el-menu-item>

          <el-menu-item index="2">
            <i class="el-icon-user"></i>
            <span slot="title">个人信息</span>
          </el-menu-item>

          <el-menu-item index="3">
            <i class="el-icon-document-copy"></i>
            <span slot="title">借阅记录</span>
          </el-menu-item>

        </el-menu>

      </el-aside>




      <el-main>
        <!--        添加路由占位符-->
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>

</template>

<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'

export default {//有了exp             ort default,其他的页面才能正常的将这个页面作为组件import
  name: 'ReaderHome',
  data(){
    return{
      isCollapse:false//定义菜单栏是否折叠属性
    }

  },
  methods:{
    logout(){
      window.sessionStorage.clear()
      this.$router.push('/Login')
    },

    toggleCollapse(){
      //在这里进行菜单折叠功能
      this.isCollapse=!this.isCollapse;
    }
  }

}
</script>

<style Lang="less" scoped>
.home_container{
  height:100%;
}
.el-header{
  display: flex;
  justify-content:space-between;
  background-color: black;
  padding-left: 0;
  align-items: center;
  color:white;
  font-size:20px;

  border-bottom: 1px solid dimgray;
  box-shadow: 0px 0px 5px black;

}
.el-header>div{
  display:flex;
  align-items:center;

}
.el-header>div>span{
  margin-left:15px;
}
.el-aside{
  background-color: #333744;
  box-shadow: 0px 0px 5px black;
}

.el-main{
  background-image:url(../assets/G211.jpg);
  background-repeat: no-repeat;
  background-size:100%;
  background-attachment: fixed;
  text-align: left;
}
.el-menu-item{
  font-size:15px;
  border-bottom: 1px solid black;
  box-shadow: 0px 0px 5px black;
}
.iconfont{
  margin-right:10px;
}
.toggle-button{
  background-color: #4A5064;
  font-size:10px;
  line-height:24px;
  color:#fff;
  text-align:center;
  letter-spacing: 0.2em;
  cursor: pointer;
  border-bottom: 1px solid dimgray;
}
</style>
