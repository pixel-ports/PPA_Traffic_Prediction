import pandas as pd

def aggregation_functionTomTom(a):

    #These are the points for which traffic data is requested and will be used as location_id
    points = ['37.948407,23.618734', '37.949056,23.622872', '37.947528,23.626445', '37.951318,23.629970', '37.944304,23.627213', '37.946127,23.633617', '37.943518,23.632879', '37.950339,23.634460', '37.949275,23.638958', '37.949459,23.645260', '37.949591,23.648858', '37.946790,23.645170', '37.942664,23.643054', '37.943530,23.645925', '37.941175,23.645508', '37.938930,23.640589', '37.937748,23.642510', '37.935599,23.635565', '37.937644,23.634318', '37.936736,23.630546']

    #We read the data from the csv generated
    data = pd.read_csv(r'C:\Users\sergi\Desktop\Environment\Raw Data\TomTomRawData.csv')

    #Do we have to remove rows with confidence lower than a threshold?
    #data = data[data['flowSegmentData.confidence']>0.5]

    #Location_id column is generated from the index column value
    data['location_id'] = (data['index'].apply(lambda x: points[x]))

    #Only location_id, timestamp and current_speed columns are kept
    data = data[['location_id','TimeStampUTC','flowSegmentData.currentSpeed']]

    #Rename columns to names defined at ppt
    data = data.rename(columns={'flowSegmentData.currentSpeed' : 'current_speed', 'TimeStampUTC' : 'timestamp'})

    #Change columns type to correct ones
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y-%m-%d %H:%M:%S')
    data['timestamp'] = data['timestamp'].map(lambda x: x.replace(second=0))
    unifiedModel = data


    '''The dataframe generated can be introduced to Prophet with the maximum accuracy available of 15min,
    now will be implemented the part with the adjustable parameter to aggregate the data to different time
    granularity'''

    #Adjustable parameter, interval length in minutes
    parameter = str(a) + "Min"

    #Pivot the table
    data = pd.pivot_table(data, index = ['timestamp'], columns = ['location_id'])


    #Aggregation of data according to freq value
    data = data.groupby(pd.Grouper(freq=parameter)).mean()

    #Changing the column names
    data.columns = [('cs_'+str(x[1])) for x in data.columns]

    #Index into column and new range index.Moreover, locations for which the data is not complete for the full period are dropped
    #data_Prophet = data.dropna(axis=1).reset_index()
    data_Prophet = data.reset_index()
    '''Now the dataframe format is almost as Prophet expect, only we should select the requested location to predict
    and the datestamp. For future stage we can consider include a datetime filter to keep the records between two dates. ''' 

    return data_Prophet