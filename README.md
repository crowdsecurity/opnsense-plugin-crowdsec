
Beware
------

This OPNsense plugin is still under testing before GA release.

Feel free to try it but note that

 * It has been tested with 21.7 and 22.1, but you have to disable circular logs under 21.7

 * you need to install the latest crowdsec and crowdsec-firewall-bouncer from this repository (see under Releases)
   because they are not yet available in the upstream repositories.

 * Don't expect many features on the web interface. Feel free to give us a feel of your priorities. The command line
   should work the same as under Linux.

 * The exact same application under Linux and FreeBSD can have logs in different location and format. This means that
   supporting OPNsense plugins may require modifying the existing parsers or writing new ones. We did that for SSH
   and the web interface, let us know what else you want us to protect on your firewall.


Installation
------------

To install the plugin you need OPNsense 21.7 or 22.1, then download:

 * crowdsec-1.2.3.txz
 * crowdsec-firewall-bouncer-0.0.22.txz
 * os-crowdsec-0.0.2.txz

Copy them to your firewall instance with scp, then install the packages in the
following order but do *not* enable them like the post-install message says:

```
# pkg add crowdsec-1.2.3.txz
...
# pkg add crowdsec-firewall-bouncer-0.0.22.txz
...
# pkg add os-crowdsec-0.0.2.txz
...
```

 * Login to OPNsense (web page, this time) and open Services/CrowdSec/Settings.

 * Read Introduction. Under the Settings tab, enable both checkboxes and save. Check Services/CrowdSec/Overview.

 * Optional, but recommended: [register to the Console](https://app.crowdsec.net/).
   This helps you to manage your instances, and us to have better overall metrics.

