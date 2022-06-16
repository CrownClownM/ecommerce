from django.db import models

# Create your models here.

#Modelo base, es donde se va a colocar todas las utilidades de forma global para heredar a otros modelos
class BaseModel(models.Model):
    """Model definition for BaseModel."""

    # TODO: Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('Estado',default = True)
    created_date = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True) #auto_now_add se usa para actualizar automaticamente el campo cuando se modifica
    modified_date = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add=False) #auto_now se usa para actualizar automaticamente el campo cuando se crea
    deleted_date = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for BaseModel."""
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'