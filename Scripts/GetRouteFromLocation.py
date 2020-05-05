import pandas as pd
import ast

def true_locations():
    points = ['37.948407,23.618734', '37.949056,23.622872', '37.947528,23.626445', '37.951318,23.629970', '37.944304,23.627213', '37.946127,23.633617', '37.943518,23.632879', '37.950339,23.634460', '37.949275,23.638958', '37.949459,23.645260', '37.949591,23.648858', '37.946790,23.645170', '37.942664,23.643054', '37.943530,23.645925', '37.941175,23.645508', '37.938930,23.640589', '37.937748,23.642510', '37.935599,23.635565', '37.937644,23.634318', '37.936736,23.630546']

    data = pd.DataFrame()
    data = pd.read_csv('ExtractLocations.csv')

    routes = data['flowSegmentData.coordinates.coordinate']
    final = pd.DataFrame()
    for index, value in routes.items():
        #print(index, value)
    
        route = ast.literal_eval(value)
        #print(type(route))
    
        lat = []
        lon = []
    
    
        for point in route:
            lat.append(point['latitude'])
            lon.append(point['longitude'])
    
        latPoint, lonPoint = points[index].split(',')
            
        row_to_append = {'Lat_Point': float(latPoint), 'Lon_Point' : float(lonPoint), 'Lat_RoutePoints' : lat, 'Lon_RoutePoints' : lon}
        final = final.append(row_to_append, ignore_index = True)
    
    return final

    
    
    
    
