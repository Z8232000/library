from django.db import models


# 用户
class User(models.Model):
    uName = models.CharField(max_length=30)
    uID = models.CharField(max_length=15)
    uPWD = models.CharField(max_length=25)
    uPhone = models.CharField(max_length=15)
    uCharacter = models.BooleanField(default=False)
    # True是管理员，False是读者，默认是读者


# 图书信息
class BookType(models.Model):
    # 图书名
    bName = models.CharField(max_length=30)
    # 图书ID
    bID = models.CharField(max_length=15)
    # 图书作者名
    bAuthor = models.CharField(max_length=20)
    # 图书出版年份
    bYear = models.IntegerField(null=True, blank=True)
    # 图书库藏总量
    bTotal = models.IntegerField(default=0)
    # 图书可借余量
    bLeft = models.IntegerField(default=0)


# 单本图书
class SingleBook(models.Model):
    # 图书ID，和在BookType的ID相同
    bID = models.CharField(max_length=15)
    # 同一书名的书可能有多本，每本书都有单独的个体ID
    bSingleID = models.CharField(max_length=15)
    # 借阅状态，True是可借状态，False是不可借状态，默认可借
    bCondition = models.BooleanField(default=True)


# 借阅记录
class BorrowRecord(models.Model):
    # 借阅记录单号
    rID = models.AutoField(primary_key=True)
    # 图书名
    bName = models.CharField(max_length=30)
    # 图书个体ID
    bSingleID = models.CharField(max_length=15)
    # 用户名
    uID = models.CharField(max_length=15)
    # 申借日期，默认在建表中该行时自动设置为当前时间
    applyDate = models.DateField('申借日期', auto_now_add=True)
    # 借书日期
    borrowDate = models.DateField(verbose_name='借书日期', blank=True, null=True)
    # 规定还书日期
    presetDate = models.DateField('规定还书日期', blank=True, null=True)
    # 还书日期
    returnDate = models.DateField('实际还书日期', blank=True, null=True)
    # 该记录状态：未确认，借阅未还，借阅已还，过期未还（0，1，2，3）
    returnCondition = models.IntegerField(default=0)


# 图书荐购信息
class RecommendBook(models.Model):
    # 荐购记录ID
    bID = models.AutoField(primary_key=True)
    # 图书名
    bName = models.CharField(max_length=30)
    # 图书作者
    bAuthor = models.CharField(max_length=20)
    # 图书出版年份
    bYear = models.IntegerField(default=0)
    # 荐购总量
    bTotal = models.IntegerField(default=1)
    # 荐购理由
    bReason = models.TextField(null=True, blank=True)
