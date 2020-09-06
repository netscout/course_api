from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Course, Route, Stop
from .serializers import RouteCreateOrUpdateSerializer, RouteRetreiveSerializer, \
    RouteListSerializer

class RouteViewSet(viewsets.ModelViewSet):
    """
    노선 데이터에 대한 요청을 처리할 뷰
    """

    #ViewSet에서 사용할 데이터 목록 설정
    queryset = Route.objects.all()

    #ViewSet에서 사용할 직렬화 / 역직렬화 클래스 설정
    def get_serializer_class(self):
        if self.action == 'create' or\
            self.action == 'update':
            return RouteCreateOrUpdateSerializer
        if self.action == 'list':
            return RouteListSerializer
        if self.action == 'retrieve':
            return RouteRetreiveSerializer

    def create(self, request, *args, **kwargs):
        """
        노선 추가
        """
        data = request.data

        #노선 검사
        route = Route.objects.filter(name=data["name"])\
            .first()
        if route is not None:
            return Response(
                {
                    'message' : '이미 존재하는 노선 입니다.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        courses = sorted(data["courses"], key=lambda c: c["order"])

        #정류장 개수 검사
        if len(courses) > 10:
            return Response(
                {
                    'message' : '노선에 정류장은 10개 까지 포함시킬 수 있습니다.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        #노선 및 정류장 이름 규칙 검사
        invalid_stop_list = [
            stop for stop in courses
            if len(stop["name"]) > 32
            ]
        if len(data["name"]) > 32 or len(invalid_stop_list) > 0:
            return Response(
                {
                    'message' : '노선 및 정류장 이름은 최대 32자입니다.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        #노선 추가
        route = Route.objects.create(
            name = data["name"]
        )

        #새로 입력된 정류장 추가
        for stop in courses:
            s = Stop.objects.filter(name=stop["name"])\
                .first()

            if s is None:
                s = Stop.objects.create(
                    name=stop["name"]
                )
            
            Course.objects.create(
                route = route,
                stop = s,
                order = stop["order"]
            )

        return Response(
                {
                    'id' : route.id
                },
                status = status.HTTP_201_CREATED
            )

    def update(self, request, *args, **kwargs):
        data = request.data

        #노선 이름 규칙 검사
        if len(data["name"]) > 32:
            return Response(
                {
                    'message' : '노선 및 정류장 이름은 최대 32자입니다.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        #노선 검사
        route = Route.objects.filter(id=data["id"])\
            .first()
        if route is None:
            return Response(
                {
                    'message' : '노선이 존재하지 않습니다.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        #기존에 존재하는 노선 이름 검사
        same_route_name = Route.objects.filter(name=data["name"])\
            .first()
        if same_route_name is not None:
            return Response(
                {
                    'message' : '이미 존재하는 노선 이름입니다.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        route.name = data["name"]
        route.modifiedDate = timezone.now()
        route.save()

        return Response(
            status = status.HTTP_200_OK
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'courses': serializer.data
            },
            status = status.HTTP_200_OK
        )

        
