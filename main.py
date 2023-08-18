import plotly.graph_objects as go

# Sample data
data = [
    ['John', 'Doe', 'New York', 'United States'],
    ['Jane', 'Smith', 'London', 'United Kingdom'],
    ['Michael', 'Johnson', 'Paris', 'France'],
    ['Emily', 'Brown', 'Sydney', 'Australia'],
    ['David', 'Lee', 'Tokyo', 'Japan'],
    ['Sarah', 'Wilson', 'Berlin', 'Germany'],
    ['Daniel', 'Taylor', 'Toronto', 'Canada'],
    ['Olivia', 'Anderson', 'Rome', 'Italy'],
    ['Matthew', 'Thomas', 'Madrid', 'Spain'],
    ['Emma', 'Roberts', 'Moscow', 'Russia']
]

# Create the datatable
datatable = go.Table(
    header=dict(values=['First Name', 'Last Name', 'City', 'Country']),
    cells=dict(values=list(zip(*data)),height=60, font=dict(size=12)),
    columnwidth=[100, 100, 100, 100],
)

# Set the layout
layout = go.Layout(
    title='Sample Datatable',
)

# Create the figure
figure = go.Figure(data=[datatable], layout=layout)

# Display the figure
figure.show()