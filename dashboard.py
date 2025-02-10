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

# ✅ 데이터 캐싱 (다른 사용자도 동일한 데이터 유지 가능)
@st.cache_data
def load_data():
    return pd.read_csv("unity_analytics_sample_fixed.csv")

df = load_data()
df["날짜"] = pd.to_datetime(df["날짜"])

# 📌 Streamlit 대시보드 시작
st.title("📊 Unity Analytics 대시보드")

# 📌 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["1. 대시보드 요약", "2. 마케팅 분석", "3. 유저 행동 분석", "4. 수익데이터 분석"])

# ✅ 모든 탭에서 디자인 개선된 시각화 적용
with tab1:
    st.header("📊 대시보드 요약")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📱 설치 수", df[df["이벤트"] == "앱 설치"].shape[0])
    col2.metric("📝 회원가입 수", df[df["이벤트"] == "회원가입 완료"].shape[0])
    col3.metric("💰 과금 유저 수", df[df["결제 금액"].notna()]["유저 ID"].nunique())
    col4.metric("📊 총 매출", f"{df['결제 금액'].sum():,.0f} 원")
    
    st.subheader("📈 최근 7일 변화")
    last_7_days = df[df["날짜"] >= df["날짜"].max() - pd.Timedelta(days=7)]
    daily_installs = last_7_days[last_7_days["이벤트"] == "앱 설치"].groupby("날짜").size()
    st.line_chart(daily_installs, use_container_width=True)

with tab2:
    st.header("📢 마케팅 분석")

    # ✅ 유입 채널별 성과 분석
    st.subheader("📌 유입 채널별 성과 분석")
    channel_data = df[df["이벤트"] == "앱 설치"]["유입 채널"].dropna().value_counts()

    if not channel_data.empty:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(channel_data.values, labels=channel_data.index, autopct='%1.1f%%', startangle=90, colors=["skyblue", "lightcoral", "lightgreen"])
        ax.set_title("유입 채널 비율")
        st.pyplot(fig)
    else:
        st.warning("⚠ 유입 채널 데이터가 없습니다.")

    # ✅ 광고 ROI 분석 (CPI, ARPU, LTV)
    st.subheader("📌 광고 ROI 분석")
    ad_costs = {"구글": 5000000, "트위터": 3000000, "네이버DA": 2000000}  # 광고비 예시
    installs = df[df["이벤트"] == "앱 설치"]["유입 채널"].value_counts()

    cpi_data = {ch: ad_costs[ch] / installs[ch] if ch in installs else 0 for ch in ad_costs}
    roi_df = pd.DataFrame.from_dict(cpi_data, orient="index", columns=["CPI (₩)"])
    st.dataframe(roi_df.style.format({"CPI (₩)": "{:,.0f}"}))

    # ✅ 광고 소재별 성과 비교 (CTR, 설치율)
    st.subheader("📌 광고 소재별 성과 비교")
    ad_creatives = df[df["이벤트"] == "광고 클릭"]["광고 소재"].value_counts()

    if not ad_creatives.empty:
        st.bar_chart(ad_creatives)
    else:
        st.warning("⚠ 광고 소재 데이터가 없습니다.")

    # ✅ 유입 후 주요 행동 비교 (광고 유입 vs 오가닉)
    st.subheader("📌 유입 후 주요 행동 비교")
    behavior_data = df[df["이벤트"].isin(["튜토리얼 완료", "스테이지 1 클리어"])]
    behavior_by_channel = behavior_data.groupby(["유입 채널", "이벤트"]).size().unstack()

    if not behavior_by_channel.empty:
        st.bar_chart(behavior_by_channel)
    else:
        st.warning("⚠ 유입 후 주요 행동 데이터가 없습니다.")

with tab3:
    st.header("🎮 유저 행동 분석")

    # ✅ 튜토리얼 완료율
    st.subheader("📌 튜토리얼 완료율")
    tutorial_completion = df[df["이벤트"] == "튜토리얼 완료"].groupby("날짜").size()
    st.line_chart(tutorial_completion, use_container_width=True)

    # ✅ 스테이지 1 클리어율
    st.subheader("📌 스테이지 1 클리어율")
    stage1_clear = df[df["이벤트"] == "스테이지 1 클리어"].groupby("날짜").size()
    st.line_chart(stage1_clear, use_container_width=True)

    # ✅ 서브 콘텐츠 참여율 (파이 차트)
    st.subheader("📌 서브 콘텐츠 참여율")
    sub_contents = ["PVP 참여", "보급 참여", "미니게임 참여", "스텔라인 참여", "서브콘텐츠 없음"]
    sub_data = df[df["이벤트"].isin(sub_contents)]["이벤트"].value_counts()

    if not sub_data.empty:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(sub_data.values, labels=sub_data.index.astype(str), autopct='%1.1f%%', startangle=90)
        ax.set_title("서브 콘텐츠 참여율")
        st.pyplot(fig)
    else:
        st.warning("⚠ 서브 콘텐츠 참여 데이터가 없습니다.")

    # ✅ 30분 이상 플레이한 유저 비율
    st.subheader("📌 30분 이상 플레이한 유저 비율")
    long_session_users = df[df["플레이 시간"] >= 30]["유저 ID"].nunique()
    total_users = df["유저 ID"].nunique()
    long_session_rate = (long_session_users / total_users) * 100 if total_users > 0 else 0
    st.metric(label="30분 이상 플레이 비율", value=f"{long_session_rate:.2f}%")

    # ✅ 회원 탈퇴율
    st.subheader("📌 회원 탈퇴율")
    delete_users = df[df["이벤트"] == "회원 탈퇴"].groupby("날짜").size()
    st.line_chart(delete_users, use_container_width=True)

    # ✅ 평균 세션 길이
    st.subheader("📌 평균 세션 길이")
    session_length = df["플레이 시간"]
    st.histogram(session_length, bins=10, use_container_width=True)

# ✅ 게임 재방문율 (D7, D30)
st.subheader("📌 게임 재방문율 (D7, D30)")
total_users = df["유저 ID"].nunique()

if total_users > 0:
    retention_data = {
        "D7": (df[df["리텐션"] == "D7"]["유저 ID"].nunique() / total_users) * 100,
        "D30": (df[df["리텐션"] == "D30"]["유저 ID"].nunique() / total_users) * 100
    }
else:
    retention_data = {"D7": 0, "D30": 0}  # 유저 수가 0이면 0%로 설정

retention_df = pd.DataFrame.from_dict(retention_data, orient="index", columns=["Retention Rate"])
st.bar_chart(retention_df, use_container_width=True)


with tab4:
    st.header("💰 수익 데이터 분석")
    
    col1, col2 = st.columns(2)
    col1.metric("💵 ARPU", f"{df['결제 금액'].sum() / df['유저 ID'].nunique():,.0f} 원")
    col2.metric("💰 ARPPU", f"{df['결제 금액'].sum() / df[df['결제 금액'] > 0]['유저 ID'].nunique():,.0f} 원")

    st.subheader("📌 과금 유저 비율")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([df['유저 ID'].nunique() - df[df['결제 금액'] > 0]['유저 ID'].nunique(), df[df['결제 금액'] > 0]['유저 ID'].nunique()], labels=["무료 유저", "유료 유저"], autopct='%1.1f%%', startangle=90, colors=["lightgray", "gold"])
    ax.set_title("과금 유저 비율")
    st.pyplot(fig)

    st.subheader("📌 광고 시청 수익 기여도")
    col1, col2 = st.columns(2)
    col1.metric("🎥 광고 시청 유저 비율", f"{(df[df['이벤트'] == '광고 시청']['유저 ID'].nunique() / df['유저 ID'].nunique()) * 100:.1f}%")
    col2.metric("👀 유저당 평균 광고 시청 횟수", f"{df[df['이벤트'] == '광고 시청'].shape[0] / df[df['이벤트'] == '광고 시청']['유저 ID'].nunique():.1f} 회")
    
    st.subheader("📌 인기 상품 TOP 3")
    top_products = df[df["이벤트"] == "인앱 구매"]["상품 ID"].value_counts().head(3)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(top_products.index, top_products.values, color=["purple", "blue", "green"])
    ax.set_xlabel("상품 ID")
    ax.set_ylabel("구매 수")
    ax.set_title("인기 상품 분석")
    st.pyplot(fig)
    
    st.subheader("📌 과금 유지율 (Retention)")
    col1, col2 = st.columns(2)
    col1.metric("D7 과금 유지율", f"{(df[(df['날짜'] >= df['날짜'].min() + pd.Timedelta(days=7)) & (df['결제 금액'] > 0)]['유저 ID'].nunique() / df[df['결제 금액'] > 0]['유저 ID'].nunique()) * 100:.1f}%")
    col2.metric("D30 과금 유지율", f"{(df[(df['날짜'] >= df['날짜'].min() + pd.Timedelta(days=30)) & (df['결제 금액'] > 0)]['유저 ID'].nunique() / df[df['결제 금액'] > 0]['유저 ID'].nunique()) * 100:.1f}%")
