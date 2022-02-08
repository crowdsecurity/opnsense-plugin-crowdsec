#!/bin/sh

if [ ! -e "/usr/local/etc/crowdsec/collections/opnsense.yaml" ]; then
    /usr/local/bin/cscli --error collections install crowdsecurity/opnsense
fi

/usr/local/bin/cscli --error hub update \
    && /usr/local/bin/cscli --error hub upgrade

if service crowdsec enabled; then
    ( service crowdsec restart || service crowdsec start ) >/dev/null
fi

