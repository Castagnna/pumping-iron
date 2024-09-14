import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


COLOR_1 = "#9370DB"
COLOR_2 = "#FFFACD"
COLOR_3 = "#3CB371"


def plot_two_axes_line_chart(data, y1, y2):
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
            opacity=0.6,
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data[y2],
            name=y2,
            line=dict(color=COLOR_2, width=5, dash="solid"),
            opacity=0.6,
        ),
        secondary_y=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def plot_stacked_bar_and_line_chart(data, min_range=70):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    y_range = [min_range, max(data["free_of_fat_mass_kg"] + data["fat_mass_kg"])]

    fig.update_xaxes(type="category")

    fig.update_yaxes(title_text="Mass (kg)", secondary_y=False, range=y_range,  title_font=dict(color=COLOR_1))
    fig.update_yaxes(
        title_text="Body fat (%)",
        secondary_y=True,
        showgrid=False,
        title_font=dict(color=COLOR_3),
        # tickfont=dict(color=COLOR_3),
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        barmode="overlay",
        xaxis_title="Date",
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
    )

    total_mass = data["free_of_fat_mass_kg"] + data["fat_mass_kg"]

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=total_mass,
            name="Total Mass",
            marker=dict(
                color=COLOR_1,
                # line=dict(color=COLOR_1, width=10)
            ),
        ),
    )
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["fat_mass_kg"],
            name="Fat",
            marker=dict(color=COLOR_2),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["body_fat"],
            name="Body fat",
            mode="markers",
            marker=dict(color=COLOR_3, size=18),
            opacity=0.95,
        ),
        secondary_y=True,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def plot_checkbox_stacked_bar_and_line_chart(data, selected_dates):
    filtered = data.loc[selected_dates]
    if not filtered.empty:
        plot_stacked_bar_and_line_chart(filtered, 0)
    else:
        st.write("Nenhum dado selecionado para exibição.")
