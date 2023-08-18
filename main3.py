import plotly.graph_objects as go

# Define the data for the first pie chart
labels1 = ['Beef', 'Chicken', 'Pork']
values1 = [25, 50, 25]

# Define the data for the second pie chart
labels2 = ['Milk', 'Cheese', 'Eggs']
values2 = [50, 25, 25]

# Define the data for the third pie chart
labels3 = ['Cows', 'Pigs', 'Chickens']
values3 = [33, 33, 33]

# Create separate figures for each pie chart
fig1 = go.Figure(data=[go.Pie(labels=labels1, values=values1)])
fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2)])
fig3 = go.Figure(data=[go.Pie(labels=labels3, values=values3)])

# Save each pie chart as a separate HTML file
fig1.write_html('pie_chart1.html')
fig2.write_html('pie_chart2.html')
fig3.write_html('pie_chart3.html')