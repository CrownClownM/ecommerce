from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import get_authorization_header

from apps.users.authentication import ExpiringTokenAuthentication


class Authentication(object):
    user = None
    user_token_expired = False

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try: #Intenta obtener la posicion 1 (0,1,2,...), debido a que se envia "Token lo-que-obtenemos",
                token = token[1].decode() #Posicion 1, es la segunda cadena la que obtenemos del get_authorization_header y ademas lo decodificamos
            except:
                return None

            token_expire = ExpiringTokenAuthentication()
            user, token, message, self.user_token_expired = token_expire.authenticate_credentials(token) #Autentica que el token efectivamente exista
            if user != None and token != None:
                self.user = user
                return user
            return message
        return None #No se envio un token en la peticion

    def dispatch(self, request, *args, **kwargs): #Metodo que toda clase de Django ejecuta primero de la clase authentication
        user = self.get_user(request) #Obtiene el user
        # found token in request
        if user is not None:
            if type(user) == str:
                response = Response({'error':user,'expired':self.user_token_expired}, status = status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()  # La respuesta es de tipo JSON
                response.accepted_media_type = 'application/json'  # Esto es de tipo application/JSON
                response.renderer_context = {}  # Contexto como parametro extra
                return response
            if not self.user_token_expired:
                return super().dispatch(request, *args, **kwargs)
        response = Response({'error': 'No se han enviado las credenciales.','expired':self.user_token_expired}, status=status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer() #La respuesta es de tipo JSON
        response.accepted_media_type = 'application/json' #Esto es de tipo application/JSON
        response.renderer_context = {} #Contexto como parametro extra
        return response