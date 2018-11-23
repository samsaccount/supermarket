from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.


from user.forms import userReg, userLogin
from user.helper import *
from user.models import User

# 注册


def reg(request):
    # 当method为POST的时候验证数据并提交
    if request.method == "POST":
        # 获取post中的数据
        data = request.POST
        # 创建form对象
        form = userReg(data)
        # 验证form是否合法，返回bool指
        if form.is_valid():
            # 验证成功，获取form对象清理数据
            data = form.cleaned_data
            # 密码转MD5码
            password = set_password(data.get("password"))
            # 存数据到数据库
            User.objects.create(phone=data.get("phone"), password=password)
            return redirect("user:login")
        else:
            context = {
                "error":form.errors
            }
            return render(request, "user/reg.html", context=context)
    else:
        return render(request, "user/reg.html")


# 登陆
def login(request):
    # 当method为POST的时候验证数据并提交
    if request.method == "POST":
        data = request.POST
        form = userLogin(data)
        # 验证form对象
        if form.is_valid():
            user = User.objects.get(phone=data.get("phone"))
            # 设置session 将登录状态和个人信息传到session中
            request.session['is_Login'] = True
            request.session['avatar'] = user.avatar
            request.session['id'] = user.id
            # 验证是否有昵称，没有昵称昵称将显示手机号
            if not user.nickname:
                request.session["nickname"] = user.phone
            else:
                request.session["nickname"] = user.nickname
            # 返回到个人中心
            return redirect("user:member")
        else:
            context ={
                "error" : form.errors
            }
            return render(request, "user/login.html", context=context)
    else:
        return render(request, "user/login.html")


# 个人中心
def member(request):
    context = {
        "nickname":request.session["nickname"],
        "avatar":request.session["avatar"]
    }
    return render(request, "user/member.html", context=context)


# 账户余额
def records(request):
    return render(request, "user/records.html")


# 积分
def integral(request):
    return render(request, "user/integral.html")


# 积分兑换
def integral_exchange(request):
    return render(request, "user/integralexchange.html")


# 兑换记录
def integral_records(request):
    return render(request, "user/integralrecords.html")


# 优惠卷
def coupons(request):
    return render(request, "user/yhq.html")


# 过期优惠卷
def coupons_overtime(request):
    return render(request, "user/ygq.html")


# 收藏
def collection(request):
    return render(request, "user/collect.html")


# 订单
def all_order(request):
    return render(request, "user/allorder.html")


# 个人资料
def user_info(request):
    if request.method == "POST":
        data = request.POST
        user = User.objects.get(id=request.session['id'])
        user.nickname = data["nickname"]
        user.sex = data["sex"]
        user.birthday = data['birthday']
        user.school = data['school']
        user.hometown = data['hometown']
        user.save()
        request.session['nickname']=data['nickname']
        return redirect("user:user_info")
    else:
        user_id = request.session['id']
        data = User.objects.get(id=user_id)
        context = {
            "avatar": data.avatar,
            "nickname": data.nickname,
            "sex": data.sex,
            "birthday": data.birthday.strftime('%Y-%m-%d'),
            "school": data.school,
            "Local": "",
            "hometown": data.hometown,
            "phone": data.phone
        }
        return render(request, "user/infor.html", context)


def UploadImg(request):
    if request.FILES.get('upload'):
        user = User.objects.get(pk=request.session.get("id"))
        user.avatar = request.FILES['upload']
        user.save()
        request.session["avatar"] = user.avatar
        return redirect("user:user_info")
    else:
        return redirect("user:user_info")
    # return JsonResponse({"status": "ok", "avatar": str(user.avatar)})


# 收获地址
def set_addr(request):
    return render(request, "user/gladdress.html")


# 安全设置
def safty(request):
    return render(request, "user/saftystep.html")


# 重置密码
def reSetPwd(request):
    return render(request, "user/password.html")


# 绑定手机
def bound_phone(request):
    return render(request, "user/boundphone.html")


# 支付密码
def payment(request):
    return render(request, "user/payment.html")


# 钱包
def wallet(request):
    return render(request, "user/money.html")


# 兼职
def job(request):
    return render(request, "user/job.html")


# 申请记录
def apply_record(request):
    return render(request, "user/")


# 兼职申请填写
def apply(request):
    return render(request, "user/applicationjob.html")


# 推荐好友
def recommend(request):
    return render(request, "user/recommend.html")


# 我的推荐
def my_recommend(request):
    return render(request, "user/myrecommend.html")


# 动态
def message(request):
    return render(request, "user/message.html")


# 动态详情
def messdetail(request):
    return render(request, "user/messdetail.html")


# 发布动态
def release(request):
    return render(request, "user/release.html")
