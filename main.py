import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alphavantage_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "7F14WX45N56HKHBV",
}
newsapi_params = {
    "q": COMPANY_NAME,
    "apiKey": "b9da483609b8413ab7cc69eab41daacb",
}
account_sid = "AC6d066e58affc4e3fc06332a66c630e25"
auth_token = "d3934e03fbef686a19dc3250980e5618"

# ------------------------------- STEP 1: Use https://www.alphavantage.co -------------------------------------
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday.
response = requests.get("https://www.alphavantage.co/query", params=alphavantage_params)
response.raise_for_status()
data = response.json()
two_previous_daily_data = [data for day, data in data["Time Series (Daily)"].items()][:2]
yesterday_close_price = float(two_previous_daily_data[0]["4. close"])
before_yesterday_close_price = float(two_previous_daily_data[1]["4. close"])
differential_percentage = round((before_yesterday_close_price-yesterday_close_price)*100/before_yesterday_close_price)
if differential_percentage > 5 or differential_percentage < -5:

    # --------------------------------- STEP 2: Use https://newsapi.org -------------------------------------------
    # Get the first 3 news pieces for the COMPANY_NAME.
    news_response = requests.get("https://newsapi.org/v2/everything", params=newsapi_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    three_last_news = news_data["articles"][:3]
    for each_news in three_last_news:
        # --------------------------- STEP 3: Use https://www.twilio.com -------------------------------------
        # Send a separate message with the percentage change and each article's title and description.
        client = Client(account_sid, auth_token)
        if differential_percentage > 5:
            message = client.messages \
                .create(
                    body=f"""
                    {COMPANY_NAME}: 🔺{differential_percentage}%
                    Headline: {each_news['title']}
                    Brief: {each_news['description']}
                    """,
                    from_='+15628421413',
                    to='+995593601624'
                )
        else:
            message = client.messages \
                .create(
                    body=f"""
                    {COMPANY_NAME}: 🔻{differential_percentage}%
                    Headline: {each_news['title']}
                    Brief: {each_news['description']}
                    """,
                    from_='+15628421413',
                    to='+995593601624'
                )
        print(message.status)
