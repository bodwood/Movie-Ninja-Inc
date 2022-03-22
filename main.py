from dash import dash
from flask import Flask, request, render_template, redirect
import dash_bootstrap_components as dbc
import data.data_parse as dp
from dash import dcc
from dash import html
import predictor as predictor
import warnings
import plotly.graph_objects as go

warnings.filterwarnings('ignore')
server = Flask(__name__)
app = Flask(__name__)
admin_id = "username"
admin_pw = "password"


##Data For Table##
table_gr = dp.table_for_vis()
##Columns From Table##
columns = table_gr["columns"]
columns_for_table = []
for column in columns:
    columns_for_table.append(html.Th(column))
##Rows From Table##
table_rows = table_gr["rows"]
rows_for_table = []
for column in columns:
    rows_for_table.append(html.Th(column))

##Add Adj. Rows##
table_header = [
    html.Thead(html.Tr([
        columns_for_table
    ]))
]
for index, row in table_rows.iterrows():
    rows_for_table.append(html.Tr([html.Td(row["director_name"]),
                                   html.Td(row["num_critic_for_reviews"]),
                                   html.Td(row["duration"]),
                                   html.Td(row["director_facebook_likes"]),
                                   html.Td(row["actor_3_facebook_likes"]),
                                   html.Td(row["actor_2_name"]),
                                   html.Td(row["actor_1_facebook_likes"]),
                                   html.Td(row["gross"]),
                                   html.Td(row["genres"]),
                                   html.Td(row["actor_1_name"]),
                                   html.Td(row["movie_title"]),
                                   html.Td(row["num_voted_users"]),
                                   html.Td(row["cast_total_facebook_likes"]),
                                   html.Td(row["actor_3_name"]),
                                   html.Td(row["plot_keywords"]),
                                   html.Td(row["movie_imdb_link"]),
                                   html.Td(row["num_user_for_reviews"]),
                                   html.Td(row["language"]),
                                   html.Td(row["country"]),
                                   html.Td(row["content_rating"]),
                                   html.Td(row["budget"]),
                                   html.Td(row["title_year"]),
                                   html.Td(row["actor_2_facebook_likes"]),
                                   html.Td(row["imdb_score"]),
                                   html.Td(row["aspect_ratio"]),
                                   html.Td(row["movie_facebook_likes"]),
                                   ]))

##Add Adj. columns##
table_body = [html.Tbody(
    rows_for_table
)]

##Data for vis1##
title_yr_likes = dp.title_yr_likes()
gofig = go.Figure()
date_count = gofig.add_trace(go.Scatter(x=title_yr_likes["title_year"], y=title_yr_likes["num_critic_for_reviews"]))

##Data for vis2##
visd1 = dp.vis_rel_count_temp()

##Data for visd2##
vis_count_by_date2 = dp.vis_count_by_date2()
gofig1 = go.Figure()
visd2 = gofig1.add_trace(go.Bar(x=vis_count_by_date2["duration"], y=vis_count_by_date2["imdb_score"]))

##Navigation Bar Static####
nav = dbc.NavbarSimple(
    children=[html.Form(dbc.NavItem(html.Button(dbc.NavLink("Back"))), action="/main", method="POST"),
              ],
    brand="Data Visualization",
    brand_href="#",
    sticky="top",
    color="#e3f2fd"
)

##Container for table##
table_name = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Raw movie_metadata.csv", style={"color": "black"}),
                        dbc.Table(table_header + table_body,
                                  bordered=True,
                                  dark=True,
                                  hover=True,
                                  responsive=True,
                                  striped=True,
                                  )
                    ]
                )
            ]
        ), html.Hr()
    ],
    className="mt-4",
)

##Container for vis1##
vis1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Number of movie likes per year", style={"color": "black"}),
                        dcc.Graph(
                            figure=date_count
                        )
                    ]
                ),
            ]
        ), html.Hr()
    ],
    className="mt-4",
)

##Container for vis2##
vis2 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Relationship between movie release date and IMDB score", style={"color": "black"}),
                        dcc.Graph(
                            id='rel_count_temp',
                            figure={
                                'data': [
                                    dict(
                                        x=visd1["title_year"],
                                        y=visd1["imdb_score"],
                                        mode='markers',
                                        opacity=0.7,
                                        marker={
                                            'size': 15,
                                            'line': {'width': 0.5, 'color': 'white'}
                                        }
                                    )
                                ],
                                'layout': dict(
                                    xaxis={'type': 'log', 'title': 'Release Year'},
                                    yaxis={'title': 'IMDB Score'},
                                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                    legend={'x': 0, 'y': 1},
                                    hovermode='closest'
                                )
                            }
                        ),
                    ]
                ),
            ]
        ), html.Hr()
    ],
    className="mt-4",
)

##Container vis3 Bar Graph##
vis3 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Number of movie likes per year", style={"color": "black"}),
                        dcc.Graph(
                            figure=visd2
                        )
                    ]
                ),
            ]
        ), html.Hr()
    ],
    className="mt-4",
)

##App for Dash & Bootstrap##
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    server=server,
    routes_pathname_prefix='/visual/'
)
app.title = "Movie Ninja Inc."
app.layout = html.Div([nav, vis2, vis1, vis3, table_name],
                      className="container")

##Login##
@server.route("/", methods=['GET'])
@server.route("/login", methods=['GET'])
def index():
    return render_template('login.html')

##Logout & Invalid login creds.##
@server.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if admin_id == request.form['login'] and admin_pw == request.form['password']:
            return redirect("/main", code=307)
        else:
            return render_template("wronginfo.html")

##Main##
@server.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        return render_template("main.html")
    else:
        return render_template("wronginfo.html")

##Predictions##
@server.route("/predict", methods=["GET","POST"])
def predict():
    if request.method == "POST":
        movie_title = request.values["movie_title"]
        movie_title = movie_title.lower()
        ml_model = predictor.recommend_movie(movie_title)
        cosine_score = predictor.cosine_score(movie_title)
        movie_name = predictor.movie_name_return(movie_title)
        h1_tags = predictor.h1_tag(movie_title)
        p1_tag = predictor.p1_tag(movie_title)
        return render_template("predict.html",
                               movie_title=movie_title,
                               ml_model=ml_model,
                               cosine_score=cosine_score,
                               movie_name=movie_name,
                               h1_tags = h1_tags,
                               p1_tag = p1_tag)

if __name__ == "__main__":
    server.run(debug=True)
