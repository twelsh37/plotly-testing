import plotly.graph_objects as go
import plotly.offline as offline

# Sample data
# I hijacked last name for my tests as i wanted to have some data that was valid and single row but the first three
# rows have last names that are just rediculous sentences to fill the cell. As can be seen,the cell expands to take
# the content.
data = [
    ['John', f'a really long line of text, that if you keep going gets rediculously rediculous. \n\nI dont even know '
             f'if I '
             'can spell', 'New York',
     'United States'],
    ['Jane', 'a really long line of text, that if you keep going gets rediculously rediculous. I do even know if I '
             'can spell a really long line of text, that if you keep going gets rediculously rediculous. I do even '
             'know if I '
             'can spell', 'London', 'United Kingdom'],
    ['Michael', 'a really long line of text, that if you keep going gets rediculously rediculous. I do even know if I '
             'can spell a really long line of text, that if you keep going gets rediculously rediculous. I do even know if I '
             'can spell a really long line of text, that if you keep going gets rediculously rediculous. I do even know if I '
             'can spell', 'Paris', 'France'],
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
    # setting cells height to 60
    cells=dict(values=list(zip(*data)), height=20, font=dict(size=12)),
    columnwidth=[50, 10, 50, 50]
)

# Set the layout
layout = go.Layout(
    title='Sample Datatable',
)

# Create the figure
figure = go.Figure(data=[datatable], layout=layout)

# Save the figure as an HTML file
offline.plot(figure, filename='datatable.html', auto_open=True)