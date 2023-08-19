# Updated code for TallTim's Quoteboard v0.04. So I suppose this makes it v0.05?
# This is a rewrite of teh code to get rid of unneccasary global variables and a chance to play with the new
# Python 3.10 match/case statement.
# Along te way I changed for loops to list comprehensions and added a few comments to help me remember what I did.
# Added doc strings and error checking
# I have also stripped out the test scrape data for conciceness. This version only works with live data from coingeko
# TallTim's Quoteboard v0.04
# Styled quoteboard based on the application card example by AnneMarieW from here ("Card Group"):
# https://dash-building-blocks.com/app_cards

import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import dash_mantine_components as dmc
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])

# Set App title
app.title = "TallTim's Quoteboard"

# Assorted Variables
interval = 6000  # update frequency - 1000 = 1 second, so 6 seconds here
interval = dcc.Interval(interval=interval)
cards = html.Div()


def get_data():
    """
    Get data from the API.

    Returns:
        dict: The data retrieved from the API.
    """
    api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    try:
        response = requests.get(api_url, timeout=1)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)

    return


def style_card(my_coin, my_price, my_change, my_color, my_gradient, my_gradient_border):
    """
    Create a styled card with the given parameters.

    Args:
        my_coin (str): The name of the coin.
        my_price (float): The price of the coin.
        my_change (float): The net change percentage of the coin.
        my_color (str): The color of the text.
        my_gradient (str): The background gradient of the card.
        my_gradient_border (str): The border gradient of the card.

    Returns:
        dash.development.base_component.Component: The styled card.
    """
    card_html = dbc.Card(
        html.Div(
            [
                html.H4(
                    [my_coin],
                    style={
                        "font-size": "160%",
                        "color": "white",
                        "text-align": "left",
                        "padding-left": "20px",
                        "padding-top": "20px",
                    },
                ),
                html.H4(
                    [
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
        style={
            "width": "270px",
            "height": "130px",
            "padding-right": "10px",
            "background": "#00000000",
        },
    )

    return card_html


def make_card(coin_name, net_change, price):
    """
    Create a card by applying styles to the given coin data.

    Args:
        coin_name (str): The name of the coin.
        net_change (float): The net change percentage of the coin.
        price (float): The price of the coin.

    Returns:
        dash.development.base_component.Component: The styled card.
    """
    # Using list comprehension to create the Grid
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
    # Using a dictionary called switch_cases to define the different cases and their corresponding values.
    # The keys in the dictionary are the conditions, and the values are tuples containing the color values.
    # Use the get() method to retrieve the values based on the condition. If none of the conditions match, it falls back
    # to the default case, which represents no change in price.

    # This approach provides a more concise and readable way to handle multiple conditions, simulating a switch
    # statement in Python. (Python 3.10 onwards)
    switch_cases = {
        net_change
        < 0: (  # Decreased price?
            colors["text_decline"],
            colors["gradient_decline"],
            colors["gradient_border_decline"],
        ),
        net_change
        > 0: (  # Increased price?
            colors["text_rally"],
            colors["gradient_rally"],
            colors["gradient_border_rally"],
        ),
    }

    # Get the values based on the condition
    color, gradient_fill, gradient_border = switch_cases.get(
        True,
        (  # Rare, but no change in price?
            colors["text_unchanged"],
            colors["gradient_unchanged"],
            colors["gradient_border_unchanged"],
        ),
    )

    return style_card(
        coin_name, price, net_change, color, gradient_fill, gradient_border
    )


@app.callback(Output(cards, "children"), Input(interval, "n_intervals"))
def update_cards(_):
    """
    Update the cards based on the API data.

    Args:
        _: The number of intervals (not used).

    Returns:
        list: The layout of the updated cards.
    """

    coin_data = get_data()

    if coin_data is None or type(coin_data) is dict:
        return dash.no_update

    drop_list = [
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

    renamed_pairs_list = {
        "id": "asset_id",
        "symbol": "ticker",
        "name": "full_name",
        "current_price": "price",
        "total_volume": "volume",
        "price_change_percentage_24h": "net_change_percent",
    }
    try:
        # Process scraped data into pandas dataframe
        df_quotes = pd.DataFrame.from_dict(coin_data, orient="columns")

        # Drop columns we don't need - helps when debugging
        df_quotes = df_quotes.drop(columns=drop_list, axis=1)

        # Rename columns for ease of reference/debugging
        df_quotes = df_quotes.rename(columns=renamed_pairs_list)

        # Sort based on volume, descending order
        df_quotes = df_quotes.sort_values(by="volume", ascending=False)

        # Reindex dataframe for ease of reference
        df_quotes = df_quotes.reset_index(drop=True)

        coin_cards = [
            make_card(*row)
            for row in df_quotes[
                ["full_name", "net_change_percent", "price"]
            ].to_numpy()
        ]

        quote_block_var_names = [f"quoteBlock_{i}" for i in range(1, 13)]
        quote_block_vars = dict(zip(quote_block_var_names, coin_cards))

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
                    dmc.Grid(
                        [quote_block_vars[var] for var in quote_block_var_names],
                        align="center",
                        justify="center",
                    ),
                ]
            )
        ]

        return card_layout

    except Exception as e:
        print(f"Error occurred: {e}")
        return dash.no_update


app.layout = dbc.Container(
    [interval, cards], className="my-5", style={"background": "#00000000"}
)

if __name__ == "__main__":
    app.run_server(debug=True)
