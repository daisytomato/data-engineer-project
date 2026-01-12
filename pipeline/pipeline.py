import sys
print ('arguments',sys.argv)

day = int(sys.argv[1])
print(f'Running pipeline for day {day}')

import pandas as pd 
data = pd.DataFrame({'A':[1,2,3],'B':[4,5,6]})
print(data.head())

data.to_parquet(f"output_day_{sys.argv[1]}.parquet")