import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ 직접 폰트 적용
font_path = "./NanumGothic.ttf"  # GitHub에 업로드한 폰트 파일 경로
fontprop = fm.FontProperties(fname=font_path, size=12)

plt.title("PVP 매칭 변화", fontproperties=fontprop)
plt.xlabel("날짜", fontproperties=fontprop)
plt.ylabel("횟수", fontproperties=fontprop)

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
