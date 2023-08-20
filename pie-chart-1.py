import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

# Create the data for the pie charts
labels = ["Category A", "Category B", "Category C"]
values1 = [33, 33, 33]
values2 = [20, 40, 20]
values3 = [50, 25, 25]

# Create the hovertemplate for Pie Chart 1, displaying values and sum
hovertemplate_1 = "<b>%{label}</b><br>Pie Chart 1: %{value}<br>" \
                  "Pie Chart 2: %{data.values[0]}<br>" \
                  "Pie Chart 3: %{data.values[1]}<br>" \
                  "<br>" \
                  "Sum: %{customdata}<br>"

# Create hovertemplates for Pie Charts 2 and 3, displaying values only
hovertemplate_2 = "<b>%{label}</b><br>Pie Chart 2 : %{value}"
hovertemplate_3 = "<b>%{label}</b><br>Pie Chart 3 : %{value}"

# Create the subplots with 1 row and 3 columns
fig = make_subplots(
    rows=1,
    cols=3,
    specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
    subplot_titles=["Pie Chart 1", "Pie Chart 2", "Pie Chart 3"],
)

# Add the first pie chart to the subplot
fig.add_trace(
    go.Pie(labels=labels, values=values1, hovertemplate=hovertemplate_1, textinfo='value'),
    row=1,
    col=1,
)

# Add the second pie chart to the subplot
fig.add_trace(
    go.Pie(labels=labels, values=values2, hovertemplate=hovertemplate_2, textinfo='value'),
    row=1,
    col=2,
)

# Add the third pie chart to the subplot
fig.add_trace(
    go.Pie(labels=labels, values=values3, hovertemplate=hovertemplate_3, textinfo='value'),
    row=1,
    col=3,
)

# Set the hovermode to 'closest' for the subplot
fig.update_layout(hovermode="closest")

# Plot the figure
plot(fig)
