import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ NanumGothic 폰트 적용 (GitHub에 업로드된 폰트 사용)
font_path = "./NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📂 CSV 파일 업로드
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

        # ✅ 회원가입 완료율 (위클리)
        installs = df[df["이벤트"] == "앱 설치"].groupby("날짜").size()
        signups = df[df["이벤트"] == "회원가입 완료"].groupby("날짜").size()
        weekly_signup_rate = (signups.resample("W").sum() / installs.resample("W").sum()).fillna(0) * 100
        
        st.subheader("📌 회원가입 완료율")
        st.line_chart(weekly_signup_rate, use_container_width=True)
    
    with tab2:
        st.header("🎮 유저 행동 분석")
        
        # ✅ 서브 콘텐츠 참여율
        sub_contents = ["PVP 참여", "보급 참여", "미니게임 참여", "스텔라인 참여", "서브콘텐츠 없음"]
        sub_data = df[df["이벤트"].isin(sub_contents)]["이벤트"].value_counts()
        
        fig, ax = plt.subplots()
        ax.pie(sub_data, labels=sub_data.index, autopct='%1.1f%%', startangle=90, fontproperties=fontprop)
        ax.set_title("서브 콘텐츠 참여율", fontproperties=fontprop)
        st.pyplot(fig)
    
    with tab3:
        st.header("💰 수익데이터 분석")
        
        # ✅ ARPU & ARPPU
        total_revenue = df["결제 금액"].sum()
        paying_users = df[df["결제 금액"].notna()]["유저 ID"].nunique()
        total_users = df["유저 ID"].nunique()
        
        arpu = total_revenue / total_users
        arppu = total_revenue / paying_users if paying_users > 0 else 0
        
        st.metric("ARPU", f"{arpu:,.0f} KRW")
        st.metric("ARPPU", f"{arppu:,.0f} KRW")
        
        # ✅ 가장 많이 팔린 제품 TOP3
        top_products = df[df["이벤트"] == "인앱 구매"]["구매한 상품"].value_counts().head(3)
        
        fig, ax = plt.subplots()
        ax.bar(top_products.index, top_products.values, color="purple")
        ax.set_title("인기 상품 분석", fontproperties=fontprop)
        ax.set_xlabel("상품 ID", fontproperties=fontprop)
        ax.set_ylabel("구매 수", fontproperties=fontprop)
        ax.set_xticklabels(top_products.index, fontproperties=fontprop)
        st.pyplot(fig)
