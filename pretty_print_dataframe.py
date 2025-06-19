"""
AI slop because I could not for the life of me find a way to print a table
with skinny columns and to make the headers multiple lines (broken up based on words)
"""

from rich.console import Console
from rich.table import Table

console = Console()


def format_value(val):
    if isinstance(val, float):
        return f"{val:.4f}".rstrip("0").rstrip(".")
    return str(val)


def longest_word_length(s):
    return max(len(word) for word in s.split())


max_column_width = 30
col_widths = {}


def pretty_print_dataframe(df):
    # Format values ahead of time
    formatted_df = df.applymap(format_value)

    for col in df.columns:
        header_width = longest_word_length(col)
        value_width = max(len(v) for v in formatted_df[col])
        col_widths[col] = min(max(header_width, value_width), max_column_width)

    # Build the table with appropriate widths
    table = Table(show_header=True, header_style="bold magenta")

    for col in df.columns:
        table.add_column(col, overflow="fold", max_width=col_widths[col])

    for _, row in formatted_df.iterrows():
        table.add_row(*row)

    console.print(table)
