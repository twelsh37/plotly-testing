import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

# Create the data for the pie charts
labels = ["Category A", "Category B", "Category C"]
values1 = [30, 40, 20]
values2 = [25, 35, 30]
values3 = [15, 25, 40]

# Create the hovertemplate for the pie charts
hovertemplate = "<b>%{label}</b><br>Value: %{value}"

# Create the subplots with 1 row and 3 columns
fig = make_subplots(
    rows=1,
    cols=3,
    specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
    subplot_titles=["Pie Chart 1", "Pie Chart 2", "Pie Chart 3"],
)

# Add the first pie chart to the subplot
fig.add_trace(
    go.Pie(values=values1, labels=labels, hovertemplate=hovertemplate),
    row=1,
    col=1,
)

# Add the second pie chart to the subplot
fig.add_trace(
    go.Pie(values=values2, labels=labels, hovertemplate=hovertemplate),
    row=1,
    col=2,
)

# Add the third pie chart to the subplot
fig.add_trace(
    go.Pie(values=values3, labels=labels, hovertemplate=hovertemplate),
    row=1,
    col=3,
)

fig.update_traces(mode="markers+lines")
# Set the hovermode to 'closest' for the subplot
fig.update_layout(hovermode="y unified")

# Plot an image
plot(fig)
