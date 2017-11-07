# DEMO FOR SHOPPING BASKET ANALYSIS WITH abs
# inspiration: http://pbpython.com/market-basket-analysis.html
# alterantive source: https://turi.com/learn/userguide/pattern_mining/frequent-pattern-mining.html

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df = pd.read_excel("data/Online Retail.xlsx")

df.columns

# transform to wide format
basket = (df[df['Country'] =="France"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))


# encode to 0 or 1 (higher quantities not relevant)
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


basket_sets = basket.applymap(encode_units)
basket_sets.drop('POSTAGE', inplace=True, axis=1)

# identify frequent itemsets
frequent_itemsets = apriori(basket_sets, min_support=0.02, use_colnames=True)

# get association rules
rules = association_rules(frequent_itemsets,
                          metric="lift", min_threshold=1.2)

rules.sort_values(by='lift', ascending=False)
