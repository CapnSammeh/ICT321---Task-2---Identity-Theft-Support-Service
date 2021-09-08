'''
Data Integration Demo

In this demo, you are required to implement a Python Script file with the name 'data_merge.py' to correctly merge records from different given data sources into one CSV output file named 'reprotingCentre_service_locations.csv".

The Python PETL Framework is recommended for this implementation.

The output file "reportingCentre_service_locations.csv" consists of the following fields: 

    • CentreServiceID – a unique field identifying each record from centreServices.csv 
    • Service – the service name from centreServices.csv 
    • CentreID – the ID for each reporting centre 
    • Suburb – the “Suburb” from reportingCentre.csv 
    • Postcode – the “Postcode” from reportingCentre.csv 
    • Latitude – the “Lat” value from centreLocations.xml 
    • Longitude – the “Lon” value from centreLocations.xml
'''

import petl at etl
