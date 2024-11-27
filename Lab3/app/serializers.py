# from rest_framework import serializers

# from .models import *


# class AstronautsSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()

#     def get_image(self, astronaut):
#         if astronaut.image:
#             return astronaut.image.url.replace("minio", "localhost", 1)

#         return "http://localhost:9000/images/default.png"

#     class Meta:
#         model = Astronaut
#         fields = ("id", "name", "status", "space_time", "image")


# class AstronautSerializer(AstronautsSerializer):
#     class Meta(AstronautsSerializer.Meta):
#         model = Astronaut
#         fields = AstronautsSerializer.Meta.fields + ("description", )


# class FlightsSerializer(serializers.ModelSerializer):
#     owner = serializers.StringRelatedField(read_only=True)
#     moderator = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Flight
#         fields = "__all__"


# class FlightSerializer(FlightsSerializer):
#     astronauts = serializers.SerializerMethodField()
            
#     def get_astronauts(self, flight):
#         items = AstronautFlight.objects.filter(flight=flight)
#         return [AstronautItemSerializer(item.astronaut, context={"value": item.value}).data for item in items]


# class AstronautItemSerializer(AstronautSerializer):
#     value = serializers.SerializerMethodField()

#     def get_value(self, astronaut):
#         return self.context.get("value")

#     class Meta(AstronautSerializer.Meta):
#         fields = "__all__"


# class AstronautFlightSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AstronautFlight
#         fields = "__all__"


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'username')


# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password', 'username')
#         write_only_fields = ('password',)
#         read_only_fields = ('id',)

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data['email'],
#             username=validated_data['username']
#         )

#         user.set_password(validated_data['password'])
#         user.save()

#         return user


# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)

from rest_framework import serializers

from .models import *


class OperationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, operation):
        if operation.image:
            return operation.image.url.replace("minio", "localhost", 1)
        return "http://localhost:9000/images/default.png"

    class Meta:
        model = Operation
        fields = ("id", "name", "status", "image_url", "description", "parameters")


class CalculationSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Calculation
        fields = "__all__"

class DetailedCalculationSerializer(CalculationSerializer):
    operations = serializers.SerializerMethodField()

    class Meta(CalculationSerializer.Meta):
        model = Calculation
        # Преобразуем fields в список для корректного объединения
        fields = list(CalculationSerializer.Meta.fields) + ["operations"]



class OperationCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationCalculation
        fields = "__all__"


class OperationCalculationDetailSerializer(serializers.ModelSerializer):
    operation = OperationSerializer(read_only=True)

    class Meta:
        model = OperationCalculation
        fields = ("operation", "value")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)