import pandas as pd

try:
    df = pd.read_csv('areaBasedList2.csv')
except FileNotFoundError:
    print("Error: areaBasedList2.csv 파일을 찾을 수 없습니다.")
    exit()

target_areas = [
    '고양시', '파주시', '의정부시', '양주시', '동두천시',
    '포천시', '연천군', '가평군', '남양주시', '구리시'
]

if 'addr1' in df.columns:
    filter_condition = df['addr1'].str.contains('|'.join(target_areas), na=False)

    df_filtered = df[filter_condition]
    df_filtered.to_csv('경기북부관광지.csv', index=False, encoding='utf-8-sig')
    print("필터링된 데이터가 '경기북부관광지.csv' 파일로 성공적으로 저장되었습니다.")
else:
    print("오류: 데이터프레임에 'addr1' 컬럼이 존재하지 않습니다. 컬럼 이름을 확인해주세요.")