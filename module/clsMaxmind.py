import geoip2.database

class Maxmind(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        try:
            self.city_obj = geoip2.database.Reader('data/GeoLite2-City.mmdb')
            self.asn_obj = geoip2.database.Reader('data/GeoLite2-ASN.mmdb')
        except Exception as ex:
            print ex

    def getData(self, ip):
        city_result = self.city_obj.city(ip)
        asn_result = self.asn_obj.asn(ip)
        return {"ip_geo" : city_result.country.iso_code, "ip_org" : asn_result.autonomous_system_organization}
