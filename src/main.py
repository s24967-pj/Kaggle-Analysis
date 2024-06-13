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

    def run_server(self):
        """Uruchomienie serwera Dash."""
        self.app.run_server(debug=True)

    def setup_layout(self):
        """Ustawienie layoutu aplikacji."""
        self.app.layout = dbc.Container([self.create_header(), self.create_top_reviewed_section(), self.create_top_genres_section(),
            self.create_input_section(), self.create_actor_movie_table_section()])

    @staticmethod
    def create_header():
        return dbc.Row(dbc.Col(html.H1("Netflix Data Visualisation", style={
            'fontSize': 60,
            'textAlign': 'center',
            'color': '#800080',
            'padding-bottom': '5rem'
        }), width={
            'size': 6,
            'offset': 3
        }))

    def create_top_reviewed_section(self):
        """Funkcja zwracajaca sekcje z wykresem najlepiej ocenianych filmow."""
        return dbc.Row([dbc.Col(dcc.Graph(id='top-reviewed-movies', figure=self.plot_top_reviewed_movies())),
            dbc.Col(self.table_top_reviewed(), width={
                'size': 4,
                'order': 2
            })])

    def create_top_genres_section(self):
        """Funkcja zwracajaca sekcje z wykresem najczesciej wystepujacych gatunkow filmow."""
        return dbc.Row(dbc.Col(dcc.Graph(id='top-genres-movies', figure=self.plot_top_genres_movies())))

    @staticmethod
    def create_input_section():
        """Funkcja zwracajaca input do wprowadzania danych."""
        return dbc.Row(dbc.Col([dcc.Input(id='input1', type='text', debounce=True, value=""), html.Div(id='output')]))

    def create_actor_movie_table_section(self):
        """Funkcja zwracajaca sekcje z tabela aktorow i filmow."""
        return dbc.Row([dbc.Col([dcc.Input(id='actor-input', type='text', placeholder='Enter actor name', debounce=True),
            html.Div(id='actor-movie-table', children=self.create_actor_movie_table(self.netflix_df))])])

    def create_actor_movie_table(self, df):
        """Funkcja zwracajaca tabele z aktorami i filmami."""
        columnDefs = [{
            'field': 'title',
            'headerName': 'Movie Title'
        }, {
            'field': 'stars',
            'headerName': 'Actors'
        }]
        table = dag.AgGrid(rowData=df[['title', 'stars']].drop_duplicates().to_dict("records"), columnDefs=columnDefs, defaultColDef={
            "filter": True,
            "sortable": True
        }, columnSize="sizeToFit", dashGridOptions={
            "animateRows": False
        })
        return table

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
        """Funkcja zwracajaca tabelę z najlepiej ocenianymi filmami."""
        review_sort = self.netflix_df.drop_duplicates('title', keep='first')[["title", "rating"]]
        columnDefs = [{
            'field': 'title',
            'sortable': False
        }, {
            'field': 'rating'
        }]

        table = html.Div([dag.AgGrid(id="row-sorting-simple", rowData=review_sort.to_dict("records"), columnDefs=columnDefs, defaultColDef={
            "filter": True
        }, columnSize="sizeToFit", dashGridOptions={
            "animateRows": False
        })])
        return table

    def setup_callbacks(self):
        """Ustawienie callbacków."""

        @callback(Output("output", "children"), Input("input1", "value"))
        def update_output(input1):
            data = self.netflix_df.drop_duplicates('title', keep='first')[["title", "stars"]]
            data2 = data[data['stars'].str.contains(input1, na=False)]
            title = data2['title']
            return f'Films: {title.values}'

        @callback(Output("actor-movie-table", "children"), Input("actor-input", "value"))
        def update_actor_movie_table(actor_name):
            data = self.netflix_df.drop_duplicates('title', keep='first')[["title", "stars"]]
            if actor_name:
                filtered_data = data[data['stars'].str.contains(actor_name, na=False)]
            else:
                filtered_data = data

            columnDefs = [{
                'field': 'title',
                'headerName': 'Movie Title'
            }, {
                'field': 'stars',
                'headerName': 'Actors'
            }]
            table = dag.AgGrid(rowData=filtered_data.to_dict("records"), columnDefs=columnDefs, defaultColDef={
                "filter": True,
                "sortable": True
            }, columnSize="sizeToFit", dashGridOptions={
                "animateRows": False
            })
            return table

    @staticmethod
    def _update_dictionary(dictionary, genre):
        """Funkcja pomocnicza do tworzenia slownika z gatunkami filmow."""
        if genre in dictionary:  # Jezeli gatunek jest juz zapisany w slowniczku dodajemy licznik +1, w przeciwnym przypadku zapisujemy w slowniku i ustawiamy licznik na 1
            dictionary[genre] = dictionary[genre] + 1
        else:
            dictionary[genre] = 1

    @staticmethod
    def _load_data():
        """Funkcja wczytujaca dane."""
        file_path = os.path.join(PROJECT_DIR, "src", "data", "n_movies.csv")
        return pd.read_csv(file_path)


if __name__ == "__main__":
    analysis = NetflixAnalysis()
    analysis.run_server()
