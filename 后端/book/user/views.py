import datetime
import operator

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from user.models import User, BorrowRecord, RecommendBook
from user.models import BookType
from user.models import SingleBook
import random
import string

# from pip._internal import req
# from zmq.backend.cython.constants import REQ
# from future.types import newrange
# from future.builtins import newround
# from docutils.utils.math.math2html import LineWriter
# from anaconda_navigator.utils.py3compat import request
# from boto.connection import HTTPResponse
# from pydocstyle.cli import ReturnCode

'''
mmy  register/ 已测试
注册：前端提供账号、姓名、密码和确认密码； 后端检查账号重复性、密码是否相同
返回：Json数据success、message
'''


def register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        new_uid = data_json.get('uID')
        new_name = data_json.get('username')
        new_pwd1 = data_json.get('password')
        new_pwd2 = data_json.get('repassword')
        new_tel = data_json.get('phonenum')
        if new_uid is None:
            return JsonResponse({'success': False, 'message': '未输入'})
        else:
            space = User.objects.filter(uID=new_uid)
            if len(space) > 0:
                return JsonResponse({'success': False, 'message': '账号已存在'})
            else:
                if new_pwd2 != new_pwd1:
                    return JsonResponse({'success': False, 'message': '两次密码不一致'})
                else:
                    new_student = User()
                    new_student.uID = new_uid
                    new_student.uName = new_name
                    new_student.uPWD = new_pwd1
                    new_student.uPhone = new_tel
                    new_student.uCharacter = False
                    new_student.save()
                    return JsonResponse({'success': True, 'message': '注册成功'})
    else:
        return JsonResponse({})


'''
mmy login/ 已测试 
登录：前端提供账号、密码；后端在数据库中检查账号存在性，验证密码正确性和身份
返回Json数据：success、message、isManager
data_json done
'''


def login(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        log_uid = data_json.get('uID')
        password = data_json.get('password')
        print(log_uid)
        print(password)
        user = User.objects.filter(uID=log_uid)  # 从数据库查询
        print(user)
        if len(user) == 0:
            return JsonResponse(
                {'success': False, 'message': '用户不存在', 'isManager': False, 'UID': log_uid,})
        else:
            if user[0].uPWD == password:
                request.session['username'] = log_uid
                if not user[0].uCharacter:
                    return JsonResponse({'success': True, 'message': '登陆成功', 'isManager': False, 'UID': log_uid,
                                         'username': user[0].uName, 'pwd': user[0].uPWD})
                else:
                    return JsonResponse({'success': True, 'message': '登陆成功', 'isManager': True, 'UID': log_uid,
                                         'username': user[0].uName, 'pwd': user[0].uPWD})
            else:
                return JsonResponse(
                    {'success': False, 'message': '密码错误', 'isManager': False, 'UID': log_uid, 'username': user[0].uName,
                     'pwd': user[0].uPWD})
    else:
        return JsonResponse({})


'''
mmy  operator/addReader/ 已测试
管理员添加读者：前端提供读者姓名、账号、密码和手机号;后端：检查账号重复性，将信息加入数据库
返回：Json数据success、message
data_json done
'''


def OperatorAddReader(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        new_uid = data_json.get('uID')
        new_name = data_json.get('uName')
        new_pwd1 = data_json.get('uPWD')
        new_tel = data_json.get('uPhone')

        if new_uid is None:
            return JsonResponse({'success': False, 'message': '未输入'}, status=404)
        else:
            space = User.objects.filter(uID=new_uid)
            if len(space) > 0:
                return JsonResponse({'success': False, 'message': '账号已存在'}, status=404)
            else:
                new_student = User()
                new_student.uID = new_uid
                new_student.uName = new_name
                new_student.uPWD = new_pwd1
                new_student.uPhone = new_tel
                new_student.uCharacter = False
                new_student.save()
                return JsonResponse({'success': True, 'message': '添加成功'}, status=201)
    else:
        return JsonResponse({})


'''mmy operator/delReader/ 已测试
管理员删除读者：前端提供账号，后端检查账号存在性，删除对应读者信息
data_json done'''


def OperatorDeleteReader(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        del_uid = data_json.get('uID')
        if del_uid is None:
            return JsonResponse({'success': False, 'message': '未输入'})
        else:
            space = User.objects.filter(uID=del_uid)
            if len(space) == 0:
                return JsonResponse({'success': False, 'message': '不存在此账号'}, status=404)
            else:
                User.objects.filter(uID=del_uid).delete()
                return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
    else:
        return JsonResponse({})


'''mmy 管理员删除荐购记录 已测试 operator/buyBooks/bID
data_json done'''


def OperatorDeleteApplyToBuyBook(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        bID = data_json.get('bID')
        set = RecommendBook.objects.filter(bID=bID)
        if len(set) == 0:
            return JsonResponse({'success': False, 'message': '没有这种书籍荐购'}, status=404)
        else:
            (RecommendBook.objects.get(bID=bID)).delete()
            return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
    else:
        return JsonResponse({})


'''mmy管理员获取荐购图书 已测试 operator/buyBooks/
data_json done'''


def OperatorGetApplyToBuyBook(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        pagenum = data_json.get('pagenum')  # 当前页码数
        pagesize = data_json.get('pagesize')  # 每页显示条目数

        if query is None:
            result = RecommendBook.objects.all()

        if qparam == "2":
            result = RecommendBook.objects.filter(bAuthor__contains=query)
        else:
            result = RecommendBook.objects.filter(bName__contains=query)

        apply_list = list(result.values('bID', 'bName', 'bAuthor', 'bYear', 'bTotal', 'bReason'))
        # print(list)
        total = len(apply_list)
        paginator = Paginator(apply_list, pagesize)
        try:
            record_info = paginator.page(pagenum)
        except PageNotAnInteger as e:
            record_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                record_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                record_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'recordInfo': list(record_info), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({})


'''mmy管理员修改未还记录 已测试 operator/return/rID/
data_json done'''
def OperatorAlterNotReturnRecord(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        rID = data_json.get('rID')
        set1 = BorrowRecord.objects.filter(Q(returnCondition=1), rID=rID)#借阅未还
        set2 = BorrowRecord.objects.filter(Q(returnCondition=3), rID=rID)#过期未还
        if len(set1) == 0 and len(set2)==0:
            return JsonResponse({'success': False, 'message': '此记录不存在'})
        elif len(set1) != 0:
            BorrowRecord.objects.filter(rID=rID, returnCondition=1) \
                .update(returnDate=datetime.date.today(), returnCondition=2)
            print("?1")
            borrowRecordx = BorrowRecord.objects.get(rID=rID)
            # 改变借阅记录状态
            bSingleID = borrowRecordx.bSingleID
            singleBook = SingleBook.objects.filter(bSingleID=bSingleID)
            print("?2")
            # 改变单本书籍借阅状态
            singleBook.update(bCondition=True)
            bookType = BookType.objects.filter(bID=singleBook[0].bID)
            bLeft = bookType[0].bLeft
            bookType.update(bLeft=bLeft + 1)
            print("?3")
            # 借完书图书库存+1
            return JsonResponse({'success': True, 'message': '还书成功'}, status=200)
        else:
            BorrowRecord.objects.filter(rID=rID, returnCondition=3) \
                .update(returnDate=datetime.date.today(), returnCondition=2)
            print("?1")
            borrowRecordx = BorrowRecord.objects.get(rID=rID)
            # 改变借阅记录状态
            bSingleID = borrowRecordx.bSingleID
            singleBook = SingleBook.objects.filter(bSingleID=bSingleID)
            print("?2")
            # 改变单本书籍借阅状态
            singleBook.update(bCondition=True)
            bookType = BookType.objects.filter(bID=singleBook[0].bID)
            bLeft = bookType[0].bLeft
            bookType.update(bLeft=bLeft + 1)
            print("?3")
            # 借完书图书库存+1
            return JsonResponse({'success': True, 'message': '还书成功'}, status=200)
    else:
        return JsonResponse({})


'''mmy管理员获取未还记录 operator/records/ 已测试
data_json done'''


def OperatorGetNotReturnRecord(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        pagenum = data_json.get('pagenum')  # 当前页码数
        pagesize = data_json.get('pagesize')  # 每页显示条目数
        qsort = data_json.get('qsort')

        if query is None:
            result = BorrowRecord.objects.all()

        if qparam == "2":
            result = BorrowRecord.objects.filter(bSingleID__contains=query, returnCondition__gte=1) \
                .exclude(returnCondition=2)
        elif qparam == "3":
            result = BorrowRecord.objects.filter(uID__contains=query, returnCondition__gte=1).exclude(returnCondition=2)
        elif qparam == "4":
            result = BorrowRecord.objects.filter(bName__contains=query, returnCondition__gte=1) \
                .exclude(returnCondition=2)
        else:
            result = BorrowRecord.objects.filter(rID__contains=query, returnCondition__gte=1).exclude(returnCondition=2)

        # rec_list = list(
        #    result.values('rID', 'bName', 'bSingleID', 'uID', 'applyDate', 'borrowDate', 'presetDate', 'returnDate',
        #                  'returnCondition'))

        # if qsort == 11:  # 按照rID升序
        # rec_list.sort(key=operator.itemgetter('rID'), reverse=False)

        if qsort == 10:
            sresult = result.order_by('-rID')
            # rec_list.sort(key=operator.itemgetter('rID'), reverse=True)
        elif qsort == 21:  # 按照bSingleID升序
            sresult = result.order_by('bSingleID')
            # rec_list.sort(key=operator.itemgetter('bSingleID'), reverse=False)
        elif qsort == 20:
            sresult = result.order_by('-bSingleID')
            # rec_list.sort(key=operator.itemgetter('bSingleID'), reverse=True)
        elif qsort == 31:  # 按照uID升序
            sresult = result.order_by('uID')
            # rec_list.sort(key=operator.itemgetter('uID'), reverse=False)
        elif qsort == 30:
            sresult = result.order_by('-uID')
            # rec_list.sort(key=operator.itemgetter('uID'), reverse=True)
        elif qsort == 41:  # 按照bName升序
            sresult = result.order_by('bName')
            # rec_list.sort(key=operator.itemgetter('bName'), reverse=False)
        elif qsort == 40:
            sresult = result.order_by('-bName')
            # rec_list.sort(key=operator.itemgetter('bName'), reverse=True)
        else:
            sresult = result.order_by('rID')
            # return JsonResponse({'success': False, 'message': 'qsort False'}, status=404)

        rec_list = sresult.values('rID', 'bName', 'bSingleID', 'uID', 'applyDate', 'borrowDate', 'presetDate',
                                  'returnDate', 'returnCondition')
        total = len(rec_list)
        paginator = Paginator(rec_list, pagesize)
        try:
            record_info = paginator.page(pagenum)
        except PageNotAnInteger as e:
            record_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                record_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                record_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'recordInfo': list(record_info), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({}, status=404)


'''mmy读者获取个人借阅记录 已测试 users/records/all/uID/
data_json done'''


def ReaderGetBorrowedRecord(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        pagenum = data_json.get('pagenum')  # 当前页码数
        pagesize = data_json.get('pagesize')  # 每页显示条目数
        qsort = data_json.get('qsort')
        uID = data_json.get('uID')

        if query is None:
            result = BorrowRecord.objects.all()

        if qparam == "1":
            result = BorrowRecord.objects.filter(rID__contains=query, uID=uID)
        elif qparam == "2":
            result = BorrowRecord.objects.filter(bSingleID__contains=query, uID=uID)
        else:
            result = BorrowRecord.objects.filter(bName__contains=query, uID=uID)
        # else:
        #    return JsonResponse({'success': False, 'message': 'qparam False'}, status=404)

        # rec_list = list(
        #    result.values('rID', 'bName', 'bSingleID', 'uID', 'applyDate', 'borrowDate', 'presetDate', 'returnDate',
        #                  'returnCondition'))
        # print(rec_list)
        # if qsort == 11:  # 按照rID升序
        # rec_list.sort(key=operator.itemgetter('rID'), reverse=False)
        if qsort == 10:
            sresult = result.order_by('-rID')
            # rec_list.sort(key=operator.itemgetter('rID'), reverse=True)
        elif qsort == 21:  # 按照bSingleID升序
            sresult = result.order_by('bSingleID')
            # rec_list.sort(key=operator.itemgetter('bSingleID'), reverse=False)
        elif qsort == 20:
            sresult = result.order_by('-bSingleID')
            # rec_list.sort(key=operator.itemgetter('bSingleID'), reverse=True)
        elif qsort == 31:  # 按照bName升序
            sresult = result.order_by('bName')
            # rec_list.sort(key=operator.itemgetter('bName'), reverse=False)
        elif qsort == 30:
            sresult = result.order_by('-bName')
            # rec_list.sort(key=operator.itemgetter('bName'), reverse=True)
        else:
            sresult = sresult = result.order_by('rID')
            # return JsonResponse({'success': False, 'message': 'qsort False'}, status=404)

        rec_list = sresult.values('rID', 'bName', 'bSingleID', 'uID', 'applyDate', 'borrowDate', 'presetDate',
                                  'returnDate', 'returnCondition')
        total = len(rec_list)

        paginator = Paginator(rec_list, pagesize)
        try:
            record_info = paginator.page(pagenum)
        except PageNotAnInteger as e:
            record_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                record_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                record_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'userINFO': list(record_info), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({}, status=303)


'''mmy读者添加荐购信息 已测试 buyBooks
data_json done'''


def ReaderApplyToBuy(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        recommend = RecommendBook()
        recommend.bName = data_json.get('bName')
        recommend.bYear = data_json.get('bYear')
        recommend.bAuthor = data_json.get('bAuthor')
        recommend.bTotal = data_json.get('bTotal')
        recommend.bReason = data_json.get('bReason')
        recommend.save()
        return JsonResponse({'success': True, 'message': "插入成功"}, status=201)  # 成功状态码201
    else:
        return JsonResponse({'success': False, 'message': "提交失败"}, status=404)


'''mmy读者添加申借记录 已测试 records/borrow/uID
data_json done'''


def ReaderApplyToBorrow(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        mbID = data_json.get('bID')
        muID = data_json.get('uID')

        if mbID is None or muID is None:
            return JsonResponse({'success': False}, status=400)

        booktype = SingleBook.objects.filter(bID=mbID)

        if len(booktype) == 0:
            # print("书本类不存在啊！！！")
            return JsonResponse({'success': False, 'message': '书本类不存在'})
        bTmp = BookType.objects.filter(bID=mbID)
        bLft = bTmp[0].bLeft
        mbName = bTmp[0].bName

        user = User.objects.filter(uID=muID)
        if len(user) == 0:
            # print("用户不存在啊！！！")
            return JsonResponse({'success': False, 'message': '用户不存在'})
        # muName=user[0].uName

        ex = SingleBook.objects.filter(bID=mbID)
        print(len(ex))
        if len(ex) < 1:
            for i in range(len(booktype)):
                bsid = booktype[i].bSingleID
                br = BorrowRecord.objects.filter(bSingleID=bsid)
                if br[0].returnCondition == 0:
                    deltaday = (datetime.datetime.now() - br[0].applyDate).day
                    if deltaday > 7:
                        BorrowRecord.objects.filter(bSingleID=bsid).update(uID=muID, applyDate=datetime.datetime.now())
                        return JsonResponse({'success': True, 'message': '申借成功'})
            return JsonResponse({'success': False, 'message': '书本库存不足'})

        lflag = False

        for i in range(len(booktype)):
            bsid = booktype[i].bSingleID
            br = SingleBook.objects.filter(bSingleID=bsid)
            if br[0].bCondition is True:
                mbSingleID = bsid
                lflag = True
                break
        if lflag is False:
            return JsonResponse({'success': False, 'message': '书本库存不足'})

        newRecord = BorrowRecord()
        newRecord.bName = mbName
        newRecord.bSingleID = mbSingleID
        # newRecord.uName=muName
        newRecord.uID = muID
        newRecord.applyDate = datetime.datetime.now().date()
        newRecord.returnCondition = 0
        newRecord.save()
        newid = newRecord.rID
        BookType.objects.filter(bID=mbID).update(bLeft=bLft - 1)
        SingleBook.objects.filter(bSingleID=mbSingleID).update(bCondition=False)
        # 总书库库存-1 单本状态修改  记录中状态新建并修改为未确认
        print("fff")
        return JsonResponse({'success': True}, safe=False)
    else:
        return JsonResponse({'success': False, 'message': '前端请求错误'})


'''get
管理员获取读者列表_zrb
data_json done
?get method?
'''


def GetReaderList(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        pagenum = data_json.get('pagenum')
        pagesize = data_json.get('pagesize')

        if query is None:
            Result = User.objects.all()

        if qparam == "2":
            Result = User.objects.filter(uID__contains=query)
        else:
            Result = User.objects.filter(uName__contains=query)

        userResult = list(Result.values('uName', 'uID', 'uPhone', 'uCharacter'))
        total = len(userResult)
        paginator = Paginator(userResult, pagesize)
        try:
            userINFO = paginator.page(pagenum)
        except PageNotAnInteger as e:
            userINFO = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                userINFO = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                userINFO = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'userInfo': list(userINFO), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
        # return JsonResponse({'Success': 'Success'})
    else:
        return JsonResponse({}, status=303)


'''
    管理员修改信息_zrb
'''


@csrf_exempt
def AdminChangeUPhone(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        uid = data_json.get('uID')
        newPhone = data_json.get('uPhone')
        if uid is None:
            return JsonResponse({'success': False, 'message': 'uid未输入'}, status=400)
        elif newPhone is None:
            return JsonResponse({'success': False, 'message': '新手机号未输入'}, status=400)
        elif len(newPhone) != 11:
            return JsonResponse({'success': False, 'message': '手机号违规'}, status=400)
        elif newPhone.isdigit() == False:
            return JsonResponse({'success': False, 'message': '手机号违规'}, status=400)
        else:
            usr = User.objects.filter(uID=uid)
            if len(usr) == 0:
                return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)
            else:
                usr.update(uPhone=newPhone)
                return JsonResponse({'success': True, 'message': '更新成功'}, status=200)
    else:
        return JsonResponse({}, status=302)


'''
读者修改个人信息
'''


def ReaderChangePWD(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        ID = data_json.get('uID')
        PWD = data_json.get('uPWD')
        checkPWD = data_json.get('ucheckPWD')
        if ID is None or PWD is None or checkPWD is None:
            return JsonResponse({'success': False, 'message': '信息不完整'})
        else:
            space = User.objects.filter(uID=ID)
            if len(space) == 0:
                return JsonResponse({'success': False, 'message': '账号不存在'})
            else:
                usr = User.objects.filter(uID=ID)
                if PWD != checkPWD:
                    return JsonResponse({'success': False, 'message': '两次密码不一致'})
                else:
                    usr.update(uPWD=PWD)
                    return JsonResponse({'success': True, 'message': '密码修改成功'})
    else:
        return JsonResponse({})


def ReaderChangeInfo(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        ID = data_json.get('uID')
        name = data_json.get('uName')
        Phone = data_json.get('uPhone')
        if ID is None or name is None or Phone is None:
            return JsonResponse({'success': False, 'message': '信息不完整'})
        else:
            space = User.objects.filter(uID=ID)
            if len(space) == 0:
                return JsonResponse({'success': False, 'message': '账号不存在'})
            else:
                usr = User.objects.filter(uID=ID)
                usr.update(uName=name, uPhone=Phone)
                return JsonResponse({'success': True, 'message': '信息修改成功'})
    else:
        return JsonResponse({})


'''
管理员添加图书类
'''


def AddBookType(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('bName')
        byear = data_json.get('bYear')
        author = data_json.get('bAuthor')
        btotal = data_json.get('bTotal')
        bleft = int(btotal)
        total = int(btotal)
        year = int(byear)
        left = int(bleft)
        if name is None:
            return JsonResponse({'success': False, 'message': '书名不完整'})

        elif year is None:
            return JsonResponse({'success': False, 'message': '年份不完整'})
        elif author is None:
            return JsonResponse({'success': False, 'message': '作者信息不完整'})
        elif total is None or left is None:
            return JsonResponse({'success': False, 'message': '书总量和余量信息不完整'})
        else:
            space = BookType.objects.filter(bName=name, bYear=year, bAuthor=author)
            if len(space) > 0:
                return JsonResponse({'success': False, 'message': '该图书已存在'})
            else:
                new_booktype = BookType()

                id = ''.join(random.sample(string.digits * 3, 8))
                space1 = BookType.objects.filter(bID=id)
                while len(space1) > 0:
                    id = ''.join(random.sample(string.digits * 3, 8))
                    space1 = BookType.objects.filter(bID=id)

                new_booktype.bID = id
                new_booktype.bName = name
                new_booktype.bAuthor = author
                new_booktype.bTotal = total
                new_booktype.bLeft = left
                new_booktype.bYear = year
                new_booktype.save()
                for i in range(total):
                    new_book = SingleBook()

                    singleid = ''.join(random.sample(string.digits * 3, 11))
                    space2 = SingleBook.objects.filter(bSingleID=singleid)
                    while len(space2) > 0:
                        singleid = ''.join(random.sample(string.digits * 3, 11))
                        space2 = SingleBook.objects.filter(bSingleID=singleid)

                    new_book.bID = id
                    new_book.bSingleID = singleid
                    new_book.save()
                return JsonResponse({'success': True, 'message': '图书添加成功'})
    else:
        return JsonResponse({})


'''
管理员删除图书类
'''


def DeleteBookType(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        ID = data_json.get('bID')
        if ID is None:
            return JsonResponse({'success': False, 'message': '信息不完整'})
        else:
            space = BookType.objects.filter(bID=ID)
            if len(space) == 0:
                return JsonResponse({'success': False, 'message': '找不到该图书'})
            else:
                books = SingleBook.objects.filter(bID=ID)
                if len(books) > 0:
                    for book in books:
                        if book.bCondition == False:
                            return JsonResponse({'success': False, 'message': '还有书没还'})
                    SingleBook.objects.filter(bID=ID).delete()
                BookType.objects.filter(bID=ID).delete()
                return JsonResponse({'success': True, 'message': '图书删除成功'})
    else:
        return JsonResponse({})


'''
管理员修改图书类
'''


def ChangeBookType(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        ID = data_json.get('bID')
        name = data_json.get('bName')
        byear = data_json.get('bYear')
        year = int(byear)
        author = data_json.get('bAuthor')
        btotal = data_json.get('bTotal')
        total = int(btotal)
        if name is None or year is None or author is None or total is None or ID is None:
            return JsonResponse({'success': False, 'message': '信息不完整'})
        else:
            space = BookType.objects.filter(bID=ID)
            if len(space) == 0:
                return JsonResponse({'success': False, 'message': '找不到该图书'})
            else:
                booktype = BookType.objects.filter(bID=ID)
                left = booktype[0].bLeft
                if booktype[0].bTotal < total:
                    cnt = total - booktype[0].bTotal
                    for i in range(cnt):
                        new_book = SingleBook()
                        singleid = ''.join(random.sample(string.digits * 3, 11))
                        space2 = SingleBook.objects.filter(bSingleID=singleid)
                        while len(space2) > 0:
                            singleid = ''.join(random.sample(string.digits * 3, 11))
                            space2 = SingleBook.objects.filter(bSingleID=singleid)

                        new_book.bID = ID
                        new_book.bSingleID = singleid
                        new_book.save()
                    left = booktype[0].bLeft + cnt
                booktype.update(bName=name, bYear=year, bAuthor=author, bTotal=total, bLeft=left)
                return JsonResponse({'success': True, 'message': '图书信息修改成功'})
    else:
        return JsonResponse({})


'''
管理员删除单本图书
'''


def DeleteSingleBook(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        singleID = data_json.get('bSingleID')
        if singleID is None:
            return JsonResponse({'success': False, 'message': '参数不全'})
        else:
            space = SingleBook.objects.filter(bSingleID=singleID)
            if len(space) == 0:
                return JsonResponse({'success': False, 'message': '找不到该本图书'})
            else:
                book = SingleBook.objects.get(bSingleID=singleID)
                if book.bCondition == False:
                    return JsonResponse({'success': False, 'message': '书还没还'})
                bID = book.bID
                booktype = BookType.objects.filter(bID=bID)
                total = booktype[0].bTotal
                left = booktype[0].bLeft
                booktype.update(bTotal=total - 1, bLeft=left - 1)
                SingleBook.objects.filter(bSingleID=singleID).delete()
                return JsonResponse({'success': True, 'message': '图书删除成功'})
    else:
        return JsonResponse({})


'''
获取图书列表
'''


def GetBookList(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        qsort = data_json.get('qsort')
        pagenum = data_json.get('pagenum')
        pagesize = data_json.get('pagesize')

        if query is None:
            Result = BookType.objects.all()
        if qparam == "2":
            Result = BookType.objects.filter(bID__contains=query)
        elif qparam == "3":
            Result = BookType.objects.filter(bAuthor__contains=query)
        else:
            Result = BookType.objects.filter(bName__contains=query)
        print(qsort)
        print(qsort == 11)

        if qsort == 21:
            Sortresult = Result.order_by('bName')
        elif qsort == 20:
            Sortresult = Result.order_by('-bName')
        elif qsort == 31:
            Sortresult = Result.order_by('bYear')
        elif qsort == 30:
            Sortresult = Result.order_by('-bYear')
        elif qsort == 41:
            Sortresult = Result.order_by('bTotal')
        elif qsort == 40:
            Sortresult = Result.order_by('-bTotal')
        elif qsort == 10:
            Sortresult = Result.order_by('-bID')
        else:
            Sortresult = Result.order_by('bID')

        sresult = Sortresult.values('bName', 'bID', 'bAuthor', 'bYear', 'bTotal', 'bLeft')

        total = len(sresult)
        paginator = Paginator(sresult, pagesize)
        try:
            bookINFO = paginator.page(pagenum)
        except PageNotAnInteger as e:
            bookINFO = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                bookINFO = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                bookINFO = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'bookInfo': list(bookINFO), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({}, status=303)


'''
1.3.2.1 获取借阅记录_zrb
url:'records/'
０５３０テスト済み
'''


def GetRecord(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        qsort = data_json.get('qsort')
        pagenum = data_json.get('pagenum')
        pagesize = data_json.get('pagesize')

        if query is None:
            Result = BorrowRecord.objects.all()

        if qparam == "2":
            Result = BorrowRecord.objects.filter(~Q(returnCondition=0), bSingleID__contains=query)
        elif qparam == "3":
            Result = BorrowRecord.objects.filter(~Q(returnCondition=0), uID__contains=query)
        elif qparam == "4":
            Result = BorrowRecord.objects.filter(~Q(returnCondition=0), bName__contains=query)
        else:
            Result = BorrowRecord.objects.filter(~Q(returnCondition=0), rID__contains=query)
            # Result = BorrowRecord.objects.filter(Q(rID__contains = query) and ~Q(returnCondition=0))
        # print(qsort=="20")

        if qsort == 10:
            SortResult = Result.order_by('-rID')
        elif qsort == 21:
            SortResult = Result.order_by('bSingleID')
        elif qsort == 20:
            SortResult = Result.order_by('-bSingleID')
        elif qsort == 31:
            SortResult = Result.order_by('uID')
        elif qsort == 30:
            SortResult = Result.order_by('-uID')
        else:
            SortResult = Result.order_by('rID')

        recordResult = list(
            SortResult.values('rID', 'bName', 'bSingleID', 'uID', 'borrowDate', 'presetDate', 'returnDate',
                              'returnCondition'))
        total = len(recordResult)
        # print(recordResult)
        paginator = Paginator(recordResult, pagesize)
        try:
            userINFO = paginator.page(pagenum)
        except PageNotAnInteger as e:
            userINFO = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                userINFO = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                userINFO = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'userINFO': list(userINFO), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
        # return HTTPResponse(json.dumps(list(userINFO),ensure_ascii=False), safe=False,status=200,content_type="application/json",charset=utf-8)

    else:
        return JsonResponse({'success': False}, status=303)


'''
1.3.2.2 添加借阅记录_zrb
url: 'records/add/'
テスト済み
'''


def AddRecords(request):
    if request.method == 'POST':
        print("aaa")
        data_json = json.loads(request.body)
        # mbName=data_json.get('bName')
        mbID = data_json.get('bID')
        # muName=data_json.get('uName')
        muID = data_json.get('uID')
        # borrowDateStr=data_json.get('borrowDate')
        # borrowDate=datetime.datetime.strptime(borrowDateStr,'%Y-%m-%d').date()
        # date_p = datetime.datetime.strptime(str_p,'%Y-%m-%d').date()
        # returnCondition=data_json.get('returnCondition')

        if mbID is None or muID is None:
            # if mbName is None or mbID is None or muName is None or muID is None or returnCondition is None :
            return JsonResponse({'success': False}, status=400)

        booktype = BookType.objects.filter(bID=mbID)

        if len(booktype) == 0:
            # print("书本类不存在啊！！！")
            return JsonResponse({'success': False, 'message': '书本类不存在'})
        bLft = booktype[0].bLeft
        mbName = booktype[0].bName

        user = User.objects.filter(uID=muID)
        if len(user) == 0:
            # print("用户不存在啊！！！")
            return JsonResponse({'success': False, 'message': '用户不存在'})
        # muName=user[0].uName
        ex = SingleBook.objects.filter(bID=mbID)
        print(len(ex))
        if len(ex) < 1:
            print("书本库存不足啊！！！")
            return JsonResponse({'success': False, 'message': '书本库存不足'})
        flag = True
        for i in range(len(ex)):
            if ex[i].bCondition is True:
                mbSingleID = ex[i].bSingleID
                flag = False
                break
        if flag is True:
            # print("书本库存不足啊！！！")
            return JsonResponse({'success': False, 'message': '书本库存不足'})
        print("eee")

        newRecord = BorrowRecord()
        newRecord.bName = mbName
        newRecord.bSingleID = mbSingleID
        # newRecord.uName=muName
        newRecord.uID = muID
        newRecord.borrowDate = datetime.datetime.now().date()
        # newRecord.applyDate=borrowDate
        newRecord.presetDate = datetime.datetime.now().date() + datetime.timedelta(days=30)
        newRecord.returnCondition = 1
        newRecord.save()
        newid = newRecord.rID
        BorrowRecord.objects.filter(rID=newid).update(applyDate=datetime.datetime.now().date())
        BookType.objects.filter(bID=mbID).update(bLeft=bLft - 1)
        print("fff")
        return JsonResponse({'success': True}, safe=False)
    else:
        return JsonResponse({'success': False, 'message': '前端请求错误'})


'''
1.3.2.3修改借阅记录即还书_zrb
url:'records/rID/'
テスト済み
'''


def ChangeRecords(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        mrID = data_json.get('rID')
        #  bName=request.POST.get('bName')
        # bSingleID=request.POST.get('bSingleID')
        #  uName=request.POST.get('uName')
        # uID=request.POST.get('uID')
        # borrowDateStr=request.POST.get('borrowDate')
        # borrowDate=datetime.datetime.strptime(borrowDateStr,'%Y-%m-%d').date()
        # presetDateStr=request.POST.get('presetDate')
        # presetDate=datetime.datetime.strptime(presetDateStr,'%Y-%m-%d').date()
        # returnDateStr=request.POST.get('returnDate')
        # returnDate=datetime.datetime.strptime(returnDateStr,'%Y-%m-%d').date()
        # 这些信息或许不需要
        # returnCondition=request.POST.get('returnCondition')
        print("aaa")
        if mrID is None:
            return JsonResponse({'success': False}, status=400)
        Result = BorrowRecord.objects.filter(rID=mrID)
        if len(Result) == 0:
            return JsonResponse({'success': False}, status=204)
        returnCondition = Result[0].returnCondition
        if (returnCondition is None or returnCondition != 1):
            return JsonResponse(status=400)

        bname = Result[0].bName
        booktype = BookType.objects.filter(bName=bname)
        mbID = booktype[0].bID
        if len(booktype) == 0:
            return JsonResponse({'success': False, 'message': '书本类不存在'}, status=404)
        bLft = booktype[0].bLeft
        BookType.objects.filter(bID=mbID).update(bLeft=bLft + 1)

        Result = BorrowRecord.objects.filter(rID=mrID)
        if len(Result) == 0:
            return JsonResponse(status=204)
        Result.update(returnCondition=2, returnDate=datetime.datetime.now().date())
        return JsonResponse({'success': True}, status=200, safe=False)
    else:
        return JsonResponse({'success': False}, status=303)


'''
1.3.2.4删除借阅记录 _zrb
'records/del/'
テスト済み
'''


def DeleteRecords(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        mrID = data_json.get('rID')
        if mrID is None:
            return JsonResponse(status=400)
        Result = BorrowRecord.objects.filter(rID=mrID)
        if len(Result) == 0:
            return JsonResponse(status=204)
        if Result[0].returnConditon == 3:
            BorrowRecord.objects.filter(rID=mrID).delete()
            return JsonResponse({'success': True}, status=200, safe=False)
        else:
            return JsonResponse({'success': False}, status=303)
    else:
        return JsonResponse({'success': False}, status=303)


'''
   1.4.2.1获取申借记录列表_zrb
   'borrow/'
'''


def GetBorrow(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        query = data_json.get('query')
        qparam = data_json.get('qparam')
        qsort = data_json.get('qsort')
        pagenum = data_json.get('pagenum')
        pagesize = data_json.get('pagesize')
        print("aaa")
        if query is None:
            Result = BorrowRecord.objects.all()

        if qparam == "2":
            Result = BorrowRecord.objects.filter(Q(returnCondition=0), bSingleID__contains=query)
        elif qparam == "3":
            Result = BorrowRecord.objects.filter(Q(returnCondition=0), uID__contains=query)
        elif qparam == "4":
            Result = BorrowRecord.objects.filter(Q(returnCondition=0), bName__contains=query)
        else:
            Result = BorrowRecord.objects.filter(Q(returnCondition=0), rID__contains=query)
        print("bbb")
        if qsort == 10:
            SortResult = Result.order_by('-rID')
        elif qsort == 21:
            SortResult = Result.order_by('bSingleID')
        elif qsort == 20:
            SortResult = Result.order_by('-bSingleID')
        elif qsort == 31:
            SortResult = Result.order_by('uID')
        elif qsort == 30:
            SortResult = Result.order_by('-uID')
        else:
            SortResult = Result.order_by('rID')
        recordResult = list(
            SortResult.values('rID', 'bName', 'bSingleID', 'uID', 'applyDate', 'borrowDate', 'presetDate', 'returnDate',
                              'returnCondition'))
        total = len(recordResult)
        paginator = Paginator(recordResult, pagesize)
        try:
            userINFO = paginator.page(pagenum)
        except PageNotAnInteger as e:
            userINFO = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                userINFO = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                userINFO = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'userInfo': list(userINFO), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})

    else:
        return JsonResponse({'success': False}, status=303)


'''
   1.4.2.2修改申借记录即申借确认_zrb
   'borrow/rID'
'''


def ConfirmBorrow(request):
    if request.method == 'POST':
        print("???rID")
        data_json = json.loads(request.body)
        mrID = data_json.get('rID')
        # bName=request.POST.get('bName')
        # bSingleID=request.POST.get('bSingleID')
        # uName=request.POST.get('uName')
        # uID=request.GET.POST('uID')
        # borrowDateStr=request.POST.get('borrowDate')
        # borrowDate=datetime.datetime.strptime(borrowDateStr,'%Y-%m-%d').date()
        # applyDateStr=request.POST.get('applyDate')
        # applyDate=datetime.datetime.strptime(applyDateStr,'%Y-%m-%d').date()

        # returnCondition=request.POST.get('returnCondition')
        if mrID is None:
            return JsonResponse({'success': False, 'message': '此借阅记录不存在'})
        book = BorrowRecord.objects.filter(rID=mrID)
        if len(book) == 0:
            return JsonResponse({'success': False, 'message': '此书库存不足'})
        rc = book[0].returnCondition
        bd = book[0].borrowDate
        if (rc is None or rc != 0):
            print(rc)
            print(rc != 0)
            return JsonResponse({'success': False, 'message': '此书被借出去了'}, status=400)

        book.update(returnCondition=1, borrowDate=datetime.datetime.now().date(),
                    presetDate=datetime.datetime.now().date() + datetime.timedelta(days=30))
        return JsonResponse({'success': True}, status=200, safe=False)
    else:
        return JsonResponse({'success': False, 'message': '前段请求错误'}, status=303)


'''现场添加借阅记录_ljw改
url：‘records/nowadd’
'''


def AddNowRecords(request):
    if request.method == 'POST':
        print("aaa")
        data_json = json.loads(request.body)
        mbID = data_json.get('bID')
        mbSingleID = data_json.get('bSingleID')
        muID = data_json.get('uID')

        if mbID is None or muID is None:
            return JsonResponse({'success': False}, status=400)

        bTmp = BookType.objects.filter(bID=mbID)

        if len(bTmp) == 0:
            # print("书本类不存在啊！！！")
            return JsonResponse({'success': False, 'message': '书本类不存在'})

        bLft = bTmp[0].bLeft
        mbName = bTmp[0].bName

        user = User.objects.filter(uID=muID)
        if len(user) == 0:
            # print("用户不存在啊！！！")
            return JsonResponse({'success': False, 'message': '用户不存在'})
        # muName=user[0].uName
        ex = SingleBook.objects.filter(bID=mbID)

        flag = True
        for i in range(len(ex)):
            if mbSingleID == ex[i].bSingleID:
                flag = False
                break
        if flag is True:
            return JsonResponse({'success': False, 'message': '此书本个体ID不存在'})

        if ex[i].bCondition is False:
            bsid = ex[i].bSingleID
            br = BorrowRecord.objects.filter(bSingleID=bsid)
            if (datetime.datetime.now() - br[0].applyDate).day > 7:
                BorrowRecord.objects.filter(bSingleID=bsid).update(uID=muID, borrowDate=datetime.datetime.now(),
                                                                   presetDate=datetime.datetime.now().date() + datetime.timedelta(
                                                                       days=30),
                                                                   returnCondition=1)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': '这本书已经被预定了，建议申借'})

        print("eee")

        newRecord = BorrowRecord()
        newRecord.bName = mbName
        newRecord.bSingleID = mbSingleID
        # newRecord.uName=muName
        newRecord.uID = muID
        newRecord.borrowDate = datetime.datetime.now().date()
        # newRecord.applyDate=borrowDate
        newRecord.presetDate = datetime.datetime.now().date() + datetime.timedelta(days=30)
        newRecord.returnCondition = 1
        newRecord.save()
        SingleBook.objects.filter(bSingleID=mbSingleID).update(bCondition=False)
        BookType.objects.filter(bID=mbID).update(bLeft=bLft - 1)
        print("fff")
        return JsonResponse({'success': True}, safe=False)
    else:
        return JsonResponse({'success': False, 'message': '前端请求错误'})
