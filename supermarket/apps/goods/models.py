from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from db.base_model import BaseModel


# Create your models here.
class Category(BaseModel):
    cate_name = models.CharField(max_length=20, verbose_name="分类名称")
    cate_intro = models.CharField(max_length=100, verbose_name="分类简介")
    cate_order = models.SmallIntegerField(default=0, verbose_name="分类优先度")

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cate_name


class Unit(BaseModel):
    unit_name = models.CharField(max_length=5, verbose_name="货物单位")

    class Meta:
        verbose_name = "商品单位"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.unit_name


class GoodsSku(BaseModel):
    goods_sku_name = models.CharField(max_length=50, verbose_name="商品名称")
    goods_brief = models.CharField(max_length=50, verbose_name="商品简介")
    goods_price = models.DecimalField(max_digits=9, decimal_places=2, default=0,verbose_name="商品价格")
    goods_unit = models.ForeignKey(to="Unit", verbose_name="商品单位")
    goods_stock = models.IntegerField(default=1, verbose_name="商品库存")
    goods_sales = models.IntegerField(default=0, verbose_name="商品销量")
    goods_logo = models.ImageField(upload_to="goods/%Y/%m/%d", verbose_name="商品logo")
    on_sale = models.BooleanField(default=False, verbose_name="是否上架")
    goods_cate = models.ForeignKey(to="Category", verbose_name="商品分类")
    goods_spu = models.ForeignKey(to="GoodsSpu", verbose_name="商品spu")

    class Meta:
        verbose_name = "商品sku"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_sku_name


class GoodsSpu(BaseModel):
    goods_spu_name = models.CharField(max_length=20, verbose_name="spu名称")
    goods_content = RichTextUploadingField(verbose_name="详情")

    class Meta:
        verbose_name = "商品spu"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_spu_name


class GoodsPic(BaseModel):
    goods_pic = models.ImageField(upload_to="goods/%Y/%m/%d", verbose_name="商品图片")
    goods_sku_name = models.ForeignKey(to="GoodsSku", verbose_name="商品名称")

    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_sku_name.goods_sku_name


class Banner(BaseModel):
    banner_name = models.CharField(max_length=20, verbose_name="轮播图名称")
    goods_skuid = models.ForeignKey(to="GoodsSku", verbose_name="商品skuid")
    banner_pic = models.ImageField(upload_to="banner/%Y/%m/%d", verbose_name="轮播图")
    order = models.IntegerField(verbose_name="排序")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.banner_name


class Events(BaseModel):
    events_name = models.CharField(max_length=20, verbose_name="活动名称")
    events_pic = models.ImageField(upload_to="events/%Y/%m/%d", verbose_name="活动图片")
    events_url = models.URLField(verbose_name="活动链接")

    class Meta:
        verbose_name = "活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.events_name


class EventsPage(BaseModel):
    page_name = models.CharField(max_length=20, verbose_name="活动页面名称")
    page_intro = RichTextUploadingField(verbose_name="活动介绍")
    order = models.IntegerField(verbose_name="活动排序")

    class Meta:
        verbose_name = "活动页面"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.page_name


class EventsGoods(BaseModel):
    events_id = models.ForeignKey(to="Events", verbose_name="活动ID")
    goods_skuid = models.ForeignKey(to="GoodsSku", verbose_name="商品SKUid")

    class Meta:
        verbose_name = "活动商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_skuid
