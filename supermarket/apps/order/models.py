from django.db import models

# Create your models here.
from db.base_model import BaseModel


class UserAddress(BaseModel):
    """用户收货地址管理"""
    user = models.ForeignKey(to="user.User", verbose_name="创建人")
    username = models.CharField(verbose_name="收货人", max_length=100)
    phone = models.CharField(verbose_name="收货人电话", max_length=11)
    hcity = models.CharField(verbose_name="省", max_length=100)
    hproper = models.CharField(verbose_name="市", max_length=100, blank=True, default='')
    harea = models.CharField(verbose_name="区", max_length=100, blank=True, default='')
    brief = models.CharField(verbose_name="详细地址", max_length=255)
    isDefault = models.BooleanField(verbose_name="是否设置为默认", default=False, blank=True)

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Payment(BaseModel):
    """
        支付方式
    """
    pay_name = models.CharField(verbose_name='支付方式',
                                max_length=20
                                )

    # logo = models.ImageField(upload_to="pya/%Y/%m/%d",verbose_name="交易图片")

    class Meta:
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name


class Transport(BaseModel):
    """
        配送方式
    """
    name = models.CharField(verbose_name='配送方式',
                            max_length=20
                            )
    money = models.DecimalField(verbose_name='金额',
                                max_digits=9,
                                decimal_places=2,
                                default=0
                                )

    class Meta:
        verbose_name = "配送方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OrderInfo(BaseModel):
    status_choices = (
        (0, "待付款"),
        (1, "待发货"),
        (2, "已发货"),
        (3, "完成"),
        (4, "已评价"),
        (5, "申请退款"),
        (6, "已退款"),
        (7, "取消订单")
    )
    order_id = models.CharField(max_length=64, verbose_name="订单编号", unique=True)
    order_cost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="订单金额", null=True, blank=True)
    user = models.ForeignKey(to="user.User", verbose_name="用户ID")
    username = models.CharField(max_length=50, verbose_name="收货人姓名")
    phone = models.CharField(max_length=11, verbose_name="收货人电话")
    addr = models.CharField(max_length=255, verbose_name="收货地址")
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    payment = models.ForeignKey(to="Payment", verbose_name="付款方式", null=True, blank=True)
    transport = models.ForeignKey(to="Transport", verbose_name="运输方式")
    payfor = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="实付金额", null=True, blank=True)

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id


class OrderSku(BaseModel):
    order = models.ForeignKey(to="OrderInfo", verbose_name="订单")
    sku = models.ForeignKey(to="goods.GoodsSku", verbose_name="sku_id")
    sku_num = models.IntegerField(verbose_name="商品数量")
    sku_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="商品价格")

    class Meta:
        verbose_name = "订单商品表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_id
