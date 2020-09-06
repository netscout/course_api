from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    name = models.CharField(max_length=32)

    createdDate = models.DateTimeField(
        auto_now_add=True,
        blank=True)

    modifiedDate = models.DateTimeField(
        auto_now_add=True,
        blank=True)

    class Meta:
        ordering = ['id']
        abstract = True

class Route(BaseModel):
    """
    노선
    노선 이름은 최대 32자까지 지정가능하며,
    최대 10개의 정류장을 가질 수 있음.
    """
    class Meta:        
        db_table="Routes"

class Stop(BaseModel):
    """
    정류장
    정류장 이름은 최대 32자까지 지정가능    
    """

    class Meta:
        db_table="Stops"

class Course(models.Model):
    """
    노선에 포함된 정류장
    """
    #Route의 courses속성으로 노선에 포함된 정류장 목록 참조
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        db_column="routeId",
        related_name="courses") 

    #Stop의 routes속성으로 정류장을 포함하는 노선 목록을 참조
    stop = models.ForeignKey(
        Stop,
        on_delete=models.CASCADE,
        db_column="stopId",
        related_name="routes")

    order = models.IntegerField()

    class Meta:
        ordering = ['id']
        db_table = "Courses"
