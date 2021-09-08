"""
RESTFUL Web Service Demo

In this  demo,  you  are  required  to  implement  a  Python script with the name ‘web_finder.py’ to provide two RESTful Web services:
    • Get  reporting  centre  services by postcode. The server should accept a ‘getServices’ query from the client browser similar to “/getServices?postcode=xxxx”. After processing this request, the service should return a HTML document containing the list of available services for a given postcode, including the following fields (attributes): 
        o Service, Suburb. 
    • Get reporting centre by service name. The server should accept a ‘getRCentre’ query from  the client browser similar to “/getRCentre?service=xxxx”. After processing this 
    request, the service should return a HTML document containing the list of available reporting centres for a given service, including the following fields (attributes): 
        o CentreID, Suburb, Latitude, Longitude. 
    The Python Bottle and petl frameworks are required for this implementation. Data for the  service is from the output file “reportingCentre_service_locations.csv” of the integration demo.
"""

from bottle import route, request, template, run
import petl as etl

# Get Import Data
data = etl.fromcsv("reportingCentre_service_locations.csv")


# Get Services Route
@route("/getServices")
def get_services():
    # Define the Postcode by the Request Query param 'postcode'
    postcode = request.query.postcode
    
    # Lookup the Postcode from our File
    lookup = etl.lookup(data, "Postcode", ("Suburb", "Service"))
    lookupResponse = lookup[postcode]
    
    #Iterate through the response to create our Services List, as well as identify the Suburb Name
    servicesList = []
    for key,value in lookupResponse:
        servicesList.append(value)
        suburb = key

    #Finally, return a dictionary (That Bottle automatically turns into a JSON object) with our required content.
    return dict(data={"suburb": suburb, "services":servicesList})


# Get Reporting Centre Route
@route("/getRCentre")
def get_reporting_centre():
    service = request.query.service
    lookup = etl.lookup(data, "Service", ("CentreID", "Suburb", "Lat", "Lon"))
    lookupResponse = lookup[service]
    return template("{{response}}", response=lookupResponse)


run(host="localhost", port=8080, reloader=True)
