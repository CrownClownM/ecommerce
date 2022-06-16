from rest_framework import serializers
from apps.users.models import User

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name','last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data): #Metodo para crear el usuario pero adicionando la encriptacion de la contraseña
        user = User(**validated_data) #Envia la data validada como un diccionario para la creacion del usuario
        user.set_password(validated_data['password']) #Encripta la contraseña
        user.save() #Almacena el usuario en la tabla
        return user

    def update(self, instance, validated_data): #Instance hace referencia al objeto que se envia para hacerle el update a su informacion
        updated_user = super().update(instance,validated_data) #Super para acceder a los metodos o atributos de la clase padre, en este caso el serializers.ModelSerializer, trae todo el objeto que hacemos instancia
        #print(updated_user) #Mira la instancia de lo que se trae
        updated_user.set_password(validated_data['password']) #Establece la contraseña despues de encriptarla
        updated_user.save() #Se guarda la nueva informacion en el objeto
        return updated_user

class UserListSerializer(serializers.ModelSerializer):
    class meta:
        model: User

    #Esto es una funcion que ya esta definida y es sobre como representa los datos, en este caso la estamos sobrescribiendo para mostrar los datos que queremos
    def to_representation(self, instance): #Su funcion es representar la informacion de la data que se le manda, solo para listar objetos
        return{
            'id':instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
            #Se maneja como un diccionario debido al ORM de Django, para hacer mas optima la muestra de los datos
        }

'''
class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    
    
    #Al realizar un is.valid se ejecuta desde el serializer una funcion que valida si es valido o no la informacion que se manda con
    #respecto a los campos del modelo, en este caso estamos sobrescribiendo la validacion al definirla nosotros mismos, se puede hacer por campo
    #Como es el caso de abajo de name y email
    def validate_name(self,value):
        if 'Develop1' in value:
            raise serializers.ValidationError('Error, no puede existir un usuario con ese nombre') #Retorna los fallos en la validacion
        return value

    def validate_email(self,value):
        if value == '':
            raise serializers.ValidationError('Tiene que indicar un correo')
        #if self.validate_name(self.context['name']) in value:
            #raise serializers.ValidationError('El email no puede contener el nombre')
        return value
        
    #O general de esta forma
    def validate(self,data):
        print("Validate general")
        return data

    #Tambien se sobrescribe esta funcion que nos permite guardar un objeto en la base de datos
    def create(self, validated_data):
        return self.models.objects.create(**validated_data)

    #Y finalmente tenemos el update, tambien esta sobrescrito en este caso, el cual es el encargado de actualizar la informacion almacenada de
    #Un usuario en la tabla
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save() #Este save hace referencia al save de la instacia de la clase osea el modelo (models.py), no es lo mismo que el save del serializer
        return instance
    
'''

