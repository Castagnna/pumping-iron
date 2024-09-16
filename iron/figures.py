import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from pandas import DataFrame

COLOR_1 = "#9370DB"
COLOR_2 = "#FFFACD"
COLOR_3 = "#3CB371"


def plot_two_axes_line_chart(data: "DataFrame", y1: str, y2: str) -> None:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_yaxes(title_text=y1, secondary_y=False)
    fig.update_yaxes(title_text=y2, secondary_y=True, showgrid=False)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1))
    # Add traces
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[y1],
            name=y1,
            line=dict(color=COLOR_1, width=5, dash="solid"),
            opacity=0.9,
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[y2],
            name=y2,
            line=dict(color=COLOR_3, width=5, dash="solid"),
            opacity=0.9,
        ),
        secondary_y=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def plot_stacked_bar_and_line_chart(data: "DataFrame", min_range: int = 70):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    total_mass = data["free_of_fat_mass_kg"] + data["fat_mass_kg"]

    y_range = [min_range, max(total_mass) + 10]

    fig.update_xaxes(type="category")

    fig.update_yaxes(title_text="Mass (kg)", secondary_y=False, range=y_range, title_font=dict(color=COLOR_1))

    secondary_y_range = [0.8 * min(data["body_fat"]), 1.2 * max(data["body_fat"])]
    fig.update_yaxes(
        title_text="Body fat (%)",
        secondary_y=True,
        showgrid=False,
        range=secondary_y_range,
        title_font=dict(color=COLOR_3),
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        barmode="overlay",
        xaxis_title="Date",
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
    )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=total_mass,
            name="Total Mass",
            marker=dict(
                color=COLOR_1,
                # line=dict(color=COLOR_1, width=10)
            ),
            text=total_mass,
            textangle=90,
            textposition="outside",
            constraintext="both",
            texttemplate="%{y:.1f}",
            textfont=dict(color=COLOR_2),
        ),
    )
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["fat_mass_kg"],
            name="Fat",
            marker=dict(color=COLOR_2),
            text=data["fat_mass_kg"],
            textangle=90,
            texttemplate="%{y:.1f}",
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["body_fat"],
            name="Body fat",
            opacity=0.95,
            mode="markers+text",
            marker=dict(color=COLOR_3, size=18),
            text=data["body_fat"],
            textposition="top center",
            textfont=dict(color=COLOR_2),
            texttemplate="%{y:.1f}",
        ),
        secondary_y=True,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def plot_checkbox_stacked_bar_and_line_chart(data: "DataFrame", selected_dates: "List[str]") -> None:
    filtered = data.loc[selected_dates]
    if not filtered.empty:
        plot_stacked_bar_and_line_chart(filtered, 0)
    else:
        st.write("Nenhum dado selecionado para exibição.")
