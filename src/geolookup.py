__author__ = 'aaron'

import GeoIP
import json
import subprocess
from radix import Radix
import ipwhois

_rt = None
_gi = None

class Lookup(object):

    def __init__(me, fpath_geoip, fpath_known_networks):

        # load known networks into radix tree
        me.rt = Radix()
        with open(fpath_known_networks, 'rb') as known_net_file:
            known_networks = json.load(known_net_file)
            for p in known_networks:
                # Only keep prefixes that we know their country
                if 'country' in p:
                    n = me.rt.add(p['net'])
                    n.data['cc'] = p['country']

        # load geoIP data
        me.gi = GeoIP.open(fpath_geoip, GeoIP.GEOIP_STANDARD)

    def geoip(me, ip_addr):
        return me.gi.country_code_by_addr(ip_addr)

    def dig(me, ip_addr):
        x = subprocess.check_output(["dig", "+short", "-x", "74.125.236.52"]).rstrip()
        if len(x) == 0: return None
        return x

    def known_networks(me, ip_addr):
        return me.rt.search_best(network=ip_addr, masklen=32)

    def whois(me, ip_addr):
        return ipwhois.IPWhois(ip_addr).lookup()['nets'][0]['country']

    def summary(me, ip_addr):
        return {
            "GeoIP" : me.geoip(ip_addr),
            "Dig"   : me.dig(ip_addr),
            "Known Networks" : me.known_networks(ip_addr),
            "Whois" : me.whois(ip_addr)
        }