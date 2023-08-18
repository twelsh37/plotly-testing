import plotly.graph_objects as go
import plotly.offline as offline

fig = go.Figure()

fig.add_barpolar(
    r=[1],
    theta=[0],
    width=[180],
)

fig.add_barpolar(
    base=0,
    r=[1],
    theta=[0],
    width=[90],
)

fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.5, marker_color='red')


# Save the fig as an HTML file
offline.plot(fig, filename='polar_bar.html', auto_open=True)