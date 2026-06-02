import requests
import csv
import json
import pandas as pd

# --- 설정 값 ---
# DATA.GO.KR 서비스 키
SERVICE_KEY = '79eA4Jw2odSc97bzYRMnACC2TlJMPETbQmcHQaZaabL7xSMIXQzMcM8Q2xNuWGYbDuHWdL6/eTaSLsIWmgdr/A=='

IOS = 'ios'
AND = 'android'
WEB = 'web'
ETC = 'etc'

MOBILE_OS = [IOS, AND, WEB, ETC]
INPUT_FILENAME = "경기북부관광지.csv"
OUTPUT_FILENAME = "detailCommon2.csv"

fieldnames = ['contentid','contenttypeid','title','createdtime','modifiedtime','tel','telname','homepage','firstimage','firstimage2','cpyrhtDivCd','areacode','sigungucode','lDongRegnCd','lDongSignguCd','lclsSystm1','lclsSystm2','lclsSystm3','cat1','cat2','cat3','addr1','addr2','zipcode','mapx','mapy','mlevel','overview']

# ----------------

def fetch_and_convert_to_csv(content_ids):
    """주어진 content_ids 리스트를 사용하여 API를 호출하고 결과를 CSV로 저장합니다."""

    print(f"총 {len(content_ids)}개의 contentId에 대해 API를 호출합니다.")

    all_items = []

    for contentId in content_ids:
        if not contentId:
            continue

        print(f"-> contentId: {contentId} 호출 중...")

        API_URL = f'https://apis.data.go.kr/B551011/KorService2/detailCommon2?MobileOS={MOBILE_OS[3]}&MobileApp=Stay-Sync&_type=json&contentId={contentId}&serviceKey={SERVICE_KEY}'
        
        try:
            # 1. API 호출
            response = requests.get(API_URL)
            response.raise_for_status() # HTTP 에러 체크
            data = response.json()

            # 2. 데이터 추출 (KeyError 발생 가능 지점)
            items = data['response']['body']['items']['item']
            
            if items:
                all_items.extend(items)
                print(f"   -> 성공적으로 {len(items)}개 항목을 가져왔습니다.")
            else:
                print(f"   -> contentId {contentId}에 대한 항목이 없습니다.")

        except requests.exceptions.RequestException as e:
            # 네트워크/HTTP 요청 관련 오류 처리
            print(f"⚠️ contentId {contentId} 호출 중 요청 오류가 발생했습니다: {e}")
            continue
        except KeyError:
            # JSON 응답 구조가 예상과 다를 때 처리
            print(f"🚨 contentId {contentId}의 데이터 구조를 찾을 수 없습니다. API 응답 구조를 확인해 주세요.")
            # 디버깅을 위해 응답 일부 출력 (선택 사항)
            # print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")
            continue
                
    if not all_items:
        print("\n❌ 모든 API 호출에서 유효한 데이터를 가져오지 못했습니다. 저장을 건너뜁니다.")
        return

    print(f"\n✅ 총 {len(all_items)}개의 데이터를 발견했습니다. CSV로 변환합니다...")

    # Pandas를 사용하여 DataFrame을 생성하고 CSV로 저장
    df = pd.DataFrame(all_items)

    # 필요한 필드만 선택하고 순서 맞추기
    df = df.reindex(columns=fieldnames)

    df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')

    print(f"\n🎉 성공적으로 CSV 파일 '{OUTPUT_FILENAME}' 저장이 완료되었습니다.")

if __name__ == "__main__":
    # 1. 경기북부관광지.csv 파일을 읽어 contentid 리스트 추출
    try:
        df_input = pd.read_csv(INPUT_FILENAME)

        # contentid 컬럼이 존재하는지 확인
        if 'contentid' not in df_input.columns:
            print(f"🚨 오류: 입력 파일 '{INPUT_FILENAME}'에 'contentid' 컬럼이 없습니다.")
        else:
            # contentid 값만 리스트로 추출 (NaN 값 제거)
            content_ids = df_input['contentid'].dropna().tolist()

            # 2. 추출된 ID를 사용하여 API 호출 및 CSV 저장 함수 실행
            fetch_and_convert_to_csv(content_ids)

    except FileNotFoundError:
        print(f"🚨 오류: 입력 파일 '{INPUT_FILENAME}'을(를) 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
    except Exception as e:
        print(f"프로그램 실행 중 예상치 못한 오류가 발생했습니다: {e}")
