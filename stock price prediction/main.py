import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import tkinter as tk
from tkinter import ttk
import datetime
import logging  # 로깅 라이브러리 추가

# 로깅 설정
logging.basicConfig(filename='stock_prediction.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def predict_all_stocks():
    # 표 초기화
    for i in tree.get_children():
        tree.delete(i)

    # 입력 받은 미래 날짜
    input_date = future_date.get()
    input_day = (pd.to_datetime(input_date) - pd.to_datetime("2019-01-01")).days

    # 모든 주식에 대한 예측 수행
    for stock in top_stocks:
        try:
            stock_data = yf.download(stock, start="2019-01-01", end=input_date, progress=False)
            latest_price = yf.Ticker(stock).history(period="1d")['Close'].iloc[-1]

            # 추가 특성 생성 및 NaN 값 제거
            stock_data['Day'] = np.arange(len(stock_data))
            stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
            stock_data['Volatility'] = stock_data['Close'].rolling(window=20).std()
            stock_data = stock_data.dropna()

            # 특성과 타겟 변수 선택
            X = stock_data[['Day', 'SMA_20', 'Volatility']]
            y = stock_data['Close']

            # 데이터 스케일링 및 모델 학습
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            model = RandomForestRegressor(n_estimators=100, random_state=0)
            model.fit(X_scaled, y)

            # 미래 날짜 예측
            future_day = pd.DataFrame([[input_day, stock_data['SMA_20'].iloc[-1], stock_data['Volatility'].iloc[-1]]],
                                      columns=['Day', 'SMA_20', 'Volatility'])
            future_day_scaled = scaler.transform(future_day)
            predicted_price = model.predict(future_day_scaled)[0]

            # 표에 결과 추가
            tree.insert("", "end", values=(stock, f"${latest_price:.2f}", f"${predicted_price:.2f}", f"${predicted_price - latest_price:.2f}"))

            # 로그 기록
            log_message = f"Stock: {stock}, Latest Price: ${latest_price:.2f}, Predicted Price: ${predicted_price:.2f}, Difference: ${predicted_price - latest_price:.2f}"
            logging.info(log_message)
        except Exception as e:
            error_message = f"Error with stock {stock}: {e}"
            print(error_message)
            logging.error(error_message)

# Tkinter 창 설정
root = tk.Tk()
root.title("주식 가격 예측")
root.geometry("900x400")

# 주식 목록 예시 (시가총액 상위 기업)
top_stocks = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "TSLA", "BRK-A", "TSM", "V", "JPM", 
    "JNJ", "WMT", "NVDA", "MA", "PG", 
    "UNH", "DIS", "HD", "BAC", "PYPL"
]


# 현재 날짜를 YYYY-MM-DD 형식으로 가져오기
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# 날짜 입력
future_date_label = tk.Label(root, text="예측할 날짜 입력 (YYYY-MM-DD):")
future_date_label.pack()
future_date = tk.Entry(root)
future_date.pack()
future_date.insert(0, current_date)  # 현재 날짜를 기본값으로 설정

# 표 설정
columns = ("Stock", "Current Price", "Predicted Price", "Difference")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(expand=True, fill="both")

# 예측 버튼
predict_button = tk.Button(root, text="전체 주가 예측", command=predict_all_stocks)
predict_button.pack()

# GUI 실행
root.mainloop()
