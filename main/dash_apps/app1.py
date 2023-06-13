from io import BytesIO
from os import listdir
from os.path import isfile, join

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
import scipy
import seaborn as sns
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
from scipy.stats import norm

FILENAMES = [f for f in listdir(".") if isfile(join(".", f))]
print(FILENAMES)
# Загрузка исходных данных для работы .
data = pd.read_excel('Копия ДКК А500С за 2020 г. УГМК-Сталь.xlsx')

# Выбираем из таблицы индексы для фильтрации и назначаем тип категории.
data["Марка стали"] = data["Марка стали"].astype("category")
data["Профиль / размер"] = data["Профиль / размер"].astype("category")
steelgrade = data["Марка стали"].drop_duplicates().tolist()
steelsize = data["Профиль / размер"].drop_duplicates().tolist()
data = data.set_index(["Марка стали", "Профиль / размер"])

steelgrade_opts = []# [{"label": i, "value": i} for i in steelgrade]
steelsize_opts =[]# [{"label": i, "value": i} for i in steelsize]
files = [{"label": i, "value": i} for i in FILENAMES]

def test_shapiro(df):
    stats1, p = scipy.stats.shapiro(df)
    if p > 0.05:
        return "Нормальное"
    else:
        return "Не является нормальным"


def test_pirson(df):
    statp1, p = scipy.stats.normaltest(df)
    if p > 0.05:
        return "Нормальное"
    else:
        return "Не является нормальным"


def test_kstest(df, norm):
    statk1, p = scipy.stats.kstest(df, norm)
    if p > 0.05:
        return "Нормальное"
    else:
        return "Не является нормальным "


test_table = np.zeros((5, 3))
test_table = test_table.astype("str")
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",

    },
]
app = DjangoDash('Stats', external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Оценка качества арматуры по механическим свойствам",
                    className="header-title",
                ),
            ],
            style={
                "background-color": "#FFFFFF",
                "position": "absolute",
                "left": "10%",
                "height": "288px",
                "width": "1264px",
                "padding": "16px 0 0 0",
                "text-align": "center",
            },
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children="Выберите файл", className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="files",
                            options=files,
                            value=files[0],
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Выберите марку стали", className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="steelgrade_opts",
                            options=steelgrade_opts,
                            value=steelgrade[0],
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Выберите профиль / размер арматуры",
                            className="menu-title",
                        ),
                        dcc.Dropdown(
                            id="steelsize_opts",
                            options=steelsize_opts,
                            value=steelsize[0],
                        ),
                    ],
                ),
            ],
            style={
                "position": "absolute",
                "left": "10%",
                "top": "15%",
                "height": "288px",
                "width": "1264px",
                "justify-content": "center",
            },
        ),
        html.Div(
            id="attention",
            style={
                "position": "absolute",
                "left": "10%",
                "top": "35%",
                "width": "1264px",
            },
        ),
        html.Div(
            children=[
                dcc.Graph(id="graph_gist", config={"displayModeBar": False}),
            ],
            style={
                "position": "absolute",
                "left": "10%",
                "top": "40%",
                "width": "1264px",
                "justify-content": "center",
            },
        ),
        html.Div(
            children=[
                html.H4(children="Оценка характера распределения:"),
                html.Table(
                    # Заголовок
                    [
                        html.Tr(
                            children=[
                                html.Th(
                                    ["Характеристика"],
                                    style={"border": "1px solid #000"},
                                ),
                                html.Th(
                                    ["Критерий Пирсона"],
                                    style={"border": "1px solid #000"},
                                ),
                                html.Th(
                                    ["Критерий Колмогорова-Смирнова"],
                                    style={"border": "1px solid #000"},
                                ),
                                html.Th(
                                    ["Критерий Шапиро-Уилка"],
                                    style={"border": "1px solid #000"},
                                ),
                            ]
                        )
                    ]
                    +
                    # Тело таблицы
                    [
                        html.Tr(
                            [
                                html.Td(
                                    "Предел текучести",
                                    style={"border": "1px solid #000"},
                                ),
                                html.Td(id="t00", style={"border": "1px solid #000"}),
                                html.Td(id="t01", style={"border": "1px solid #000"}),
                                html.Td(id="t02", style={"border": "1px solid #000"}),
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    "Временное сопротивление",
                                    style={"border": "1px solid #000"},
                                ),
                                html.Td(id="t10", style={"border": "1px solid #000"}),
                                html.Td(id="t11", style={"border": "1px solid #000"}),
                                html.Td(id="t12", style={"border": "1px solid #000"}),
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    "Относительное удлинение",
                                    style={"border": "1px solid #000"},
                                ),
                                html.Td(id="t20", style={"border": "1px solid #000"}),
                                html.Td(id="t21", style={"border": "1px solid #000"}),
                                html.Td(id="t22", style={"border": "1px solid #000"}),
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td("Относительное равномерное удлинение"),
                                html.Td(id="t30", style={"border": "1px solid #000"}),
                                html.Td(id="t31", style={"border": "1px solid #000"}),
                                html.Td(id="t32", style={"border": "1px solid #000"}),
                            ]
                        ),
                        html.Tr(
                            [
                                html.Td(
                                    "Относительная площадь смятия поперечных рёбер",
                                    style={"border": "1px solid #000"},
                                ),
                                html.Td(id="t40", style={"border": "1px solid #000"}),
                                html.Td(id="t41", style={"border": "1px solid #000"}),
                                html.Td(id="t42", style={"border": "1px solid #000"}),
                            ]
                        ),
                    ],
                    style={
                        "border-collapse": "collapse",
                        "width": "1264px",
                        "text-align": "center",
                        "border": "1px solid #000",
                    },
                ),
            ],
            style={
                "position": "absolute",
                "left": "10%",
                "top": "95%",
                "width": "1264px",
                "justify-content": "center",
            },
        ),
    ],
    style={"columnCount": 2},
)


# От выброра марки будут зависить размеры,которые можно выброть, как в датасете
@app.callback([Output("steelsize_opts", "options"), Output("steelgrade_opts", "options")], [Input("files", "value")])
def update_dropdown(X):
    print(X)
    if isinstance(X, str):
        data = pd.read_excel(X)
    else:
        data = pd.read_excel(X['value'])
        X = X['value']
# Выбираем из таблицы индексы для фильтрации и назначаем тип категории.
    data["Марка стали"] = data["Марка стали"].astype("category")
    data["Профиль / размер"] = data["Профиль / размер"].astype("category")
    steelgrade = data["Марка стали"].drop_duplicates().tolist()
    steelsize = data["Профиль / размер"].drop_duplicates().tolist()
    data = data.set_index(["Марка стали", "Профиль / размер"])
    steelgrade_opts = [{"label": i, "value": i} for i in steelgrade]
    steelsize_opts = [{"label": i, "value": i} for i in steelsize]
    # steelsize = data.xs(X).index.drop_duplicates().tolist()
    # steelsize_opts = [{"label": i, "value": i} for i in steelsize]
    return steelsize_opts, steelgrade_opts


# От выбранных пунктов в чек-листе будет зависить отображенные на странице данные
@app.callback(
    [
        Output("attention", "children"),
        Output("graph_gist", "figure"),
        Output("t00", "children"),
        Output("t01", "children"),
        Output("t02", "children"),
        Output("t10", "children"),
        Output("t11", "children"),
        Output("t12", "children"),
        Output("t20", "children"),
        Output("t21", "children"),
        Output("t22", "children"),
        Output("t30", "children"),
        Output("t31", "children"),
        Output("t32", "children"),
        Output("t40", "children"),
        Output("t41", "children"),
        Output("t42", "children"),
    ],
    [Input("steelgrade_opts", "value"), Input("steelsize_opts", "value")],
)
def update_figure(grade, size):
    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=(
            "Предел текучести, Н/м²",
            "Временное сопротивление, Н/мм²",
            "Относительное удлинение, %",
            "Относительное равномерное удлинение, %",
            "Относительная площадь смятия поперечных рёбер",
        ),
    )
    df = data.xs((grade, size))
    data_len = len(df["Предел текучести, Н/мм²"])
    if data_len < 25:
        s = "Предупреждение: объём выборок менее 25 значений, что может привести к некорректным результатам оценки"
        test_table[0, 0] = "недостаточно данных"
        test_table[0, 1] = "недостаточно данных"
        test_table[0, 2] = "недостаточно данных"
        test_table[1, 0] = "недостаточно данных"
        test_table[1, 1] = "недостаточно данных"
        test_table[1, 2] = "недостаточно данных"
        test_table[2, 0] = "недостаточно данных"
        test_table[2, 1] = "недостаточно данных"
        test_table[2, 2] = "недостаточно данных"
        test_table[3, 0] = "недостаточно данных"
        test_table[3, 1] = "недостаточно данных"
        test_table[3, 2] = "недостаточно данных"
        test_table[4, 0] = "недостаточно данных"
        test_table[4, 1] = "недостаточно данных"
        test_table[4, 2] = "недостаточно данных"
    else:
        # График 1
        x_now = df["Предел текучести, Н/мм²"]
        fig.add_trace(
            go.Histogram(
                x=x_now,
                histnorm="probability",
                name="Предел текучести, Н/мм²",
                showlegend=False,
            ),
            1,
            1,
        )

        loc, scale = norm.fit(x_now)
        n = norm(loc=loc, scale=scale)
        x_norm = np.arange(x_now.min(), x_now.max() + 0.2, 0.2)
        fig.add_trace(
            go.Scatter(
                x=x_norm,
                y=5 * n.pdf(x_norm),
                name="Теоретическая форма нормального распределения",
                line_color="red",
            ),
            1,
            1,
        )

        test_table[0, 0] = test_pirson(x_now)
        test_table[0, 1] = test_kstest(x_now, n.cdf)
        test_table[0, 2] = test_shapiro(x_now)
        # График 2
        x_now = df["Временное сопротивление, Н/мм²"]
        fig.add_trace(
            go.Histogram(
                x=x_now,
                histnorm="probability",
                name="Временное сопротивление, Н/мм²",
                showlegend=False,
            ),
            1,
            2,
        )

        loc, scale = norm.fit(x_now)
        n = norm(loc=loc, scale=scale)
        x_norm = np.arange(x_now.min(), x_now.max() + 0.2, 0.2)
        fig.add_trace(
            go.Scatter(
                x=x_norm,
                y=5 * n.pdf(x_norm),
                name="Теоретическая форма нормального распределения",
                line_color="red",
                showlegend=False,
            ),
            1,
            2,
        )

        test_table[1, 0] = test_pirson(x_now)
        test_table[1, 1] = test_kstest(x_now, n.cdf)
        test_table[1, 2] = test_shapiro(x_now)
        # График 3
        x_now = df["Относительное удлинение, %"]
        fig.add_trace(
            go.Histogram(
                x=x_now,
                histnorm="probability",
                name="Относительное удлинение, %",
                showlegend=False,
            ),
            2,
            1,
        )

        loc, scale = norm.fit(x_now)
        n = norm(loc=loc, scale=scale)
        x_norm = np.arange(x_now.min(), x_now.max() + 0.2, 0.2)
        fig.add_trace(
            go.Scatter(
                x=x_norm,
                y=0.5 * n.pdf(x_norm),
                name="Теоретическая форма нормального распределения",
                showlegend=False,
                line_color="red",
            ),
            2,
            1,
        )

        test_table[2, 0] = test_pirson(x_now)
        test_table[2, 1] = test_kstest(x_now, n.cdf)
        test_table[2, 2] = test_shapiro(x_now)
        # График 4
        x_now = df["Относительное равномерное удлинение, %"]
        fig.add_trace(
            go.Histogram(
                x=x_now,
                histnorm="probability",
                name="Относительное равномерное удлинение, %",
                showlegend=False,
            ),
            2,
            2,
        )

        loc, scale = norm.fit(x_now)
        n = norm(loc=loc, scale=scale)
        x_norm = np.arange(x_now.min(), x_now.max() + 0.2, 0.2)
        fig.add_trace(
            go.Scatter(
                x=x_norm,
                y=0.25 * n.pdf(x_norm),
                name="Теоретическая форма нормального распределения",
                showlegend=False,
                line_color="red",
            ),
            2,
            2,
        )

        test_table[3, 0] = test_pirson(x_now)
        test_table[3, 1] = test_kstest(x_now, n.cdf)
        test_table[3, 2] = test_shapiro(x_now)
        # График 5
        x_now = df["fr"]
        fig.add_trace(
            go.Histogram(
                x=x_now,
                histnorm="probability",
                name="Относительная площадь смятия поперечных рёбер",
                showlegend=False,
            ),
            3,
            1,
        )

        loc, scale = norm.fit(x_now)
        n = norm(loc=loc, scale=scale)
        x_norm = np.arange(x_now.min(), x_now.max() + 0.2, 0.2)

        test_table[4, 0] = test_pirson(x_now)
        test_table[4, 1] = test_kstest(x_now, n.cdf)
        test_table[4, 2] = test_shapiro(x_now)

        fig.update_layout(
            legend_orientation="h",
            legend=dict(x=0.5, xanchor="center"),
            hovermode="x",
            margin=dict(l=0, r=0, t=30, b=0),
        )
        # fig.update_traces(hoverinfo="all", hovertemplate="Аргумент: %{x}<br>Функция: %{y}")
        s = "Объем выборки: " + str(data_len)

    return (
        s,
        fig,
        test_table[0, 0],
        test_table[0, 1],
        test_table[0, 2],
        test_table[1, 0],
        test_table[1, 1],
        test_table[1, 2],
        test_table[2, 0],
        test_table[2, 1],
        test_table[2, 2],
        test_table[3, 0],
        test_table[3, 1],
        test_table[3, 2],
        test_table[4, 0],
        test_table[4, 1],
        test_table[4, 2],
    )

