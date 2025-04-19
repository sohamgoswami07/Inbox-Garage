from django.contrib import admin
from .models import BrandDetail, EmailDetail, TemplatesDetail

# Register your models here.
class BrandDetailAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'brand_type')
    
class EmailDetailAdmin(admin.ModelAdmin):
    list_display = ('email_subject', 'email_category')
    
class TemplatesDetailAdmin(admin.ModelAdmin):
    list_display = ('template_subject', )

admin.site.register(BrandDetail, BrandDetailAdmin)
admin.site.register(EmailDetail, EmailDetailAdmin)
admin.site.register(TemplatesDetail, TemplatesDetailAdmin)