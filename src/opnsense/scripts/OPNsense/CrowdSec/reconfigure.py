#!/usr/bin/env python3

import urllib.parse
import json
import yaml


def load_config(filename):
    with open(filename) as fin:
        return yaml.safe_load(fin)

def save_config(filename, config):
    with open(filename, 'w') as fout:
        yaml.dump(config, fout)


def get_netloc(settings):
    return '{lapi_listen_address}:{lapi_listen_port}'.format(**settings)

def get_new_url(old_url, settings):
    old_tuple = urllib.parse.urlsplit(old_url)
    new_tuple = old_tuple._replace(netloc=get_netloc(settings))
    new_url = urllib.parse.urlunsplit(new_tuple)
    if not new_tuple.query and not new_tuple.fragment and not new_url.endswith('/'):
        new_url += '/'
    return new_url


def configure_agent(settings):
    config_path = '/usr/local/etc/crowdsec/config.yaml'
    config = load_config(config_path)

    config['api']['server']['listen_uri'] = get_netloc(settings)
    config['common']['log_dir'] = '/var/log/crowdsec'
    config['crowdsec_service']['acquisition_dir'] = '/usr/local/etc/crowdsec/acquis.d/'

    save_config(config_path, config)


def configure_lapi_credentials(settings):
    config_path = '/usr/local/etc/crowdsec/local_api_credentials.yaml'
    config = load_config(config_path)

    config['url'] = get_new_url(config['url'], settings)

    save_config(config_path, config)


def configure_bouncer(settings):
    config_path = '/usr/local/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml'
    config = load_config(config_path)

    config['api_url'] = get_new_url(config['api_url'], settings)
    config['log_dir'] = '/var/log/crowdsec'
    config['blacklists_ipv4'] = 'crowdsec_blacklists'
    config['blacklists_ipv6'] = 'crowdsec6_blacklists'
    config['pf'] = {'anchor_name': ''}

    save_config(config_path, config)


if __name__ == '__main__':
    with open('/usr/local/etc/crowdsec/opnsense-settings.json') as f:
        settings = json.load(f)
    configure_agent(settings)
    configure_lapi_credentials(settings)
    configure_bouncer(settings)
