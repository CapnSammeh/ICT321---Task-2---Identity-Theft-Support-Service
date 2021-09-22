"""
RESTFUL Web Service Demo

In this  demo,  you  are  required  to  implement  a  Python script with the name ‘web_finder.py’ to provide two RESTful Web services:
    ✅ Get  reporting  centre  services by postcode. The server should accept a ‘getServices’ query from the client browser similar to “/getServices?postcode=xxxx”. After processing this request, the service should return a HTML document containing the list of available services for a given postcode, including the following fields (attributes): 
        ✅ Service, Suburb. 
    ✅ Get reporting centre by service name. The server should accept a ‘getRCentre’ query from  the client browser similar to “/getRCentre?service=xxxx”. After processing this request, the service should return a HTML document containing the list of available reporting centres for a given service, including the following fields (attributes): 
        ✅ CentreID, Suburb, Latitude, Longitude. 
    The Python Bottle and petl frameworks are required for this implementation. Data for the  service is from the output file “reportingCentre_service_locations.csv” of the integration demo.

Other features:
    ✅ Input Error Handling
    ✅ Clearly Documented
"""

from bottle import app, abort, route, request, run
import petl as etl

app.catchall = False

# Get Import Data
data = etl.fromcsv("reportingCentre_service_locations.csv")

# Get Services Route
@route("/getServices", method='GET')
def get_services():
    # Define the Postcode by the Request Query param 'postcode' and ensure it meets the Aus. Standard
    postcodeInput = request.query.postcode
    
    # Typically I would use the RE Library to perform a REGEX match here, but we're not allowed to use any libraries other than Bottle and PETL 😔
    # Generate a list of the valid Postcodes that appear in the file; we'll use this list to validate the user input
    postcodes = etl.values(data, "Postcode")
    validPostcodes = []
    for postcode in postcodes:
        if postcode not in validPostcodes:
            validPostcodes.append(postcode)

    # Error Handling
    # TODO Need considerations for asking for all Services irrespective of Postcode.
    if(len(postcodeInput) != 4):
        abort(400, "Invalid Postcode; please adhere to the XXXX format")
    elif(postcodeInput not in validPostcodes):
        abort(404, "No content available for the supplied postcode")
    
    try:
        # Lookup the Postcode from our File
        lookup = etl.lookup(data, "Postcode", ("Suburb", "Service"))
        lookupResponse = lookup[postcodeInput]

        # Iterate through the response to create our Services List, as well as identify the Suburb Name
        servicesList = []
        for key, value in lookupResponse:
            servicesList.append(value)
            suburb = key

        # Finally, return a dictionary (That Bottle automatically turns into a JSON object) with our required content.
        return dict(data={"postcode": postcodeInput, "suburb": suburb, "services": servicesList})
    except:
        # This is likely to never occur, but better safe than sorry!
        abort(204, "Other")

# Get Reporting Centre Route
@route("/getRCentre", method='GET')
def get_reporting_centre():
    # Define the Service by the Request Query param 'service'
    service = request.query.service
    
    if(len(service) == ''):
        abort(400, "A service must be provided")
        # TODO | This isn't good API design; when someone queries the endpoint and doesn't specify a service, we should return all the information instead

    # Use DictLookup to slice the data by Service into a dict
    services = etl.dictlookup(data, "Service")    
    # Filter this list down to only the service we've queried
    try:
        centres = services[service]
    except:
        print("snap")
        abort(404, "Please provide a valid Service")

    # Iterate through the list of Centres and create a dictionary for each of the responses using the keys. Then, populate the list with these dictionaries
    centresList = []
    for i in range(len(centres)):
        if(i == 0):
            continue
        centreObject = {
            "CentreID": centres[i]['CentreID'],
            "Suburb": centres[i]['Suburb'],
            "Latitude": centres[i]['Lat'],
            "Longitude": centres[i]['Lon'],
        }
        centresList.append(centreObject)

    # Finally, return a dictionary with our list of centres in the relevant JSON structure.
    return dict(data={"service": service, "reporting_centres": centresList})

run(host="localhost", port=8080, reloader=True)
