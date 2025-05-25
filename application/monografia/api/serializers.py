from rest_framework import serializers
from ..models import Monografia

class MonografiaSerializer(serializers.ModelSerializer):

    arquivo = serializers.FileField(use_url=False)

    class Meta:
        model = Monografia
        fields = "__all__"
        read_only_fields = ('id', 'created_at', 'updated_at')

