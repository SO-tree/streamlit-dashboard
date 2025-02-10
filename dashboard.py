import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 깃허브에 업로드한 NanumGothic.ttf 폰트 불러오기
font_path = "./NanumGothic.ttf"  # 현재 저장소에 올린 폰트 경로
if os.path.exists(font_path):
    fontprop = fm.FontProperties(fname=font_path)
else:
    st.error("⚠ 폰트 파일을 찾을 수 없습니다. NanumGothic.ttf가 올바르게 업로드되었는지 확인하세요.")
    fontprop = None  # 폰트 없을 경우 대비

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📂 CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ✅ 📊 PVP 매칭 추세 그래프 (폰트 적용)
    st.write("🏆 **PVP 매칭 추세**")
    pvp_data = df[df["이벤트"] == "PVP 매칭 시작"].groupby("날짜").size()

    plt.figure(figsize=(10, 5))
    plt.plot(pvp_data.index, pvp_data.values, marker="o", linestyle="-", color="blue")
    plt.title("PVP 매칭 변화", fontproperties=fontprop)
    plt.xlabel("날짜", fontproperties=fontprop)
    plt.ylabel("횟수", fontproperties=fontprop)
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

    # ✅ 📊 인기 상품 분석 (폰트 적용)
    st.write("🛍 **인기 상품 분석**")
    if "상품 ID" in df.columns:
        top_products = df[df["이벤트"] == "인앱 구매"]["상품 ID"].value_counts().head(3)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(top_products.index, top_products.values, color="purple")
        ax.set_title("인기 상품 분석", fontproperties=fontprop)
        ax.set_xlabel("상품 ID", fontproperties=fontprop)
        ax.set_ylabel("구매 수", fontproperties=fontprop)
        st.pyplot(fig)
    else:
        st.warning("⚠ 데이터에 '상품 ID' 컬럼이 없습니다. CSV 파일을 확인하세요.")
