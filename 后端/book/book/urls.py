"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import user.views
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/', include(user.urls)),

    url(r'^$', TemplateView.as_view(template_name="index.html")),

    path('users/', user.views.GetReaderList),
    path('users/uID/', user.views.AdminChangeUPhone),
    path('users/uPWD/', user.views.ReaderChangePWD),
    path('users/uInform/', user.views.ReaderChangeInfo),

    path('users/booklist/', user.views.GetBookList),
    path('books/', user.views.AddBookType),
    path('books/bID/', user.views.ChangeBookType),
    path('books/del_bID/', user.views.DeleteBookType),
    path('books/bID/bSingleID/', user.views.DeleteSingleBook),

    # -----BEGIN-----有问题找mmy-----
    # 注册登录
    path('register/', user.views.register),
    path('login/', user.views.login),

    path('operator/addReader/', user.views.OperatorAddReader),
    path('operator/delReader/', user.views.OperatorDeleteReader),

    path('operator/buyBooks/bID/', user.views.OperatorDeleteApplyToBuyBook),
    path('operator/buyBooks/', user.views.OperatorGetApplyToBuyBook),
    path('operator/return/rID/', user.views.OperatorAlterNotReturnRecord),
    path('operator/records/', user.views.OperatorGetNotReturnRecord),
    # 读者
    path('users/buyBooks/', user.views.ReaderApplyToBuy),
    path('users/records/borrow/uID/', user.views.ReaderApplyToBorrow),
    path('users/records/all/uID/', user.views.ReaderGetBorrowedRecord),
    # -----END-----mmy-----
    
    path('records/', user.views.GetRecord),#1.3.2.1获取借阅记录列表
    path('records/add/', user.views.AddRecords),#1.3.2.2添加借阅记录（现场借书）
    path('records/rID/', user.views.ChangeRecords),#1.3.2.3修改借阅记录即还书
    path('records/del/',user.views.DeleteRecords),#1.3.2.4删除借阅记录
    
    path('borrow/',user.views.GetBorrow),#1.4.2.1获取申借记录列表
    path('borrow/rID/',user.views.ConfirmBorrow),#1.4.2.2修改申借记录即申借确认s

    path('records/addnow/',user.views.AddNowRecords),#ljw现场借书
]













