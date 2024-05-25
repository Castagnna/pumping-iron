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
            line=dict(color="olivedrab", width=5, dash="solid"),
            opacity=0.6,
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[y2],
            name=y2,
            line=dict(color="honeydew", width=5, dash="solid"),
            opacity=0.6,
        ),
        secondary_y=True,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_stacked_bar_and_line_chart(data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    range = [75, max(data["free_of_fat_mass_kg"] + data["fat_mass_kg"])]
    fig.update_yaxes(title_text="Mass kg", secondary_y=False, range=range)
    fig.update_yaxes(title_text="Body fat %", secondary_y=True, showgrid=False)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        barmode="stack",
    )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["free_of_fat_mass_kg"],
            name="Free fat",
            marker=dict(color="olivedrab"),
        ),
    )
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["fat_mass_kg"],
            name="Fat",
            marker=dict(color="honeydew"),
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["body_fat"],
            name="Body fat",
            line=dict(color="orange", width=5, dash="solid"),
            opacity=0.6,
        ),
        secondary_y=True,
    )
    st.plotly_chart(fig, use_container_width=True)
