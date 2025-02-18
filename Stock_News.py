import streamlit as st
import feedparser
import pandas as pd

def show():
    st.title("📰 Latest Stock News (RSS)")

    ticker = st.text_input("Enter Stock Ticker", "AAPL")
    if ticker:
        rss_url = f"https://news.google.com/rss/search?q={ticker}+stock"
        feed = feedparser.parse(rss_url)

        if feed.bozo:
            st.error("⚠️ Failed to fetch news from RSS feed.")
        else:
            entries = feed.entries
            if entries:
                news_items = []
                for entry in entries:
                    # 날짜를 YYYY-MM-DD 형식으로 변환 (UTC 기준)
                    date_parsed = pd.to_datetime(entry.published, utc=True).strftime("%Y-%m-%d")
                    
                    news_items.append({
                        "Title": entry.title,
                        "Link": entry.link,
                        "Date": date_parsed
                    })

                # 최신 뉴스가 가장 위에 오도록 정렬
                news_df = pd.DataFrame(news_items)
                news_df = news_df.sort_values(by="Date", ascending=False)

                # 뉴스 제목을 클릭할 수 있도록 하이퍼링크 처리
                news_df["Title"] = news_df.apply(lambda row: f"[{row['Title']}]({row['Link']})", axis=1)

                # 필요 없는 컬럼 제거 (Link는 이미 Title에 포함됨)
                news_df = news_df[["Date", "Title"]]

                st.write("## Latest News")
                st.table(news_df)  # 가독성 좋은 테이블 사용
            else:
                st.write("ℹ️ No news articles found.")
