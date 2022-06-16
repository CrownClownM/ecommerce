from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.base.api import GeneralListApiView
from apps.users.authentication_mixins import Authentication
from apps.products.api.serializers.product_serializers import ProductSerializer

class ProductViewSet(Authentication ,viewsets.ModelViewSet):
    '''
    Hola, desde productos
    '''
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state=True) #Realiza una consulta para obtener los objetos de productos

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)  #Consulta para obtener todos los objetos de products
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first() #Consulta para encontrar el objeto exacto a listar

    def list(self, request):
        '''
        Hola, desde productos2
        '''
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data,status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #Al sobrescribir el metodo delete cambiamos la forma de eliminar el objeto, haciendolo ahora de una forma logica
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first() #Validando que el id sea igual al pk?
        if product:
            product.state = False #Cambiando el estado a falso para no tener en cuenta el objeto al momento de listar o hacer otros metodos
            product.save()
            return Response({'message':'producto eliminado correctamente!'}, status = status.HTTP_200_OK)
        return Response({'error': 'No existe un producto con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

'''
class ProductListAPIView(GeneralListApiView): #Definiendo la clase para listar objetos de la tabla
    serializer_class = ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView): #Definiendo la clase para crear productos
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state=True) #Realiza una consulta para obtener los objetos de productos para imprimir en pantalla

    def post(self, request): #Sobrescribiendo el metodo post para guardar los productos en la tabla
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): #Definiendo clase para mostrar unicamente un objeto de la tabla por su ID
    serializer_class = ProductSerializer

    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True) #Consulta para encontrar el objeto exactp a listar
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk,state=True).first()

    def patch(self,request,pk=None): #Obtener informacion del objeto
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(product_serializer.data, status=status.HTTP_200_OK) #Retorna una respuesta con los datos del objeto a actualizar
        return Response({'error': 'No existe un producto con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None): #Actualizar la informacion enviada desde la vista
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data,status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''





