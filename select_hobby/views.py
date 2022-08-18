from unicodedata import category
from django.shortcuts import render, redirect
import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from django.utils import timezone
from .models import your_hobby
from .serializers import your_hobbySerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    # hobbys=your_hobby.objects.all()
    return render(request, 'index.html')

def  recommend(request):
    return render(request, 'recommend.html')
@csrf_exempt
def create(request):
    #MBTI 별 취미 리스트 1개 만들기
    #각 카테고리별 취미 딕셔너리 만들기
    #각 취미별 딕셔너리 만들기
    # 프론트에서 첫번째로 MBTI  값을 받아오면 해당 MBTI에 맞는 값을 받아서 파이썬 numpy 배열에 값을 저장
    # 그 후 두번째 사용자에게 입력받은 값과 빼서 가장 가까운 취미를 추천
    MBTI_dic={
    'INFJ':['스쿼시','수영','러닝','사이클','마라톤','등산','요가','웨이트','탁구','배드민턴','테니스','골프','승마','피아노','기타','드럼','서예','작사','음악 감상','영화 감상,','뮤지컬 감상','전시회','독서','사진촬영','산책','여행','드라이브','차 마시기','블로그','일기쓰기','재능기부'],
    "INTJ":['스쿼시','웨이트','마라톤','등산','클라이밍','스키','보드','서핑','수상스키','피아노','드럼','기타','작곡 배우기','드로잉','보컬 트레이닝','요리','베이킹','전문서적읽기','홈인테리어','외국어공부','컴퓨터게임','모바일게임','방탈출'],
    'INFP':['스쿼시','클라이밍','골프','승마','스키','보드','수상스키','서핑','플룻','첼로','클라리넷','젬베','작곡','드로잉','작사','보컬','디제잉','댄스','요리','베이킹','독서','사진촬영','영화감상','음악감상','뮤지컬감상','전시회','엑세서리 만들기','외국어공부','블로그','캠핑','방탈출'],
    'INTP':['스쿼시','웨이트','롱보드','피아노','가야금','독서','사진촬영','컴퓨터게임','모바일게임','방탈출'],
    'ESTJ':['웨이트','클라이밍','테니스','대금 연주','클래식 공연 관람 동호회','외국어공부','목공방에서 가구 만들기','베이킹'],
    'ESTP':['서핑','레이싱','복싱','스카이다이빙','드렁','일렉 기타','캠핑','페스티벌 즐기기','추리 소설 읽기'],
    'ESFP':['컴퓨터게임','유도','스쿼시','마술','방구석 콘서트 열기','홈 인테리어'],
    'ENFJ':['요가','댄스','봉사활동' '본질에 대해 토론하기','독서 모임','철학 책 읽기','영화관람'],
    'ISTJ':['웨이트','사이클','마라톤','탁구','피아노','드럼','뜨개질','십자수','요리','베이킹'],
    'ISFJ':['스키','보드','피아노','작곡','홈 인테리어','뮤지컬 감상','영화 감상','쇼핑','컴퓨터게임','모바일 게임','독서'],
    'ISTP':['사이클','축구','야구','피아노','기타','드럼','여행','드라이브','베이킹'],
    'ISFP':['웨이트','축구','야구','피아노','기타','작곡','여행','드라이브','요리','베이킹','십자수'],
    'ESFJ':['축구','야구','농구','크로스핏','댄스','캠핑','여행','자원봉사','차 마시기'],
    'ENFP':['클라이밍','승마','서핑','수상스키','탁구','배드민턴','테니스','스쿼시','드로잉','디제잉','독서','드라이브','음악감상','영화감상','전시회','뮤지컬관람'],
    'ENTP':['클라이밍','서핑','수상스키','스쿼시','크로스핏','복싱','드로잉','서예','독서','전시회','여행','드라이브'],
    'ENTJ':['웨이트','필라테스','요가','축구','야구','배드민턴','피아노','드럼','기타','디제잉','홈 인테리어','컴퓨터게임','방탈출',''],
    }
    
    hobby={'스쿼시':[55,21,49],
           '수영':[27,20,15],
           '러닝':[25,95,14],
           '웨이트':[36,19,48],
           '마라톤':[61,100,15],
           '클라이밍':[52,50,30],
           '골프':[73,69,12],
           '롱보드':[72,92,10],
           '테니스':[81,76,24],
           '서핑':[32,100,0],
           '레이싱':[80,100,8],
           '피아노':[5,8,50],
           '복싱':[59,25,60],
           '컴퓨터게임':[77,0,50],
           '유도':[84,24,45],
           '요가':[48,25,47],
           '댄스':[50,40,45],
           '사이클':[49,99,17],
           '스키':[32,100,100],
           '보드':[35,100,100],
           '축구':[97,96,28],
           '야구':[99,96,28],
           '농구':[85,50,60],
           '승마':[29,94,26],
           '수상스키':[23,100,5],
           '필라테스':[40,17,53],
           '배구' :[83,19,62],
           '탁구' :[80,15,48],
           '족구' :[82,66,23],
           '배드민턴' :[81,25,30],
           '크로스핏' :[87,22,51],
           '등산' :[50,100,10],
           '태권도' :[82,26,48],
           '합기도' :[84,25,49],
           '검도' :[81,27,50],
           '주짓수' :[86,22,46],
           '에어로빅' :[87,50,45],
           '드럼' :[28,15,52],
           '기타' :[15,18,51],
           '디제잉' :[61,6,45],
           '작곡' :[2,8,49],
           '드로잉' :[1,42,53],
           '서예' :[0,11,52],
           '작사' :[3,26,51],
           '보컬' :[17,9,48],
           '플룻연주' :[2,12,51],
           '첼로' :[4,10,52],
           '클라리넷' :[3,11,53],
           '잼베' :[5,14,45],
           '요리' :[26,8,50],
           '베이킹' :[24,6,48],
           '퀄트' :[4,25,54],
           '자수' :[2,23,52],
           '독서' :[1,50,50],
           '사진촬영' :[10,76,43],
           '캠핑' :[55,97,16],
           '여행' :[53,90,45],
           '드라이브' :[47,98,55],
           '모바일게임':[20,50,48],
           '방탈출':[80,5,51],
           '영화감상':[50,22,55],
           '음악감상':[5,20,55],
           '홈인테리어':[3,15,55],
           '맛집탐방':[52,19,57],
           '뮤지컬관람':[55,5,62],
           '전시회투어':[21,10,60],
           '엑세서리 만들기':[4,16,70],
           '클러빙':[90,19,45],
           '외국어 공부':[47,43,50],
           '자원봉사':[75,70,46],
           '차 마시기':[15,25,70],
           '산책':[20,96,40],
           '블로그':[0,0,50],
           '재능기부':[78,50,50],
           '일기쓰기':[0,1,50],
           '전문서적읽기':[3,6,51],
           '목공방에서 가구만들기':[28,7,48],
           '페스티벌 즐기기':[90,98,35],
           '추리소설읽기':[1,16,56],
           '마술':[80,42,57],
           '방구석 콘서트열기':[50,15,50],
           '본질에 대해 토론하기':[83,39,50],
           '철학책 읽기':[2,8,50],
           }
    categorys= {
        '스포츠' : [
            '스쿼시',
            '수영',
            '러닝',
            '웨이트',
            '마라톤',
            '클라이밍',
            '골프',
            '롱보드',
            '테니스',
            '서핑',
            '레이싱',
            '복싱',
            '유도',
            '요가',
            '댄스',
            '사이클',
            '스키',
            '보드',
            '축구',
            '야구',
            '농구',
            '승마',
            '수상스키',
            '필라테스',
            '배구',
            '탁구',
            '족구',
            '배드민턴',
            '크로스핏',
            '등산',
            '태권도',
            '합기도',
            '검도',
            '주짓수',
            '에어로빅',
        ],
        '예술' : [
            '피아노',
            '드럼',
            '기타',
            '디제잉',
            '작곡' ,
            '드로잉',
            '서예',
            '작사',
            '보컬',
            '플룻연주',
            '첼로',
            '클라리넷',
            '잼베',
            ],
        '기타' : [
            '댄스',
            '컴퓨터게임',
            '요리',
            '베이킹',
            '퀄트',
            '자수',
            '독서',
            '사진촬영',
            '캠핑',
            '여행',
            '드라이브',
            '모바일게임',
            '방탈출',
            '영화감상',
            '음악감상',
            '홈인테리어',
            '맛집탐방',
            '뮤지컬관람',
            '전시회투어',
            '엑세서리 만들기',
            '클러빙',
            '외국어 공부',
            '자원봉사',
            '차 마시기',
            '산책',
            '블로그',
            '재능기부',
            '일기쓰기',
            '전문서적읽기',
            '목공방에서 가구만들기',
            '페스티벌 즐기기',
            '추리소설읽기',
            '마술',
            '방구석 콘서트열기',
            '본질에 대해 토론하기',
            '철학책 읽기',
            ],
        '랜덤추천': [],
    }
    hobby_list_point=[]
    if(request.method =='POST'):
        #밑 변수 4개는 프론트에서 json파일의 값을 받아와서 값을 넣어주는곳
        y=your_hobby()
        data=json.load(request)
        y.your_MBTI=data['MBTI']
        y.hobby_category=data['category']
        y.first_point=data['people_number']
        y.second_point=data['inout']
        y.third_point=data['weather']
        print(y.your_MBTI)
        print(y.hobby_category)
        print(y.first_point)
        print(y.second_point)
        print(y.third_point)
        
        # y.your_MBTI=request.POST['MBTI']
        # print(request.POST['MBTI'])
        # y.hobby_category=request.POST['cate']
        # print(y.hobby_category)
        # y.first_point=request.POST['first']  #입력받은숫자1
        # print(y.first_point)
        # #print(type(y.first_point))
        # y.first_point=int(y.first_point)
        # #print(type(y.first_point))
        # y.second_point=request.POST['second'] #입력받은숫자2
        # y.second_point=int(y.second_point)
        # print(y.second_point)
        # #print(type(y.second_point))
        # y.third_point=request.POST['third'] #입력받은숫자3
        # y.third_point=int(y.third_point)
        # print(y.third_point)
        #print(type(y.third_p
        if MBTI_dic.get(y.your_MBTI):
            print('if문 돌아갑니다~')
            print(MBTI_dic[y.your_MBTI])
            L1=MBTI_dic[y.your_MBTI]
            L2=categorys[y.hobby_category]
            if y.hobby_category=="랜덤추천":
                user_hobby_list=MBTI_dic[y.your_MBTI]
            else:
                user_hobby_list=[]
                for i in L1:
                    for j in L2:
                        if i== j:
                            user_hobby_list.append(i)
            #print(MBTI_dic[y.your_MBTI])
            # if y.hobby_category=="랜덤 추천":
            #     user_hobby_list=MBTI_dic[y.your_MBTI] #사용자 MBTI에 맞는 취미 목록 리스트 변수
            # else:
            #     set1=set(MBTI_dic[y.your_MBTI])  # MBTI 취미리스트를 set으로 변환
            #     print(set1)
            #     set2=set(categorys[y.hobby_category]) # 카테고리 취미리스트를 set으로 변환
            #     print(set2)
            #     user_hobby_list=list(set1 & set2) # set1과 set2의 교집합을 user_hobby_list에 담기
            print(user_hobby_list)
        for i in range(len(user_hobby_list)):
            if hobby.get(user_hobby_list[i]):
                # 리스트로 바로 넣으면 오류가 떠서 리스트안에 리스트를 넣을 수 없어서 리스트를 변수로 설정해서 값을 대입
                a=hobby[user_hobby_list[i]]
                hobby_list_point.append(a)
        hobby_list_point=np.array(hobby_list_point) #MBTI에 들어가져있는 취미들의 점수 목록을 numpy 시킴
        # print(hobby_list_point)
        # print(type(hobby_list_point[0][0]))
        # print(y.first_point-hobby_list_point[0][0])
        user_point=np.array([y.first_point,y.second_point,y.third_point])  #사용자에게 입력받은 값
        #print(user_point)
        n=np.linalg.norm(hobby_list_point-user_point,axis=1)
        print(n)
        i= np.argsort(n)[::1][0]
        print(np.argsort(n)[::1])
        print(i)
        y.return_hobby=user_hobby_list[i]
        print(y.return_hobby)
        print(type(y.return_hobby))
        y.save()
        global dic
        dic={}
        dic['return_hobby']=str(y.return_hobby)
        print(dic)
        print(JsonResponse(dic))
    #return dic
    return JsonResponse(dic) #redirect("select_hobby")
    #HTTPresponse