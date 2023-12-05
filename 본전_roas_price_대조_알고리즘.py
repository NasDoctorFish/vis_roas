# -*- coding: utf-8 -*-
"""본전 ROAS PRICE 대조 알고리즘.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bTkCcBtyucE3G3GuCZjwMXyLawIsJwVK
"""

import pandas as pd
import matplotlib.pyplot as plt

columns = ['상품 이름', '상품 등록가', '쿠폰가', '목표 판매가', '원가', '수수료', '부가세', '택배비', '마진', '본전 ROAS']
product_data = pd.DataFrame(columns = columns)
#commision_rates는 추후 업데이트 예정
commission_rates = {
    '농수산물': '10.6%',
    # Add more categories and their commission rates as needed
    '전자제품': '8.2%',
    '영양제'	:	'7.6%',
    '채소류'  :	'7.6%',
    '쌀/잡곡류' :	'5.8%',
    '면/라면'	: '10.9%'
}

# 빈 DataFrame을 초기화합니다.
columns = ['가격', '비용', '마진', '마진율','본전 ROAS']
data = pd.DataFrame(columns=columns)
#시장가
global market_price

def calculate_margin_rate(price, cost):
    #수수료까지 합쳐서
    #택배비는 2300이라고 가정
    margin = price*0.894 - cost - 2300
    ROAS = (price / margin) * 100 if price != 0 else 0
    margin_rate = (margin / price) * 100 if price != 0 else 0

    #순서대로 리턴
    return margin, ROAS, margin_rate

def append_data(price, cost):
    #여기서 DICTIONARY에 자동으로 열에 맟춰서 추가하는 듯
    margin, ROAS, margin_rate = calculate_margin_rate(price, cost)
    #입력받은 값을 바탕으로 DICTIONARY 하나 만듬
    new_entry = {'가격': price, '비용': cost, '마진': margin, '마진율': margin_rate, '본전 ROAS': ROAS}
    return data.append(new_entry, ignore_index=True)


#def filter_outlier(pd_data):


# 사용자 입력을 계속해서 받는 메인 루프
while True:
    try:
        user_price = float(input("가격을 입력하세요: "))
        user_cost = float(input("비용을 입력하세요: "))
        market_price = float(input("시장평균가를 입력하세요: "))

        # DataFrame에 데이터 추가
        #처음 열 두개 만 추가하여 뒤에 마진과 마진율은 변하지 않음
        init_price = user_price*0.8
        for _ in range(16):
          data = append_data(init_price, user_cost)
          #0.04는 23만원 일때 1만원의 비율이 대략적으로 4%라서임.
          init_price += init_price*0.04
        #그래프 그리기
        print("\n업데이트된 데이터:")
        print(data)

        #그래프 그리기
        pd_data = pd.DataFrame(data)

        # Plotting the relationship between columns 'X' and 'Y'
        plt.plot(pd_data['가격'], pd_data['본전 ROAS'], marker='o')  # Plotting 가격, 본전 ROAS with markers

        plt.xlabel('Price(Won)')  # Set x-axis label
        plt.ylabel('ROAS', color = 'b')  # Set y-axis label 본전 ROAS
        plt.title('ROAS & PRICE GRAPH')  # Set plot title

        plt.grid(True)  # Show grid
        # Value for the dotted line on the x-axis
        #is market_price global variable
        ymin, ymax = plt.ylim()

        #draw a vertical line that has x_value on x-axis
        plt.vlines(x=market_price, ymin=ymin, ymax=ymax, color='r', linestyle='--', label = 'Market Price')  # Adding a vertical dotted line at x_value

        plt.legend()
        plt.grid(True)  # Show grid

        plt.show()

    except ValueError:
        print("가격과 비용에 유효한 숫자 값을 입력하세요.")

    else:
        continue_calculation = input("계속하시겠습니까? (예/아니요) ").lower()
        if continue_calculation != "예":
          break

"""#위의 코드는 간단하게 가격과 원가를 입력하면 마진율을 OUTPUT하는 코드임"""