import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def show():
    st.title("📊 Stock Analysis")

    ticker = st.text_input("Enter Stock Ticker", "AAPL")
    if ticker:
        stock = yf.Ticker(ticker)
        
        # 📌 1️⃣ 주요 지표 가져오기
        info = stock.info
        try:
            market_cap = info.get("marketCap", "N/A")
            pe_ratio = info.get("trailingPE", "N/A")
            dividend_yield = info.get("dividendYield", "N/A")
            beta = info.get("beta", "N/A")
        except:
            st.error("⚠️ Unable to fetch stock information.")
            return
        
        # 📌 2️⃣ 최근 6개월 주가 데이터 가져오기
        df = stock.history(period="6mo", interval="1d")
        df.reset_index(inplace=True)
        df["Date"] = pd.to_datetime(df["Date"])
        
        if df.empty:
            st.error("⚠️ No historical data found for this stock.")
            return
        
        # 📌 3️⃣ 전월 대비 증감율 계산
        df["Month"] = df["Date"].dt.to_period("M")
        monthly_close = df.groupby("Month")["Close"].last()
        monthly_change = monthly_close.pct_change() * 100  # 증감율 (%)
        
        # 📌 4️⃣ 주요 지표 표출
        st.write("### Key Metrics")
        metrics_data = {
            "Market Cap": [f"${market_cap:,}" if market_cap != "N/A" else "N/A"],
            "PE Ratio": [round(pe_ratio, 2) if pe_ratio != "N/A" else "N/A"],
            "Dividend Yield": [f"{round(dividend_yield * 100, 2)}%" if dividend_yield != "N/A" else "N/A"],
            "Beta": [round(beta, 2) if beta != "N/A" else "N/A"],
        }
        st.table(pd.DataFrame(metrics_data, index=[ticker]))
        
        # 📌 5️⃣ 📈 그래프: 최근 6개월 주가 트렌드 (Plotly 변환)
        st.write("### 📈 Stock Price Trend (Last 6 Months)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Date"], 
            y=df["Close"], 
            mode="lines+markers",
            name="Close Price",
            line=dict(color="#3A86FF", width=2),
            marker=dict(size=6, symbol="circle", opacity=0.8)
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Stock Price (USD)",
            template="plotly_white",
            legend=dict(x=0, y=1, borderwidth=1),
            font=dict(family="Arial, sans-serif", size=12, color="#333333"),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

        # 📌 6️⃣ 📊 전월 대비 증감율 그래프 (Plotly 변환)
        st.write("### 📊 Monthly Percentage Change")
        colors = ["#FF006E" if x < 0 else "#3A86FF" for x in monthly_change]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=monthly_change.index.astype(str),
            y=monthly_change,
            marker_color=colors,
            text=[f"{x:.2f}%" for x in monthly_change],
            textposition="auto",
        ))
        fig2.update_layout(
            xaxis_title="Month",
            yaxis_title="Change (%)",
            title=f"{ticker} Monthly Percentage Change",
            template="plotly_white",
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 📌 7️⃣ 분석 요약
        st.write("### 📌 Summary Analysis")
        if monthly_change.iloc[-1] > 0:
            st.success(f"✅ The stock price has increased by {monthly_change.iloc[-1]:.2f}% compared to last month.")
        elif monthly_change.iloc[-1] < 0:
            st.error(f"🔻 The stock price has decreased by {abs(monthly_change.iloc[-1]):.2f}% compared to last month.")
        else:
            st.info("ℹ️ The stock price remained stable compared to last month.")
