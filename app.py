import streamlit as st
import numpy as np
import pandas as pd

# 1. 페이지 헤더 설정
st.set_page_config(page_title="청소년 중독 취약 환경 시뮬레이터", layout="wide")
st.title("📊 청소년 중독 취약 환경 분석 및 예측 시뮬레이터")
st.write(
    "본 시뮬레이터는 **3학년 사회문제탐구 설문조사 결과**를 기반으로 청소년 중독 환경 변수를 입력받아, "
    "**2학년 때 탐구한 로지스틱 미분방정식 모델**을 통해 미래 중독 확산 추이를 예측하고 구체적 사회적 해결책을 제안합니다."
)

st.markdown("---")

# 2. 사이드바 - 설문조사 기반 기본 환경 변수 입력 (3대 조작변인 기준 설정)
st.sidebar.header("📋 기초 설문조사 데이터 입력")
st.sidebar.write("실제 설문조사에서 도출된 영역별 평균값(1~10점)을 입력하세요.")

# 개인적 요인 (가중치 299)
st.sidebar.subheader("🔴 1. 개인적 요인 (가중치: 299)")
stress = st.sidebar.slider("학업 및 경쟁 스트레스 지수", 1.0, 10.0, 6.0, step=0.1)

# 또래 + 미디어 요인 (가중치 302)
st.sidebar.subheader("🟠 2. 또래 + 미디어 요인 (가중치: 302)")
media = st.sidebar.slider("미디어 및 SNS 노출 빈도", 1.0, 10.0, 7.0, step=0.1)
peer = st.sidebar.slider("또래 집단 압박 및 소외감", 1.0, 10.0, 5.0, step=0.1)

# 사회적 요인 (가중치 257)
st.sidebar.subheader("🟢 3. 사회적 요인 (가중치: 257)")
education = st.sidebar.slider("교내 예방 교육 및 상담 인프라", 1.0, 10.0, 4.0, step=0.1)
family = st.sidebar.slider("가정 및 사회적 공동체 관심도", 1.0, 10.0, 5.0, step=0.1)

# [수학적 기초 모델 설계]
total_weight = 299 + 257 + 302
w_personal = 299 / total_weight
w_social = 257 / total_weight
w_peer_media = 302 / total_weight

# [현상 유지 상태의 변수 계산]
risk_index_raw = (w_personal * stress) + (w_peer_media * ((media + peer) / 2.0))
a_raw = risk_index_raw * 0.1
protection_index_raw = w_social * ((education + family) / 2.0)
K_raw = (risk_index_raw / (risk_index_raw + 0.8 * protection_index_raw)) * 100

P0 = 1.0  # 초기 중독률 1.0% 가정
months = np.linspace(0, 24, 100)
P_current = (K_raw * P0) / (P0 + (K_raw - P0) * np.exp(-a_raw * months))


# 3. 화면을 두 개의 탭(Tab) 섹션으로 분리
tab1, tab2 = st.tabs(["🚨 [섹션 1] 현상 유지 시나리오", "🎯 [섹션 2] 3대 요인별 해결책 적용 시나리오"])

# ---------------------------------------------------------------- Project Tab 1
with tab1:
    st.subheader("🕵️‍♂️ 아무런 사회적 해결책도 도입하지 않고 방치했을 때")
    st.warning("현재 설문조사 결과대로 청소년들의 환경이 방치될 경우 미분방정식 모델이 예측하는 결과입니다.")
    
    col_raw1, col_raw2 = st.columns([1, 1])
    with col_raw1:
        st.info(f"📈 **최종 누적 잠재 중독율 임계선 (K):** **{K_raw:.1f}%**")
        st.text(f"- 현재 환경 확산 계수 (a): {a_raw:.3f}")
        st.text(f"- 현재 환경 제어 계수 (b): {(a_raw / (K_raw + 1e-5)):.5f}")
    
    with col_raw2:
        st.write("**⚠️ 확산 예측 그래프 (현상 유지)**")
        raw_chart_data = pd.DataFrame({"현재 추세 유지 (방치형)": P_current}, index=months)
        st.line_chart(raw_chart_data, color="#ff4b4b")

    st.markdown("---")
    st.write("📋 **방치형 모델에 대한 학술적 해석:**")
    st.write(
        f"개인적 스트레스 요인({w_personal*100:.1f}%)과 또래/미디어 요인({w_peer_media*100:.1f}%)의 높은 결합 가중치로 인해, "
        f"초기 확산 속도를 뜻하는 확산 계수(a)가 매우 가파르게 상승합니다. 반면 이를 제어할 사회적 요인의 지지력이 상대적으로 낮아 "
        f"집단 내 중독율이 최종적으로 **{K_raw:.1f}%**라는 심각한 수치에 수렴하게 됨을 보여줍니다."
    )

# ---------------------------------------------------------------- Project Tab 2
with tab2:
    st.subheader("🛠️ 3대 조작변인별 구체적 정책 개입")
    st.write("각 요인에 대응하는 구체화된 정책 카드를 조절하여 사회적 변화 폭을 시뮬레이션하세요.")
    
    # 3대 요인별 정책 구체화 슬라이더 배치
    policy_col1, policy_col2, policy_col3 = st.columns(3)
    
    with policy_col1:
        st.markdown("### 🏫 1. 개인적 요인 해결책")
        st.caption("**[Rest-Zone 및 학업 압박 분산 프로그램]**")
        policy_personal = st.slider("개인 스트레스 감소율 (%)", 0, 50, 20, step=5)
        
    with policy_col2:
        st.markdown("### 📱 2. 또래+미디어 요인 해결책")
        st.caption("**[디지털 디톡스 챌린지 및 자치 규약]**")
        policy_peer_media = st.slider("또래 동조 및 노출 통제율 (%)", 0, 50, 25, step=5)
        
    with policy_col3:
        st.markdown("### 🏥 3. 사회적 요인 해결책")
        st.caption("**[Wee클래스 접근성 강화 및 교육 확충]**")
        policy_social = st.slider("상담 및 교육 인프라 강화율 (%)", 0, 100, 40, step=10)

    # 개입 시나리오가 반영된 새로운 수학적 변수 계산 (299:302:257 가중치 적용)
    stress_opt = stress * (1 - policy_personal / 100.0)
    
    media_opt = media * (1 - policy_peer_media / 100.0)
    peer_opt = peer * (1 - policy_peer_media / 100.0)
    
    edu_opt = education * (1 + policy_social / 100.0)
    family_opt = family * (1 + policy_social / 100.0)

    risk_index_opt = (w_personal * stress_opt) + (w_peer_media * ((media_opt + peer_opt) / 2.0))
    a_opt = risk_index_opt * 0.1
    protection_index_opt = w_social * ((edu_opt + family_opt) / 2.0)
    K_opt = (risk_index_opt / (risk_index_opt + 0.8 * protection_index_opt)) * 100

    P_optimized = (K_opt * P0) / (P0 + (K_opt - P0) * np.exp(-a_opt * months))

    # 개선 효과 대시보드 출력
    opt_col1, opt_col2 = st.columns([1, 1])
    with opt_col1:
        st.success(f"❇️ **개선된 임계 중독율 (K_opt):** **{K_opt:.1f}%**")
        st.metric(label="중독 한계선 감소 폭", value=f"-{K_raw - K_opt:.1f}%p")
        st.text(f"- 정책 최적화 확산 계수 (a_opt): {a_opt:.3f}")
        st.text(f"- 정책 최적화 제어 계수 (b_opt): {(a_opt / (K_opt + 1e-5)):.5f}")
        
    with opt_col2:
        st.write("**📊 정책 개입 전/후 예측 추이 비교**")
        compare_chart_data = pd.DataFrame({
            "현재 추세 유지 (방치형)": P_current,
            "3대 해결책 적극 적용": P_optimized
        }, index=months)
        st.line_chart(compare_chart_data)

    st.markdown("---")
    st.subheader("💡 결론 및 실천 정책 제언")
    st.write(
        f"분석 결과, 제민이가 기획한 **3대 정책(스트레스 완화 {policy_personal}%, 미디어 통제 {policy_peer_media}%, 인프라 강화 {policy_social}%)**을 동시 가동할 때, "
        f"청소년 사회의 잠재적 중독 한계선을 **{K_raw:.1f}%**에서 **{K_opt:.1f}%**로 대폭 억제할 수 있음이 수학적 기법으로 검증되었습니다."
    )
    st.info(
        "📝 **발표자 주석:** 이 정량적 시뮬레이션 결과는 우리가 제시한 구체적 대안들(교내 Rest-Zone 설치, 학생회 디지털 디톡스 자치 규약, 모바일 Wee클래스 연동 시스템)이 "
        "단순히 감정적인 주장을 넘어 실제 수학적 제어 시스템상에서 유의미한 위험률 감소를 이끌어낼 수 있다는 명확한 당위성을 입증합니다."
    )
