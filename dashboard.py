import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 📌 한글 폰트 설정 추가 (폰트 깨짐 해결)
plt.rcParams['font.family'] = 'NanumGothic'  # 한글 폰트 적용 (Windows: 맑은 고딕, Mac: AppleGothic 등)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스(-) 기호 깨짐 방지

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📂 CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 📊 PVP 매칭 추세 그래프
    st.write("🏆 **PVP 매칭 추세**")
    pvp_data = df[df["이벤트"] == "PVP 매칭 시작"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.plot(pvp_data.index, pvp_data.values, marker="o", linestyle="-", color="blue")
    plt.title("PVP 매칭 변화")
    plt.xlabel("날짜")
    plt.ylabel("횟수")
    plt.grid()
    st.pyplot(plt)
