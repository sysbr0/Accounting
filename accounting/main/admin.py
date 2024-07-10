from django.contrib import admin
from .models import payment , mainPoduct , branches , buyes , buyesInner , accounts , clints 
# Register your models here.
admin.site.register(clints)
admin.site.register(payment)
admin.site.register(mainPoduct)
admin.site.register(branches)
admin.site.register(buyes)
admin.site.register(buyesInner)
admin.site.register(accounts)
