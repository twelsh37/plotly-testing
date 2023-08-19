# TallTim's Quoteboard v0.04
# Styled quoteboard based on the application card example by AnneMarieW from here ("Card Group"):
# https://dash-building-blocks.com/app_cards

import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import dash_mantine_components as dmc
import pandas as pd

# If you want to work with the original example code you'll need to enable the 'SUPERHERO' stylesheet here...
# even though I'm not
# using the icons, I left it in as a convenience...
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])

# Assorted Variables
interval = 6000  # update frequency - 1000 = 1 second, so 6 seconds here
interval = dcc.Interval(interval=interval)
cards = html.Div()


def get_data():  # Get data via API, pass exceptions to console if any generated
    # Access API
    api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    try:
        response = requests.get(api_url, timeout=1)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)

    return


def style_card(my_coin, my_price, my_change, my_color, my_gradient, my_gradient_border):
    card_html = dbc.Card(
        html.Div(
            [
                html.H4(  # Our asset name font size/style
                    [my_coin],  # full_name of asset
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
                        # Either change the number of decimals by changing the round(number,places) statement or the
                        # quoteblock width down at the end
                        html.Span(
                            f"${round(my_price, 5):,}",
                            style={
                                "font-size": "90%",
                                "color": "white",
                                "text-align": "left",
                                "padding-left": "20px",
                            },
                        ),
                        html.Span(
                            f"{round(my_change, 2):+}%",
                            style={
                                "font-size": "90%",
                                "color": my_color,
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
                "background-image": my_gradient,
                "border": "1px",
                "solid": "#00000000",
                "border-radius": "5px",
                "border-style": "solid",
                "color": my_gradient_border,
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


def make_card(my_name, my_change, my_price):
    colors = {
        "text_decline": "#C70000",  # Red
        "text_rally": "#00C700",  # Green
        "text_unchanged": "#A8A8A8",  # Off-white
        "gradient_decline": "linear-gradient(0deg,#870900,#000000 95%)",
        "gradient_border_decline": "#940000",
        "gradient_rally": "linear-gradient(0deg,#008709,#000000 95%)",
        "gradient_border_rally": "#009400",
        "gradient_unchanged": "linear-gradient(0deg,#A8A8A8,#000000 95%)",
        "gradient_border_unchanged": "#949494",
    }

    # Define the cases and their corresponding values
    switch_cases = {
        my_change < 0: (
            colors["text_decline"],
            colors["gradient_decline"],
            colors["gradient_border_decline"],
        ),
        my_change > 0: (
            colors["text_rally"],
            colors["gradient_rally"],
            colors["gradient_border_rally"],
        ),
    }

    # Get the values based on the condition
    color, gradient_fill, gradient_border = switch_cases.get(True, (
        colors["text_unchanged"],
        colors["gradient_unchanged"],
        colors["gradient_border_unchanged"],
    ))

    return style_card(my_name, my_price, my_change, color, gradient_fill, gradient_border)

@app.callback(Output(cards, "children"), Input(interval, "n_intervals"))
def update_cards(_):
    # Get our coin data
    coin_data = get_data()

    if coin_data is None or type(coin_data) is dict:  # Catch none type exception
        return dash.no_update

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

    # Renamed columns - original:new name -- You can change these, but you need to alter their references in the rest of
    # the code...
    renamedPairsList = {
        "id": "asset_id",
        "symbol": "ticker",
        "name": "full_name",
        "current_price": "price",
        "total_volume": "volume",
        "price_change_percentage_24h": "net_change_percent",
    }

    # Process scraped data into pandas dataframe
    df_quotes = pd.DataFrame.from_dict(coin_data, orient="columns")
    # Drop columns we don't need - helps when debugging
    df_quotes = df_quotes.drop(columns=dropList, axis=1)
    # Rename columns for ease of reference/debugging
    df_quotes = df_quotes.rename(columns=renamedPairsList)
    # Sort based on volume, descending order
    df_quotes = df_quotes.sort_values(by="volume", ascending=False)
    # Reindex dataframe for ease of reference
    df_quotes = df_quotes.reset_index(drop=True)

    # Using list comprehension to create coin_cards
    coin_cards = [
        make_card(coin_name, net_change, price)
        for coin_name, net_change, price in zip(
            df_quotes["full_name"], df_quotes["net_change_percent"], df_quotes["price"]
        )
    ]

    # Used in assigning cards to quoteblock vars -- must match length of 'coins' list above...
    quote_block_var_names = [
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

    quote_block_vars = {var: card for var, card in zip(quote_block_var_names, coin_cards)}

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
                # Using list comprehension to create the Grid
                dmc.Grid(
                    [quote_block_vars[var] for var in quote_block_var_names],
                    align="center",
                    justify="center",
                ),
            ]
        )
    ]

    return card_layout

# Run the App
if __name__ == "__main__":
    app.run_server(debug=True)
