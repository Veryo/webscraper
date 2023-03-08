from django.contrib import admin
from .models import Product , Opinions
# Register your models here.
class OpinionsInline(admin.TabularInline):
    model = Opinions
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [OpinionsInline]

class OpinionsAdmin(admin.ModelAdmin):
    list_display = ('opinion_id', 'product', 'author')
    list_filter = ('product__name', )

admin.site.register(Product, ProductAdmin)
admin.site.register(Opinions,OpinionsAdmin)
