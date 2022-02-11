
Beware
------

This OPNsense plugin is still under testing before GA release.

Feel free to try it but note that

 * It has been tested with 21.7 and 22.1, but you have to disable circular logs under 21.7

 * you need to install the latest crowdsec and crowdsec-firewall-bouncer from this repository (see under Releases)
   because they are not yet available in the upstream repositories. Previous versions won't work properly.

 * Don't expect many features on the web interface. Feel free to give us a feel of your priorities. The command line
   should work the same as under Linux.

 * The exact same application under Linux and FreeBSD can have logs in different location and format. This means that
   supporting OPNsense plugins may require modifying the existing parsers or writing new ones. We did that for SSH
   and the web interface, let us know what else you want us to protect on your firewall.


Installation
------------

Once the plugin is release, you will be able to install from the OPNsense admin interface.

For now, to install the plugin you need OPNsense 21.7 or 22.1, then download:

 * crowdsec-1.3.0.txz
 * crowdsec-firewall-bouncer-0.0.22_2.txz
 * os-crowdsec-0.0.5.txz

You find them in the
[Releases](https://github.com/crowdsecurity/opnsense-plugin-crowdsec/releases)
page, under "Assets". For example, `opnsense_22.1-freebsd_13-oscrowdsec_0.0.5.tar` contains
the three files listed above.

Copy them to your firewall instance with scp, then install the packages in the
following order but do *not* enable them like the post-install message says:

```
# pkg add ./crowdsec-1.3.0.txz
...
# pkg add ./crowdsec-firewall-bouncer-0.0.22_2.txz
...
# pkg add ./os-crowdsec-0.0.5.txz
...
```

 * Login to OPNsense (web page, this time) and open Services/CrowdSec/Settings.

 * Read Introduction. Under the Settings tab, enable both checkboxes and save. Check Services/CrowdSec/Overview.

 * Optional, but recommended: [register to the Console](https://app.crowdsec.net/).
   This helps you to manage your instances, and us to have better overall metrics.


Upgrade
-------

Download the new version and use "pkg upgrade" instead of "pkg add".

You can also use "pkg remove crowdsec crowdsec-firewall-bouncer oscrowdsec"
followed by the three "pkg add", but respect the installation order.


Changelog
---------

v0.0.5

 - fixed an issue that prevented the bouncer from banning IPs on opnsense
 - fixed support for notification plugins

