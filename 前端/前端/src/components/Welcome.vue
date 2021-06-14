<template>
  <div class="aaa">
    <h3 style="color:white!important;margin-left:20px; ">欢迎使用本图书管理系统</h3>
    <el-carousel :interval="4000" type="card" height="400px">
      <el-carousel-item v-for="item in imgLink" :key="item">
        <el-image :src="item.graphLink"></el-image>
      </el-carousel-item>
    </el-carousel>
    <div class="bbb">
    <el-row :gutter="24">
      <el-col :span="16">
        <el-card>
          <h4>文明读者公约</h4>
          要衣着整洁；不穿背心、拖鞋入馆。<br>
          要讲究卫生；不随地吐痰、乱扔废弃物。<br>
          要举止文明；不在馆内争吵、打闹。<br>
          要保持安静；不在阅览室内喧哗、使用有声通讯工具。<br>
          要珍惜时间；不在阅览室内占座位、闲聊、睡觉。<br>
          要爱护公物；不污损建筑设施、毁坏书刊资料。<br>
          要遵纪守法；不做违反馆章馆规之事。<br>
          要自尊自爱；不做有碍人格和观瞻之举。<br>
          北航图书馆期望读者积极响应倡议，协助航图做好读者服务工作。<br>

          <h4> 北航图书馆服务规范</h4>
          爱岗敬业，无私奉献。<br>
          精通业务，开拓创新。<br>
          尊重读者，服务规范。<br>
          保护文献，传承文明。<br>

        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="aside">
          <el-image :src="require('../assets/7.jpeg')"></el-image>
          <div>
            <a href="https://movie.douban.com/subject/2976111/" target="_blank" style="color:grey ;"><h4>近日推荐书籍：我和狗狗的十个约定</h4></a>
            推荐句子：我永远都不会忘记和你在一起度过的美好时光，所以请你答应我，在我即将离开这个世界的时候，请你陪在我的身边。
          </div>
        </el-card>
        <el-card class="aside">
          <el-image :src="require('../assets/6.jpeg')"></el-image>
          <div>
            <a href="https://book.douban.com/subject/1084336/" target="_blank" style="color:grey ;"><h4>近日推荐书籍：小王子</h4></a>
            推荐句子：星星发光是为了让每一个人都能找到属于自己的星星。
          </div>
        </el-card>

      </el-col>
    </el-row>

    </div>

  </div>
</template>

<script>
export default {
  name: "Welcome",
  data(){
    return{
      imgLink:[
        {graphLink:require('../assets/81.jpg')},
        {graphLink:require('../assets/71.jpeg')},
        {graphLink:require('../assets/73.jpeg')},
        {graphLink:require('../assets/2.jpeg')},
          ],
    }
  }
}
</script>

<style Lang="less" scoped>

.el-carousel__item .el-image{
  width:100%;
  height:100%;
}
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;


}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

.el-card{
  text-align: center;
  line-height: 50px;

}
.aside{
  padding-top: 20px;
  margin-bottom: 20px;
  line-height: 30px;
}
.aaa{
  background-image:url(../assets/G210.jpg);
  background-repeat: no-repeat;
  background-size:100%;
  background-attachment: fixed;
}
.bbb{
  filter:alpha(Opacity=90);
  -moz-opacity:0.90;
  opacity: 0.90;
}
a:hover
{

  color:cornflowerblue !important;
  text-decoration:underline;
}
</style>
