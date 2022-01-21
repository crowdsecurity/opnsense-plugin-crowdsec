#!/bin/sh

if [ ! -e "/usr/local/etc/crowdsec/collections/opnsense.yaml" ]; then
    /usr/local/bin/cscli --error collections install crowdsecurity/opnsense
fi

/usr/local/bin/cscli --error hub update \
    && /usr/local/bin/cscli --error hub upgrade

service crowdsec enabled && service crowdsec restart

