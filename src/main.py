import os

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import callback, dcc, html
from dash.dependencies import Input, Output

from utils.utils import PROJECT_DIR


class NetflixAnalysis:
    """Analiza Netflix dataset ładowanie danych i init dash app."""

    def __init__(self):
        self.netflix_df = self._load_data()
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):

        # self.app.layout = dbc.Container([
        #     html.Div([
        #     html.H1("Netflix Data Visualisation"), 
        #     dcc.Graph(id='top-reviewed-movies', figure=self.plot_top_reviewed_movies()),
        #     dcc.Graph(id='top-genres-movies', figure=self.plot_top_genres_movies())             
        #     ]), 
        #     self.table_top_reviewed()],   
        # )
        # add some padding.

        self.app.layout = dbc.Container([dbc.Row(dbc.Col([html.H1("Netflix Data Visualisation", style={
            'fontSize': 60,
            'textAlign': 'center',
            'color': '#800080',
            'padding-bottom': '5rem'
        }, )], width={
            'size': 6,
            'offset': 3
        }, ), ), dbc.Row([dbc.Col(dcc.Graph(id='top-reviewed-movies', figure=self.plot_top_reviewed_movies())),
                          dbc.Col([self.table_top_reviewed()], width={
                              'size': 4,
                              'order': 2
                          }, )]), dbc.Row(dbc.Col(dcc.Graph(id='top-genres-movies', figure=self.plot_top_genres_movies()))),
                                         dbc.Row([dbc.Col([dcc.Input(id='input1', type='text', debounce=True, value=""), html.Div(id='output')])  # [
                                                  #     html.P('Enter actor name'),
                                                  #     dcc.Input(id='num', type='text', debounce=True),
                                                  #     html.P(id='err', style={'color': 'red'}),
                                                  #     html.P(id='out')
                                                  # ]
                                                  #     )
                                                  # )
                                                  ])])

    def setup_callbacks(self):

        @callback(Output("output", "children"), Input("input1", "value"), )
        def update_output(input1):
            data = self.netflix_df.drop_duplicates('title', keep='first')[["title", "stars"]]
            data2 = data[data['stars'].str.contains(input1)]
            print(data2)
            title = data2['title']
            return f'Films: {title.values}'

    # @callback(
    #     Output('out', 'children'),
    #     Output('err', 'children'),
    #     Input('num', 'value')
    # )  
    # def update_output(self):
    #     # return f'Actor: {input1}'
    #     # return self.searching_actor(input1)
    #     if self.netflix_df["stars"] is None:
    #         return '', ''

    #     if input in self.netflix_df["stars"].values:
    #         return f"Actor found: {input}", ''
    #     else:
    #         return "Actor not found", ''

    # def searching_actor(self):
    #     if self.update_output.input1 in self.netflix_df["stars"].values:
    #         return f"Actor found: {self.update_output.input1}"
    #     else:
    #         return "Actor not found"

    def plot_top_reviewed_movies(self):
        """Funkcja zwracajaca wykres najlepiej ocenianych filmow."""
        top_reviewed = self.netflix_df.drop_duplicates('title', keep='first').nlargest(10, "rating")[
            ["title", "rating"]]  # wybor 10 filmow z najwieksza wartoscia w 'rating' zapisujac 1 wynik, aby nie bylo powtorek
        colors = ['#ff0087']
        fig = px.bar(top_reviewed, x='rating', y='title', orientation='h', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='Rating',
                          yaxis_title='Movie Title',
                          title="Top 10 Best Reviewed Movies",
                          title_font=dict(size=20, color='black', family='Arial', weight='bold'),
                          title_x=0.5)
        return fig

    def plot_top_genres_movies(self):
        """"Funkcja zwracajaca wykres najczesciej wystepujacych gatunkow filmow."""
        dictionary = {}  # Stworzenie slownika

        for genre in self.netflix_df["genre"]:  # Przechodzimy przez cala koumne genre
            if type(genre) is not str:  # Rozwiaznie problemu zle wprowadzonych danych w jednym z filmow
                continue
            if ',' not in genre:  # Jeżeli w 'genre' nie ma kilku gatunkow przypisanych do jednego filmu
                self._update_dictionary(dictionary, genre)
            else:  # Jeżeli mamy przypisane wiecej niz jeden gatunek do filmu
                for element in genre.split(', '):  # rozdzielanie gatunkow po przecinku
                    self._update_dictionary(dictionary, element)

        genre_counts_df = pd.DataFrame.from_dict(data=dictionary, orient='index', columns=['counts'])  # Zmiana typu z listy na dataframe
        genre_counts = genre_counts_df['counts'].sort_values(ascending=False).head(5)  # Sortowanie wartosci malejaco i wybranie 5
        labels = genre_counts.index  # Etykiety
        values = genre_counts.values  # Wartosci do wykresu
        colors = ['#ffe0ee', '#ffc2db', '#ffa9c7', '#ff679d', '#ff0087']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors))])
        fig.update_layout(title_text='Top 5 Popular Genres', title_font=dict(size=20, color='black', family='Arial', weight='bold'), title_x=0.5)
        return fig

    def table_top_reviewed(self):
        # review_sort = self.netflix_df.drop_duplicates('title', keep='first').sort_values('rating', ascending=False)[["title", "rating"]] #sortowanie danych z ratings

        review_sort = self.netflix_df.drop_duplicates('title', keep='first')[["title", "rating"]]
        columnDefs = [{
            'field': 'title',
            'sortable': False
        }, {
            'field': 'rating'
        }  # {"name": "Rating", "id": "rating", "type": "numeric"}
        ]

        table = html.Div([dag.AgGrid(id="row-sorting-simple", rowData=review_sort.to_dict("records"), columnDefs=columnDefs, defaultColDef={
            "filter": True
        }, columnSize="sizeToFit", dashGridOptions={
            "animateRows": False
        }), ], )
        # table = dash_table.DataTable(review_sort.to_dict('records'),
        # table = dash_table.DataTable(
        #     review_sort.to_dict('records'),
        #     columnDefs=columnDefs,
        #     defaultColDef={"filter": True},
        #     # sort_action="native", #umozliwia sortowanie
        #     style_header={
        #         'backgroundColor': 'pink',
        #         'fontWeight': 'bold'
        #     },
        #     style_data={
        #         'whiteSpace': 'auto',
        #         'height': 'auto'
        #     },
        #     style_table={
        #         'height': '300px', 
        #         'overflowY': 'auto'
        #     },
        #     style_cell={
        #         'textAlign': 'left'
        #     },
        #     style_cell_conditional=[
        #         {'if': {'column_id': 'title'},
        #          'width': 'auto'},
        #         {'if': {'column_id': 'rating'},
        #           'width': '90px'}
        #     ],     
        # ) #zapisanie posortowanych danych do tabeli
        return table

    @staticmethod
    def _update_dictionary(dictionary, genre):
        if genre in dictionary:  # Jezeli gatunek jest juz zapisany w slowniczku dodajemy licznik +1, w przeciwnym przypadku zapisujemy w slowniku i ustawiamy licznik na 1
            dictionary[genre] = dictionary[genre] + 1
        else:
            dictionary[genre] = 1

    @staticmethod
    # Załadowanie datasetu
    def _load_data():
        file_path = os.path.join(PROJECT_DIR, "src", "data", "n_movies.csv")
        return pd.read_csv(file_path)

    def run_server(self):
        # Uruchomienie serwera Dash
        self.app.run_server(debug=True)


if __name__ == "__main__":
    analysis = NetflixAnalysis()
    analysis.run_server()
