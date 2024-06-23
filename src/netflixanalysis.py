import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import callback, dcc, html
from dash.dependencies import Input, Output

from data import dataframe
import figureservice
import tableservice


class NetflixAnalysis:
    """Analiza Netflix dataset ładowanie danych i init dash app."""

    def __init__(self):
        """Konstruktor."""
        self.figure_service = figureservice.FigureService() 
        self.table_service = tableservice.TableService()
        self.netflix_df = dataframe.DataFrame().get() 
        self.app = dash.Dash(__name__, external_stylesheets=[
                             dbc.themes.BOOTSTRAP])  # init bootstrapa
        self._setup_layout()
        self._setup_callbacks()

    def run_server(self):
        """Uruchomienie serwera Dash."""
        self.app.run_server(debug=True)

    def _setup_layout(self):
        """Ustawienie layoutu aplikacji."""
        self.app.layout = dbc.Container([self._create_header(), self._create_top_reviewed_section(), self._create_top_genres_section(),
                                         # stworzenie containera z metodami tworzacymi widok kolumn i rzedow
                                         self._create_actor_movie_table_section()])

    @staticmethod
    def _create_header():
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

    def _create_top_reviewed_section(self):
        """Funkcja zwracajaca sekcje z wykresem najlepiej ocenianych filmow."""
        return dbc.Row([dbc.Col(dcc.Graph(id='top-reviewed-movies', figure=self.figure_service.plot_top_reviewed_movies(self.netflix_df))),
                        dbc.Col(self.table_service.table_top_reviewed(self.netflix_df), width={
                            'size': 4,
                            'order': 2
                        })])  # rzad zawierajacy dwie kolumny - z graphem i tabela

    def _create_top_genres_section(self):
        """Funkcja zwracajaca sekcje z wykresem najczesciej wystepujacych gatunkow filmow."""
        return dbc.Row([
            dbc.Col([
                dbc.Button('Change values', outline=True, color="info",
                       className="me-1", id='btn-nclicks-1', n_clicks=1)
            ], width={
                'size': 1,
                'offset': 2
            }, style={'padding-top': 200}),  # ustawienie przysisku na srodku
            dbc.Col(html.Div(id='plot-top-genres', children=dcc.Graph(figure=self.figure_service.plot_top_genres_movies(self.netflix_df))),
                    width={
                'size': 6
            })
        ])  # 1R 2K z przyciskiem i wykresem kolwoym

    def _create_actor_movie_table_section(self):
        """Funkcja zwracajaca sekcje z tabela aktorow i filmow."""
        return dbc.Row([dbc.Col([dcc.Input(id='actor-input', type='text', placeholder='Enter actor name', debounce=True),
                                 # rzad z tabela aktorow i filmow, input do wprowadzania danych
                                 html.Div(id='actor-movie-table', children=self.table_service.create_actor_movie_table(self.netflix_df))])])

    def _setup_callbacks(self):
        """ustawienie callbackow"""
        @callback(  # eventy do odbierania zdarzen, aby akutalizowac aplikacje, aby apka byla responsywna
            # id i children jako komponent ktory chce sae zaaktualizowac
            Output("actor-movie-table", "children"),
            # id ktory nasluchujemy na zdarzenie i value jako wartosc przekazywana do metody i wykorzystywana do przefiltrowania danych
            Input("actor-input", "value")
        )
        def _update_actor_movie_table(actor_name):
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
        def _update_pie_chart(n_clicks):
            fig = self.figure_service.plot_top_genres_movies(self.netflix_df)
            if n_clicks % 2 == 0:
                # jesli modulo z liczby klikniec rowna sie 0 pokazujemy dane bez %
                return dcc.Graph(figure=fig.update_traces(hoverinfo='label+percent', textinfo='value'))
            else:
                # jak modulo inne to graf sie nie zmienia
                return dcc.Graph(figure=fig)
