In [1]: import pandas as pd

 james_bond_tables = pd.read_html(
      "https://en.wikipedia.org/wiki/List_of_James_Bond_novels_and_short_stories"
 )
 james_bond_data = james_bond_tables[1].convert_dtypes()