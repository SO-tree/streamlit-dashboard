import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 📌 대시보드 제목
st.title("📊 Unity Analytics 대시보드")

# 📂 CSV 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    # 📌 데이터 불러오기
    df = pd.read_csv(uploaded_file)

    # 📌 데이터 미리보기
    st.write("### 데이터 미리보기")
    st.dataframe(df.head())

    # 📌 주요 지표 계산
    total_installs = df[df["이벤트"] == "앱 설치"].shape[0]
    tutorial_completions = df[df["이벤트"] == "튜토리얼 완료"].shape[0]
    pvp_matches = df[df["이벤트"] == "PVP 매칭 시작"].shape[0]

    # 📌 주요 지표 표시
    st.write("### 📈 주요 지표")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 설치 수", total_installs)
    col2.metric("튜토리얼 완료 수", tutorial_completions)
    col3.metric("PVP 매칭 수", pvp_matches)

    # 📊 PVP 매칭 추세 그래프
    st.write("### 🏆 PVP 매칭 추세")
    pvp_data = df[df["이벤트"] == "PVP 매칭 시작"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.plot(pvp_data.index, pvp_data.values, marker="o", linestyle="-", color="blue")
    plt.title("PVP 매칭 변화")
    plt.xlabel("날짜")
    plt.ylabel("매칭 수")
    plt.grid()
    st.pyplot(plt)

    # 📊 설치 수 변화 그래프
    st.write("### 📥 설치 수 추세")
    install_data = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.bar(install_data.index, install_data.values, color="green")
    plt.title("일별 설치 수 변화")
    plt.xlabel("날짜")
    plt.ylabel("설치 수")
    plt.grid()
    st.pyplot(plt)
