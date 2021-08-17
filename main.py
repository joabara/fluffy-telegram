import pandas as pd
laptops = pd.read_csv('laptops.csv', encoding='latin1')

laptops['Ram'] = [pd.to_numeric(str(laptops['Ram'].iloc[x]).replace('GB','')) for x in range(len(laptops['Ram']))]
laptops['Weight'] = [pd.to_numeric(str(laptops['Ram'].iloc[x]).replace('kg','')) for x in range(len(laptops['Ram']))]
laptops['Price_dollars'] = round(laptops['Price_euros']*1.18,2)
laptops = laptops.drop('Price_euros',axis=1)

cpu = pd.read_csv('CPU Ranks.csv')

gpu = pd.read_csv('GPU_ranks.csv')
gpu = gpu.drop(columns=['Unnamed: 5', 'Unnamed: 6'])
########New Code added 8-16-2021

gpu = gpu[(gpu['Videocard Name'] != 'Videocard Name')]
gpu.dropna(subset=['Videocard Name'], inplace = True)

gpu['Passmark G3D Mark'] = pd.to_numeric(gpu['Passmark G3D Mark'])
gpu['Rank'] = [pd.to_numeric(str(gpu['Rank'].iloc[x])) if gpu['Rank'].iloc[x] == gpu['Rank'].iloc[x] else np.nan for x in range(len(gpu['Rank']))]
gpu['Videocard Value'] = [pd.to_numeric(str(gpu['Videocard Value'].iloc[x])) if gpu['Videocard Value'].iloc[x] == gpu['Videocard Value'].iloc[x] else np.nan for x in range(len(gpu['Videocard Value']))]
gpu['usd'] = [pd.to_numeric(str(gpu['usd'].iloc[x]).replace('$','').replace('*','').replace(',','').replace('Price','').replace('(USD)','')) if gpu['usd'].iloc[x] == gpu['usd'].iloc[x] else np.nan for x in range(len(gpu['usd']))]

cpu['Price (USD)'] = [pd.to_numeric(str(cpu['Price (USD)'].iloc[x]).replace('$','').replace('*','').replace(',','').replace('Price','').replace('(USD)','')) if cpu['Price (USD)'].iloc[x] == cpu['Price (USD)'].iloc[x] else np.nan for x in range(len(cpu['Price (USD)']))]
cpu['CPU Mark (Higher is better)'] = [pd.to_numeric(str(cpu['CPU Mark (Higher is better)'].iloc[x]).replace(',','')) if cpu['CPU Mark (Higher is better)'].iloc[x] == cpu['CPU Mark (Higher is better)'].iloc[x] else np.nan for x in range(len(cpu['CPU Mark (Higher is better)']))]
cpu['CPU Value (Higher is better)'] = [pd.to_numeric(str(cpu['CPU Value (Higher is better)'].iloc[x])) if cpu['CPU Value (Higher is better)'].iloc[x] == cpu['CPU Value (Higher is better)'].iloc[x] else np.nan for x in range(len(cpu['CPU Value (Higher is better)']))]
