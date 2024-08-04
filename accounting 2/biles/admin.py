from django.contrib import admin
from .models import Package , Jar , ProductHam , MainProduct , UdsBills  , UdsBill_inner # ,UdsBill , yh 

admin.site.register(Package)
admin.site.register(Jar)
admin.site.register(ProductHam)
admin.site.register(MainProduct)
admin.site.register(UdsBill_inner)
#admin.site.register(UdsBill)

#admin.site.register(yh)
admin.site.register(UdsBills)
# Register your models here.
