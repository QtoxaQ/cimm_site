from dash import Dash, html, dcc, Output, Input, State, callback_context
import json
import dash_bootstrap_components as dbc
from states import Data


data_file = "reactions.json"
data = Data()


app = Dash(__name__,
           title="Storages",
           external_stylesheets=[dbc.themes.BOOTSTRAP]
           )


content = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H1("Заполнение JSON файла",
                            className="text-center"),
                    ), width=12
                )
            ),

        dbc.Row([
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col([
                            html.H3("Введите SMILES реакции:"),
                            dbc.Textarea(
                                id="reaction-input",
                                placeholder="Пример: NCC([O-])=O>>O",
                                style={"width": "100%"},
                                ),
                            ])
                        ),

                    dbc.Row(
                        dbc.Col(
                            html.H4("Укажите параметры реакции:")
                            )
                        ),

                    dbc.Row([
                        dbc.Col([
                            html.Label("Соотношение реагентов:"),
                            dcc.Input(
                                id="reagent-input",
                                type="text",
                                placeholder="Пример: 1:1.5:2",
                                className="form-control",
                                style={"height": 50}
                                ),
                            ], width=4),

                        dbc.Col([
                            html.Label(
                                "Соотношение катализаторов:"
                                ),
                            dcc.Input(
                                id="catalyst-input",
                                type="text",
                                placeholder="При наличии",
                                className="form-control",
                                style={"height": 50}
                                ),
                            ], width=4),

                        dbc.Col([
                            html.Label("Соотношение продуктов:"),
                            dcc.Input(
                                id="product-input",
                                type="text",
                                placeholder="Пример: 0.5:1",
                                className="form-control",
                                style={"height": 50}
                                ),
                            ], width=4),
                        ], style={"height": 100}),

                    dbc.Row([
                        dbc.Col([
                            html.Label("Температура (°C):"),
                            dcc.Input(
                                id="temp-input",
                                type="text",
                                placeholder="25",
                                className="form-control",
                                style={"height": 50}
                                ),
                            ], width=4),

                        dbc.Col([
                            html.Label("Время:"),
                            dcc.Input(
                                id="time-input",
                                type="text",
                                placeholder="(сек)",
                                className="form-control",
                                style={"height": 50}
                                ),
                            ], width=4),

                        dbc.Col([
                            html.Label("Количество продукта №1:"),
                            dcc.Input(
                                id="quantity-input",
                                type="text",
                                placeholder="(Моль)",
                                className="form-control",
                                style={"height": 50}
                                ),
                            ], width=4),
                        ], style={"height": 100}),

                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Записать реакцию",
                                id="submit1-button",
                                color="primary",
                                className="mt-3 mb-3",
                                style={"height": 50}
                                ),
                            ]),

                        dbc.Col([
                            dbc.Button(
                                "Удалить последнюю",
                                id="submit2-button",
                                color="primary",
                                className="mt-3 mb-3",
                                style={"height": 50}
                                ),
                            ]),

                        dbc.Col([
                            dbc.Button(
                                "Удалить все",
                                id="submit3-button",
                                color="primary",
                                className="mt-3 mb-3",
                                style={"height": 50}
                                ),
                            ])
                        ]),
                    ], width=6
                ),

            dbc.Col(
                [
                    html.H3("Список реакций:"),
                    html.Div(
                        id="file-content",
                        style={
                            "border": "1px solid #ddd",
                            "padding": "10px",
                            "border-radius": "5px",
                            "height": "700px",
                            "overflow-y": "scroll",
                            "whiteSpace": "pre-wrap",
                            "backgroundColor": "#f9f9f9"
                            }
                        )
                    ], width=6
                ),
            ]),
        html.Div(id="hidden-div", style={"display": "none"})
        ],
    fluid=True
    )


app.layout = content


@app.callback(
    [Output("file-content", "children"),
     Output("hidden-div", "children")],
    [Input("submit1-button", "n_clicks"),
     Input("submit2-button", "n_clicks"),
     Input("submit3-button", "n_clicks")],
    [State("reaction-input", "value"),
     State("reagent-input", "value"),
     State("catalyst-input", "value"),
     State("product-input", "value"),
     State("temp-input", "value"),
     State("time-input", "value"),
     State("quantity-input", "value")]
)
def update_file(n1_clicks,
                n2_clicks,
                n3_clicks,
                reaction,
                reagent, catalyst, product,
                temp, time, quantity):
    ctx = callback_context
    if not ctx.triggered:
        with open(data_file, "r") as f:
            content = f.read()
            data.json = json.loads(content)
            data.num_of_reactions = len(data.json)
        return content, ""

    btn_id = ctx.triggered_id

    if btn_id == 'submit1-button':
        reagent = str(reagent).split(':')
        new_reagent = {}
        reagent_states = {}
        reagent_density = {}
        for key, value in enumerate(reagent):
            new_reagent[str(key+1)] = value
            reagent_states[str(key+1)] = "liquid"
            reagent_density[str(key+1)] = 1.0

        if catalyst:
            catalyst = str(catalyst).split(':')
            new_catalyst = {}
            catalyst_states = {}
            catalyst_density = {}
            for key, value in enumerate(catalyst):
                new_catalyst[str(key+1)] = value
                catalyst_states[str(key+1)] = "liquid"
                catalyst_density[str(key+1)] = 1.0

        product = str(product).split(':')
        new_product = {}
        product_states = {}
        for key, value in enumerate(product):
            new_product[str(key+1)] = value
            product_states[str(key+1)] = None

        record = {}
        record["num"] = data.num_of_reactions + 1
        record["reaction"] = reaction
        if catalyst:
            record["stoichiometry"] = {"reactants": new_reagent,
                                       "products": new_product,
                                       "reagents": new_catalyst}
        else:
            record["stoichiometry"] = {"reactants": new_reagent,
                                       "products": new_product}
        record["target"] = {"product": True,
                            "idx": 1,
                            "mols": float(quantity),
                            "mass": None}
        if catalyst:
            record["states"] = {"reactants": reagent_states,
                                "products": product_states,
                                "reagents": catalyst_states}
            record["density"] = {"reactants": reagent_density,
                                 "reagents": catalyst_density},
        else:
            record["states"] = {"reactants": reagent_states,
                                "products": product_states}
            record["density"] = {"reactants": reagent_density},
        record["solvent"] = {"density": 1.0, "smiles": "O"}
        record["sample_dilution_ratio"] = 10
        record["chromatograph_method"] = 'PS_Gly_synthesis'
        record["reaction_type"] = 'peptide_synthesis'
        record["procedure_type"] = 'synthesis'
        record["temperature"] = float(temp)
        record["time"] = int(time)

        data.json.append(record)
        data.num_of_reactions = len(data.json)

        with open(data_file, "w") as f:
            json.dump(data.json, f, indent=2)

        with open(data_file, "r") as f:
            content = f.read()

        return content, ""

    elif btn_id == 'submit2-button':
        # n2_clicks = None
        with open(data_file, "w") as f:
            if data.num_of_reactions > 1:
                data.json = data.json[:-1]
                data.num_of_reactions -= 1
            else:
                data.json = []
                data.num_of_reactions = 0
            json.dump(data.json, f, indent=2)

        with open(data_file) as f:
            content = f.read()
        return content, ""

    elif btn_id == 'submit3-button':
        # n3_clicks = None
        data.json = []
        data.num_of_reactions = 0
        with open(data_file, "w") as f:
            json.dump(data.json, f, indent=2)

        with open(data_file) as f:
            content = f.read()
        return content, ""


@app.callback(
    Output("file-content", "children", allow_duplicate=True),
    Input("hidden-div", "children"),
    prevent_initial_call=True
)
def load_initial_content(_):
    with open(data_file, "r") as f:
        content = f.read()
        data.json = json.loads(content)
        data.num_of_reactions = len(data.json)

    return content


if __name__ == '__main__':
    app.run(debug=True, port=8051)
