from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from goods.models import GoodsSku
from django_redis import get_redis_connection


def cart(request):
    r = get_redis_connection("default")
    # 查找用户id
    user_id = request.session.get("id")
    # 创建哈希key
    cart_key = "cart_key_{}".format(user_id)
    data = r.hgetall(cart_key)
    goods = []
    if data:
        for sku_id, count in data.items():
            sku = GoodsSku.objects.get(id=sku_id)
            num = count
            goods.append({"good":sku,"count":num})
    context ={
        "goods":goods
    }
    return render(request, "cart/shopcart.html",context=context)


def cart_count(request):
    if request.method == "POST":
        # 查找用户id验证登陆
        user_id = request.session.get("id")
        if not user_id:
            return JsonResponse({"status": "0", "errmsg": "尚未登陆，请登陆后添加到购物车"})
        # 接收商品ID和商品数量
        good_id = request.POST.get("good_id")
        count = request.POST.get("count")
        # 验证参数
        try:
            good_id = int(good_id)
            count = int(count)
        except:
            return JsonResponse({"status": "1", "errmsg": "参数错误"})
        # if count < 0:
        #     return JsonResponse({"status": "1", "errmsg": "参数错误"})
        # # 验证是否存在该商品
        try:
            goods = GoodsSku.objects.get(id=good_id)
        except GoodsSku.DoesNotExist:
            return JsonResponse({"status": "4", "errmsg": "商品不存在"})
        # 验证库存是否足够
        if goods.goods_stock < count:
            return JsonResponse({"status": "5", "errmsg": "库存不足"})
        # 添加到redis中
        # 链接到redis上
        r = get_redis_connection("default")
        # 创建哈希key
        cart_key = "cart_key_{}".format(user_id)
        # 保存到redis中
        sku_id_count = r.hincrby(cart_key, good_id, count)
        if sku_id_count <= 0:
            r.hdel(cart_key, good_id)
        count = 0
        data = r.hgetall(cart_key)
        if data:
            for sku_id, num in data.items():
                count += int(num)
        return JsonResponse({"status": "2", "count": count})
