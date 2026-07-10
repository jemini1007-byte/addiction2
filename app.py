import streamlit as st
import numpy as np
import pandas as pd

# 1. 페이지 헤더 및 테마 기본 설정
st.set_page_config(page_title="청소년 중독 취약 환경 시뮬레이터", layout="wide")

# 고급스러운 대시보드 느낌을 위한 커스텀 CSS 주입
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #1e3a8a;
        font-family: 'Nanum Square', sans-serif;
        font-weight: 800;
    }
    h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: bold;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        color: #1e3a8a !important;
        border-bottom-color: #1e3a8a !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #10b981;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 청소년 중독 취약 환경 분석 및 예측 시뮬레이터")
st.write(
    "본 시뮬레이터는 **3학년 사회문제탐구 설문조사 결과**를 기반으로 청소년 중독 환경 변수를 입력받아, "
    "**2학년 때 탐구한 로지스틱 미분방정식 모델**을 통해 미래 중독 확산 추이를 예측하고 구체적 사회적 해결책을 제안합니다."
)

st.markdown("---")

# 2. 사이드바 디자인 및 데이터 입력 (3대 조작변인 위험 요소 설정)
st.sidebar.markdown("## 📋 설문 실측 데이터")
st.sidebar.write("영역별 위험 지수(1~10점)를 입력하세요.")

# 개인적 요인 (가중치 299)
st.sidebar.markdown("### 🔴 1. 개인적 요인 (가중치: 299)")
stress = st.sidebar.slider("학업 및 경쟁 스트레스 지수", 1.0, 10.0, 6.0, step=0.1)

# 또래 + 미디어 요인 (가중치 302)
st.sidebar.markdown("### 🟠 2. 또래 + 미디어 요인 (가중치: 302)")
media = st.sidebar.slider("미디어 및 SNS 노출 빈도", 1.0, 10.0, 7.0, step=0.1)
peer = st.sidebar.slider("또래 집단 압박 및 소외감", 1.0, 10.0, 5.0, step=0.1)

# 사회적 요인 (가중치 257)
st.sidebar.markdown("### 🟢 3. 사회적 요인 (가중치: 257)")
education = st.sidebar.slider("교내 예방 교육 및 상담 인프라 부족도", 1.0, 10.0, 6.0, step=0.1)
family = st.sidebar.slider("가정 및 사회적 공동체 방임도", 1.0, 10.0, 5.0, step=0.1)

# [수학적 기초 모델 설계 (3대 요인 가중치 비율 299 : 302 : 257 적용)]
total_weight = 299 + 302 + 257
w_personal = 299 / total_weight
w_peer_media = 302 / total_weight
w_social = 257 / total_weight

# [현상 유지 상태의 위험 지수 및 로지스틱 변수 계산]
risk_index_raw = (w_personal * stress) + (w_peer_media * ((media + peer) / 2.0)) + (w_social * ((education + family) / 2.0))
a_raw = risk_index_raw * 0.1  # 환경 확산 계수 (a)
K_raw = (risk_index_raw / 10.0) * 100.0  # 최종 누적 잠재 중독율 임계선 (K)
b_raw = a_raw / (K_raw + 1e-5)  # 환경 제어 계수 (b)

P0 = 1.0  # 초기 중독률 1.0% 가정
months = np.linspace(0, 24, 100)
P_current = (K_raw * P0) / (P0 + (K_raw - P0) * np.exp(-a_raw * months))


# 3. 화면을 두 개의 탭(Tab) 섹션으로 시각적 분리
tab1, tab2 = st.tabs(["🚨 [섹션 1] 현상 유지 시나리오", "🎯 [섹션 2] 3대 요인별 해결책 적용 시나리오"])

# ---------------------------------------------------------------- Project Tab 1
with tab1:
    st.subheader("🕵️‍♂️ 아무런 사회적 해결책도 도입하지 않고 방치했을 때")
    st.warning("현재 설문조사 결과대로 청소년들의 환경이 방치될 경우 미분방정식 모델이 예측하는 결과입니다.")
    
    col_raw1, col_raw2 = st.columns([1, 1])
    with col_raw1:
        st.markdown(f"<div style='padding:20px; background-color:#fff5f5; border-left:6px solid #e53e3e; border-radius:4px;'>"
                    f"<h4>🛑 최종 누적 잠재 중독율 임계선 (K): <b>{K_raw:.1f}%</b></h4></div>", unsafe_allow_html=True)
        st.write("")
        st.text(f"• 환경 확산 계수 (a): {a_raw:.5f}")
        st.text(f"• 환경 제어 계수 (b): {b_raw:.5f}")
        st.caption("※ 모든 요인이 위험 요인으로 작동하므로, 세 가지 지표의 누적치가 환경 확산 계수(a)와 최종 수렴 한계선인 임계선(K)을 동시에 밀어 올립니다.")
    
    with col_raw2:
        st.write("**⚠️ 확산 예측 그래프 (현상 유지)**")
        raw_chart_data = pd.DataFrame({"현재 추세 유지 (방치형)": P_current}, index=months)
        st.line_chart(raw_chart_data, color="#ff4b4b")

    st.markdown("---")
    st.markdown("#### 📋 방치형 모델에 대한 학술적 해석")
    st.write(
        f"개인적 스트레스 요인({w_personal*100:.1f}%), 또래/미디어 요인({w_peer_media*100:.1f}%), 그리고 사회적 인프라 결핍 및 방임 요인({w_social*100:.1f}%)이 "
        f"모두 위험 요인으로서 동일 선상에서 중독 취약성을 자극하고 있습니다. 이에 따라 복합 위험 지수가 유의미하게 상승하여, "
        f"초기 확산 속도를 지배하는 환경 확산 계수(a)가 가파르게 형성되며, 최종 수렴치인 최종 누적 잠재 중독율 임계선(K) 역시 **{K_raw:.1f}%**라는 높은 수준으로 고착화됩니다."
    )

# ---------------------------------------------------------------- Project Tab 2
with tab2:
    st.subheader("🛠️ 3대 조작변인별 구체적 정책 개입")
    st.write("각 요인의 위험도를 낮추기 위해 기획된 구체화된 정책 카드를 조절하여 변화 폭을 시뮬레이션하세요.")
    
    # 3대 요인별 정책 구체화 슬라이더 배치
    policy_col1, policy_col2, policy_col3 = st.columns(3)
    
    with policy_col1:
        st.markdown("<div style='background-color:#eff6ff; padding:15px; border-radius:8px; border:1px solid #bfdbfe;'>", unsafe_allow_html=True)
        st.markdown("### 🏫 1. 개인적 요인 대안")
        st.caption("**[Rest-Zone 및 학업 압박 분산]**")
        policy_personal = st.slider("개인 스트레스 감소율 (%)", 0, 50, 20, step=5)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with policy_col2:
        st.markdown("<div style='background-color:#fff7ed; padding:15px; border-radius:8px; border:1px solid #fed7aa;'>", unsafe_allow_html=True)
        st.markdown("### 📱 2. 또래+미디어 대안")
        st.caption("**[디지털 디톡스 및 자치 규약]**")
        policy_peer_media = st.slider("또래 동조 및 노출 통제율 (%)", 0, 50, 25, step=5)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with policy_col3:
        st.markdown("<div style='background-color:#f0fdf4; padding:15px; border-radius:8px; border:1px solid #bbf7d0;'>", unsafe_allow_html=True)
        st.markdown("### 🏥 3. 사회적 요인 대안")
        st.caption("**[Wee클래스 인프라 확충]**")
        policy_social = st.slider("사회적 위험 요인 개선율 (%)", 0, 100, 40, step=10)
        st.markdown("</div>", unsafe_allow_html=True)

    # 개입 시나리오가 반영된 새로운 수학적 변수 계산
    stress_opt = stress * (1 - policy_personal / 100.0)
    media_opt = media * (1 - policy_peer_media / 100.0)
    peer_opt = peer * (1 - policy_peer_media / 100.0)
    edu_opt = education * (1 - policy_social / 100.0)
    family_opt = family * (1 - policy_social / 100.0)

    # 위험 요인들의 결합치 계산
    risk_index_opt = (w_personal * stress_opt) + (w_peer_media * ((media_opt + peer_opt) / 2.0)) + (w_social * ((edu_opt + family_opt) / 2.0))
    a_opt = risk_index_opt * 0.1
    K_opt = (risk_index_opt / 10.0) * 100.0
    b_opt = a_opt / (K_opt + 1e-5)

    P_optimized = (K_opt * P0) / (P0 + (K_opt - P0) * np.exp(-a_opt * months))

    # 개선 효과 대시보드 출력
    st.write("")
    opt_col1, opt_col2 = st.columns([1, 1])
    with opt_col1:
        st.markdown(f"<div style='padding:20px; background-color:#f0fdf4; border-left:6px solid #16a34a; border-radius:4px;'>"
                    f"<h4>🍀 개선된 최종 누적 잠재 중독율 임계선 (K_opt): <b>{K_opt:.1f}%</b></h4></div>", unsafe_allow_html=True)
        st.write("")
        st.text(f"• 최적화 환경 확산 계수 (a_opt): {a_opt:.5f}")
        st.text(f"• 최적화 환경 제어 계수 (b_opt): {b_opt:.5f}")
        
        decrease_value = K_raw - K_opt
        st.metric(label="📊 정책 개입을 통한 임계선 감소 폭", value=f"-{decrease_value:.1f}%p")
        
    with opt_col2:
        st.write("**📊 정책 개입 전/후 예측 추이 비교**")
        compare_chart_data = pd.DataFrame({
            "현재 추세 유지 (방치형)": P_current,
            "3대 해결책 적극 적용": P_optimized
        }, index=months)
        st.line_chart(compare_chart_data)

    st.markdown("---")
    st.markdown("#### 💡 결론 및 실천 정책 제언")
    st.write(
        f"분석 결과, 기획된 **3대 정책(스트레스 완화 {policy_personal}%, 미디어 통제 {policy_peer_media}%, 사회적 인프라 결핍 보완 {policy_social}%)**을 동시 가동할 때, "
        f"청소년 사회의 잠재적 중독 한계선을 **{K_raw:.1f}%**에서 **{K_opt:.1f}%**로 대폭 억제할 수 있음이 수학적 기법으로 검증되었습니다. "
        "이는 위험 요인으로 작동하던 사회적 결핍 환경을 정책 개입을 통해 정량적으로 상쇄 및 통제함으로써 실현 가능한 실천적 대안임을 시사합니다."
    )
