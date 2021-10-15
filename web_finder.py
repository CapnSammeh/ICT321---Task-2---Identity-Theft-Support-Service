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
    # Define the Postcode by the Request Query param 'postcode'
    postcodeInput = request.query.postcode
    
    # Typically I would use the RE Library to perform a REGEX match here, but we're not allowed to use any libraries other than Bottle and PETL 😔
    # Generate a list of the valid Postcodes that appear in the file; we'll use this list to validate the user input
    postcodes = etl.values(data, "Postcode")
    validPostcodes = []
    for postcode in postcodes:
        if postcode not in validPostcodes:
            validPostcodes.append(postcode)

    ## Error Handling
    # If the postcode isn't null, but is less than or greater than 4 characters, it's an incorrectly formatted postcode
    if(postcodeInput != '' and len(postcodeInput) != 4):
        abort(400, "Invalid Postcode; please adhere to the XXXX format")
    # If the postcode isn't in our list of valid postcodes (pulled from the data source), then we have no information to display
    elif(postcodeInput != '' and postcodeInput not in validPostcodes):
        abort(404, "No content available for the supplied postcode")
    
    # If there isn't a postcode submitted, we want to return all the data
    elif(postcodeInput == ''):
        # Lookup the Postcode from our File
        lookup = etl.lookup(data, ("Postcode", "Suburb"), "Service")

        #Iterate through the response to create our Services List, as well as identify the Suburb Name
        servicesList = []
        for key, value in lookup.items():
            test = {"postcode": key[0], "suburb": key[1], "services":value}
            servicesList.append(test)

        # Return the relevant data 
        return dict(data=servicesList)
    
    # Finally, if the user's input is valid, let's perform the lookup
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
    query = request.query.service

    # Generate both a list of all serivces, and a dictionary lookup of the services data.
    serviceDictionary = etl.dictlookup(data, "Service")
    allServices = etl.values(data, "Service")

    # Get all the Services Available
    serviceList = []
    for i in range(len(allServices)):
      if(i == 0):
         continue
      service = allServices[i]
      if(service not in serviceList):
         serviceList.append(service)

    # If the user's input isn't in the list, return a message
    if(query):
        if(query not in serviceList):
            # Throw a 204 (No Content Found) if the user's query isn't a valid service
            abort(204)
        # Otherwise, we're able to serve up the Service Data
        else:
            centresList = []
            # Iterate over the list of services in the Dictionary
            for i in range(len(serviceDictionary[query])):
                if(i == 0):
                    continue
                # Build out the JSON Object for the service
                centreObject = {
                    "CentreID": serviceDictionary[query][i]['CentreID'],
                    "Suburb": serviceDictionary[query][i]['Suburb'],
                    "Latitude": serviceDictionary[query][i]['Lat'],
                    "Longitude": serviceDictionary[query][i]['Lon'],
                }
                # Populate a list with the Centre Objects
                centresList.append(centreObject)
            # Finally, return the data in a structured response
            return dict(data = [{"service": query, "reporting_centres": centresList}])

    # If the user's query was blank or null, return all the service data
    elif (query == None or query == ""):
        returnData = []

        # For each Service, iterate through the Service Dictionary and populate the same JSON Structure as above.
        for i in range(len(serviceList)):
            if(i == 0):
                continue
            currentService = serviceList[i]
            currentCentres = []
            for i in range(len(serviceDictionary[currentService])):
                if (i == 0):
                    continue
                centreObject = {
                    "CentreID": serviceDictionary[currentService][i]['CentreID'],
                    "Suburb": serviceDictionary[currentService][i]['Suburb'],
                    "Latitude": serviceDictionary[currentService][i]['Lat'],
                    "Longitude": serviceDictionary[currentService][i]['Lon'],
                }
                currentCentres.append(centreObject)
                allCentres = {"service": currentService, "reporting_centres": currentCentres}
                returnData.append(allCentres)
        return dict(data=returnData)

run(host="localhost", port=8080, reloader=True)
