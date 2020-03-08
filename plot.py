import random
from collections import defaultdict
from pathlib import Path
from queue import Queue
from bokeh.plotting import output_file, figure, show
from bokeh.models import DatetimeTickFormatter


def plot_wise(data):
    """Takes in {act: {date: [Transaction, ...]}} and converts it to (act, [dates], [balances], color)."""
    lines = []
    colors = ('aqua','blue','brown','cyan','darkblue','darkgreen','darkorange','darkred','gold','green','grey','hotpink','ivory','lime','orange','pink','purple','red','silver','tan','yellow')
    used = [None, ] # used colors

    # Check the validity of the input data.
    dates = set()

    for act, act_dates in data.items():
        for date, trans in act_dates.items():
            dates.add(date)
            if len(trans) == 0:
                raise Exception("Account: '{}', Date: {} doesn't have a balance.".format(act, date))
    
    for act, act_dates in data.items():
        if set(act_dates) != dates:
            raise Exception("Account: '{}' doesn't have the same dates as other given accounts.".format(act))


    for act, act_dates in data.items():
        # pick a random color for this account
        c = None
        while c in used: c = random.choice(colors)
        used.append(c)

        # append the data as a line
        lines.append([act, list(act_dates.keys()), lisT(act_dates.values()), c])

    return lines


def plot(data):
    output_file("plot.html", mode="inline")
    p = figure(title="Balance vs Date/time",
               x_axis_label="Date/time",
               y_axis_label="$ Balance",
               x_axis_type="datetime",
               sizing_mode="stretch_both")

    lines = plot_wise(data)
    lines = fill_balances(lines)
    for act, dates, trans, color in lines:
        p.line(dates, trans, line_color=color, legend_label=act, line_width=4)

    show(p)
    return p
