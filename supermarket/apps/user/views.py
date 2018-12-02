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
@verify_login_required
def member(request):
    context = {
        "nickname":request.session["nickname"],
        "avatar":request.session["avatar"]
    }
    return render(request, "user/member.html", context=context)


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
