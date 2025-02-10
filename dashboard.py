import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ 직접 폰트 적용 (GitHub에 업로드한 폰트 사용)
font_path = "./NanumGothic.ttf"  # 저장소에 업로드한 폰트 경로
fontprop = fm.FontProperties(fname=font_path, size=12)

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📂 CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ✅ 📊 PVP 매칭 추세 그래프 (폰트 적용 추가)
    st.write("🏆 **PVP 매칭 추세**")
    pvp_data = df[df["이벤트"] == "PVP 매칭 시작"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.plot(pvp_data.index, pvp_data.values, marker="o", linestyle="-", color="blue")
    plt.title("PVP 매칭 변화", fontproperties=fontprop)
    plt.xlabel("날짜", fontproperties=fontprop)
    plt.ylabel("횟수", fontproperties=fontprop)
    plt.grid()
    st.pyplot(plt)

    # ✅ 📊 설치 수 추세 그래프 (폰트 적용 추가)
    st.write("🛠 **설치 수 추세**")
    install_data = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.bar(install_data.index, install_data.values, color="green")
    plt.title("설치 수 변화", fontproperties=fontprop)
    plt.xlabel("날짜", fontproperties=fontprop)
    plt.ylabel("설치 수", fontproperties=fontprop)
    plt.grid()
    st.pyplot(plt)
