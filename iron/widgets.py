import streamlit as st
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from pandas import DataFrame


def date_checkboxes(data: "DataFrame", n_columns: int) -> "List[str]":
    n_columns = 5
    columns = st.columns(n_columns)
    checkbox_values = []

    for i, date in enumerate(data.index):
        col = columns[i % n_columns]
        with col:
            checked = st.checkbox(f"{date}", value=True, key=f"checkbox_{date}")
            checkbox_values.append((date, checked))

    return [date for date, checked in checkbox_values if checked]
