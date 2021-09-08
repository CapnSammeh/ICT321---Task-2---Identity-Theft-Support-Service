'''
RESTFUL Web Service Demo

In this  demo,  you  are  required  to  implement  a  Python script with the name ‘web_finder.py’ to provide two RESTful Web services:
    • Get  reporting  centre  services by postcode. The server should accept a ‘getServices’ query from the client browser similar to “/getServices?postcode=xxxx”. After processing this request, the service should return a HTML document containing the list of available services for a given postcode, including the following fields (attributes): 
        o Service, Suburb. 
    • Get reporting centre by service name. The server should accept a ‘getRCentre’ query from  the client browser similar to “/getRCentre?service=xxxx”. After processing this 
    request, the service should return a HTML document containing the list of available reporting centres for a given service, including the following fields (attributes): 
        o CentreID, Suburb, Latitude, Longitude. 
    The Python Bottle and petl frameworks are required for this implementation. Data for the  service is from the output file “reportingCentre_service_locations.csv” of the integration demo.
'''

from bottle import route, request, response, template, run
import petl as etl

# Get Import Data
data = etl.fromcsv('reportingCentre_service_locations.csv')

# Get Services Route
@route('/getServices')
def get_services():
    postcode = request.query.postcode
    lookup = etl.lookup(data, 'Postcode', ('Service, Suburb'))
    lookupResponse = lookup[postcode]
    return template('{{Service}}, {{Suburb}}', Service=lookupResponse[2], Suburb=postcode)
run(host='localhost', port=8080)

# Get Reporting Centre Route
@route('/‘getRCentre’')
def get_services():
    postcode = request.query.postcode
    return template('{{CentreID}}, {{Suburb}}, {{Latitude}}, {{Longitude}}', service=postcode, suburb=postcode)

run(host='localhost', port=8080)