from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import numpy as np
import json
import plotly

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_type = request.form.get("chart_type", "box")

    # Load coffee sales data from CSV
    df = pd.read_csv("static/coffee_exports.csv")
    if "Year" in df.columns and "Export_Tons" in df.columns:
        x_col, y_col = "Year", "Export_Tons"

    # Select chart type
    if chart_type == "bar":
        #print(df.head())
        df_grouped = df.groupby("Country", as_index=False)["Export_Value_USD"].sum()
        fig = px.bar(df_grouped, x="Country", y="Export_Value_USD", color="Country", title="Country vs Export Value USD")
    elif chart_type == "scatter":
        fig = px.scatter(df, x="Year", y="Export_Value_USD", color="Country", title="Coffee Exports Scatter")
        print(df.head())
    else:
        fig = px.box(df, x="Region", y=y_col, color="Country", title="Coffee Exports by Region")

    # Dark layout
    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#ffffff',
        autosize=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )
    fig.update_xaxes(showgrid=False, color='#cccccc')
    fig.update_yaxes(showgrid=False, color='#cccccc')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)

if __name__ == "__main__":
    app.run(debug=True)