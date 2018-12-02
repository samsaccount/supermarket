from django.shortcuts import render
from goods.models import *
from django_redis import get_redis_connection

# Create your views here.

def index(request):
    banner = Banner.objects.all()
    events = Events.objects.all()
    sku = GoodsSku.objects.all()
    cate_id = Category.objects.filter(cate_order=9).get().id
    context = {
        "banner": banner,
        "events": events,
        "sku": sku,
        "cate_id":cate_id
    }
    return render(request, "goods/index.html", context)


def detail(request, sku_id):
    data = GoodsSku.objects.get(id=sku_id)

    context = {
        "sku": data
    }
    return render(request, "goods/detail.html", context)


def category(request, cate_id, order_id):
    cate = Category.objects.all().order_by("-cate_order")
    cate_id = int(cate_id)
    order_id = int(order_id)
    goods = {}
    if order_id == 1:
        goods = GoodsSku.objects.filter(goods_cate_id=cate_id).all()
    elif order_id == 2:
        goods = GoodsSku.objects.filter(goods_cate_id=cate_id).all().order_by("goods_sales")
    elif order_id == 3:
        goods = GoodsSku.objects.filter(goods_cate_id=cate_id).all().order_by("goods_price")
    elif order_id == 4:
        goods = GoodsSku.objects.filter(goods_cate_id=cate_id).all().order_by("-goods_price")
    else:
        goods = GoodsSku.objects.filter(goods_cate_id=cate_id).all().order_by("create_time")
    # 购物车数量
    # 验证是否登陆
    user_id = request.session.get("id")
    # 若未登陆
    count = 0
    if not user_id:
        count = 0
    else:
        r= get_redis_connection("default")
        cart_key = "cart_key_{}".format(user_id)
        data = r.hgetall(cart_key)
        if data:
            for sku_id,num in data.items():
                count += int(num)
        else:
            count = 0
    context = {
        "cate_id": cate_id,
        "cate": cate,
        "order_id": order_id,
        "goods": goods,
        "count":count
    }
    return render(request, "goods/category.html", context)
