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

laptops['OpSys'].value_counts()

#66 values have 'No OS' for it's operating system. We checked some of the laptop models that had 'No OS' specified, and from our research it seemed like a majority of these laptops did not actually come with an operating system installed. For example, when shopping for a Lenovo Thinkpad the user can decide whether they want to have Windows 10 or Chrome OS installed. Therefore, 'No OS' was a customization feature and we decided to keep this operating system category.

#For Linux OS, only some computers come pre-installed with Linux. Others with Linux as their listed OS are only Linux compatible. Therefore, we searched the product name to see if it had 'Linux' in it. If it did, then we kept Linux as the operating system. If it didn't, we converted it to Windows 10.
laptops['OpSys'] = ['Windows 10' if laptops['OpSys'].iloc[x] == 'Linux' and 'Linux' not in laptops['Product'].iloc[x] else laptops['OpSys'].iloc[x] for x in range(len(laptops['OpSys']))]
laptops['OpSys'].value_counts()

#Creating dummy variables for OS systems.
df = pd.get_dummies(laptops['OpSys'])
laptops = laptops.drop('OpSys',axis=1)
laptops = pd.concat([laptops, df], axis=1, join='inner')
laptops.head()

#Split memory into two features: 'Memory': Memory Capacity
#                                'SSD'/'HDD'/'Hybrid': Type of memory. SSD or HDD will be 0 if Hybrid=1

laptops['Memory'] = [(laptops['Memory'].iloc[x]).replace(' Flash Storage',' SSD') for x in range(len(laptops['Memory']))]
laptops['Hybrid'] = [1 if 'Hybrid' in laptops['Memory'].iloc[x] or '+' in laptops['Memory'].iloc[x] else 0 for x in range(len(laptops['Memory']))]
laptops['SSD'] = [1 if 'SSD' in laptops['Memory'].iloc[x] and laptops['Hybrid'].iloc[x] != 1 else 0 for x in range(len(laptops['Memory']))]
laptops['HDD'] = [1 if 'HDD' in laptops['Memory'].iloc[x] and laptops['Hybrid'].iloc[x] != 1 else 0 for x in range(len(laptops['Memory']))]

laptops['Memory1'] = 0
laptops['Memory2'] = 0

for x in range(len(laptops['Memory'])):
    if '+' in laptops['Memory'].iloc[x]:
        split_string = laptops['Memory'].iloc[x].split("+",)
        if len(split_string) == 1:
            laptops['Memory1'].iloc[x] = split_string[0]
            laptops['Memory2'].iloc[x] = 0
        if len(split_string) == 2:
            laptops['Memory1'].iloc[x] = split_string[0]
            laptops['Memory2'].iloc[x] = split_string[1]
    else:
        laptops['Memory1'].iloc[x] = laptops['Memory'].iloc[x]
        laptops['Memory2'].iloc[x] = 0
        
laptops['Memory1'] = [pd.to_numeric(str(laptops['Memory1'].iloc[x]).replace('GB','').replace(' ','').replace('1.0TB','1000').replace('1TB','1000').replace('SSD','').replace('HDD',''),errors = 'coerce') for x in range(len(laptops['Memory1']))]
laptops['Memory2'] = [pd.to_numeric(str(laptops['Memory2'].iloc[x]).replace('GB','').replace(' ','').replace('1.0TB','1000').replace('1TB','1000').replace('SSD','').replace('HDD',''),errors = 'coerce') for x in range(len(laptops['Memory2']))]
laptops['Memory'] = laptops['Memory1'] + laptops['Memory2']
laptops = laptops.drop('Memory1',axis=1)
laptops = laptops.drop('Memory2',axis=1)

#####END LAPTOP MEMORY######

gpu = gpu[(gpu['Videocard Name'] != 'Videocard Name')]
gpu.dropna(subset=['Videocard Name'], inplace = True)

gpu['Passmark G3D Mark'] = pd.to_numeric(gpu['Passmark G3D Mark'])
gpu['Rank'] = [pd.to_numeric(str(gpu['Rank'].iloc[x])) if gpu['Rank'].iloc[x] == gpu['Rank'].iloc[x] else np.nan for x in range(len(gpu['Rank']))]
gpu['Videocard Value'] = [pd.to_numeric(str(gpu['Videocard Value'].iloc[x])) if gpu['Videocard Value'].iloc[x] == gpu['Videocard Value'].iloc[x] else np.nan for x in range(len(gpu['Videocard Value']))]
gpu['usd'] = [pd.to_numeric(str(gpu['usd'].iloc[x]).replace('$','').replace('*','').replace(',','').replace('Price','').replace('(USD)','')) if gpu['usd'].iloc[x] == gpu['usd'].iloc[x] else np.nan for x in range(len(gpu['usd']))]

cpu['Price (USD)'] = [pd.to_numeric(str(cpu['Price (USD)'].iloc[x]).replace('$','').replace('*','').replace(',','').replace('Price','').replace('(USD)','')) if cpu['Price (USD)'].iloc[x] == cpu['Price (USD)'].iloc[x] else np.nan for x in range(len(cpu['Price (USD)']))]
cpu['CPU Mark (Higher is better)'] = [pd.to_numeric(str(cpu['CPU Mark (Higher is better)'].iloc[x]).replace(',','')) if cpu['CPU Mark (Higher is better)'].iloc[x] == cpu['CPU Mark (Higher is better)'].iloc[x] else np.nan for x in range(len(cpu['CPU Mark (Higher is better)']))]
cpu['CPU Value (Higher is better)'] = [pd.to_numeric(str(cpu['CPU Value (Higher is better)'].iloc[x])) if cpu['CPU Value (Higher is better)'].iloc[x] == cpu['CPU Value (Higher is better)'].iloc[x] else np.nan for x in range(len(cpu['CPU Value (Higher is better)']))]
