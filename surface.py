import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.offline as offline
fig = go.Figure(
data=[
go.Surface(
x=list(range(1,21)),
y=list(range(1,11)),
z=np.random.random(size=(21,11)).T
)
]
)
fig.update_layout(
autosize=False,
width=1200,
height=800,
scene=dict( # Adding explicit x/y ranges
xaxis = dict(range=[1,21]),
yaxis = dict(range=[1,11]),
),
)

# Save the fig as an HTML file
offline.plot(fig, filename='surface.html', auto_open=True)