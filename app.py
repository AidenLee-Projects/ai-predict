
import streamlit as st

st.set_page_config(page_title="AI Stock Prediction - 주식 예측 AI", layout="wide")

# Google Search Console 소유권 확인을 위한 메타 태그 추가
st.markdown("""
    <meta name="google-site-verification" content="ZizTnykpaL1-LKN9NOoUMTucMDKg3PYyZ3IQZ8dPLRo" />
""", unsafe_allow_html=True)





# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["📈 Predict", "📊 Stock Metrics", "📰 Stock News"]
)

st.sidebar.markdown("---")

# Load selected page
if page == "📈 Predict":
    import Predict
    Predict.show()
elif page == "📊 Stock Metrics":
    import Stock_Metrics
    Stock_Metrics.show()
elif page == "📰 Stock News":
    import Stock_News
    Stock_News.show()

# 🔥 사이드바 광고 (추천 도서 2개 추가)
st.sidebar.markdown("---")  # 구분선 추가
st.sidebar.markdown("### 📢 추천 도서")  

# 첫 번째 추천 도서
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 10px;">
        <a href="https://link.coupang.com/a/cfgNjB" target="_blank" referrerpolicy="unsafe-url">
            <img src="https://image8.coupangcdn.com/image/affiliate/banner/6b288e126df12b0277c93ddb678d3ced@2x.jpg"
            alt="돈의 속성, 김승호 저, 스노우폭스북스"
            width="120" height="240">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# 두 번째 추천 도서
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <a href="https://link.coupang.com/a/cfgVxq" target="_blank" referrerpolicy="unsafe-url">
            <img src="https://img3a.coupangcdn.com/image/affiliate/banner/f83e4de858ab6e7b3a0664ac2be1bc12@2x.jpg"
            alt="돈 뜨겁게 사랑하고 차갑게 다루어라, 앙드레 코스톨라니, 미래의창"
            width="120" height="240">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
