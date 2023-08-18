import plotly.graph_objects as go
import plotly.offline as offline

# Sample data - Note the <br> in the second row second cell
data = [
    ['John', 'Doe', 'New York', 'United States'],
    ['Jane', 'Smith<br>Smithson', 'London', 'United Kingdom'],
    ['Michael', 'The<br>Quick<br>Brown<br>Fox<br>Jumped<br>Over<br>The<br>Lazy<br>Dog', 'Paris', 'France'],
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
    cells=dict(values=list(zip(*data)), font=dict(size=12)),
    columnwidth=[100, 100, 100, 100],
)

# Set the layout
layout = go.Layout(
    title='Sample Datatable',
)

figure = go.Figure(data=[datatable], layout=layout)

# Save to HTML file
offline.plot(figure, filename='datatable.html', auto_open=True)