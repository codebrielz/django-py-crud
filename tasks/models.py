from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# models.Model es para que django pueda crear la tabla
class Task(models.Model):
    title = models.CharField(max_length= 100)
    description = models.TextField(blank=True) #TextField es para campos de textos más largos y encaso de que este vacío el campo que por defecto este vacío 
    created = models.DateTimeField(auto_now_add=True) # añade la hora y dia por defecto
    datecompleted = models.DateTimeField(null=True, blank=True) # inicialmente será un campo vacío que tendrá que añadir el usuario (es obligatorio) pero en la base de datos es opcional.
    important = models.BooleanField(default=False)
    # ForeignKey es para relacionar una tabla con otra, en este caso, Task con la tabla User (django tiene creado el model 
    # User por defecto)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Esto significa que hace una eliminación en cascada, quiere decir
    # que todo lo relacionado con la tabla USER eliminado se eliminará tambien.
    
    # cuando utilicen este modelo como un string que retorne el title (para mostrar en el gestor administrativo)
    def __str__(self):
        return self.title + ' - by ' + self.user.username