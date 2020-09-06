# 노선 관리 백엔드 API

## 실행 방법
프로젝트 설정 및 실행은 아래의 절차에 따라 진행하세요.

### 필요한 개발 환경
이 프로젝트는 다음과 같은 도구 및 환경에서 작성되었습니다.:

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python 3.7.8(64-bit)](https://www.python.org/downloads/release/python-378/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop) (2.3.0.4)

### Setup
다음과 같이 설정을 진행하세요:

  1. 리포지토리 복제
  2. Python 가상환경 패키지 설치:
     ```
     pip install virtualenv
     ```
  3. Python 가상환경 생성 및 활성화:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
  4. 리포지토리의 루트 폴더에서 필요한 Python 패키지 설치:
     ```
     cd course_api
     pip install -r requirements.txt
     ```
  5. 다음으로, vs code를 실행:
     ```
     code .
     ```
  6. `\course_api\my_settings.py` 파일을 새로 추가하고 데이터 베이스 정보를 설정(기본 설정):
     ```
     DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'BackendTest',
            'USER': 'user',
            'PASSWORD': 'dbwjvotmdnjem',
            'HOST': 'localhost',
            'PORT': '3306',
        }
     }
     ```
  7. 다음으로, 데이터 베이스를 설정(환경에 따라 20-30초 소요):
     ```
     docker-compose up -d
     ```
  8. 다음으로, 데이터베이스에 모델을 마이그레이션 수행:
     ```
     python manage.py migrate
     ```
  9. 다음으로, 개발 서버를 실행:
     ```
     python manage.py runserver
     ```
  10. 브라우저에서 [http://127.0.0.1:8000/api/Route/](http://127.0.0.1:8000/api/Route/) 에 접속하여 동작을 확인

### 테스트 코드 실행
이 프로젝트는 TDD방식으로 진행되었습니다. 테스트 코드를 실행하려면 다음 절차를 진행하세요:

  1. mysql 서버에 접속하여 user계정에 테스트 데이터베이스(test_{DB명}) 생성 및 접근 권한 설정
     ```
     데이터베이스 이름이 BackendTest인 경우, 테스트 데이터베이스는 test_BackendTest
     ```
  2. 다음 명령으로 테스트 코드 실행:
     ```
     python manage.py test
     ```

### 테이블 생성 SQL
Django Rest Framework의 특성상 TDD방식으로 진행하기 위해 모델 객체의 데이터베이스 마이그레이션 생성이 필수 입니다. Managed=False 설정으로 진행해보려 하였으나 해결책을 찾지 못하여 ORM으로 데이터베이스 마이그레이션을 진행하였습니다.

아래 SQL은 데이터베이스에서 역으로 생성한 SQL 쿼리입니다.

     
	USE `BackendTest`;
	
	-- 노선(Routes) 테이블
	CREATE TABLE IF NOT EXISTS `Routes` (
	  `id` int NOT NULL AUTO_INCREMENT,
	  `name` varchar(32) NOT NULL,
	  `createdDate` datetime(6) NOT NULL,
	  `modifiedDate` datetime(6) NOT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	
	-- 정류장(Stops)테이블
	CREATE TABLE IF NOT EXISTS `Stops` (
	  `id` int NOT NULL AUTO_INCREMENT,
	  `name` varchar(32) NOT NULL,
	  `createdDate` datetime(6) NOT NULL,
	  `modifiedDate` datetime(6) NOT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

	-- 노선에 포함된 정류장(Courses) 테이블
	CREATE TABLE IF NOT EXISTS `Courses` (
	  `id` int NOT NULL AUTO_INCREMENT,
	  `order` int NOT NULL,
	  `routeId` int NOT NULL,
	  `stopId` int NOT NULL,
	  PRIMARY KEY (`id`),
	  KEY `Courses_routeId_c7995f84_fk_Routes_id` (`routeId`),
	  KEY `Courses_stopId_a71d860c_fk_Stops_id` (`stopId`),
	  CONSTRAINT `Courses_routeId_c7995f84_fk_Routes_id` FOREIGN KEY (`routeId`) REFERENCES `Routes` (`id`),
	  CONSTRAINT `Courses_stopId_a71d860c_fk_Stops_id` FOREIGN KEY (`stopId`) REFERENCES `Stops` (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
     

### API 활용 방법
1. 노선 추가(POST) : http://127.0.0.1:8000/api/Route/
```
{
    "name": "노선A",
    "courses": [
        {"name": "정류장A", "order":1},
        {"name": "정류장B", "order":2},
        {"name": "정류장C", "order":3},
        {"name": "정류장D", "order":4}
    ]
}
```

2. 노선 전체목록 조회(GET): http://127.0.0.1:8000/api/Route/
3. 노선 상세 조회(GET) : http://127.0.0.1:8000/api/Route/1
4. 노선 수정(PUT) : http://127.0.0.1:8000/api/Route
```
{
    "id": 1,
    "name": "노선C"
}
```
5. 노선 삭제(DELETE) : http://127.0.0.1:8000/api/Route/1
