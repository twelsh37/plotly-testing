## TallTim's Quoteboard v0.04
## Styled quoteboard based on the application card example by AnneMarieW from here ("Card Group"):
## https://dash-building-blocks.com/app_cards

import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import dash_mantine_components as dmc
import pandas as pd

# If you want to work with the original example code you'll need to enable the 'SUPERHERO' stylesheet here...even though I'm not
# using the icons, I left it in as a convenience...
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])

#################### This is a flag you can set for testing so you don't ping the site API ####################
# testFlag = "False" # Uses live data from API URL request
testFlag = "False"  # Uses test data, no URL requests
###############################################################################################################

# Assorted Variables
# Define coins to make quoteblocks from, this is asset_id column in the df.Quotes dataframe
# This will change if you change data sources
# coins = [
#     "bitcoin",
#     "ethereum",
#     "binancecoin",
#     "ripple",
#     "usd-coin",
#     "tether",
#     "bnb",
#     "usdc",
#     "staked-ether",
#     "dogecoin",
#     "solana",
#     "cardano",
#     "tron",
#     "matic-network",
# ]
interval = 6000  # update frequency - 1000 = 1 second, so 6 seconds here
# Access API
api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
# Colors For Card Backgrounds/Borders/Text
text_decline = "#C70000"  # Red
text_rally = "#00C700"  # Green
text_unchanged = "#A8A8A8"  # Off-white
gradient_decline = "linear-gradient(0deg,#870900,#000000 95%)"
gradient_border_decline = "#940000"
gradient_rally = "linear-gradient(0deg,#008709,#000000 95%)"
gradient_border_rally = "#009400"
gradient_unchanged = "linear-gradient(0deg,#A8A8A8,#000000 95%)"
gradient_border_unchanged = "#949494"

change = 0
price = 0
icon = ""
color = ""
interval = dcc.Interval(interval=interval)
cards = html.Div()
df_Quotes = pd.DataFrame()  # Init empty dataframe

# Used in assigning cards to quoteblock vars -- must match length of 'coins' list above...
quoteBlockVarNames = [
    "quoteBlock_1",
    "quoteBlock_2",
    "quoteBlock_3",
    "quoteBlock_4",
    "quoteBlock_5",
    "quoteBlock_6",
    "quoteBlock_7",
    "quoteBlock_8",
    "quoteBlock_9",
    "quoteBlock_10",
    "quoteBlock_11",
    "quoteBlock_12",
]

# Debug -- snapshot of data served by CoinGecko so I can test style/layout without pinging the site...
# Testing volume sorting - edited volume so the sorted order should be:
# Bitcoin - 1000, Ethereum - 900, Ripple - 800, USD-Coin - 700, Doge - 650, Tether - 600, BinanceCoin - 500, Staked-Ether - 400, Solana - 300, Matic - 200, Tron - 10, Cardano - 5

scraped_data = [
    {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1547033579",
        "current_price": 29346,
        "market_cap": 571125444188,
        "market_cap_rank": 1,
        "fully_diluted_valuation": 616394102148,
        "total_volume": 1000,
        "high_24h": 29653,
        "low_24h": 29263,
        "price_change_24h": -51.54874027145706,
        "price_change_percentage_24h": 5.25,
        "market_cap_change_24h": -896753676.9368896,
        "market_cap_change_percentage_24h": -0.15677,
        "circulating_supply": 19457737.0,
        "total_supply": 21000000.0,
        "max_supply": 21000000.0,
        "ath": 69045,
        "ath_change_percentage": -57.50061,
        "ath_date": "2021-11-10T14:24:11.849Z",
        "atl": 67.81,
        "atl_change_percentage": 43173.91396,
        "atl_date": "2013-07-06T00:00:00.000Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:38.522Z",
    },
    {
        "id": "ethereum",
        "symbol": "eth",
        "name": "Ethereum",
        "image": "https://assets.coingecko.com/coins/images/279/large/ethereum.png?1595348880",
        "current_price": 1840.48,
        "market_cap": 221180610887,
        "market_cap_rank": 2,
        "fully_diluted_valuation": 221180610887,
        "total_volume": 900,
        "high_24h": 1854.61,
        "low_24h": 1836.08,
        "price_change_24h": -5.970458272938913,
        "price_change_percentage_24h": -0.32335,
        "market_cap_change_24h": -599404386.0502014,
        "market_cap_change_percentage_24h": -0.27027,
        "circulating_supply": 120142222.589507,
        "total_supply": 120142222.589507,
        "max_supply": None,
        "ath": 4878.26,
        "ath_change_percentage": -62.27958,
        "ath_date": "2021-11-10T14:24:19.604Z",
        "atl": 0.432979,
        "atl_change_percentage": 424886.14404,
        "atl_date": "2015-10-20T00:00:00.000Z",
        "roi": {
            "times": 82.83960831086297,
            "currency": "btc",
            "percentage": 8283.960831086297,
        },
        "last_updated": "2023-08-15T05:38:39.869Z",
    },
    {
        "id": "tether",
        "symbol": "usdt",
        "name": "Tether",
        "image": "https://assets.coingecko.com/coins/images/325/large/Tether.png?1668148663",
        "current_price": 0.998601,
        "market_cap": 83275370679,
        "market_cap_rank": 3,
        "fully_diluted_valuation": 83275370679,
        "total_volume": 600,
        "high_24h": 1.001,
        "low_24h": 0.995176,
        "price_change_24h": 0,
        "price_change_percentage_24h": 0,
        "market_cap_change_24h": -21912507.411972046,
        "market_cap_change_percentage_24h": -0.02631,
        "circulating_supply": 83410866925.5156,
        "total_supply": 83410866925.5156,
        "max_supply": None,
        "ath": 1.32,
        "ath_change_percentage": -24.52252,
        "ath_date": "2018-07-24T00:00:00.000Z",
        "atl": 0.572521,
        "atl_change_percentage": 74.42837,
        "atl_date": "2015-03-02T00:00:00.000Z",
        "roi": None,
        "last_updated": "2023-08-15T05:35:00.921Z",
    },
    {
        "id": "binancecoin",
        "symbol": "bnb",
        "name": "BNB",
        "image": "https://assets.coingecko.com/coins/images/825/large/bnb-icon2_2x.png?1644979850",
        "current_price": 239.27,
        "market_cap": 36813979487,
        "market_cap_rank": 4,
        "fully_diluted_valuation": 47855063951,
        "total_volume": 500,
        "high_24h": 241.0,
        "low_24h": 239.13,
        "price_change_24h": -1.3132428836969154,
        "price_change_percentage_24h": -0.54587,
        "market_cap_change_24h": -216913346.59331512,
        "market_cap_change_percentage_24h": -0.58576,
        "circulating_supply": 153856150.0,
        "total_supply": 153856150.0,
        "max_supply": 200000000.0,
        "ath": 686.31,
        "ath_change_percentage": -65.13848,
        "ath_date": "2021-05-10T07:24:17.097Z",
        "atl": 0.0398177,
        "atl_change_percentage": 600780.88219,
        "atl_date": "2017-10-19T00:00:00.000Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:39.120Z",
    },
    {
        "id": "ripple",
        "symbol": "xrp",
        "name": "XRP",
        "image": "https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png?1605778731",
        "current_price": 0.628703,
        "market_cap": 33176786260,
        "market_cap_rank": 5,
        "fully_diluted_valuation": 62849958286,
        "total_volume": 800,
        "high_24h": 0.635508,
        "low_24h": 0.625689,
        "price_change_24h": -0.003263613505237073,
        "price_change_percentage_24h": -0.51642,
        "market_cap_change_24h": -213536726.86206436,
        "market_cap_change_percentage_24h": -0.63952,
        "circulating_supply": 52787284454.0,
        "total_supply": 99988519823.0,
        "max_supply": 100000000000.0,
        "ath": 3.4,
        "ath_change_percentage": -81.52247,
        "ath_date": "2018-01-07T00:00:00.000Z",
        "atl": 0.00268621,
        "atl_change_percentage": 23276.81696,
        "atl_date": "2014-05-22T00:00:00.000Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:40.312Z",
    },
    {
        "id": "usd-coin",
        "symbol": "usdc",
        "name": "USD Coin",
        "image": "https://assets.coingecko.com/coins/images/6319/large/USD_Coin_icon.png?1547042389",
        "current_price": 1.0,
        "market_cap": 26002210526,
        "market_cap_rank": 6,
        "fully_diluted_valuation": 25995337308,
        "total_volume": 700,
        "high_24h": 1.001,
        "low_24h": 0.995914,
        "price_change_24h": 0.00024895,
        "price_change_percentage_24h": 0.0249,
        "market_cap_change_24h": -164825818.58258438,
        "market_cap_change_percentage_24h": -0.6299,
        "circulating_supply": 26002476366.8477,
        "total_supply": 25995603078.5546,
        "max_supply": None,
        "ath": 1.17,
        "ath_change_percentage": -14.76763,
        "ath_date": "2019-05-08T00:40:28.300Z",
        "atl": 0.877647,
        "atl_change_percentage": 13.88698,
        "atl_date": "2023-03-11T08:02:13.981Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:41.408Z",
    },
    {
        "id": "staked-ether",
        "symbol": "steth",
        "name": "Lido Staked Ether",
        "image": "https://assets.coingecko.com/coins/images/13442/large/steth_logo.png?1608607546",
        "current_price": 1840.15,
        "market_cap": 14926181150,
        "market_cap_rank": 7,
        "fully_diluted_valuation": 14922486712,
        "total_volume": 400,
        "high_24h": 1853.33,
        "low_24h": 1837.27,
        "price_change_24h": -5.9586862118578665,
        "price_change_percentage_24h": -0.32277,
        "market_cap_change_24h": -23891417.27374077,
        "market_cap_change_percentage_24h": -0.15981,
        "circulating_supply": 8109614.0695121,
        "total_supply": 8109614.0695121,
        "max_supply": 8107606.82716179,
        "ath": 4829.57,
        "ath_change_percentage": -61.9037,
        "ath_date": "2021-11-10T14:40:47.256Z",
        "atl": 482.9,
        "atl_change_percentage": 281.01098,
        "atl_date": "2020-12-22T04:08:21.854Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:41.375Z",
    },
    {
        "id": "dogecoin",
        "symbol": "doge",
        "name": "Dogecoin",
        "image": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png?1547792256",
        "current_price": 0.07442,
        "market_cap": 10463841439,
        "market_cap_rank": 8,
        "fully_diluted_valuation": 10463755851,
        "total_volume": 650,
        "high_24h": 0.075371,
        "low_24h": 0.073692,
        "price_change_24h": -0.000596043719873193,
        "price_change_percentage_24h": -0.79455,
        "market_cap_change_24h": -93366893.82887459,
        "market_cap_change_percentage_24h": -0.88439,
        "circulating_supply": 140595866383.705,
        "total_supply": 140594716383.705,
        "max_supply": None,
        "ath": 0.731578,
        "ath_change_percentage": -89.83321,
        "ath_date": "2021-05-08T05:08:23.458Z",
        "atl": 8.69e-05,
        "atl_change_percentage": 85486.66332,
        "atl_date": "2015-05-06T00:00:00.000Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:46.559Z",
    },
    {
        "id": "solana",
        "symbol": "sol",
        "name": "Solana",
        "image": "https://assets.coingecko.com/coins/images/4128/large/solana.png?1640133422",
        "current_price": 24.96,
        "market_cap": 10142116320,
        "market_cap_rank": 9,
        "fully_diluted_valuation": 13859120315,
        "total_volume": 300,
        "high_24h": 25.24,
        "low_24h": 24.36,
        "price_change_24h": 0.530718,
        "price_change_percentage_24h": 2.17233,
        "market_cap_change_24h": 211395396,
        "market_cap_change_percentage_24h": 2.1287,
        "circulating_supply": 406100728.206927,
        "total_supply": 554933376.28717,
        "max_supply": None,
        "ath": 259.96,
        "ath_change_percentage": -90.4005,
        "ath_date": "2021-11-06T21:54:35.825Z",
        "atl": 0.500801,
        "atl_change_percentage": 4882.97123,
        "atl_date": "2020-05-11T19:35:23.449Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:39.674Z",
    },
    {
        "id": "cardano",
        "symbol": "ada",
        "name": "Cardano",
        "image": "https://assets.coingecko.com/coins/images/975/large/cardano.png?1547034860",
        "current_price": 0.289028,
        "market_cap": 10129225134,
        "market_cap_rank": 10,
        "fully_diluted_valuation": 13006558999,
        "total_volume": 5,
        "high_24h": 0.292078,
        "low_24h": 0.287716,
        "price_change_24h": -0.001666535922617174,
        "price_change_percentage_24h": -0.57329,
        "market_cap_change_24h": -58743586.493177414,
        "market_cap_change_percentage_24h": -0.5766,
        "circulating_supply": 35045020830.3234,
        "total_supply": 45000000000.0,
        "max_supply": 45000000000.0,
        "ath": 3.09,
        "ath_change_percentage": -90.64588,
        "ath_date": "2021-09-02T06:00:10.474Z",
        "atl": 0.01925275,
        "atl_change_percentage": 1399.80376,
        "atl_date": "2020-03-13T02:22:55.044Z",
        "roi": None,
        "last_updated": "2023-08-15T05:38:46.726Z",
    },
    {
        "id": "tron",
        "symbol": "trx",
        "name": "TRON",
        "image": "https://assets.coingecko.com/coins/images/1094/large/tron-logo.png?1547035066",
        "current_price": 0.077272,
        "market_cap": 6915242709,
        "market_cap_rank": 11,
        "fully_diluted_valuation": 6915291935,
        "total_volume": 10,
        "high_24h": 0.077575,
        "low_24h": 0.077072,
        "price_change_24h": 0.00011325,
        "price_change_percentage_24h": 0.14678,
        "market_cap_change_24h": 4577588,
        "market_cap_change_percentage_24h": 0.06624,
        "circulating_supply": 89471632948.6968,
        "total_supply": 89472269852.3265,
        "max_supply": None,
        "ath": 0.231673,
        "ath_change_percentage": -66.63921,
        "ath_date": "2018-01-05T00:00:00.000Z",
        "atl": 0.00180434,
        "atl_change_percentage": 4183.43794,
        "atl_date": "2017-11-12T00:00:00.000Z",
        "roi": {
            "times": 39.66971290740434,
            "currency": "usd",
            "percentage": 3966.9712907404337,
        },
        "last_updated": "2023-08-15T05:38:39.511Z",
    },
    {
        "id": "matic-network",
        "symbol": "matic",
        "name": "Polygon",
        "image": "https://assets.coingecko.com/coins/images/4713/large/matic-token-icon.png?1624446912",
        "current_price": 0.674663,
        "market_cap": 6290066896,
        "market_cap_rank": 12,
        "fully_diluted_valuation": 6749383306,
        "total_volume": 200,
        "high_24h": 0.684453,
        "low_24h": 0.674531,
        "price_change_24h": -0.006132114034599567,
        "price_change_percentage_24h": -0.90073,
        "market_cap_change_24h": -48608944.01885128,
        "market_cap_change_percentage_24h": -0.76686,
        "circulating_supply": 9319469069.28493,
        "total_supply": 10000000000.0,
        "max_supply": 10000000000.0,
        "ath": 2.92,
        "ath_change_percentage": -76.86017,
        "ath_date": "2021-12-27T02:08:34.307Z",
        "atl": 0.00314376,
        "atl_change_percentage": 21365.32317,
        "atl_date": "2019-05-10T00:00:00.000Z",
        "roi": {
            "times": 255.5260048380359,
            "currency": "usd",
            "percentage": 25552.600483803588,
        },
        "last_updated": "2023-08-15T05:38:39.642Z",
    },
]


def get_data():  # Get data via API, pass exceptions to console if any generated
    try:
        response = requests.get(api_url, timeout=1)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)

    return


def styleCard(myCoin, myPrice, myChange, myColor, myGradient, myGradientBorder):
    card_html = dbc.Card(
        html.Div(
            [
                html.H4(  # Our asset name font size/style
                    [myCoin],  # full_name of asset
                    style={
                        "font-size": "160%",
                        "color": "white",
                        "text-align": "left",
                        "padding-left": "20px",
                        "padding-top": "20px",
                    },
                ),
                html.H4(  # Price and Net Change format/style/padding
                    [
                        # Either change the number of decimals by changing the round(number,places) statement or the quoteblock width down at the end
                        html.Span(
                            f"${round(myPrice, 5):,}",
                            style={
                                "font-size": "90%",
                                "color": "white",
                                "text-align": "left",
                                "padding-left": "20px",
                            },
                        ),
                        html.Span(
                            f"{round(myChange, 2):+}%",
                            style={
                                "font-size": "90%",
                                "color": myColor,
                                "text-align": "left",
                                "padding-left": "10px",
                                "padding-top": "5px",
                            },
                        ),
                    ]
                ),
            ],
            # Background gradient/colorstops of quoteblock/padding - transparent background color
            style={
                "background": "#00000000",
                "background-image": myGradient,
                "border": "1px",
                "solid": "#00000000",
                "border-radius": "5px",
                "border-style": "solid",
                "color": myGradientBorder,
                "padding-bottom": "10px",
            },
        ),
        # Quoteblock set width/height/padding/background - Also can be used to fit more decimals...
        # Note that color here for the background is transparent so it doesn't clash with the overall theme background
        style={
            "width": "270px",
            "height": "130px",
            "padding-right": "10px",
            "background": "#00000000",
        },
    )

    return card_html


app.layout = dbc.Container(
    [interval, cards], className="my-5", style={"background": "#00000000"}
)  # Same here, transparent background


def make_card(myName, myChange, myPrice):  # passes full_name, net_change_percent, price
    if myChange < 0:  # Decreased price?
        color = text_decline  # Color of net change % +/-
        gradient_fill = gradient_decline
        gradient_border = gradient_border_decline
    elif myChange > 0:  # Increased price?
        color = text_rally
        gradient_fill = gradient_rally
        gradient_border = gradient_border_rally
    else:  # Rare, but no change in price?
        color = text_unchanged
        gradient_fill = gradient_unchanged
        gradient_border = gradient_border_unchanged

    return styleCard(myName, myPrice, myChange, color, gradient_fill, gradient_border)


# Columns we don't need from data -- feel free to change if you want to use these
dropList = [
    "image",
    "market_cap",
    "market_cap_rank",
    "fully_diluted_valuation",
    "high_24h",
    "low_24h",
    "price_change_24h",
    "market_cap_change_24h",
    "market_cap_change_percentage_24h",
    "circulating_supply",
    "total_supply",
    "max_supply",
    "ath",
    "ath_change_percentage",
    "ath_date",
    "atl",
    "atl_change_percentage",
    "atl_date",
    "roi",
    "last_updated",
]

# Renamed columns - original:new name -- You can change these, but you need to alter their references in the rest of the code...
renamedPairsList = {
    "id": "asset_id",
    "symbol": "ticker",
    "name": "full_name",
    "current_price": "price",
    "total_volume": "volume",
    "price_change_percentage_24h": "net_change_percent",
}


@app.callback(Output(cards, "children"), Input(interval, "n_intervals"))
def update_cards(_):
    if testFlag == "True":
        coin_data = scraped_data  # For debug so I don't poll the site a bazillion times

    if testFlag == "False":
        coin_data = get_data()  # Live data

    if coin_data is None or type(coin_data) is dict:  # Catch none type exception
        return dash.no_update

    ## Process scraped data into pandas dataframe
    df_Quotes = pd.DataFrame.from_dict(coin_data, orient="columns")
    # Drop columns we don't need - helps when debugging
    df_Quotes = df_Quotes.drop(columns=dropList, axis=1)
    # Rename columns for ease of reference/debugging
    df_Quotes = df_Quotes.rename(columns=renamedPairsList)
    # Sort based on volume, descending order
    df_Quotes = df_Quotes.sort_values(by="volume", ascending=False)
    # Reindex dataframe for ease of reference
    df_Quotes = df_Quotes.reset_index(drop=True)

    # Debug
    # Print data types if needed
    # print(df_Quotes.info())
    # Print dataframe contents
    # print("Dataframe Contents: \n" + df_Quotes.to_string() + "\n")

    # Our list of cards with data fully styled
    coin_cards = []

    # Assign dataframe columns to variables
    coin_name = df_Quotes["full_name"]
    net_change = df_Quotes["net_change_percent"]
    price = df_Quotes["price"]

    # Using dataframes, iterate via index
    for idx, item in enumerate(coin_name):
        coin_cards.append(
            make_card(coin_name[idx], net_change[idx], price[idx])
        )  # pass asset_id, net change, price

    # Don't like the padding on this one, not sure how to adjust - tried a lot of variants...(not shown, but trust me, I did)
    # Just leaving it here for demonstration sake...

    # make the card layout -- this works -- but the grid is spaced out more than I'd like...
    # card_layout = [
    # 	dmc.Grid([
    # 		dbc.Row([
    # 					dmc.Col(card, md=1) for card in coin_cards
    # 				])
    # 	])
    # ]

    # I prefer this layout, even though its a bit simplistic...
    # Assign variables values in loop
    for idx, var in enumerate(
        quoteBlockVarNames
    ):  # If you want more cards, just add to the list in the variable section up top
        globals()[var] = coin_cards[
            idx
        ]  # Assign our quoteblock variable names the proper coin_card[] using proper index

    # Simple nested structure with main Div and a Grid inside...
    card_layout = [
        html.Div(
            [
                html.H1(
                    ["Top Crypto Assets - By Volume"],
                    style={
                        "padding-left": "20px",
                        "font-size": "30px",
                        "font-weight": "bold",
                    },
                ),
                html.Br(),
                # Probably could use a loop to assign this as well, but honestly I'm tired and this is all the cards I want...
                dmc.Grid(
                    [
                        quoteBlock_1,
                        quoteBlock_2,
                        quoteBlock_3,
                        quoteBlock_4,
                        quoteBlock_5,
                        quoteBlock_6,
                        quoteBlock_7,
                        quoteBlock_8,
                        quoteBlock_9,
                        quoteBlock_10,
                        quoteBlock_11,
                        quoteBlock_12,
                    ],
                    align="center",
                    justify="center",
                ),
            ]
        )
    ]

    return card_layout


# Run the App
if __name__ == "__main__":
    app.run_server(
        debug=True
    )  # Set host argument to allow LAN connections, Port for custom ports
