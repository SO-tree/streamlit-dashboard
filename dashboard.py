import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker

# ✅ 폰트 적용
font_path = "./NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path, size=12)

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📂 CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ✅ 📊 PVP 매칭 추세 그래프 (X축 날짜 조정)
    st.write("🏆 **PVP 매칭 추세**")
    pvp_data = df[df["이벤트"] == "PVP 매칭 시작"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.plot(pvp_data.index, pvp_data.values, marker="o", linestyle="-", color="blue")
    plt.title("PVP 매칭 변화", fontproperties=fontprop)
    plt.xlabel("날짜", fontproperties=fontprop)
    plt.ylabel("횟수", fontproperties=fontprop)
    plt.xticks(rotation=45)  # ✅ 날짜 기울이기
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))  # ✅ 5일 간격으로 날짜 표시
    plt.grid()
    st.pyplot(plt)

    # ✅ 📊 설치 수 추세 그래프 (X축 날짜 조정)
    st.write("🛠 **설치 수 추세**")
    install_data = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.bar(install_data.index, install_data.values, color="green")
    plt.title("설치 수 변화", fontproperties=fontprop)
    plt.xlabel("날짜", fontproperties=fontprop)
    plt.ylabel("설치 수", fontproperties=fontprop)
    plt.xticks(rotation=45)  # ✅ 날짜 기울이기
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))  # ✅ 5일 간격으로 날짜 표시
    plt.grid()
    st.pyplot(plt)
