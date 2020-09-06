from rest_framework import serializers
from .models import Course, Stop, Route

class CourseItemSerializer(serializers.ModelSerializer):
    """
    정류장 목록에 포함될 정류장 데이터 시리얼라이저
    """
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        stop = Stop.objects.filter(id=obj.stop_id)\
            .first()
        return stop.name

    class Meta:
        model = Course
        fields = ('order', 'name')

class RouteCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    노선 추가 및 수정 시리얼라이저
    """
    id = serializers.IntegerField(
        required=False
    )

    class Meta:
        model = Route
        fields = ('id', 'name')

class RouteListSerializer(serializers.ModelSerializer):
    """
    노선 목록 시리얼라이저
    """
    class Meta:
        model = Route
        fields = ('id', 'name')

class RouteRetreiveSerializer(serializers.ModelSerializer):
    """
    노선 상세 조회 시리얼 라이저
    """
    courses = serializers.SerializerMethodField()

    def get_courses(self, obj):
        qset = Course.objects.filter(route_id=obj.id)

        return [CourseItemSerializer(c).data for c in qset]

    class Meta:
        model = Route
        fields = ('id', 'name', 'courses')