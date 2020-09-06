from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from . models import Course, Stop, Route

from . serializers import RouteCreateOrUpdateSerializer

class CourseApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()    

    def test_create_route(self):
        """
        노선 생성 테스트
        노선에 포함될 정류장은 최대 10개까지
        노선 및 정류장 이름은 최대 32자 까지
        이미 존재하는 노선 이름 사용 불가
        """

        #-------------------준비------------------
        
        #정상 데이터1
        valid_route_data1 = {
            'name': '노선A',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }
        #정상 데이터2
        valid_route_data2 = {
            'name': '노선B',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장D', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장B', 'order':4}
            ]
        }
        
        #비정상 데이터1 - 정류장 개수 10개 초과
        invalid_route_data1 = {
            'name': '노선C',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4},
                {'name': '정류장E', 'order':5},
                {'name': '정류장F', 'order':6},
                {'name': '정류장G', 'order':7},
                {'name': '정류장H', 'order':8},
                {'name': '정류장I', 'order':9},
                {'name': '정류장J', 'order':10},
                {'name': '정류장K', 'order':11},
                {'name': '정류장L', 'order':12}
            ]
        }

        #비정상 데이터2 - 이미 존재하는 노선 이름
        invalid_route_data2 = {
            'name': '노선A',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }

        #비정상 데이터3 - 노선 이름 32자 초과
        invalid_route_data3 = {
            'name': f'노선{"하" * 32}',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }

        #비정상 데이터4 - 정류장 이름 32자 초과
        invalid_route_data4 = {
            'name': '노선A',
            'courses': [
                {'name': f'정류장{"하" * 32}', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }

        #-------------------테스트------------------

        valid_response1 = self.client.post(
            reverse('create_update_route'),
            valid_route_data1,
            format='json'
        )
        valid_response2 = self.client.post(
            reverse('create_update_route'),
            valid_route_data2,
            format='json'
        )
        invalid_response1 = self.client.post(
            reverse('create_update_route'),
            invalid_route_data1,
            format='json'
        )
        invalid_response2 = self.client.post(
            reverse('create_update_route'),
            invalid_route_data2,
            format='json'
        )
        invalid_response3 = self.client.post(
            reverse('create_update_route'),
            invalid_route_data3,
            format='json'
        )
        invalid_response4 = self.client.post(
            reverse('create_update_route'),
            invalid_route_data4,
            format='json'
        )

        #-------------------검증------------------
        self.assertEqual(
            valid_response1.status_code,
            status.HTTP_201_CREATED)
        self.assertEqual(
            valid_response2.status_code,
            status.HTTP_201_CREATED)

        self.assertEqual(
            invalid_response1.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            invalid_response2.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            invalid_response3.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            invalid_response4.status_code,
            status.HTTP_400_BAD_REQUEST)
    
    def test_update_route(self):
        """
        노선 정보 수정
        """

        #-------------------준비------------------
        
        #테스트를 위한 노선 데이터
        valid_route_data1 = {
            'name': '노선A',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }

        #테스트를 위한 노선 데이터
        valid_route_data2 = {
            'name': '노선B',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장D', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장B', 'order':4}
            ]
        }
        
        self.client.post(
            reverse('create_update_route'),
            valid_route_data1,
            format='json'
        )
        #노선B의 id를 테스트에서 활용
        valid_response2 = self.client.post(
            reverse('create_update_route'),
            valid_route_data2,
            format='json'
        )
        id = valid_response2.data["id"]

        #정상 수정 요청
        valid_route_update = {
            'id': id,
            'name': '노선C'
        }
        #비정상 수정 요청1 - 이미 존재하는 이름으로 수정
        invalid_route_update1 = {
            'id': id,
            'name': '노선A'
        }
        #비정상 수정 요청2 - 노선 이름 32자 초과
        invalid_route_update2 = {
            'id': id,
            'name': f'노선{"하"*32}'
        }

        #-------------------테스트------------------

        valid_response = self.client.put(
            reverse('create_update_route'),
            valid_route_update,
            format='json'
        )
        invalid_response1 = self.client.put(
            reverse('create_update_route'),
            invalid_route_update1,
            format='json'
        )
        invalid_response2 = self.client.put(
            reverse('create_update_route'),
            invalid_route_update2,
            format='json'
        )

        #-------------------검증------------------

        self.assertEqual(
            valid_response.status_code,
            status.HTTP_200_OK)

        self.assertEqual(
            invalid_response1.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            invalid_response2.status_code,
            status.HTTP_400_BAD_REQUEST)


    def test_get_list_of_route(self):
        """
        노선 전체 목록 조회
        """

        #-------------------준비------------------

        #테스트를 위한 노선 데이터
        valid_route_data1 = {
            'name': '노선A',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }
        #테스트를 위한 노선 데이터
        valid_route_data2 = {
            'name': '노선B',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장D', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장B', 'order':4}
            ]
        }
        self.client.post(
            reverse('create_update_route'),
            valid_route_data1,
            format='json'
        )
        self.client.post(
            reverse('create_update_route'),
            valid_route_data2,
            format='json'
        )

        #-------------------테스트------------------
        
        response = self.client.get(
            reverse('get_route_list'),
            format='json'
        )

        #-------------------검증------------------

        data = response.data["courses"]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data[1]["name"],
            "노선B"
        )
    
    def test_retrieve_route(self):
        """
        노선 상세 조회
        """

        #-------------------준비------------------

        #테스트를 위한 노선 데이터
        valid_route_data1 = {
            'name': '노선A',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }
        #테스트를 위한 노선 데이터
        valid_route_data2 = {
            'name': '노선B',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장D', 'order':2},
                {'name': '정류장C', 'order':3}
            ]
        }
        
        valid_response1 = self.client.post(
            reverse('create_update_route'),
            valid_route_data1,
            format='json'
        )
        id1 = valid_response1.data["id"]

        valid_response2 = self.client.post(
            reverse('create_update_route'),
            valid_route_data2,
            format='json'
        )
        id2 = valid_response2.data["id"]

        #-------------------테스트------------------

        response1 = self.client.get(
            reverse('retrieve_route', kwargs={'pk': id1}),
            format='json'
        )
        response2 = self.client.get(
            reverse('retrieve_route', kwargs={'pk': id2}),
            format='json'
        )

        #-------------------검증------------------

        data = response1.data

        self.assertEqual(
            response1.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data["name"],
            "노선A"
        )
        self.assertEqual(
            len(data["courses"]),
            4
        )

        data = response2.data

        self.assertEqual(
            response2.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data["name"],
            "노선B"
        )
        self.assertEqual(
            len(data["courses"]),
            3
        )

    def test_delete_route(self):
        """
        노선 삭제
        """

        #-------------------준비------------------

        #테스트를 위한 노선 데이터
        valid_route_data1 = {
            'name': '노선A',
            'courses': [
                {'name': '정류장A', 'order':1},
                {'name': '정류장B', 'order':2},
                {'name': '정류장C', 'order':3},
                {'name': '정류장D', 'order':4}
            ]
        }
        
        valid_response1 = self.client.post(
            reverse('create_update_route'),
            valid_route_data1,
            format='json'
        )
        id1 = valid_response1.data["id"]

        #-------------------테스트------------------

        #삭제
        delete_response = self.client.delete(
            reverse('retrieve_route', kwargs={'pk': id1}),
            format='json'
        )

        #삭제 여부 확인
        confirm_response = self.client.get(
            reverse('retrieve_route', kwargs={'pk': id1}),
            format='json'
        )

        #-------------------검증------------------

        self.assertEqual(
            delete_response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            confirm_response.status_code,
            status.HTTP_404_NOT_FOUND
        )