import os
import time
from datetime import datetime
import random
from alipay import AliPay
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
# Create your views here.
from django_redis import get_redis_connection

from goods.models import GoodsSku
from order.forms import AddressModelForm, AddressEditModelForm
from order.models import UserAddress, Transport, OrderInfo, OrderSku


def createAddr(request):
    if request.method == "POST":
        data = request.POST.dict()
        data['user_id'] = request.session["id"]
        form = AddressModelForm(data)
        if form.is_valid():
            form.instance.user_id = request.session["id"]
            form.save()
            return redirect("order:addr_manage")
        else:
            context = {
                "form": form
            }
            return render(request, "order/address.html", context)
    else:
        return render(request, 'order/address.html')


def addrManage(request):
    user_id = request.session['id']
    data = UserAddress.objects.filter(user_id=user_id, is_delete=False).order_by("-isDefault")
    context = {
        "data": data
    }
    return render(request, 'order/gladdress.html', context)


def editAddr(request, id):
    if request.method == "POST":
        data = request.POST.dict()
        user_id = request.session["id"]
        data['user_id'] = user_id
        form = AddressEditModelForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            id = data.get("id")
            UserAddress.objects.filter(user_id=user_id, id=id).update(**cleaned_data)
            return redirect("order:addr_manage")
        else:
            context = {
                "form": form,
                "data": data,
            }
            return render(request, "order/editAddress.html", context)
    else:
        user_id = request.session["id"]
        try:
            data = UserAddress.objects.get(id=id, user_id=user_id)
        except UserAddress.DoesNotExist:
            return redirect("order:addr_manage")
        context = {
            "data": data
        }
        return render(request, 'order/editAddress.html', context)


def delAddr(request):
    addr_id = request.POST.get("addr_id")
    try:
        UserAddress.objects.get(id=addr_id)
    except UserAddress.DoesNotExist:
        return JsonResponse({"status": 4, "errmsg": "未找到对应地址"})
    UserAddress.objects.filter(id=addr_id).update(is_delete=True)
    return JsonResponse({"status": 2})


def setDefault(request):
    user_id = request.session['id']
    addr_id = request.POST.get("addr_id")
    try:
        UserAddress.objects.get(id=addr_id)
    except UserAddress.DoesNotExist:
        return JsonResponse({"status": 4, "errmsg": "未找到对应地址"})
    UserAddress.objects.filter(user_id=user_id).update(isDefault=False)
    UserAddress.objects.filter(id=addr_id).update(isDefault=True)
    return JsonResponse({"status": 2})


@transaction.atomic
def confirmOrder(request):
    if request.method == "GET":
        # 获取用户ID
        user_id = request.session["id"]
        # 获取用户的默认地址
        addr = UserAddress.objects.filter(user_id=user_id, is_delete=False).order_by("-isDefault").first()
        # 用getlist获取GET请求中所有的sku_id
        sku_ids = request.GET.getlist("sku_id")
        # 准备序列存贮sku
        goods_skus = []
        # 购物车中的数量(redis)
        r = get_redis_connection("default")
        # 准备键
        cart_key = "cart_key_{}".format(user_id)

        # 计算商品总价格
        total_price = 0
        # 遍历
        for sku_id in sku_ids:
            sku_id = int(sku_id)
            # 获取商品信息
            goods_info = GoodsSku.objects.get(id=sku_id)
            # 获取商品数量
            goods_info.count = int(r.hget(cart_key, sku_id))
            # 计算商品总价
            total_price += goods_info.count * goods_info.goods_price
            # 将所有总价添加到商品列表中
            goods_skus.append(goods_info)
        # 将所有的运输方式获取
        transports = Transport.objects.filter(is_delete=False).order_by("money")
        context = {
            "addr": addr,
            "goods_skus": goods_skus,
            "transports": transports,
            "total_price": total_price
        }
        return render(request, "order/order.html", context)
    else:
        # 验证是否登陆
        user_id = request.session.get("id")
        if not user_id:
            return JsonResponse({"code": 1, "errmsg": "没有登陆"})
        # 获取数据
        addr = request.POST.get("addr")
        sku_ids = request.POST.getlist("sku_id")
        transport = request.POST.get("transport")
        # 创建商品列表
        skus = []
        # 验证是否存在参数
        if not all([addr, sku_ids, transport]):
            return JsonResponse({"code": 2, "errmsg": "参数错误"})
        # 验证能否整数化参数
        try:
            addr = int(addr)
            sku_ids = [int(sku_id) for sku_id in sku_ids]
            transport = int(transport)
        except:
            return JsonResponse({"code": 3, "errmsg": "参数整数化错误"})
        # 验证是否存在商品
        try:
            for sku_id in sku_ids:
                # 悲观锁 select_for_update()
                sku = GoodsSku.objects.select_for_update().get(id=sku_id, is_delete=False, on_sale=True)
                skus.append(sku)
        except GoodsSku.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "商品不存在"})
        # 验证是否存在地址与运输方式
        try:
            addr = UserAddress.objects.get(id=addr)
        except UserAddress.DoesNotExist:
            return JsonResponse({"code": 5, "errmsg": "地址不存在"})
        try:
            transport = Transport.objects.get(pk=transport)
        except Transport.DoesNotExist:
            return JsonResponse({"code": 6, "errmsg": "运输方式不存在"})
        # 生成订单编号
        order_id = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randint(10000, 99999))
        # 准备详细地址
        address_brief = "{}{}{}-{}".format(addr.hcity, addr.hproper, addr.harea, addr.brief)
        # 开启事务
        sid = transaction.savepoint()
        order = OrderInfo.objects.create(
            user_id=user_id,
            order_id=order_id,
            username=addr.username,
            phone=addr.phone,
            addr=address_brief,
            transport_id=transport.id
        )
        total_price = 0
        # 验证库存是否足够
        cart_key = "cart_key_{}".format(user_id)
        r = get_redis_connection("default")
        for sku in skus:
            sku_num = int(r.hget(cart_key, sku.id))
            if sku_num > sku.goods_stock:
                transaction.savepoint_rollback(sid)
                return JsonResponse({"code": 7, "errmsg": "库存不足"})
            else:
                total_price += sku.goods_price * sku_num
                sku.goods_stock = sku.goods_stock - sku_num
                sku.save()
                order_sku = OrderSku.objects.create(
                    order_id=order.id,
                    sku_id=sku.id,
                    sku_num=sku_num,
                    sku_price=sku.goods_price
                )
        try:
            order.order_cost = total_price
            order.save()
        except:
            transaction.savepoint_rollback(sid)
            return JsonResponse({"code": 8, "errmsg": "保存商品总金额失败"})
        # 删除redis中的订单
        r.hdel(cart_key, *sku_ids)
        # 成功后跳转确认支付页面
        return JsonResponse({"code": 0, "msg": "创建订单成功!", "order_id": order_id})


def showOrder(request):
    user_id = request.session.get("id")
    order_id = request.GET.get("order_id")
    try:
        order = OrderInfo.objects.get(order_id=order_id, user_id=user_id)
    except OrderInfo.DoesNotExist:
        return redirect("cart:cart")
    total_price = order.order_cost + order.transport.money
    order.payfor = total_price
    order.save()
    context = {
        "total_price ": total_price,
        "order": order
    }
    return render(request, "order/trueorder.html", context)


def pay(request):
    # 接收请求中order_sn
    order_id = request.GET.get("order_id")
    if order_id is None:
        return redirect("cart:cart")

    brief = "sam超市支付"
    user_id = request.session.get("id")
    # 查询订单信息
    try:
        order = OrderInfo.objects.get(order_id=order_id, user_id=user_id, order_status=0)
    except OrderInfo.DoesNotExist:
        return redirect("goods:index")

    app_private_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/private_key.txt")).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/ali_public_key.txt")).read()

    # 创建对象
    alipay = AliPay(
        appid="2016092300576142",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    # 发起支付
    # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order.order_id,  # 订单号
        total_amount=str(order.payfor),  # 总金额
        subject=brief,
        return_url="http://127.0.0.1:8001/order/success/",
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 跳转到支付链接
    # return HttpResponse("https://openapi.alipaydev.com/gateway.do?{}".format(order_string))
    return redirect("https://openapi.alipaydev.com/gateway.do?{}".format(order_string))


def success(request):
    app_private_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/private_key.txt")).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "apps/order/ali_public_key.txt")).read()

    # 创建对象
    alipay = AliPay(
        appid="2016092300576142",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 获取参数
    out_trade_no = request.GET.get('out_trade_no')
    paid = False
    for i in range(3):
        result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            break
        else:
            time.sleep(3)

    if paid is False:
        context = {
            "message": "支付失败"
        }
    else:
        # 支付成功
        # 修改状态
        user_id = request.session.get("id")
        OrderInfo.objects.filter(order_id=out_trade_no, user_id=user_id, order_status=0).update(order_status=1)

        # 渲染数据
        context = {
            "message": "支付成功"
        }

    # 支付成功之后返回的页面
    return render(request, 'order/pay.html', context)