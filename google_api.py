"""API helper functions for Google Timezone and Geocoding."""
import googlemaps
import os

gmaps = googlemaps.Client(key=os.environ['GOOGLE_KEY'])


# -------------------- geocoding --------------------

def _get_possible_locations(location):
    """Makes API call to get possible locations matching given string."""
    return gmaps.geocode(location)


# -------------------- timezone --------------------

def _get_timezone(lat, lng):
    """Makes API call to get timezone matching given lat/long."""
    return gmaps.timezone((lat, lng))


# -------------------- helpers --------------------

def _bundle_single_location(location):
    name = location['formatted_address']
    lat = location['geometry']['location']['lat']
    lng = location['geometry']['location']['lng']

    timezone_res = _get_timezone(lat, lng)
    if 'timeZoneId' not in timezone_res:
        error = timezone_res.get('errorMessage',
                                 'Couldn\'t get timezone info.')
        raise FailedTimezoneRequestError(error)

    timezone = timezone_res['timeZoneId']
    return {'name': name, 'timezone': timezone}


def bundle_location_data(location):
    location_res = _get_possible_locations(location)
    bundle = []

    for possible_location in location_res:
        try:
            data = _bundle_single_location(possible_location)
        except FailedTimezoneRequestError as e:
            print e.message
            continue

        bundle.append(data)

    if not bundle:
        raise NoLocationResultsError('No location data was found.')

    return bundle


# -------------------- errors --------------------

class FailedTimezoneRequestError(ValueError):
    """Error occurred while fetching timezone."""
    pass


class NoLocationResultsError(ValueError):
    """No location data was found."""
    pass
