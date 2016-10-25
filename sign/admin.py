from django.contrib import admin
from sign.models import *
from django.contrib.auth.admin import UserAdmin  # 从django继承过来后进行定制
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # admin中涉及到的两个表单


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_time','id']
    search_fields = ['name']    # 搜索功能
    list_filter = ['status']    # 过滤器


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone','email','sign','create_time','event_id']
    list_display_links = ('realname', 'phone') # 显示链接
    search_fields = ['realname','phone']       # 搜索功能
    list_filter = ['event_id']                 # 过滤器

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'get_email','get_is_active')  # 定义admin总览里每行的显示信息，由于email是在userprofile的外键user表中，所以需要特殊返回，注意这个字段不能用user__email的形式
    search_fields = ('user__username',
                         'name')  # 定义搜索框以哪些字段可以搜索，因为username是在user表中，所以用user__username的形式，这里需要注意下，不能直接用user表名，要用字段名，表名__字段名
    list_filter = ('user__groups', 'user__is_active')  # 传入的需要是列表，设定过滤列表

    def get_email(self, obj):  # 定义这个函数是由于email是在userprofile表的外键表user里，所以需要单独return一下
         return obj.user.email

    get_email.short_description = 'Email'  # list展示时候显示的title
    get_email.admin_order_field = 'user__email'  # 指定排序字段

    def get_is_active(self, obj):
        return obj.user.is_active

    get_is_active.short_description = '有效'
    get_is_active.admin_order_field = 'user__is_active'



admin.site.register(Userprofile,UserProfileAdmin)  # 引用的固定格式，注册的model和对应的Admin，Admin放在后边，同样还有noregister方法：比如admin.site.noregister(Group)，把group这个表在admin中去掉（默认user和group都是注册到admin中的）

# class User_exAdmin(admin.ModelAdmin):  # 验证码部分展示
#     list_display = ('valid_code', 'valid_time', 'email')
#
#
# # custom user admin
# class MyUserCreationForm(UserCreationForm):  # 增加用户表单重新定义，继承自UserCreationForm
#     def __init__(self, *args, **kwargs):
#         super(MyUserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['email'].required = True   # 为了让此字段在admin中为必选项，自定义一个form
#         self.fields['name'].required = True  # 其实这个name字段可以不用设定required，因为在models中的MyUser类中已经设定了blank=False，但email字段在系统自带User的models中已经设定为
#         # email = models.EmailField(_('email address'), blank=True)，除非直接改源码的django（不建议这么做），不然还是自定义一个表单做一下继承吧。
#
#
# class MyUserChangeForm(UserChangeForm):  # 编辑用户表单重新定义，继承自UserChangeForm
#     def __init__(self, *args, **kwargs):
#         super(MyUserChangeForm, self).__init__(*args, **kwargs)
#         self.fields['email'].required = True
#         self.fields['name'].required = True
#
#
# class CustomUserAdmin(UserAdmin):
#     def __init__(self, *args, **kwargs):
#         super(CustomUserAdmin, self).__init__(*args, **kwargs)
#         self.list_display = ('username', 'name', 'email', 'is_active', 'is_staff', 'is_superuser')
#         self.search_fields = ('username', 'email', 'name')
#         self.form = MyUserChangeForm  #  编辑用户表单，使用自定义的表单
#         self.add_form = MyUserCreationForm  # 添加用户表单，使用自定义的表单
#         # 以上的属性都可以在django源码的UserAdmin类中找到，我们做以覆盖
#
#     def changelist_view(self, request, extra_context=None):  # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同
#         if not request.user.is_superuser:  # 非super用户不能设定编辑是否为super用户
#             self.fieldsets = ((None, {'fields': ('username', 'password',)}),
#                               (_('Personal info'), {'fields': ('name', 'email')}),  # _ 将('')里的内容国际化,这样可以让admin里的文字自动随着LANGUAGE_CODE切换中英文
#                               (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
#                               (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#                               )  # 这里('Permissions')中没有'is_superuser',此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
#             self.add_fieldsets = ((None, {'classes': ('wide',),
#                                           'fields': ('username', 'name', 'password1', 'password2', 'email', 'is_active',
#                                                      'is_staff', 'groups'),
#                                           }),
#                                   )  #此字段定义UserCreationForm表单中的具体显示内容
#         else:  # super账户可以做任何事
#             self.fieldsets = ((None, {'fields': ('username', 'password',)}),
#                               (_('Personal info'), {'fields': ('name', 'email')}),
#                               (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
#                               (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#                               )
#             self.add_fieldsets = ((None, {'classes': ('wide',),
#                                           'fields': ('username', 'name', 'password1', 'password2', 'email', 'is_active',
#                                                      'is_staff', 'is_superuser', 'groups'),
#                                           }),
#                                   )
#         return super(CustomUserAdmin, self).changelist_view(request, extra_context)
#
#
# admin.site.register(MyUser, CustomUserAdmin)  # 注册一下
# admin.site.register(User_ex, User_exAdmin)

admin.site.register(UserGroup)
admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
