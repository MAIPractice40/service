from django.contrib import admin
from .models import Application, Contract, Customer

admin.site.register(Application)
admin.site.register(Contract)
admin.site.register(Customer)

# Register your models here.
