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
        """Konstruktor."""
        self.netflix_df = self._load_data()  # załadowanie danych
        self._clean_df()  # funkcja do czyszczenia danych w pliku
        self.app = dash.Dash(__name__, external_stylesheets=[
                             dbc.themes.BOOTSTRAP])  # init bootstrapa
        self.setup_layout()
        self.setup_callbacks()

    def _clean_df(self):
        """Oczyszczanie pliku csv"""
        self.netflix_df.drop_duplicates(
            'title', keep='first', inplace=True)  # usuniecie duplikatow z df
        # roroznienie danych zapisanych po przecinku w kolumnie genre
        self.netflix_df['genre'] = self.netflix_df['genre'].str.split(', ')

    def run_server(self):
        """Uruchomienie serwera Dash."""
        self.app.run_server(debug=True)

    def setup_layout(self):
        """Ustawienie layoutu aplikacji."""
        self.app.layout = dbc.Container([self.create_header(), self.create_top_reviewed_section(), self.create_top_genres_section(),
                                         # stworzenie containera z metodami tworzacymi widok kolumn i rzedow
                                         self.create_actor_movie_table_section()])

    @staticmethod
    def create_header():
        """Funkcja zwracajaca naglowek."""
        return dbc.Row(dbc.Col(html.H1("Netflix Data Visualisation", style={
            'fontSize': 50,
            'textAlign': 'center',
            'color': 'black',
            'padding-bottom': '5rem',
            'padding-top': '3rem'
        }), width={
            'size': 6,  # 6/12
            'offset': 3  # odleglosc
        }))

    def create_top_reviewed_section(self):
        """Funkcja zwracajaca sekcje z wykresem najlepiej ocenianych filmow."""
        return dbc.Row([dbc.Col(dcc.Graph(id='top-reviewed-movies', figure=self.plot_top_reviewed_movies())),
                        dbc.Col(self.table_top_reviewed(), width={
                            'size': 4,
                            'order': 2
                        })])  # rzad zawierajacy dwie kolumny - z graphem i tabela

    def create_top_genres_section(self):
        """Funkcja zwracajaca sekcje z wykresem najczesciej wystepujacych gatunkow filmow."""
        return dbc.Row([
            dbc.Col([
                dbc.Button('Change values', outline=True, color="info",
                       className="me-1", id='btn-nclicks-1', n_clicks=1)
            ], width={
                'size': 1,
                'offset': 2
            }, style={'padding-top': 200}),  # ustawienie przysisku na srodku
            dbc.Col(html.Div(id='plot-top-genres', children=dcc.Graph(figure=self.plot_top_genres_movies())),
                    width={
                'size': 6
            })
        ])  # 1R 2K z przyciskiem i wykresem kolwoym

    def create_actor_movie_table_section(self):
        """Funkcja zwracajaca sekcje z tabela aktorow i filmow."""
        return dbc.Row([dbc.Col([dcc.Input(id='actor-input', type='text', placeholder='Enter actor name', debounce=True),
                                 # rzad z tabela aktorow i filmow, input do wprowadzania danych
                                 html.Div(id='actor-movie-table', children=self.create_actor_movie_table())])])

    def create_actor_movie_table(self):
        """Funkcja zwracajaca tabele z aktorami i filmami."""
        columnDefs = [{
            'field': 'title',
            'headerName': 'Movie Title'
        }, {
            'field': 'stars',
            'headerName': 'Actors'
        }]  # zdefiniowanie kolumn tabeli, nadanie nazw
        table = dag.AgGrid(rowData=self.netflix_df[['title', 'stars']].to_dict("records"), columnDefs=columnDefs, defaultColDef={
        }, columnSize="sizeToFit", dashGridOptions={
            "animateRows": False
        })  # tworzenie tabeli z danymi z pliku csv
        return table

    def plot_top_reviewed_movies(self):
        """Funkcja zwracajaca wykres najlepiej ocenianych filmow."""
        top_reviewed = self.netflix_df.nlargest(10, "rating")[
            ["title", "rating"]]  # wybor 10 filmow z najwieksza wartoscia w 'rating'
        top_reviewed = top_reviewed.sort_values(
            by="rating", ascending=True)  # sortowanie danych malejaco
        colors = ['#ff0087']
        fig = px.bar(top_reviewed, x='rating', y='title',
                     orientation='h', color_discrete_sequence=colors)
        fig.update_layout(xaxis_title='Rating',
                          yaxis_title='Movie Title',
                          title="Top 10 Best Reviewed Movies",
                          title_font=dict(size=20, color='#89CFF0',
                                          family='Arial', weight='bold'),
                          title_x=0.5)
        return fig

    def plot_top_genres_movies(self):
        """"Funkcja zwracajaca wykres najczesciej wystepujacych gatunkow filmow."""
        df_genres = self.netflix_df.explode(
            'genre')  # rozdzielenie gatunkow na osobne rzedy - kilka do jednego filmu
        genre_counts = df_genres['genre'].value_counts().head(
            5)  # zliczenie 5 najczestszych
        labels = genre_counts.index  # Etykiety
        values = genre_counts  # Wartosci do wykresu
        colors = ['#ffe0ee', '#ffc2db', '#ffa9c7', '#ff679d', '#ff0087']
        fig = go.Figure(
            data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors))])
        fig.update_layout(title_text='Top 5 Popular Genres', title_font=dict(
            size=20, color='#89CFF0', family='Arial', weight='bold'), title_x=0.5)
        return fig

    def table_top_reviewed(self):
        """Funkcja zwracajaca tabelę z najlepiej ocenianymi filmami."""
        review_sort = self.netflix_df[["title", "rating"]
                                      ]  # z csv bierzemy 2 kolumy -title i rating
        columnDefs = [{
            'field': 'title',
            'sortable': False
        }, {
            'field': 'rating'
        }]  # zdef kolumn
        table = html.Div([dag.AgGrid(id="row-sorting-simple", rowData=review_sort.to_dict("records"), columnDefs=columnDefs, defaultColDef={
            "filter": True
        }, columnSize="sizeToFit", dashGridOptions={
            "animateRows": False
            # tworzymy tabele, todict aby dane byly przekazane w odpowiedni sposob 'records’ : list like [{column -> value},{tytul -> Avatar}] - zwracamy liste slownikow
        })])
        return table

    def setup_callbacks(self):
        """ustawienie callbackow"""
        @callback(  # eventy do odbierania zdarzen, aby akutalizowac aplikacje, aby apka byla responsywna
            # id i children jako komponent ktory chce sae zaaktualizowac
            Output("actor-movie-table", "children"),
            # id ktory nasluchujemy na zdarzenie i value jako wartosc przekazywana do metody i wykorzystywana do przefiltrowania danych
            Input("actor-input", "value")
        )
        def update_actor_movie_table(actor_name):
            data = self.netflix_df[["title", "stars"]]
            if actor_name:
                # sprawdzamy czy zostala wpisana wartosc i czy kolumna ja zawiera
                filtered_data = data[data['stars'].str.contains(
                    actor_name, na=False)]
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
                "filter": False,
                "sortable": True
            }, columnSize="sizeToFit", dashGridOptions={
                "animateRows": False
            })  # zwracane przefiltrowane dane w tabeli

            return table  # zwracana jest nowa zupdatowana do naszych wyszukiwan tabela

        @callback(
            Output('plot-top-genres', 'children'),
            Input('btn-nclicks-1', 'n_clicks')
        )
        def update_pie_chart(n_clicks):
            fig = self.plot_top_genres_movies()
            if n_clicks % 2 == 0:
                # jesli modulo z liczby klikniec rowna sie 0 pokazujemy dane bez %
                return dcc.Graph(figure=fig.update_traces(hoverinfo='label+percent', textinfo='value'))
            else:
                # jak modulo inne to graf sie nie zmienia
                return dcc.Graph(figure=fig)

    @staticmethod
    def _load_data():
        """Funkcja wczytujaca dane."""
        file_path = os.path.join(PROJECT_DIR, "src", "data", "n_movies.csv")
        return pd.read_csv(file_path)


if __name__ == "__main__":
    analysis = NetflixAnalysis()
    analysis.run_server()
