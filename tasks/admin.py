from django.contrib import admin
from .models import Task

# heredamos el ModelAdmin
class TaskAdmin(admin.ModelAdmin):
    # Aqui le digo que me muestre este campo en el panel administrativo de la tabla Task
    readonly_fields = ("created",) # Es una tupla

# Para crear un superusuario debemos escribir en el entorno de python el siguiente codigo:
# python manage.py createsuperuser

# esta clase admin es para el gestor de administrador que existe por defecto en django, la ruta es /admin y podemos indicarle
# aqui todas las tablas que puede tener acceso ese panel administrativo.
# Register your models here.
admin.site.register(Task, TaskAdmin)