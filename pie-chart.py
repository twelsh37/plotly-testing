import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

# Create the data for the pie charts
labels = ["Category A", "Category B", "Category C"]
values1 = [20, 40, 40]
values2 = [40, 20, 40]
values3 = [40, 40, 20]

# Create the hovertemplate for Pie Chart 1, displaying values for each category and the sum
hovertemplate_1 = (
    "<b>%{label}</b><br>Pie Chart 1: %{value}<br>"
    "Pie Chart 2: %{data.values[0]}<br>"
    "Pie Chart 3: %{data.values[1]}<br>"
    "<br>"
    "Sum of %{label}: %{customdata[0]}<br>"
)

# Create the hovertemplate for Pie Charts 2 and 3, displaying values only
hovertemplate_2 = "<b>%{label}</b><br>Pie Chart 2: %{value}<br>"
hovertemplate_3 = "<b>%{label}</b><br>Pie Chart 3: %{value}<br>"

# Calculate the sum of the values for each category in Pie Chart 1
sum_category_a = sum([values1[0], values2[0], values3[0]])
sum_category_b = sum([values1[1], values2[1], values3[1]])
sum_category_c = sum([values1[2], values2[2], values3[2]])

# Create the subplots with 1 row and 3 columns
fig = make_subplots(
    rows=1,
    cols=3,
    specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
    subplot_titles=["Pie Chart 1", "Pie Chart 2", "Pie Chart 3"],
)

# Add the first pie chart to the subplot
fig.add_trace(
    go.Pie(
        labels=labels,
        values=values1,
        hovertemplate=hovertemplate_1,
        textinfo="value",
        customdata=[sum_category_a, sum_category_b, sum_category_c],
    ),
    row=1,
    col=1,
)

# Add the second pie chart to the subplot
fig.add_trace(
    go.Pie(
        labels=labels, values=values2, hovertemplate=hovertemplate_2, textinfo="value"
    ),
    row=1,
    col=2,
)

# Add the third pie chart to the subplot
fig.add_trace(
    go.Pie(
        labels=labels, values=values3, hovertemplate=hovertemplate_3, textinfo="value"
    ),
    row=1,
    col=3,
)

# Set the hovermode to 'closest' for the subplot
fig.update_layout(hovermode="closest")

# Plot the figure
plot(fig)
