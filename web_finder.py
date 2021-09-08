"""
RESTFUL Web Service Demo

In this  demo,  you  are  required  to  implement  a  Python script with the name ‘web_finder.py’ to provide two RESTful Web services:
    • Get  reporting  centre  services by postcode. The server should accept a ‘getServices’ query from the client browser similar to “/getServices?postcode=xxxx”. After processing this request, the service should return a HTML document containing the list of available services for a given postcode, including the following fields (attributes): 
        o Service, Suburb. 
    • Get reporting centre by service name. The server should accept a ‘getRCentre’ query from  the client browser similar to “/getRCentre?service=xxxx”. After processing this request, the service should return a HTML document containing the list of available reporting centres for a given service, including the following fields (attributes): 
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

    # Iterate through the response to create our Services List, as well as identify the Suburb Name
    servicesList = []
    for key, value in lookupResponse:
        servicesList.append(value)
        suburb = key

    # Finally, return a dictionary (That Bottle automatically turns into a JSON object) with our required content.
    return dict(data={"postcode": postcode, "suburb": suburb, "services": servicesList})


# Get Reporting Centre Route
@route("/getRCentre")
def get_reporting_centre():
    # Define the Service by the Request Query param 'service'
    service = request.query.service

    # Use Facet to slice the data by Service
    services = etl.facet(data, "Service")
    # Filter this list down to only the service we've queried
    centres = services[service]

    # Iterate through the list of Centres and create a dictionary for each of the responses using the keys. Then, populate the list with these dictionaries
    centresList = []
    for i in range(len(centres["CentreID"])):
        if (i == 0):
            continue
        d = {
            "CentreID": centres[i][0],
            "Suburb": centres[i][1],
            "Latitude": centres[i][4],
            "Longitude": centres[i][5],
        }
        centresList.append(d)

    # Finally, return a dictionary with our required content in the relevant JSON structure.
    return dict(data={"service": service, "reporting_centres": centresList})


run(host="localhost", port=8080, reloader=True)
