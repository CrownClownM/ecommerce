from django.contrib import admin
from apps.products.models import *

# Register your models here.
class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ('id','description') #Muestra los campos suministrados como columnas en el panel de administrador

class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id','description')

admin.site.register(MeasureUnit,MeasureUnitAdmin) #Son los modelos que se podran visualizar desde el panel de administracion
admin.site.register(CategoryProduct,CategoryProductAdmin)
admin.site.register(Indicator)
admin.site.register(Product)