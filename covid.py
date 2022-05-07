import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey="boZekjwilAq30T3C6fn8GboYI3OCDnZeP11s2XfYg0QkqbP9+G/nlc6xctjtSMiCryY/4hu290ouse5o2G7cJg=="

#[CODE 1] URL 접속을 요청하고 응답을 받아서 변환한다.
def getRequestUrl(url):    
    req = urllib.request.Request(url)    
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


#[CODE 2] 코로나 확진 현황 서비스의 오픈 API를 사용하여 데이터 요청 URL을 만들고 [CODE 1]의 getRequestUrl(url)을 호출해서 받은 응답 데이터를 반환한다.
def getCovidStatsItem(startCreateDt, endCreateDt):    
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?_type=json&serviceKey=" + ServiceKey   #인증키
    parameters += "&startCreateDt" + startCreateDt
    parameters += "&endCreateDt" + endCreateDt
    url = service_url + parameters
    
    retData = getRequestUrl(url)   #[CODE 1]
    
    if (retData == None):
        return None
    else:
         return json.loads(retData)

#[CODE 3] 수집 기간 동안 일 단위로 [CODE 2]의 getTourismStatsItem()을 호출해 받은 데이터를 리스트로 묶어 반환한다.
def getCovidStatsService(startCreateDt, endCreateDt):
    jsonResult = []
    result = []
    dataEND = "{0}{1:0>2}".format(str(year(endCreateDt)), str(12)) #데이터 끝 초기화
    isDataEnd = 0 #데이터 끝 확인용 flag 초기화    
    
    for year in range(year(startCreateDt), year(endCreateDt)):        
        for month in range(1, 13):
            if(isDataEnd == 1): break #데이터 끝 flag 설정되어있으면 작업 중지.
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))            
            jsonData = getCovidStatsItem(startCreateDt, endCreateDt) #[CODE 2]
            
            if (jsonData['response']['header']['resultMsg'] == 'NORMAL SERVICE.'):               
                # 입력된 범위까지 수집하지 않았지만, 더이상 제공되는 데이터가 없는 마지막 항목인 경우 -------------------
                if jsonData['response']['body']['items'] == '': 
                    isDataEnd = 1 #데이터 끝 flag 설정
                    dataEND = "{0}{1:0>2}".format(str(year), str(month-1))
                    print("데이터 없음.... \n 제공되는 통계 데이터는 %s년 %s월까지입니다."                          
                          %(str(year), str(month-1)))                    
                    break                
                #jsonData를 출력하여 확인......................................................
                print (json.dumps(jsonData, indent=4, 
                         sort_keys=True, ensure_ascii=False))          
                 = jsonData['response']['body']['items']['item']['natKorNm']
                natName = natName.replace(' ', '')
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item']['ed']
                print('[ %s_%s : %s ]' %(natName, yyyymm, num))
                print('----------------------------------------------------------------------')             
                jsonResult.append({'기준일': stateDt, '기준시간': nat_cd, '확진자수': , '사망자수' : , '누적 확진률' : , '등록일시분초' : ,
                                 'yyyymm': yyyymm, 'visit_cnt': num})
                result.append([natName, nat_cd, yyyymm, num])
                
    return (jsonResult, result, natName, ed, dataEND)

#[CODE 0]
def main():
    jsonResult = []
    result = []
    print("코로나 19 현황입니다.")
    startCreateDt = input('검색할 범위의 시작 날짜를 입력하세요 (YYYYMMDD)')
    endCreateDt = input('검색할 범위의 마지막 날짜를 입력하세요 (YYYYMMDD)')
    
    jsonResult, result, natName, ed, dataEND =getTourismStatsService(nat_cd,
                                            ed_cd, nStartYear, nEndYear) #[CODE 3]

    if (natName=='') : #URL 요청은 성공하였지만, 데이터 제공이 안된 경우
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
    else:
        #파일저장 1 : json 파일       
        with open('./%s_%s_%d_%s.json' % (natName, ed, nStartYear, dataEND), 'w', 
                    encoding='utf8') as outfile:
            jsonFile  = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile)
        #파일저장 2 : csv 파일   
        columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
        result_df = pd.DataFrame(result, columns = columns)
        result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND),
                    index=False, encoding='cp949')
    
if __name__ == '__main__':
    main()
