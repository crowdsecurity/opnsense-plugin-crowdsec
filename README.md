
This OPNsense plugin is still under testing before GA release.

Feel free to try it but note that

 * It has been tested with 21.7 and 22.1, but you have to disable circular logs under 21.7

 * you need to install the latest crowdsec and crowdsec-firewall-bouncer from this repository (see under Releases)
   because they are not yet available in the upstream repository.

 * Don't expect many features on the web interface. Feel free to give us a feel of your priorities. The command line
   should work the same as under Linux.

 * The exact same application under Linux and FreeBSD can have logs in different location and format. This means that
   supporting OPNsense plugins may require modifying the existing parsers or writing new ones. We did that for SSH
   and the web interface, let us know what else you want us to protect on your firewall.

