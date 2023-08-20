# https://www.tutorialspoint.com/how-to-plot-pie-charts-as-subplots-with-custom-size-in-python-plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot

# Create subplots
fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])

# Set traces for the pie chart
fig.add_trace(
    go.Pie(
        values=[16, 15, 12, 6, 5, 4, 42],
        labels=["green", "red", "blue", "yellow", "orange", "purple"],
        domain=dict(x=[0, 0.5]),
        name="colors1",
    ),
    row=1,
    col=1,
)

# Traces for the second pie chart
fig.add_trace(
    go.Pie(
        values=[27, 11, 25, 8, 1, 3, 25],
        labels=["white", "grey", "green", "maroon", "pink", "red"],
        domain=dict(x=[0.5, 1.0]),
        name="colors2",
    ),
    row=1,
    col=2,
)
# Plot an image
plot(fig)
