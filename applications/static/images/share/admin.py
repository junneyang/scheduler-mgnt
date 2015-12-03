from django.contrib import admin

# Register your models here.
from app.models import Job

'''define your model ui
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('full_name','address','tel')
    search_fields = ('full_name',) 

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','create_date')
    search_fields = ('product_name','price')
    list_filter = ('create_date',) 
    date_hierarchy = 'create_date' 
    ordering = ('-create_date',)
    fields  = ('product_name','stock','price','create_date',)'''

class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job,JobAdmin)


