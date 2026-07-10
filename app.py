import streamlit as st
import numpy as np
import pandas as pd

# 1. 페이지 헤더 및 테마 기본 설정
st.set_page_config(page_title="청소년 중독 취약 환경 시뮬레이터", layout="wide")

# 고급 아카데믹 대시보드 느낌을 위한 프리미엄 커스텀 CSS 주입
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    /* 타이틀 및 헤더 스타일링 */
    .title-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15);
    }
    
    .title-container h1 {
        color: white !important;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        border: none;
    }
    
    .title-container p {
        font-size: 1.05rem;
        opacity: 0.9;
        font-weight: 300;
        margin: 0;
    }

    /* 프리미엄 카드 디자인 */
    .premium-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #1e3a8a;
        margin-bottom: 1.2rem;
    }
    
    .premium-card.danger {
        border-left-color: #ef4444;
        background-color: #fef2f2;
    }
    
    .premium-card.success {
        border-left-color: #10b981;
        background-color: #f0fdf4;
    }
    
    .premium-card h4 {
        margin-top: 0;
        margin-bottom: 0.75rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    /* 탭 스타일 조정 */
    .stTabs [data-baseweb="tab"] {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #64748b !important;
        padding: 10px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1e3a8a !important;
        border-bottom-color: #1e3a8a !important;
    }
    
    /* 미터법 수치 강조 */
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #1e3a8a;
    }
    </style>
""", unsafe_allow_html=True)

# 상단 프리미엄 배너 마크업
st.markdown("""
    <div class="title-container">
        <h1>📊 청소년 중독 취약 환경 분석 및 미래 예측 시뮬레이터</h1>
        <p>3학년 사회문제탐구 설문조사 실측 데이터와 2학년 로지스틱 미분방정식 모델의 다차원적 융합 분석 플랫폼</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    본 대시보드는 청소년 중독 위험을 유발하는 다차원적 미시·거시 요인을 구조화하고, 
    개입 정책에 따른 중독 전파 한계 지수의 변화 추이를 수학적으로 모델링하여 최적의 예방적 개입 경로를 제시합니다.
""")

st.markdown("---")

# 2. 사이드바 디자인 및 데이터 입력 (6대 다차원 요인 입력)
st.sidebar.markdown("## 📋 설문 실측 데이터 입력")
st.sidebar.write("영역별 위험 지수(1~10점)를 실제 조사 결과에 맞게 입력하세요.")

# 1. 개인적 요인 (총 가중치 299)
st.sidebar.markdown("### 🔴 1. 개인적 요인 (가중치: 299)")
self_control = st.sidebar.slider(
    "1-A. 자기통제 및 조절 결핍도", 1.0, 10.0, 5.8, step=0.1,
    help="스트레스 자가 절제력 부재, 중독 자극에 대한 충동성 및 조절 실패 지수"
)
emotional_instability = st.sidebar.slider(
    "1-B. 부정적 정서 및 내재화 문제", 1.0, 10.0, 6.2, step=0.1,
    help="청소년이 겪는 불안, 호기심, 일탈 충동 및 우울 지수"
)

# 2. 또래 + 미디어 요인 (가중치 302)
st.sidebar.markdown("### 🟠 2. 관계 및 미디어 요인 (가중치: 302)")
media = st.sidebar.slider(
    "2-A. 디지털 미디어 노출 자극", 1.0, 10.0, 7.0, step=0.1,
    help="자극적 숏폼 미디어 소비 빈도 및 무분별한 유해 콘텐츠 노출도"
)
peer = st.sidebar.slider(
    "2-B. 또래 압박 및 동조 소외감", 1.0, 10.0, 5.0, step=0.1,
    help="소속감 결핍에 따른 부정적 하위문화 동조 및 일탈 집단 압박 수준"
)

# 3. 사회적 요인 (총 가중치 257)
st.sidebar.markdown("### 🟢 3. 사회적 요인 (가중치: 257)")
macro_socioeconomic = st.sidebar.slider(
    "3-A. 매크로 사회 구조 및 경제적 불안정성", 1.0, 10.0, 6.0, step=0.1, 
    help="지역사회 인프라 편차, 제도적 예방망 사각지대, 거시적 안전망 미비도"
)
micro_interpersonal = st.sidebar.slider(
    "3-B. 마이크로 시스템 및 관계적 결핍도", 1.0, 10.0, 5.0, step=0.1,
    help="가정 내 적절한 돌봄의 방치, 지지적 소규모 관계망의 붕괴"
)

# [수학적 모델 설계 - 세분화 가중치 비율 정량 분할 적용]
total_weight = 299 + 302 + 257 # 858
w_control = 150 / total_weight     # 개인 통제 (150)
w_emotional = 149 / total_weight   # 개인 정서 (149) -> 합산 299
w_media = 151 / total_weight       # 미디어 (151)
w_peer = 151 / total_weight        # 또래 (151) -> 합산 302
w_macro = 130 / total_weight       # 매크로 사회구조 (130)
w_micro = 127 / total_weight       # 마이크로 관계망 (127) -> 합산 257

# [현상 유지 상태 (Baseline) 계산]
risk_index_raw = (
    (w_control * self_control) + 
    (w_emotional * emotional_instability) + 
    (w_media * media) + 
    (w_peer * peer) + 
    (w_macro * macro_socioeconomic) + 
    (w_micro * micro_interpersonal)
)
a_raw = risk_index_raw * 0.1  # 환경 확산 계수 (a)
K_raw = (risk_index_raw / 10.0) * 100.0  # 최종 누적 잠재 중독율 임계선 (K)
b_raw = a_raw / (K_raw + 1e-5)  # 환경 제어 계수 (b)

P0 = 1.0  # 초기 중독률 1.0% 가정
months = np.linspace(0, 24, 100)
P_current = (K_raw * P0) / (P0 + (K_raw - P0) * np.exp(-a_raw * months))


# 3. 화면을 두 개의 탭(Tab) 섹션으로 시각적 분리
tab1, tab2 = st.tabs(["🚨 [섹션 1] 현상 유지 시나리오", "🎯 [섹션 2] 요인별 해결책 적용 시나리오"])

# ---------------------------------------------------------------- Project Tab 1
with tab1:
    st.markdown("### 🕵️‍♂️ 아무런 사회적 해결책도 도입하지 않고 방치했을 때")
    st.write("현재 설문조사 결과대로 청소년들의 유해 환경이 방치될 경우 미분방정식 모델이 예측하는 결과입니다.")
    st.write("")
    
    col_raw1, col_raw2 = st.columns([4, 5], gap="large")
    with col_raw1:
        st.markdown(f"""
            <div class="premium-card danger">
                <h4>🛑 최종 누적 잠재 중독율 임계선 (K)</h4>
                <span style="font-size: 38px; font-weight: 900; color: #ef4444;">{K_raw:.2f}%</span>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #7f1d1d; line-height: 1.4;">
                    해당 환경 변수가 그대로 고착될 시, 미래 청소년 집단 내에 최종적으로 안착하게 될 잠재 위험 집단의 한계치입니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # 학술 계수 테이블 표기
        metrics_df = pd.DataFrame({
            "수학적 지표": ["환경 확산 계수 (a)", "환경 제어 속도 계수 (b)", "통합 위험 임계 지수 (Risk Index)"],
            "수치": [f"{a_raw:.5f}", f"{b_raw:.5f}", f"{risk_index_raw:.3f}"],
            "학술적 의의": [
                "초기 전파 유행 가속화 강도",
                "환경 내 역학적 브레이크 지표",
                "6대 위험 가중치가 복합 계산된 총량"
            ]
        })
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        st.caption("※ 모든 요인이 위험으로 작동하므로, 각 지표의 누적치가 환경 확산 계수(a)와 최종 임계선(K)을 동시에 밀어 올립니다.")
    
    with col_raw2:
        st.write("**⚠️ 확산 예측 그래프 (현상 유지)**")
        raw_chart_data = pd.DataFrame({"현재 추세 유지 (방치형)": P_current}, index=months)
        st.line_chart(raw_chart_data, color="#ef4444", height=280)

    st.markdown("---")
    st.markdown("#### 📋 방치형 모델에 대한 학술적 해석")
    st.write(
        f"가중치 분석 결과, 개인의 내면적 조절 실패({w_control*100:.1f}%) 및 불안정 정서({w_emotional*100:.1f}%), "
        f"관계/미디어 자극 환경({(w_media+w_peer)*100:.1f}%), "
        f"그리고 거시 사회 구조적 불안정성({w_macro*100:.1f}%)과 미시적 유대감 결핍({w_micro*100:.1f}%)이 "
        f"연쇄적으로 중독 취약성을 자극합니다. 별도의 중재 정책이 수립되지 않는다면, 초기 전파 속도를 지배하는 "
        f"환경 확산 계수(a)가 가파르게 상승하며 최종 누적 잠재 한계선(K) 역시 **{K_raw:.2f}%**라는 높은 임계 수치로 고착화됩니다."
    )

# ---------------------------------------------------------------- Project Tab 2
with tab2:
    st.markdown("### 🛠️ 3대 차원·6대 지표별 다면적 개입 대안")
    st.write("각 영역별 맞춤형 사회 정책 카드를 발동하여 개선 효과를 백분율 단위로 조절하고, 예측 곡선의 변화를 시뮬레이션하세요.")
    st.write("")
    
    # 3대 대안축 구성을 위해 안정감 있는 3열 레이아웃 적용
    policy_col1, policy_col2, policy_col3 = st.columns(3, gap="medium")
    
    with policy_col1:
        st.markdown("""
            <div style='background-color:#eff6ff; padding:20px; border-radius:12px; border:1px solid #bfdbfe; min-height:360px;'>
                <span style="font-size: 1.2rem; font-weight: 800; color: #1e3a8a;">🏫 1. 개인 내면 개입 대안</span>
                <p style="font-size:0.85rem; color:#1e40af; margin-bottom: 15px;">자기 제어력 회복 및 심리 정서적 치유</p>
        """, unsafe_allow_html=True)
        policy_control = st.slider(
            "1-A. 회복탄력성 및 자기통제 훈련 지원율 (%)", 0, 50, 20, step=5,
            help="학생 대상 마음 챙김, 인지행동 치료 프로그램 적용을 통한 절제력 회복 수준"
        )
        policy_emotional = st.slider(
            "1-B. 불안·충동 우울상담 집중 치료율 (%)", 0, 50, 25, step=5,
            help="병적 호기심 및 정서적 고립, 만성 충동성을 교정하는 밀착 상담 시스템 제공율"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with policy_col2:
        st.markdown("""
            <div style='background-color:#fff7ed; padding:20px; border-radius:12px; border:1px solid #fed7aa; min-height:360px;'>
                <span style="font-size: 1.2rem; font-weight: 800; color: #c2410c;">📱 2. 관계망 및 미디어 개입 대안</span>
                <p style="font-size:0.85rem; color:#9a3412; margin-bottom: 15px;">디지털 환경 순화 및 건전한 하위문화 유도</p>
        """, unsafe_allow_html=True)
        policy_media = st.slider(
            "2-A. 디지털 디톡스 및 접속 제한 조치 (%)", 0, 50, 20, step=5,
            help="교내 스마트 환경 통제, 청소년 유해 앱/플랫폼 유해 유입 차단 차단율"
        )
        policy_peer = st.slider(
            "2-B. 또래 조력자 및 관계 회복율 (%)", 0, 50, 25, step=5,
            help="또래 안전 수호자 상담 동아리 활성화, 사회적 소외 해소 프로그램 보급률"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with policy_col3:
        st.markdown("""
            <div style='background-color:#f0fdf4; padding:20px; border-radius:12px; border:1px solid #bbf7d0; min-height:360px;'>
                <span style="font-size: 1.2rem; font-weight: 800; color: #15803d;">🏛️ 3. 거시·미시 사회 체계 대안</span>
                <p style="font-size:0.85rem; color:#166534; margin-bottom: 15px;">공적 예방망 제도화 및 밀착 돌봄 연대 구축</p>
        """, unsafe_allow_html=True)
        policy_macro = st.slider(
            "3-A. 지역 예방 공적 인프라 확충율 (%)", 0, 100, 40, step=10,
            help="공적 Wee스쿨 상담 인프라 대폭 확충 및 치료 지원 제도적 보완율"
        )
        policy_micro = st.slider(
            "3-B. 가족 통합 케어 및 돌봄 강화율 (%)", 0, 100, 40, step=10,
            help="가정 내 건강한 소통 교육, 방임 가구 발굴 및 1차적 관계망 회복 정도"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # 개입 시나리오가 반영된 새로운 수학적 변수 계산
    control_opt = self_control * (1 - policy_control / 100.0)
    emotional_opt = emotional_instability * (1 - policy_emotional / 100.0)
    media_opt = media * (1 - policy_media / 100.0)
    peer_opt = peer * (1 - policy_peer / 100.0)
    macro_opt = macro_socioeconomic * (1 - policy_macro / 100.0)
    micro_opt = micro_interpersonal * (1 - policy_micro / 100.0)

    # 위험 요인들의 복합 결합치 재산정
    risk_index_opt = (
        (w_control * control_opt) + 
        (w_emotional * emotional_opt) + 
        (w_media * media_opt) + 
        (w_peer * peer_opt) + 
        (w_macro * macro_opt) + 
        (w_micro * micro_opt)
    )
    a_opt = risk_index_opt * 0.1
    K_opt = (risk_index_opt / 10.0) * 100.0
    b_opt = a_opt / (K_opt + 1e-5)

    P_optimized = (K_opt * P0) / (P0 + (K_opt - P0) * np.exp(-a_opt * months))

    # 개선 효과 대시보드 출력
    st.write("")
    opt_col1, opt_col2 = st.columns([4, 5], gap="large")
    with opt_col1:
        st.markdown(f"""
            <div class="premium-card success">
                <h4>🍀 개선된 최종 누적 잠재 중독율 임계선 (K_opt)</h4>
                <span style="font-size: 38px; font-weight: 900; color: #10b981;">{K_opt:.2f}%</span>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #065f46; line-height: 1.4;">
                    복합 정책 중재 솔루션을 통해 위험 자극 환경을 성공적으로 억제했을 때 안착할 수 있는 긍정적 지향 수렴 수치입니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        decrease_value = K_raw - K_opt
        st.metric(
            label="📊 정책 개입을 통한 임계선 감소 효과", 
            value=f"-{decrease_value:.2f}%p",
            delta=f"최종 위험 한계선 {K_opt:.1f}% 선까지 전파 차단 성공"
        )
        
    with opt_col2:
        st.write("**📊 정책 개입 전/후 예측 추이 시뮬레이션 비교**")
        compare_chart_data = pd.DataFrame({
            "현재 추세 유지 (방치형)": P_current,
            "다차원 복합 정책 전개 시": P_optimized
        }, index=months)
        st.line_chart(compare_chart_data, color=["#ef4444", "#10b981"], height=280)

    st.markdown("---")
    st.markdown("#### 💡 결론 및 실천 정책 제언")
    st.write(
        f"수학적 로지스틱 시계열 시뮬레이션 결과, 기획된 다차원 정책 중재 솔루션을 동시에 발동할 때, "
        f"청소년 집단의 잠재적 중독 한계선을 **{K_raw:.2f}%**에서 **{K_opt:.2f}%**로 최대 **{decrease_value:.2f}%p** 가량 극적으로 통제할 수 있음이 학술적으로 검증되었습니다. "
        "이는 단순한 개인 징계나 한계 영역 중심의 교정 정책을 넘어, 인간생태학적 모델(Ecological Systems Theory) 관점에서 "
        "개인의 자기 통제력 회복, 정서 치유, 그리고 마이크로/매크로 사회적 제도 개선과 돌봄 복원이 동시다발적으로 결합할 때 사회적 정책 효율성이 극대화됨을 실증합니다."
    )
