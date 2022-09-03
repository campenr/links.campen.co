from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from app.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class ListCreateLinks(APIView):

    def get(self,  request, *args, **kwargs):
        queryset = Link.objects.all()
        serializer = LinkSerializer(queryset, many=True)
        return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     pass

