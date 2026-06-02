import requests
import pandas as pd

# =========================
# 1. 기본 설정
# =========================
url = "https://openapi.gg.go.kr/TOURESRTINFO"
API_KEY = "b1b149ed62d8472896883b772b062f05"

page_size = 1000
page = 1

all_rows = []

# =========================
# 2. 전체 페이지 수집
# =========================
while True:
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": page,
        "pSize": page_size
    }

    res = requests.get(url, params=params)
    res.raise_for_status()

    data = res.json()

    if "TOURESRTINFO" not in data:
        print("TOURESRTINFO 키가 없습니다.")
        print(data)
        break

    rows = None

    for item in data["TOURESRTINFO"]:
        if isinstance(item, dict) and "row" in item:
            rows = item["row"]
            break

    if not rows:
        print(f"{page}페이지에 데이터가 없습니다. 수집 종료")
        break

    all_rows.extend(rows)

    print(f"{page}페이지 수집 완료: {len(rows)}건")

    if len(rows) < page_size:
        print("마지막 페이지 수집 완료")
        break

    page += 1

# =========================
# 3. 전체 데이터를 DataFrame으로 변환
# =========================
df = pd.DataFrame(all_rows)

print("전체 수집 데이터 수:", len(df))
print("컬럼 목록:")
print(df.columns.tolist())

# 전체 원본 저장
df.to_csv(
    "경기도_관광지정보_전체.csv",
    index=False,
    encoding="utf-8-sig"
)

print("전체 CSV 저장 완료: 경기도_관광지정보_전체.csv")

# =========================
# 4. 경기 북부 지역 목록
# =========================
north_gyeonggi_cities = [
    "고양시",
    "남양주시",
    "파주시",
    "의정부시",
    "양주시",
    "구리시",
    "포천시",
    "동두천시",
    "가평군",
    "연천군"
]

# =========================
# 5. DataFrame에서 경기 북부만 필터링
# =========================
north_df = df[df["SIGUN_NM"].isin(north_gyeonggi_cities)].copy()

print("경기 북부 데이터 수:", len(north_df))
print("경기 북부 포함 시군:")
print(north_df["SIGUN_NM"].unique())

# =========================
# 6. 경기 북부 CSV 저장
# =========================
north_df.to_csv(
    "경기북부_관광지정보.csv",
    index=False,
    encoding="utf-8-sig"
)

print("경기 북부 CSV 저장 완료: 경기북부_관광지정보.csv")