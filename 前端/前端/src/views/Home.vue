<template>
  <el-container class="home_container">
    <el-header>
      <div>
        <img src="../assets/bookLOGO.png" alt="" />
        <span>图书管理系统</span>
      </div>
      <el-button type="info" @click="logout">退出</el-button>
    </el-header>
    <el-container>
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <!--侧边栏菜单区  -->
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <!--  侧边栏收缩按钮      -->
        <el-menu
          background-color="#333744"
          text-color="#fff"
          active-text-color="#409EFF"
          unique-opened
          :collapse="isCollapse"
          :collapse-transition="false"
          router
          :default-active="this.$route.path.substring(1, length)"
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
            <span slot="title">用户列表</span>
          </el-menu-item>

          <el-menu-item index="3">
            <i class="el-icon-document-copy"></i>
            <span slot="title">借阅记录</span>
          </el-menu-item>

          <el-menu-item index="4">
            <i class="el-icon-message"></i>
            <span slot="title">书籍借阅</span>
          </el-menu-item>

          <el-menu-item index="5">
            <i class="el-icon-thumb"></i>
            <span slot="title">书籍归还</span>
          </el-menu-item>
          <el-menu-item index="6">
            <i class="el-icon-goods"></i>
            <span slot="title">图书荐购</span>
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

export default {
  //有了export default,其他的页面才能正常的将这个页面作为组件import
  name: "Home",
  data() {
    return {
      isCollapse: false, //定义菜单栏是否折叠属性
    };
  },
  methods: {
    logout() {
      window.sessionStorage.clear();
      this.$router.push("/Login");
      this.$store.commit("logout");
    },
    login() {
      this.$router.push("/Login");
      this.$store.commit("login");
    },

    toggleCollapse() {
      //在这里进行菜单折叠功能
      this.isCollapse = !this.isCollapse;
    },
  },
};
</script>

<style Lang="less" scoped>
.home_container {
  height: 100%;
}
.el-header {
  display: flex;
  justify-content: space-between;
  background-color: black;
  padding-left: 0;
  align-items: center;
  color: white;
  font-size: 20px;

  border-bottom: 1px solid dimgray;
  box-shadow: 0px 0px 5px black;
}
.el-header > div {
  display: flex;
  align-items: center;
}
.el-header > div > span {
  margin-left: 15px;
}
.el-aside {
  background-color: #333744;
  box-shadow: 0px 0px 5px black;
}

.el-main {
  position: relative;
  background-color: #eaedf1;
  text-align: left;
}

.el-menu-item {
  font-size: 15px;
  border-bottom: 1px solid black;
  box-shadow: 0px 0px 5px black;
}

.iconfont {
  margin-right: 10px;
}
.toggle-button {
  background-color: #4a5064;
  font-size: 10px;
  line-height: 24px;
  color: white;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
  border-bottom: 1px solid dimgray;
}
.aaa {
  /*filter:alpha(Opacity=85);
  -moz-opacity:0.85;
  opacity: 0.85;
  */
}

/*在这里修改侧边栏和顶部颜色
.el-header{
  background-color: black;
}
.el-aside{
  background-color: rgb(0,102,0);
}
.el-menu-item{
  background-color:rgb(0,102,0)!important;
}
.el-menu-item.is-active{
  background-color:rgb(97,193,0)!important;
}
.toggle-button{
  background-color: rgb(0,102,0);
}*/
</style>