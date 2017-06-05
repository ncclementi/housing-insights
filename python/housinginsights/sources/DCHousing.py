"""
Module provides the api connection class for DCHousing data in opendata.dc.gov
web site.
"""
#This first if __name__ is needed if this file is test-run from the command line. 
# path.append needs to happen before the first from import statement
import sys, os
if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir)))


from pprint import pprint
import logging

from housinginsights.sources.base import BaseApiConn
from housinginsights.sources.models.DCHousing import FIELDS,\
    DCHousingResult


class DCHousingApiConn(BaseApiConn):
    """
    API Interface to the Affordable Housing data set on opendata.dc.gov.

    Inherits from BaseApiConn class.
    """

    BASEURL = 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/' \
              'Property_and_Land_WebMercator/MapServer/62'
    # default query to get all data as json output
    QUERY = '/query?where=1%3D1&outFields=*&outSR=4326&f=json'

    def __init__(self):
        super().__init__(DCHousingApiConn.BASEURL)

        self._available_unique_data_ids = ['dchousing']

    def get_data(self, unique_data_ids=None, sample=False, output_type = 'csv', **kwargs):
        """
        Returns JSON object of the entire data set.

        """
        if unique_data_ids == None:
            unique_data_ids = self._available_unique_data_ids

        for u in unique_data_ids:
            if (u not in self._available_unique_data_ids):
                #TODO this will always be raised when passing a list to get_multiple_api_sources method for those not in this class. 
                logging.info("  The unique_data_id '{}' is not supported by the DCHousingApiConn".format(u))

            else:
                result = self.get(DCHousingApiConn.QUERY)
                if result.status_code != 200:
                    err = "An error occurred during request: status {0}"
                    raise Exception(err.format(result.status_code))

                if output_type == 'stdout':
                    pprint(result.json())
                elif output_type == 'csv':
                    data = result.json()['features']
                    results = [DCHousingResult(address['attributes']).data for address in
                               data]
                    self.result_to_csv(FIELDS, results, self.output_paths[u])

if __name__ == '__main__':
    
    # Pushes everything from the logger to the command line output as well.
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,"logs","sources.log"))
    logging.basicConfig(filename=log_path, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    api_conn = DCHousingApiConn()
    unique_data_ids = None #['crime_2013']
    api_conn.get_data(unique_data_ids)