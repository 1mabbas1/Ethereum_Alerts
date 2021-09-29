import requests
from newsapi.newsapi_client import NewsApiClient
import datetime
from twilio.rest import Client
import os


#get todays and yesterdays dates
todate  = (datetime.datetime.today().strftime('%Y-%m-%d'))
yesterdate = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

#your twilio account sid and auth_token allows you to send text messages
account_sid = 'sid'
auth_token = 'auth_token'

#apikey is api key of alphavantage, this service provides a json of prices.
crypto_parameters = {'function': 'DIGITAL_CURRENCY_DAILY',
              'symbol': 'ETH',
              'market' : 'USD',
              'apikey': 'alpha vantage api key'}

#news_parameters = {'apikey':''}
crypto_response = requests.get('https://www.alphavantage.co/query', params = crypto_parameters)
prices = crypto_response.json()

yday_volume= round(float(prices['Time Series (Digital Currency Daily)'][yesterdate]['5. volume']),2)
yday_open =  round(float(prices['Time Series (Digital Currency Daily)'][yesterdate]['1a. open (USD)']),2)
yday_close = round(float(prices['Time Series (Digital Currency Daily)'][yesterdate]['4a. close (USD)']),2)
yday_percentage = round((yday_open-yday_close)/100,2)

newsapi = NewsApiClient(api_key='newsapi api key')

all_articles = newsapi.get_everything(q='ethereum',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param=yesterdate,
                                      to=todate,
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)


#Enter your twilio and personal phone numbers to recieve text messages from twilio
#Messages are only sent if the percentage change in price is significant (5%)
if abs(yday_percentage) <= 5:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=f"ETH News\nYesterday Open: ${yday_open}\nYesterday Close: ${yday_close}\n"
             f"Percentage Change: {yday_percentage}%\nYesterday Volume: {yday_volume}",
        from_='twilio phone number',
        to='your personal phone number')


    for articles in range(1,4):
        headline = (all_articles['articles'][articles]['title'])
        description = ((all_articles['articles'][articles]['description']))

        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=f"{headline}\n{description}",
            from_='twilio phone number',
            to='your personal phone number')
