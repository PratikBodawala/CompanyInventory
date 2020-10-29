from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from employee.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    last_login = serializers.CharField(read_only=True)

    def create(self, validated_data):
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups)
        user.user_permissions.set(user_permissions)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

    class Meta:
        model = User
        fields = '__all__'
