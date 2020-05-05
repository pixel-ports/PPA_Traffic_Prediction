import pandas as pd
import ast



def aggregation_functionWeather(a):

    df = pd.DataFrame()
    df = pd.read_csv(r'C:\Users\sergi\Desktop\Environment\Raw Data\WeatherRawData.csv')
    weather_data = pd.DataFrame()

    for index, row in df.iterrows():
        darkSky = row['darkSkyPireaus']
        dict_darkSky = ast.literal_eval(darkSky)
        currently = dict_darkSky['currently']
        
        weather_data = weather_data.append(currently, ignore_index = True)
    weather_data['time'] = weather_data['time'].apply(lambda x: pd.Timestamp(x, unit = 's'))
    weather_data = weather_data.drop_duplicates()
    
    weather_data['time'] = pd.to_datetime(weather_data['time'], format='%Y-%m-%d %H:%M:%S')
    weather_data['time'] = weather_data['time'].map(lambda x: x.replace(second=0))
    a = str(a) + 'Min'
    weather_data.set_index('time', inplace = True)
    weather_data = weather_data.groupby(pd.Grouper(freq=a)).mean()

    return weather_data