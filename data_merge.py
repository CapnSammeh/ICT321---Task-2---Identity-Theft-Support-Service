'''
Data Integration Demo

In this demo, you are required to implement a Python Script file with the name 'data_merge.py' to correctly merge records from different given data sources into one CSV output file named 'reportingCentre_service_locations.csv".

The Python PETL Framework is recommended for this implementation.

The output file "reportingCentre_service_locations.csv" consists of the following fields: 

    ✅ CentreServiceID – a unique field identifying each record from centreServices.csv 
    ✅ Service – the service name from centreServices.csv 
    ✅ CentreID – the ID for each reporting centre 
    ✅ Suburb – the “Suburb” from reportingCentre.csv 
    ✅ Postcode – the “Postcode” from reportingCentre.csv 
    ✅ Latitude – the “Lat” value from centreLocations.xml 
    ✅ Longitude – the “Lon” value from centreLocations.xml

Other features:
    ✅ Clearly Documented
'''

# Import the PETL Library as the variable 'etl'
import petl as etl

# Specifically, we require the 'merge' function to perform the data merge we're attempting.
from petl.transform.reductions import merge

# Structure the Centre Locations from the base XML file
centreLocations = etl.fromxml('centreLocations.xml', "Centre", {
    'CentreID': "CentreID",
    'Lat':'Lat',
    'Lon':'Lon'
})

# Convert both the CentreServices.csv and ReportingCentres.csv files into ETL objects for us to manipulate.
centreServices = etl.fromcsv('centreServices.csv')
reportingCentres = etl.fromcsv('reportingCentres.csv')

# Perform two (2) merges; one to merge the CentreLocations and Services on the CentreID key, and another to merge the ReportingCentre data on top.
merge1 = etl.join(centreLocations, centreServices, key="CentreID")
merge2 = etl.join(reportingCentres, merge1, key="CentreID")

# Finally, export the result as a CSV in the root directory of the project
etl.tocsv(merge2, 'reportingCentre_service_locations.csv')