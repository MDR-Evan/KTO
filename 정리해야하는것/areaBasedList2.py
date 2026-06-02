import requests
import csv
import json

# --- 설정 값 ---
# DATA.GO.KR 서비스 키
SERVICE_KEY = '79eA4Jw2odSc97bzYRMnACC2TlJMPETbQmcHQaZaabL7xSMIXQzMcM8Q2xNuWGYbDuHWdL6/eTaSLsIWmgdr/A=='

IOS = 'ios'
AND = 'android'
WEB = 'web'
ETC = 'etc'

MOBILE_OS = [IOS, AND, WEB, ETC]
# areaBasedList2 API URL (지역기반 관광정보조회)
API_URL = f'https://apis.data.go.kr/B551011/KorService2/areaBasedList2?numOfRows=9712&MobileOS={MOBILE_OS[3]}&MobileApp=Stay-Sync&_type=json&serviceKey={SERVICE_KEY}&lDongRegnCd=41'
OUTPUT_FILENAME = input("출력 파일명을 입력하세요 (확장자 포함): ")

# /areaBasedList2 지역기반 관광정보조회 API 필드명
fieldnames = ['addr1', 'addr2', 'areacode', 'cat1', 'cat2', 'cat3', 'contentid', 'contenttypeid', 'createdtime', 'firstimage', 'firstimage2', 'cpyrhtDivCd', 'mapx', 'mapy', 'mlevel', 'modifiedtime', 'sigungucode', 'tel', 'title', 'zipcode', 'lDongRegnCd', 'lDongSignguCd', 'lclsSystm1', 'lclsSystm2', 'lclsSystm3']
# ----------------

def fetch_and_convert_to_csv(url, filename):
    print("API를 호출하고 데이터를 가져오는 중...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 호출 중 오류가 발생했습니다: {e}")
        return

    try:
        items = data['response']['body']['items']['item']
    except KeyError:
        print("🚨 데이터 구조를 찾을 수 없습니다. API 응답 구조를 확인해 주세요.")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if not items:
        print("저장할 데이터 항목이 없습니다.")
        return

    print(f"총 {len(items)}개의 데이터를 발견했습니다. CSV로 변환합니다...")

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for item in items:
            # 선언된 fieldnames를 사용하여 item의 데이터를 row에 매핑합니다.
            row = {field: item.get(field, '') for field in fieldnames}
            writer.writerow(row)

    print(f"\n✅ 성공적으로 CSV 파일 '{filename}' 저장이 완료되었습니다.")

if __name__ == "__main__":
    fetch_and_convert_to_csv(API_URL, OUTPUT_FILENAME)