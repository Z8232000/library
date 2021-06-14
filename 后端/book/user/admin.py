from django.contrib import admin
from user.models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['uName', 'uID', 'uPWD', 'uPhone', 'uCharacter']


admin.site.register(User, UserAdmin)


class BookTypeAdmin(admin.ModelAdmin):
    list_display = ['bID', 'bName', 'bAuthor', 'bYear', 'bTotal', 'bLeft']


admin.site.register(BookType, BookTypeAdmin)


class SingleBookAdmin(admin.ModelAdmin):
    list_display = ['bID', 'bSingleID', 'bCondition']


admin.site.register(SingleBook, SingleBookAdmin)


class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['rID', 'bName', 'bSingleID', 'uID', 'applyDate', 'borrowDate', 'presetDate', 'returnDate',
                    'returnCondition']


admin.site.register(BorrowRecord, BorrowRecordAdmin)


class RecommendBookAdmin(admin.ModelAdmin):
    list_display = ['bID', 'bName', 'bAuthor', 'bYear', 'bTotal', 'bReason']


admin.site.register(RecommendBook, RecommendBookAdmin)
