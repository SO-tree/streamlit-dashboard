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

# 📂 CSV 파일 업로드
st.title("📊 Unity Analytics 대시보드")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 📌 탭 생성
    tab1, tab2, tab3 = st.tabs(["1. 마케팅 분석", "2. 유저 행동 분석", "3. 수익데이터 분석"])

    with tab1:
        st.header("📈 마케팅 분석")

        # ✅ 설치 수 (데일리 & 위클리)
        daily_installs = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()
        weekly_installs = daily_installs.resample("W").sum()

        st.subheader("📌 설치 수 분석")
        st.line_chart(daily_installs, use_container_width=True)
        st.bar_chart(weekly_installs, use_container_width=True)

        # ✅ 유입 경로 분석 (파이 차트)
        st.subheader("📌 유입 경로 분석")
        channel_data = df[df["이벤트"] == "앱 설치"]["유입 채널"].dropna().value_counts()

        if not channel_data.empty:
            fig, ax = plt.subplots()
            ax.pie(channel_data.values, labels=channel_data.index.astype(str), autopct='%1.1f%%', startangle=90)
            ax.set_title("유입 경로 분석")
            st.pyplot(fig)
        else:
            st.warning("⚠ 유입 경로 데이터가 없습니다.")

    with tab2:
        st.header("🎮 유저 행동 분석")

        # ✅ 서브 콘텐츠 참여율 (PVP, 보급, 미니게임, 스텔라인, 아무것도 안함)
        sub_contents = ["PVP 참여", "보급 참여", "미니게임 참여", "스텔라인 참여", "서브콘텐츠 없음"]
        sub_data = df[df["이벤트"].isin(sub_contents)]["이벤트"].value_counts()

        if not sub_data.empty:
            fig, ax = plt.subplots()
            ax.pie(sub_data.values, labels=sub_data.index.astype(str), autopct='%1.1f%%', startangle=90)
            ax.set_title("서브 콘텐츠 참여율")
            st.pyplot(fig)
        else:
            st.warning("⚠ 서브 콘텐츠 참여 데이터가 없습니다.")

    with tab3:
        st.header("💰 수익데이터 분석")

        # ✅ 과금 유저 비율 (무료 vs 유료, 파이 차트)
        st.subheader("📌 과금 유저 비율")
        paying_users = df[df["결제 금액"].notna()]["유저 ID"].nunique()
        total_users = df["유저 ID"].nunique()
        free_users = total_users - paying_users
        payment_data = pd.Series([free_users, paying_users], index=["무료 유저", "유료 유저"])

        if not payment_data.empty:
            fig, ax = plt.subplots()
            ax.pie(payment_data.values, labels=payment_data.index.astype(str), autopct='%1.1f%%', startangle=90)
            ax.set_title("과금 유저 비율")
            st.pyplot(fig)
        else:
            st.warning("⚠ 과금 유저 데이터가 없습니다.")
else:
    st.warning("📂 CSV 파일을 업로드해주세요!")
