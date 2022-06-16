from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created #Tiempo que ha pasado desde que se creo hasta el tiempo actual
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed #Tiempo definido para expire menos el tiempo transcurrido
        return left_time #Retorna el tiempo de expiracion

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0) #Retorna un True si el tiempo aun no ha expirado

    def token_expire_handler(self, token): #Nos dice si el token expiro o no, dependiendo de si es asi o no, refresca el token del usuario al borrarlo y volverlo a crear
        is_expire = self.is_token_expired(token) #Llama a las anteriores funciones para el calculo del tiempo de expiracion
        if is_expire:
            self.expired = True
            user = token.user #Obtenemos el usuario
            token.delete #Eliminamos el token
            token = self.get_model().objects.create(user=user) #Le asignamos otro token al usuario
        return is_expire, token

    def authenticate_credentials(self, key):
        message, token, user = None, None, None
        try:
            token = self.get_model().objects.select_related('user').get(key=key) #Obtenemos el token si existe
            user = token.user
        except self.get_model().DoesNotExist: #Excepcion que se genera al no encontrar ese token
            message = 'Token invalido'
            self.expired = True

        if token is not None:
            if not token.user.is_active:
                message = 'Usuario no activo o eliminado'
            is_expired = self.token_expire_handler(token)

            if is_expired:
                message = 'Su token ha expirado'
        return (user,token,message,self.expired)