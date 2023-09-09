import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_two_axes_line_chart(data, y1, y2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_yaxes(title_text=y1, secondary_y=False)
    fig.update_yaxes(title_text=y2, secondary_y=True, showgrid=False)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1)
    )
    # Add traces
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[y1],
            name=y1,
            line=dict(color="royalblue", width=3, dash="dot"),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[y2],
            name=y2,
            line=dict(color="khaki", width=3, dash="dot"),
        ),
        secondary_y=True,
    )
    st.plotly_chart(fig, use_container_width=True)
