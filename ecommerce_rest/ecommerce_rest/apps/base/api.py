from rest_framework import generics

class GeneralListApiView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self): #Funcion para listar objetos de la tabla referente al modelo MeasureUnit
        model = self.get_serializer().Meta.model #Obtiene el modelo especifico que se define en el meta de cada serializador
        return model.objects.filter(state = True) #Listado obtenido como GET de lo almacenado en las tablas, pero en formato Json