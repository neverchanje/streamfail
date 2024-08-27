import json
from datetime import datetime
import pandas as pd
from plotnine import ggplot, aes, geom_line, labs, theme_538, expand_limits, geom_point, scale_color_brewer
import matplotlib.pyplot as plt
import re

sum_balance = []
offset = []
with open('output.json', 'r') as f:
    for line in f.readlines():
        pattern = r'-?\d+'
        number = re.findall(pattern, line)
        if "key" in line and "sum_balance" in line and number:
            print(f'Extracted numbers: {number}')
            sum_balance.append(int(number[0]))
        if "offset" in line and number:
            offset.append(int(number[0]))

min_sum_balance = df['sum_balance'].min()
max_sum_balance = df['sum_balance'].max()
print(min_sum_balance)
print(max_sum_balance)

plot = (
    ggplot(df, aes(x='offset', y='sum_balance', color='system')) +
    geom_line() +
    labs(x='output #', y='total', title='Internal Consistency Issue in Risingwave') +
    scale_color_brewer(type='qual', palette='Set2') +
    geom_point(size=3)
)

#print(plot)
plot.save(filename='inconsistent.png', format='png', dpi=300, width=8, height=6)
