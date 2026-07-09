import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="청소년 중독 및 사회적 개입 시뮬레이션",
    page_icon="🧠",
    layout="wide"
)

# 2. 메인 타이틀
st.title("🧠 청소년 미디어 중독 시뮬레이션 및 정책 개입 효과 분석")
st.write("미분방정식(로지스틱 모델)을 활용하여 사회적 개입에 따른 중독률 변화를 예측합니다.")

st.markdown("---")

# 3. 사이드바 - 기본 매개변수 설정
st.sidebar.header("📊 기본 시뮬레이션 설정")
P0 = st.sidebar.slider("초기 중독률 (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1) / 100.0
months = st.sidebar.slider("예측 기간 (개월)", min_value=6, max_value=36, value=24, step=6)

# 4. 본문 화면 - 두 구역으로 분할 (사용자 개입 입력 칸)
st.subheader("💡 사회적 개입 효과 시뮬레이션 (시나리오 조정)")
st.write("아래 슬라이더를 조절하여 학교와 지역사회의 개입 강도를 설정해보세요.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏫 [해결책 1] 교내 스트레스 완화 정책")
    stress_reduction = st.slider("스트레스 감소 정책 강도 (%)", min_value=0, max_value=100, value=20, step=5)

with col2:
    st.markdown("### 🏥 [해결책 2] 상담 인프라 및 예방 교육")
    edu_increase = st.slider("상담 및 교육 인프라 확대 (%)", min_value=0, max_value=100, value=30, step=5)

# 5. 변수 계산 (개입 효과 반영)
base_stress = 0.7
base_education = 0.4
base_media = 0.8
base_family = 0.5

stress_opt = base_stress * (1 - stress_reduction / 100.0)
edu_opt = base_education * (1 + edu_increase / 100.0)

risk_index_opt = (0.4 * stress_opt) + (0.3 * base_media)
protection_index_opt = (0.5 * edu_opt) + (0.5 * base_family)

# 환경 수용량 (K) 계산
K_opt = risk_index_opt / (risk_index_opt + protection_index_opt)
r = 0.25 

# 6. 미분방정식 수치적 해석 (로지스틱 방정식 해 구하기)
t = np.linspace(0, months, months * 10)
P_t = (K_opt * P0) / (P0 + (K_opt - P0) * np.exp(-r * t))

st.markdown("---")

# 7. 결과 그래프 시각화
st.subheader("📈 시뮬레이션 예측 결과")

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(t, P_t * 100, label="Post-Intervention", color="#1f77b4", linewidth=2.5)
ax.axhline(K_opt * 100, color="red", linestyle="--", alpha=0.7, label=f"Limit ({K_opt*100:.1f}%)")

ax.set_title("Addiction Rate Prediction Over Time", fontsize=14, pad=15)
ax.set_xlabel("Time (Months)", fontsize=11)
ax.set_ylabel("Addiction Rate (%)", fontsize=11)
ax.set_ylim(0, 100)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper left")

# 스트림릿 화면에 그래프 출력
st.pyplot(fig)

# 8. 수치적 요약 결과 출력
st.markdown("### 📊 수치 요약 및 정책 제언")
col_res1, col_res2, col_res3 = st.columns(3)

with col_res1:
    st.metric(label="최종 예측 중독률", value=f"{P_t[-1]*100:.1f}%")
with col_res2:
    st.metric(label="개입 후 위험 지수", value=f"{risk_index_opt:.2f}")
with col_res3:
    st.metric(label="개입 후 보호 지수", value=f"{protection_index_opt:.2f}")

st.info(f"💡 **분석 결과:** 현재 세팅된 정책을 시행할 경우, 사회적 확산 한계선(K)이 **{K_opt*100:.1f}%** 수준에서 억제되는 효과를 보입니다. 수학적 모델링에 따르면 스트레스 감소와 교육 인프라 확충이 동반될 때 확산 곡선의 기울기가 완만해집니다.")
