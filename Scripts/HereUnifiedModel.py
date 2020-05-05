import pandas as pd

def aggregation_functionHere(a):
    #We read the data from the csv generated
    data = pd.read_csv(r'C:\Users\sergi\Desktop\Environment\Raw Data\HereRawData.csv')

    #Do we have to remove rows with confidence lower than a threshold?
    #data = data[data['CN']>0.5]

    '''Before defining the location_id is important to understand the description information at each record

        - DE_RW : Description based on the RW(composite item for flow across an entire roadway) which the record belongs
        - DE : Each record has its own description inside RW 
        - QD: Queuing direction
    
        My first approach to identify each record as unique would be a location_id composed of: DE + QD + DE_RW
    
        This approach generates long IDs so I replace them by an index and generate a secondary dataframe as a master table
        '''


    location_dataframe = data[['DE', 'DE_RW', 'QD', 'LE']].drop_duplicates().reset_index()

    #Incoporate an index column to dataframe to help the next left join. 
    location_dataframe = location_dataframe.drop(['index'], axis = 1).reset_index()


    #Merge the location dataframe with the dataframe which has the speed records, in order to assing a location id to each one
    data = pd.merge(data, location_dataframe, how = 'left', on =['DE', 'DE_RW', 'QD', 'LE'])

    #Only these columns are kept
    data = data[['TimeStampUTC', 'index_y', 'SU']]

    #Rename columns to names defined at ppt
    data = data.rename(columns={'TimeStampUTC' : 'timestamp', 'index_y' : 'location_id', 'SU' : 'current_speed'})

    #Change columns type to correct ones
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y-%m-%d %H:%M:%S')
    data['timestamp'] = data['timestamp'].map(lambda x: x.replace(second=0))
    unifiedModel = data


    '''The dataframe generated can be introduced to Prophet with the maximum accuracy available of 15min,
    now will be implemented the part with the adjustable parameter to aggregate the data to different time
    granularity'''

    #Adjustable parameter, interval length in minutes
    parameter = 30

    #Pivot the table
    data = pd.pivot_table(data, index = ['timestamp'], columns = ['location_id'])


    #Aggregation of data according to freq value
    data = data.groupby(pd.Grouper(freq="15Min")).mean()

    #Changing the column names
    data.columns = [('cs_'+str(x[1])) for x in data.columns]

    #Index into column and new range index. Moreover, locations for which the data is not complete for the full period are dropped
    data_Prophet = data.reset_index()
    #data_Prophet = data.dropna(axis=1).reset_index()
    data_Prophet.to_csv('HereProphetData.csv')

    '''Now the dataframe format is almost as Prophet expect, only we should select the requested location to predict
    and the datestamp. For future stage we can consider include a datetime filter to keep the records between two dates. ''' 

    return data_Prophet