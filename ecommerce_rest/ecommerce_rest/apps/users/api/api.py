from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, UserListSerializer

#Decorador @api_view, es una vista basica para las funciones
#Define los metodos que puede utilizar la funcion
@api_view(['GET', 'POST']) #Se definen los metodos de la funcion que se van a implementar
def user_api_view(request): #Obtiene la solicitud desde el frontend con toda la informacion
    # list
    if request.method == 'GET': #Se determina si hay un metodo que corresponda en la solicitud, en este caso para obtener datos
        # queryset
        users = User.objects.all().values('id','username','email','password') #Se obtienen los objetos del modelo User que estan almacenados en la tabla, en este caso se optimiza al solo pedir esos 4 atributos
        users_serializer = UserListSerializer(users, many=True) #Se hace llamado a la clase para serializar todos los datos de los objetos User
        '''
        #Prueba de como se valida y guarda en la base de datos con un serializer
        test_data = {
            'name' : 'Develop',
            'email' : 'test@gmail.com'
        }

        test_user = TestUserSerializer(data = test_data, context = test_data)
        if test_user.is_valid():
            user_instance = test_user.save()
            print(user_instance)
        else:
            print(test_user.errors) #Imprime los errores que se almacenaron con un raise en el serializador en un diccionario
        '''
        return Response(users_serializer.data, status=status.HTTP_200_OK) #Envia una respuesta con  los datos y el codigo de estatus de la peticion

    # create
    elif request.method == 'POST': #Guardar Usuarios
        user_serializer = UserSerializer(data=request.data)

        # validation
        if user_serializer.is_valid(): #Validar que los datos ingresados sean validos para los campos del modelo
            user_serializer.save() #Almacenar la informacion en la tabla
            return Response({'message': 'Usuario creado correctamente!'}, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    # queryset
    user = User.objects.filter(id=pk).first() #Obtener el usuario por medio de su ID

    # validation
    if user:

        # retrieve
        if request.method == 'GET': #Obtener datos de un solo usuario
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        # update
        elif request.method == 'PUT':#Actualizar datos de un usuario
            user_serializer = UserSerializer(user, data=request.data) #Cuando se envia el user y la data, es porque se va a hacer un update
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # delete
        elif request.method == 'DELETE':#Eliminar un usuario
            user.delete()
            return Response({'message': 'Usuario Eliminado correctamente!'}, status=status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)