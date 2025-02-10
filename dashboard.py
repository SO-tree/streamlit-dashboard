import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ NanumGothic 폰트 강제 로드
font_path = "./NanumGothic.ttf"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rc("font", family="NanumGothic")
else:
    st.warning("⚠ NanumGothic 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")

# ✅ 고정된 CSV 데이터 로드 (업로드 없이 바로 실행 가능)
@st.cache_data
def load_data():
    return pd.read_csv("unity_analytics_sample_fixed.csv")

df = load_data()
df["날짜"] = pd.to_datetime(df["날짜"])

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📌 탭 생성
tab1, tab2, tab3 = st.tabs(["📈 마케팅 분석", "🎮 유저 행동 분석", "💰 수익데이터 분석"])

with tab1:
    st.header("📝 마케팅 분석")

    # ✅ 설치 수 분석
    st.subheader("📌 설치 수 분석")
    daily_installs = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()
    weekly_installs = daily_installs.resample("W").sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📌 총 설치 수", value=f"{daily_installs.sum()} 명")
        st.metric(label="📌 일 평균 설치 수", value=f"{daily_installs.mean():.2f} 명")

    # ✅ 그래프 개선 (배경 스타일 추가)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily_installs.index, daily_installs.values, marker="o", linestyle="-", color="royalblue", linewidth=2, markersize=5)
    ax.set_title("📊 일별 설치 수 추세", fontsize=14, fontweight="bold")
    ax.set_xlabel("날짜")
    ax.set_ylabel("설치 수")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

    # ✅ 바 그래프 개선
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(weekly_installs.index, weekly_installs.values, color="green", alpha=0.7, width=4)
    ax.set_title("📊 주간 설치 수", fontsize=14, fontweight="bold")
    ax.set_xlabel("날짜")
    ax.set_ylabel("설치 수")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    # ✅ 유입 경로 분석
    st.subheader("📌 유입 경로 분석")
    channel_data = df[df["이벤트"] == "앱 설치"]["유입 채널"].dropna().value_counts()

    if not channel_data.empty:
        fig, ax = plt.subplots()
        ax.pie(channel_data.values, labels=channel_data.index.astype(str), autopct='%1.1f%%', startangle=90, colors=["skyblue", "lightcoral", "lightgreen"])
        ax.set_title("📊 유입 경로 분석", fontsize=14, fontweight="bold")
        st.pyplot(fig)
    else:
        st.warning("⚠ 유입 경로 데이터가 없습니다.")
