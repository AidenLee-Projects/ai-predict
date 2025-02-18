import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import os
from nixtla import NixtlaClient
from sklearn.metrics import mean_absolute_percentage_error

API_KEY = os.getenv("HF_API_KEY")
nixtla_client = NixtlaClient(api_key=API_KEY)

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import os
from nixtla import NixtlaClient
from sklearn.metrics import mean_absolute_percentage_error

API_KEY = os.getenv("HF_API_KEY")
nixtla_client = NixtlaClient(api_key=API_KEY)

def show():
    st.title('📈 AI Stock Prediction')

    ticker = st.text_input('Enter Stock Ticker (e.g., AAPL)', 'AAPL')
    period = st.selectbox('Select Time Interval', ['Monthly', 'Weekly', 'Daily'])
    period_dict = {'Monthly': '1mo', 'Weekly': '1wk', 'Daily': '1d'}
    yf_period = period_dict[period]

    if st.button('Load Data'):
        stock_data = yf.download(ticker, period='1y', interval=yf_period)
        stock_data.reset_index(inplace=True)

        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = stock_data.columns.get_level_values(0)

        stock_data = stock_data.loc[:, ~stock_data.columns.str.contains(ticker, case=False, na=False)]

        expected_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        if len(stock_data.columns) != len(expected_columns):
            stock_data.columns = expected_columns[:len(stock_data.columns)]

        if 'Close' not in stock_data.columns and 'Adj Close' in stock_data.columns:
            stock_data.rename(columns={'Adj Close': 'Close'}, inplace=True)

        if 'unique_id' not in stock_data.columns:
            stock_data['unique_id'] = ticker  

        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        if period == 'Daily':
            full_index = pd.date_range(start=stock_data['Date'].min(), end=stock_data['Date'].max(), freq='B')
            stock_data = (
                stock_data.set_index('Date')
                .reindex(full_index)
                .fillna(method='ffill')
                .reset_index()
                .rename(columns={'index': 'Date'})
            )
            stock_data['unique_id'] = ticker

        if stock_data.empty:
            st.error(f"⚠️ No data found for {ticker}. Please check the ticker symbol.")
        else:
            st.subheader(f'{ticker} Stock Data ({period})')
            st.dataframe(stock_data)



        forecast_horizon = {'Monthly': 3, 'Weekly': 3, 'Daily': 3}[period]
        freq_dict = {'Monthly': 'M', 'Weekly': 'W', 'Daily': 'B'} 
        freq = freq_dict[period]

        forecast = nixtla_client.forecast(
            df=stock_data,
            h=forecast_horizon,
            freq=freq,
            time_col='Date',
            target_col='Close',
            id_col='unique_id'
        )

        target_column = next(
            (col for col in forecast.columns if col.lower() in ['close', 'yhat', 'prediction', 'timegpt']),
            None
        )

        if target_column is None:
            st.error("⚠️ Forecast data is missing expected columns. Please check the API response.")
        else:
            forecast['Date'] = pd.to_datetime(forecast['Date'])

            st.subheader('📊 AI Predicted Stock Prices')
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=stock_data['Date'].tail(180),
                y=stock_data['Close'].tail(180),
                mode='lines+markers',
                name="Actual Price",
                line=dict(color='#3A86FF', width=2),
                marker=dict(size=6, symbol='circle', opacity=0.8)
            ))

            fig.add_trace(go.Scatter(
                x=forecast['Date'],
                y=forecast[target_column],
                mode='lines+markers',
                name="Predicted Price",
                line=dict(color='#FF006E', width=2, dash='dot'),
                marker=dict(size=6, symbol='square', opacity=0.8)
            ))

            fig.update_layout(
                title=f"{ticker} Stock Price Prediction ({period})",
                xaxis_title="Date",
                yaxis_title="Stock Price (USD)",
                template="plotly_white",
                legend=dict(x=0, y=1, borderwidth=1),
                font=dict(family="Arial, sans-serif", size=12, color="#333333"),
                margin=dict(l=40, r=40, t=40, b=40)
            )

            st.plotly_chart(fig, use_container_width=True)

            y_actual = stock_data['Close'].tail(len(forecast))
            y_predicted = forecast[target_column]

            if len(y_actual) == len(y_predicted):
                mape_score = mean_absolute_percentage_error(y_actual, y_predicted) * 100
                st.subheader("📊 Forecast Accuracy")
                st.write(f"✅ The AI model has a Mean Absolute Percentage Error (MAPE) of **{mape_score:.2f}%**.")
                st.write(
                    "A lower MAPE value indicates a more accurate forecast. Typically, a value under 10% is considered "
                    "highly accurate, while 10-20% is reasonably good."
                )
            else:
                st.warning("⚠️ Unable to calculate MAPE due to mismatched data lengths.")

            st.info(
                "📢 **Disclaimer:** This stock prediction is generated using an advanced AI algorithm. "
                "Please note that these predictions are for informational purposes only and should not be considered "
                "financial advice. Investing in stocks involves risks, and all investment decisions should be made at "
                "your own discretion. We do not take any responsibility for financial losses incurred as a result of using this data. 📈📊"
            )


        # 🔥 하단에 쿠팡 광고 배너 삽입
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <a href="https://link.coupang.com/a/cfgJa0" target="_blank" referrerpolicy="unsafe-url">
                <img src="https://ads-partners.coupang.com/banners/840123?subId=&traceId=V0-301-879dd1202e5c73b2-I840123&w=728&h=90" width="728" height="90" alt="쿠팡 광고">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
