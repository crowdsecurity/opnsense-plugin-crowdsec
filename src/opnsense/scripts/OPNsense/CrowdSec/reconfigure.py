#!/usr/bin/env python3

import yaml

agent_config_path = '/usr/local/etc/crowdsec/config.yaml'
bouncer_config_path = '/usr/local/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml'

def configure_agent():
    with open(agent_config_path) as fin:
        config = yaml.safe_load(fin)

    config['common']['log_dir'] = '/var/log/crowdsec'
    config['crowdsec_service']['acquisition_dir'] = '/usr/local/etc/crowdsec/acquis.d/'

    with open(agent_config_path, 'w') as fout:
        yaml.dump(config, fout)


def configure_bouncer():
    with open(bouncer_config_path) as fin:
        config = yaml.safe_load(fin)

    config['log_dir'] = '/var/log/crowdsec'
    config['blacklists_ipv4'] = 'crowdsec_blacklists'
    config['blacklists_ipv6'] = 'crowdsec6_blacklists'
    config['pf'] = {'anchor_name': ''}

    with open(bouncer_config_path, 'w') as fout:
        yaml.dump(config, fout)


if __name__ == '__main__':
    configure_agent()
    configure_bouncer()
