# README
### 회고

django Template과 session을 이용한 웹 어플리케이션 개발 경험은 있었으나  JWT인증은 처음해 보았고 DRF는 부분적으로 사용하다 전체 비즈니스 로직을 짜 본 것은 처음이었습니다. 이전 작업은 프론트와 백엔드를 동시에 작업한 경우가 대부분이라 백엔드 부분만 작성하는데 조금 어색했던 것 같습니다. 로직을 백엔드에서만 돌아가는 형태로 구성하다보니 프론트에서 간단하게 할 수 있는 부분도 직접 구현하려는 시도를 많이 해서 개발 시간이 더 오래 걸린 것 같습니다. 

1. JWT를 이용하여 access, refresh 토큰을 발급 받아 프론트 state에 저장하고 api 요청 시 header의 bearer에 access토큰을 집어 넣어 인증합니다. access토큰이 만료되면 refresh토큰으로 access토큰을 제 발급 받아 계속 서비스를 이용할 수 있습니다. 
2. 본인의 소비 내역을 확인할 수 있는 CRUD를 구성했습니다. 사용자 외 다른 사람은 볼 수 없기 때문에 JWT인증을 통해 내역을 작성한 사람 외에는 접근 할 수 없습니다. 
3. 단축 URL을 이용하여 개인의 소비 내역에 접근할 수 있도록 구성했습니다. 단축 URL은 랜덤 문자열을 만들고 해당 문자열을 key로 그리고 문서의 PK를 value로 저장, 900초 후에 만료되는 캐시를 만들어 활용했습니다. 





### 작업 플로우 정리 

1. **[완료]** django setting
2. **[완료]** django app 설정
3. **[완료]** django drf 세팅
4. **[완료]** django simple-jwt 설정
5. **[완료]** Redis cache 이용한 임시url 생성 및 만료시간 설정
6. **[미완료]** 데이터베이스 변경(sqlite to mysql 5.7) 및 migration 진행 (django 경우 mysqlclient를 이용하여 database 데이터베이스 세팅이 단순하여 시간 상 진행하지 못함)

### 기능정리
#### user App 
1. 공통 기능 정리    

  2. 이메일 / 비밀번호 입력을 통한 회원가입 

3. 모델 정리 

   1. user :override Django base user model  | 아이템을 사용자와 매칭
   2. amount : INT | 지출 또는 수입 금액을 입력한다. 
   3. note : CHAR | 지출 내역을 기록
   4. createdAt : DATETIME | 생성날짜, 시각
   5. updatedAt : DATETIME | 업데이트 날짜, 시각

4. 세부 기능 정리  

   1. JWTSignupView

      POST: `/accounts/signgup/`

      1. header - None

      2. body - form 

         1. email: 아이디로 사용할 이메일 입력
         2. password: 비밀번호 입력

      3. return status

         1. 200: 계정 생성 성공

            `{'access':'token', 'refresh':'token'}`

         2. 400: 계정 생성 실패

   2. JWTLoginView

      POST: `/accounts/login/`

      1. header - None

      2. body - form 

         1. email: 아이디로 사용할 이메일 입력
         2. password: 비밀번호 입력

      3. return status

         1. 200: 로그인 성공

            `{'access':'token', 'refresh':'token'}`

         2. 400: 로그인 실패 

   3. JWTLogOutView

      POST: `/accounts/logout/`

   4. TokenObtainPairView

      simplejwt built-in class: jwt 발행 시 사용

   5. TokenRefreshView

      simplejwt built-in class: jwt 리프레시 시  사용

   6. TokenVerifyView

      simplejwt built-in class: jwt 검증 시 사용

   

#### checker App 
1. 공통 기능 정리
   1. 로그인한  사용자만 가계부(checker) 기능을 사용할 수 있다. 
   2. 로그인 하지 않고 가계부의 일부 항목은 토큰 발행을 통해 유효한 토큰일 때 사용할 수 있다. 

2. 모델 정리 

   1. pk : INT | PK
   2. amount : INT | 기록한 금액을 입력한다. 
   3. memo : STR | 메모를 입력한다. 
   4. createdAt: datetime | 생성일을 기록한다. 
   5. updatedAt : datetime | 업데이트 날짜를 기록한다. 

3. 세부 기능 정리
   1. ItemListAPIView

      1. GET : /checker/item/

         1. header - access token

         2. body - None

         3. return status

            1. 200: 사용자가 입력한 항목 리스트

               `[{"user":2,"amount":100,"note":"test","createdAt":"2023-01-21T10:49:55.747645"},...]`

            2. 401: 토큰 유효성 검증에 실패한 경우 

            3. 402: 토큰이 만료된 경우 

      2. POST: /checker/item/

         1. header - access token
         2. body - form
            1. user : 사용자 pk
            2. amount : 입출금 금액
            3. note : 항목을 설명하는 노트
         3. return status
            1. 200: 사용자의 새로운 아이템(포스트) 생성
            2. 401: 토큰 유효성 검증에 실패한 경우 
            3. 402: 토큰이 만료된 경우 

   2. ItemDetailAPIView

      1. GET: /checker/item/pk/

         1. header - access token

         2. body - None

         3. return status

            1. 200: 사용자가 작성한 개별 아이템

               `{"user":2,"amount":100,"note":"test","createdAt":"2023-01-21T10:49:55.747645"}`

            2. 401: 토큰 유효성 검증에 실패한 경우 

            3. 402: 토큰이 만료된 경우 

      2. PUT: /checker/item/pk/

         1. header - access token
         2. body - form
            1. user : 사용자 pk
            2. amount : 입출금 금액
            3. note : 항목을 설명하는 노트
         3. return status
            1. 200: 사용자가 선택한 아이템(포스트) 수정
            2. 401: 토큰 유효성 검증에 실패한 경우 
            3. 402: 토큰이 만료된 경우 

      3. DELETE: /checker/item/pk/

         1. header - access token
         2. body - None
         3. return status
            1. 200: 사용자가 선택한 아이템(포스트) 생성
            2. 401: 토큰 유효성 검증에 실패한 경우 
            3. 402: 토큰이 만료된 경우 

   3. ShortenUrlGenerator

      GET: /checker/item/pk/share/

      1. header - access token

      2. body - None
   
      3. return status
   
         1. 200: redis 캐시에 생성된 문자열 
   
            `{ "shortenUrl": "key값"}`
   
         2. 401: 토큰 유효성 검증에 실패한 경우 
   
         3. 402: 토큰이 만료된 경우 
   
   4. ShortenUrl
   
      GET: /checker/shorten/key/
      
      1. header - access token
      
      2. body - None
      
      3. return status
      
         1. 200: 사용자가 선택한 아이템(포스트) 생성
      
            ```
            {
                "user": 2,
                "amount": 100,
                "note": "test",
                "createdAt": "2023-01-21T10:49:55.747645"
            }
            ```
      
         2. 422: url값이 만료된 경우
      
         3. 402: 토큰이 만료된 경우 

