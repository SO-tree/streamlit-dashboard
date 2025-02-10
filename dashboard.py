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

    # ✅ 📌 탭 구성 (마케팅, 유저 행동, 수익 분석)
    tab1, tab2, tab3 = st.tabs(["📢 마케팅 성과", "🎮 유저 행동", "💰 수익 분석"])

    # 📢 **마케팅 성과 탭**
    with tab1:
        st.write("📥 **설치 수 추세 (DAU)**")
        install_data = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()

        plt.figure(figsize=(10, 5))
        plt.bar(install_data.index, install_data.values, color="green")
        plt.title("설치 수 변화", fontproperties=fontprop)
        plt.xlabel("날짜", fontproperties=fontprop)
        plt.ylabel("설치 수", fontproperties=fontprop)
        plt.xticks(rotation=45)
        plt.grid()
        st.pyplot(plt)

        st.write("📌 **유입 경로 비율**")
        source_data = df[df["이벤트"] == "앱 설치"]["유입 채널"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(source_data, labels=source_data.index, autopct="%1.1f%%", startangle=140)
        ax.set_title("유입 경로 분석", fontproperties=fontprop)
        st.pyplot(fig)

    # 🎮 **유저 행동 탭**
    with tab2:
        st.write("📖 **튜토리얼 완료율**")
        tutorial_data = df[df["이벤트"] == "튜토리얼 완료"].groupby("날짜").size()

        plt.figure(figsize=(10, 5))
        plt.plot(tutorial_data.index, tutorial_data.values, marker="o", linestyle="-", color="blue")
        plt.title("튜토리얼 완료율 변화", fontproperties=fontprop)
        plt.xlabel("날짜", fontproperties=fontprop)
        plt.ylabel("완료 수", fontproperties=fontprop)
        plt.xticks(rotation=45)
        plt.grid()
        st.pyplot(plt)

        st.write("🎮 **주요 콘텐츠 참여율 (PVP vs 던전)**")
        content_data = df[df["이벤트"].isin(["PVP 매칭 시작", "던전 시작"])].groupby("이벤트").size()

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(content_data, labels=content_data.index, autopct="%1.1f%%", startangle=140)
        ax.set_title("콘텐츠 참여 분석", fontproperties=fontprop)
        st.pyplot(fig)

    # 💰 **수익 분석 탭**
    with tab3:
        st.write("💰 **과금 유저 비율**")
        paying_users = df[df["이벤트"] == "인앱 구매"]["유저 ID"].nunique()
        total_users = df["유저 ID"].nunique()
        paying_ratio = (paying_users / total_users) * 100

        st.metric(label="과금 유저 비율", value=f"{paying_ratio:.2f}%")

        st.write("🛍 **인기 상품 TOP 3**")
        top_products = df[df["이벤트"] == "인앱 구매"]["상품 ID"].value_counts().head(3)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(top_products.index, top_products.values, color="purple")
        ax.set_title("인기 상품 분석", fontproperties=fontprop)
        ax.set_xlabel("상품 ID", fontproperties=fontprop)
        ax.set_ylabel("구매 수", fontproperties=fontprop)
        st.pyplot(fig)
