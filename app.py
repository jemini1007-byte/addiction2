import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Streamlit 클라우드 및 일반 환경에서 깨짐 방지용 기본 폰트 설정)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 1. 페이지 헤더 설정
st.set_page_config(page_title="청소년 중독 취약 환경 시뮬레이터", layout="wide")
st.title("📊 청소년 중독 취약 환경 분석 및 예측 시뮬레이터")
st.write(
    "본 시뮬레이터는 **3학년 사회문제탐구 설문조사 결과**를 기반으로 청소년 중독 환경 변수를 입력받아, "
    "**2학년 때 탐구한 로지스틱 미분방정식 모델**을 통해 미래 중독 확산 추이를 예측하고 사회적 해결책을 제안합니다."
)

st.markdown("---")

# 2. 사이드바 - 설문조사 기반 환경 변수 입력 (3대 조작변인 반영)
st.sidebar.header("📋 설문조사 변수 입력 (Scale: 1 ~ 10)")
st.sidebar.write("실제 설문조사에서 도출된 영역별 평균값을 입력하세요.")

# 개인적 요인 (가중치 299/858 ≈ 34.85%)
st.sidebar.subheader("🔴 1. 개인적 요인 (설문 가중치: 299)")
stress = st.sidebar.slider("학업 및 경쟁 스트레스 지수", 1.0, 10.0, 6.0, step=0.1)

# 또래 + 미디어 요인 (가중치 302/858 ≈ 35.20%)
st.sidebar.subheader("🟠 2. 또래 + 미디어 요인 (설문 가중치: 302)")
media = st.sidebar.slider("미디어 및 SNS 노출 빈도", 1.0, 10.0, 7.0, step=0.1)
peer = st.sidebar.slider("또래 집단 압박 및 소외감", 1.0, 10.0, 5.0, step=0.1)

# 사회적 요인 (가중치 257/858 ≈ 29.95%)
st.sidebar.subheader("🟢 3. 사회적 요인 (설문 가중치: 257)")
education = st.sidebar.slider("교내 예방 교육 및 상담 인프라", 1.0, 10.0, 4.0, step=0.1)
family = st.sidebar.slider("가정 및 사회적 공동체 관심도", 1.0, 10.0, 5.0, step=0.1)

# 3. 모델 수학적 설계 (제민이의 조작변인 비율 299 : 257 : 302 적용)
total_weight = 299 + 257 + 302  # 총 가중치: 858
w_personal = 299 / total_weight     # 약 0.3485
w_social = 257 / total_weight       # 약 0.2995
w_peer_media = 302 / total_weight   # 약 0.3520

# 위험 요인(촉진)과 보호 요인(억제)의 가중치 수식 정의
# 촉진 요인: 개인적 요인(stress) + 또래 및 미디어 요인(media와 peer의 평균값)
risk_index = (w_personal * stress) + (w_peer_media * ((media + peer) / 2.0))
a = risk_index * 0.1  # 확산 계수 (초기 속도)

# 억제 요인: 사회적 요인(education과 family의 평균값)
protection_index = w_social * ((education + family) / 2.0)

# K는 최대 잠재 중독율(%). 위험 요인이 높을수록 100%에 근접하고 보호 요인이 저항력으로 작동
K = (risk_index / (risk_index + 0.8 * protection_index)) * 100 
b = a / (K + 1e-5) # dP/dt = aP - bP^2 수식 유도용 상수 b

# 4. 정책 개입 시나리오 분석 (우리가 제안하는 해결책 효과 예측)
st.subheader("💡 사회적 개입 효과 시뮬레이션 (해결책 적용)")
st.write(
    f"설문 기반 조작변인 영향도 비율인 **개인(스트레스) {w_personal*100:.1f}% : 사회(인프라) {w_social*100:.1f}% : 또래+미디어 {w_peer_media*100:.1f}%**가 "
    "시뮬레이션 가중치 시스템에 직접 결합되어 실시간으로 가동됩니다."
)
col1, col2 = st.columns(2)

with col1:
    st.write("**[해결책 1] 교내 스트레스 완화 프로그램 도입 시 (개인적 요인 개선)**")
    stress_reduction = st.slider("스트레스 감소율 (%)", 0, 50, 20, step=5)
with col2:
    st.write("**[해결책 2] 상담 인프라 및 예방 교육 예산 확충 시 (사회적 요인 개선)**")
    edu_increase = st.slider("상담 및 교육 인프라 강화율 (%)", 0, 100, 40, step=10)

# 해결책이 적용된 새로운 변수 계산 (299:257:302 가중치 비율 유지)
stress_opt = stress * (1 - stress_reduction / 100.0)
edu_opt = education * (1 + edu_increase / 100.0)

risk_index_opt = (w_personal * stress_opt) + (w_peer_media * ((media + peer) / 2.0))
a_opt = risk_index_opt * 0.1
protection_index_opt = w_social * ((edu_opt + family) / 2.0)
K_opt = (risk_index_opt / (risk_index_opt + 0.8 * protection_index_opt)) * 100

# 5. 미분방정식 수치적 해석 (해 구하기)
# 로지스틱 방정식의 해석해: P(t) = (K * P0) / (P0 + (K - P0) * e^(-at))
P0 = 1.0  # 초기 중독률 1.0% 가정
months = np.linspace(0, 24, 100)  # 향후 2년간(24개월)의 추이 예측

P_current = (K * P0) / (P0 + (K - P0) * np.exp(-a * months))
P_optimized = (K_opt * P0) / (P0 + (K_opt - P0) * np.exp(-a_opt * months))

# 6. 화면 출력 및 대시보드 구성
main_col1, main_col2 = st.columns([1, 1])

with main_col1:
    st.subheader("📌 현재 환경 기반 방정식 모델")
    st.latex(r"\frac{dP}{dt} = aP - bP^2")
    st.write(f"- **현재 환경 확산 계수 ($a$):** `{a:.3f}` (중독의 초기 속도)")
    st.write(f"- **현재 환경 제어 계수 ($b$):** `{b:.5f}` (사회의 자연적 억제력)")
    st.info(f"🚨 **현재 환경 방치 시 예상 임계 중독율 ($K = a/b$):** **{K:.1f}%**")

with main_col2:
    st.subheader("🎯 정책 해결책 도입 후 모델")
    st.latex(r"\frac{dP}{dt} = a_{opt}P - b_{opt}P^2")
    st.write(f"- **최적화 확산 계수 ($a_{opt}$):** `{a_opt:.3f}`")
    st.write(f"- **최적화 제어 계수 ($b_{opt}$):** `{(a_opt / (K_opt + 1e-5)):.5f}`")
    st.success(f"❇️ **정책 도입 시 개선된 임계 중독율 ($K_{opt}$):** **{K_opt:.1f}%** (약 **{K - K_opt:.1f}%p 감소** 효과)")

st.markdown("---")
st.subheader("📈 향후 24개월 중독 확산률 예측 추이 비교")

# 데이터프레임 구축 후 라인차트 그리기
chart_data = pd.DataFrame({
    "현재 추세 유지 (방치형)": P_current,
    "해결책 적용 (선제적 예방)": P_optimized
}, index=months)

st.line_chart(chart_data)
st.write("💡 *가로축: 경과 시간(월), 세로축: 잠재적 청소년 중독율 (%)*")

st.markdown("---")
st.subheader("📝 분석 리포트 및 정책 제언")
st.write(
    f"제민이의 실측 설문 조사 데이터 분석 결과, 조작변인 기여율인 **개인(299) : 사회(257) : 또래+미디어(302)** 비율을 시스템 가치로 대입했을 때, "
    f"현 상태 유지 시 청소년 집단의 최대 중독 임계 수치($K$)는 **{K:.1f}%** 수준에 달하는 것으로 예측되었습니다. "
    f"그러나 우리가 고안한 **스트레스 완화 프로그램({stress_reduction}% 감소)** 및 **상담/예방 인프라 확대({edu_increase}% 강화)**를 선제 적용할 경우, "
    f"위험 요인은 대폭 상쇄되고 사회적 보호 장치가 활성화되어 집단 내 중독율 한계선을 최대 **{K_opt:.1f}%** 이하로 고정하여 차단할 수 있음을 수학적으로 규명하였습니다."
)
