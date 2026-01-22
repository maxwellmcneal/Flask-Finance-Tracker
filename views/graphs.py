from flask import Blueprint, render_template, url_for, redirect, flash, request
from extensions import db
import datetime as dt
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

graphs_bp = Blueprint("graphs", __name__, url_prefix="/graphs")

@graphs_bp.route("/", methods=["GET"])
def create_graph():
    x = np.random.rand(100).tolist()
    y = np.random.rand(100).tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='Random Scatter Plot',
        xaxis_title='X Axis',
        yaxis_title='Y Axis'
    )
    graph_html = pio.to_html(fig, include_plotlyjs='cdn', div_id='plot')
    return render_template("graphs.html", graph_html=graph_html, active_page="graphs")
