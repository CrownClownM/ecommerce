from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.api.serializers import UserTokenSerializer

class UserToken(APIView):
    def get(self,request,*args,**kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(user = UserTokenSerializer().Meta.model.objects.filter(username = username).first())
            return Response({
                'token': user_token.key
            })
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas.'
            },status = status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken): #Vista normal que hereda apiview donde se define su post

    def post(self,request,*args,**kwargs): #*args: , **kwargs:
        # Enviar al serializer el usuario y contraseña
        print(request.user)
        login_serializer = self.serializer_class(data = request.data, context = {'request':request}) #serializer_class contiene 2 campos username y password
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user'] # login serializer return user in validated_data
            if user.is_active: #Verifica que el estado sea True
                token, created = Token.objects.get_or_create(user=user) #Obtiene el token del usuario si existe y si no tiene un token se lo crea, se almacena en token, created es una bandera dependiendo del caso de que exista o no
                user_serializer = UserTokenSerializer(user)
                if created: #Si se crea imprime la informacion del usuario junto al token
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de Sesión Exitoso.'
                    }, status=status.HTTP_201_CREATED)
                else: #De lo contrario borramos el actual y le creamos uno nuevo
                    '''
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now()) #Todas las sesiones que su tiempo de sesion sean mayor que el tiempo actual y no hayan expirado
                    if all_sessions.exists(): #Si hay sesiones existentes
                        for session in all_sessions: #Dentro de las sesiones va recorriendo cada sesion
                            session_data = session.get_decoded() #Decodifica
                            if user.id == int(session_data.get('_auth_user_id')): #Verifica si es el ID al cual corresponde a una sesion actual del mismo usuario, verificando que no haya una sesion iniciada, de ser asi se cerraran las sesiones del usuario con ese ID
                                session.delete() #Las sesiones que hayan de ese ID las borra y por ende se cierran
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de Sesión Exitoso.'
                    }, status=status.HTTP_201_CREATED)
                '''
                    token.delete()
                    return Response({'error': 'Ya se ha iniciado sesion con este usuario.'}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'error': 'Este usuario no puede iniciar sesion.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrectos.'},status = status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Hola desde response.'}, status=status.HTTP_200_OK)

class Logout(APIView):
    def get(self, request, *args, **kwargs):
        try: #Instrucciones de lo que se quiere hacer
            token = request.GET.get('token') #Obtiene el token de la peticion
            token = Token.objects.filter(key=token).first() #Filtra por el token que ya obtuvimos, verificando que si exista
            if token:
                user = token.user
                # Cierra las sesiones del usuario que hizo el logout
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        # search auth_user_id, this field is primary_key's user on the session
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete() # Elimina el token del usuario
                session_message = 'Sesiones de usuario eliminadas.'
                token_message = 'Token eliminado.'
                return Response({'token_message': token_message, 'session_message': session_message},
                                status=status.HTTP_200_OK)

            return Response({'error': 'No se ha encontrado un usuario con estas credenciales.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except: #Cualquier cosa que pare la ejecucion del cogigo try, entonces  que haga lo del except
            return Response({'error': 'No se ha encontrado token en la petición.'},
                            status=status.HTTP_409_CONFLICT)

