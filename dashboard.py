
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 스크립트 파일의 위치를 기준으로 파일 경로를 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "unity_analytics_sample_final.xlsx")
st.write(f"📂 파일 경로: `{file_path}`")

if not os.path.exists(file_path):
    st.error("❌ 데이터 파일을 찾을 수 없습니다. 파일 위치를 확인해주세요!")
    st.stop()


file_path = os.path.abspath("unity_analytics_sample_final.xlsx")
st.write(f"📂 파일 경로: `{file_path}`")

if not os.path.exists(file_path):
    st.error("❌ 데이터 파일을 찾을 수 없습니다. 파일 위치를 확인해주세요!")
    st.stop()

df = pd.read_excel(file_path)

st.cache_data.clear()  # 캐시 초기화


# ✅ NanumGothic 폰트 강제 로드
font_path = "./NanumGothic.ttf"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rc("font", family="NanumGothic")
else:
    st.warning("⚠ NanumGothic 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")

# ✅ 데이터 로드 함수 (엑셀 지원)
@st.cache_data
def load_data():
    file_path = "unity_analytics_sample_final.xlsx"  # Excel 파일 경로
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        st.error("⚠ 데이터 파일을 찾을 수 없습니다. 올바른 파일을 업로드하세요.")
        return pd.DataFrame()


df = load_data()
if df.empty:
    st.stop()

df.columns = df.columns.str.strip()  # 컬럼명 공백 제거

df["날짜"] = pd.to_datetime(df["날짜"])

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📌 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["1. 대시보드 요약", "2. 마케팅 분석", "3. 유저 행동 분석", "4. 수익데이터 분석"])

# ✅ 대시보드 요약
total_installs = df[df["이벤트"] == "앱 설치"].shape[0]
total_signups = df[df["이벤트"] == "회원가입 완료"].shape[0]
total_payers = df[df["결제 금액"].notna()]["유저 ID"].nunique()
total_revenue = df["결제 금액"].sum()

daily_installs = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()

total_active_users = df["유저 ID"].nunique()

total_ad_clicks = df[df["이벤트"] == "광고 클릭"].shape[0]

total_sessions = df.shape[0]

with tab1:
    st.header("📊 대시보드 요약")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📱 설치 수", total_installs)
    col2.metric("📝 회원가입 수", total_signups)
    col3.metric("💰 과금 유저 수", total_payers)
    col4.metric("📊 총 매출", f"{total_revenue:,.0f} 원")
    
    st.subheader("📈 최근 7일 변화")
    last_7_days = df[df["날짜"] >= df["날짜"].max() - pd.Timedelta(days=7)]
    daily_installs_7d = last_7_days[last_7_days["이벤트"] == "앱 설치"].groupby("날짜").size()
    st.line_chart(daily_installs_7d, use_container_width=True)

# ✅ 마케팅 분석
if total_ad_clicks > 0:
    ad_creatives = df[df["이벤트"] == "광고 클릭"]["광고 소재"].value_counts()
    with tab2:
        st.header("📢 마케팅 분석")
        st.subheader("📌 광고 소재별 성과 비교")
        st.bar_chart(ad_creatives)
else:
    with tab2:
        st.warning("⚠ 광고 클릭 데이터가 없습니다.")

# ✅ 유저 행동 분석
with tab3:
    st.header("🎮 유저 행동 분석")
    tutorial_completion = df[df["이벤트"] == "튜토리얼 완료"].groupby("날짜").size()
    st.subheader("📌 튜토리얼 완료율")
    st.line_chart(tutorial_completion, use_container_width=True)

    session_lengths = df["플레이 시간"].dropna()
    if not session_lengths.empty:
        st.subheader("📌 평균 세션 길이")
        st.histogram(session_lengths, bins=10, use_container_width=True)

# ✅ 수익 데이터 분석
arpu = total_revenue / total_active_users if total_active_users > 0 else 0
arppu = total_revenue / total_payers if total_payers > 0 else 0

with tab4:
    st.header("💰 수익 데이터 분석")
    col1, col2 = st.columns(2)
    col1.metric("💵 ARPU", f"{arpu:,.0f} 원")
    col2.metric("💰 ARPPU", f"{arppu:,.0f} 원")
    
    revenue_by_product = df[df["이벤트"] == "인앱 구매"]["상품 ID"].value_counts().head(3)
    if not revenue_by_product.empty:
        st.subheader("📌 인기 상품 TOP 3")
        st.bar_chart(revenue_by_product)

st.success("✅ 대시보드가 정상적으로 로드되었습니다.")
