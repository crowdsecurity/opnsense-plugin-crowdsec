
Beware
------

This OPNsense plugin is still under testing before GA release.

Feel free to try it but note that

 * In this pre-release version you may need some manual steps, see below under Configuration
   and under Upgrade.

 * It has been tested with 21.7 and 22.1, but you have to disable circular logs under 21.7

 * you need to install the latest crowdsec and crowdsec-firewall-bouncer from
   this repository because they are not yet available in the upstream
   repositories. Previous versions may not work properly.

 * Don't expect many features on the web interface. Feel free to give us a feel
   of your priorities. The command line should work the same as under Linux.

 * The exact same application under Linux and FreeBSD can have logs in
   different location and format. This means that supporting OPNsense plugins
   may require modifying the existing parsers or writing new ones. We did that
   for SSH and the web interface, let us know what else you want us to protect
   on your firewall.


Installation
------------

> If you are upgrading from v0.0.5, you had to create a couple of Alias and
> related Rules objects in the admin interface. This is not necessary anymore.
> It's a good idea to remove them before upgrading, to avoid any conflict and
> test the new automated configuration. You can do that under Firewall -> Aliases
> and Firewall -> Rules -> Floating.
>
> The plugin will re-create the Alias objects and two associated floating rules
> (automatically generated, hidden by default).

Once the plugin is released, you will be able to install it from the OPNsense admin interface.

For now, to install it you need OPNsense 21.7 or 22.1, then download:

 * crowdsec-1.3.2.txz
 * crowdsec-firewall-bouncer-0.0.23.r2.txz
 * os-crowdsec-0.1.txz

You find them in the
[Releases](https://github.com/crowdsecurity/opnsense-plugin-crowdsec/releases)
page, under "Assets". For example, `opnsense_22.1-freebsd_13-oscrowdsec_0.1.tar` contains
the three files listed above.

Copy them to your firewall instance with scp, then install the packages in the
following order but do *not* enable them like the post-install messages say.
These instruction are for using them without OPNsense.

```
# pkg add ./crowdsec-1.3.2.txz
...
# pkg add ./crowdsec-firewall-bouncer-0.0.23.r2.txz
...
# pkg add ./os-crowdsec-0.0.7.txz
...
```

 * Login to OPNsense (web page, this time) and open Services/CrowdSec/Settings.

 * Read Introduction. Under the Settings tab, enable both checkboxes and save. Check Services/CrowdSec/Overview.

 * Optional, but recommended: [register to the Console](https://app.crowdsec.net/).
   This helps you to manage your instances, and us to have better overall metrics.


Configuration
-------------

The creation of firewall tables and rules has now been automated, you don't need
to do anything.

You should already be able to see the blocked IPs in Firewall -> Diagnostics -> Aliases.

A quick way to test that everything is working correctly is to execute the
following command. Your ssh session should freeze and kick you out. You will
not be able to connect to the firewall from the same IP address for two
minutes. It might be a good idea to have a secondary IP from which you can
connect, should anything go wrong.

```
# cscli decisions add -t ban -d 2m -i `echo $SSH_CLIENT | cut -d' ' -f1`
```

Remote LAPI configuration (optional)
------------------------------------
To use an external Local API server, the configuration must be done manually.
These instructions assume you already have set up a central LAPI server that is
reachable by the OPNSense instance. You will also need SSH access with root permissions
to both OPNSense and LAPI server.

These instructions largely follow the ones in [Crowdsec Tutorials](https://crowdsec.net/blog/multi-server-setup/)

- Register the LAPI server (url is e.g. `http://10.0.0.10:8080`):
```
# cscli lapi register -u <url>
```
- Edit `/usr/local/rc.d/crowdsec`, in `crowdsec_start()` -function, append `-no-api` to the start command:
```
crowdsec_start()                                                                
{                                                                               
    /usr/sbin/daemon -f -p ${pidfile} -t "${desc}" -- \                         
        ${command} -c "${crowdsec_config}" ${crowdsec_flags} -no-api            
} 
```
- In the web UI under Settings, change the LAPI Listen address and port according to your LAPI server
  and click Apply
- At this stage Crowdsec service will fail to start, you need to validate OPNSense on the LAPI server.
  Login via SSH and first get the machine ID of OPNSense:
```
[root@lapi-server ~]# cscli machines list
---------------------------------------------------------------------------------------------------...
 NAME                                              IP ADDRESS     LAST UPDATE           STATUS     ...
---------------------------------------------------------------------------------------------------...
 be689d27c623aa393d1c8604eda5d1b47a62526b2e2e0201  10.0.0.10   2022-05-28T05:21:24Z  ✔️       v1.3.4...
 97f403614b44aa27d60c1ff8adb93d6fae8f9d9697e1a98c  10.0.0.1    2022-05-29T10:03:33Z  🚫             ...                                                                   
---------------------------------------------------------------------------------------------------...
[root@lapi-server ~]# 
```
- Then validate the OPNSense machine using the ID from the NAME column from the listing:
```
# cscli machines validate 97f403614b44aa27d60c1ff8adb93d6fae8f9d9697e1a98c
```
- Reload Crowdsec on OPNSense, either with `service crowdsec reload` or by clicking Apply
  in the web interface.
- Next, set up OPNSense as a bouncer on the LAPI server. On the LAPI server (replace `opnsense` with a name you want):
```
[root@lapi-server ~]# cscli bouncers add opnsense
Api key for 'opnsense':

   563e64de5ab7bda490add012bc9ad09b0

Please keep this key since you will not be able to retrieve it!
```
- On OPNSense, edit `/usr/local/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml`
  and replace `api_key: ` with the output from the previous command on the LAPI server
- Reload Crowdsec again, either with `service crowdsec reload` or by clicking Apply
  in the web interface.





Upgrade
-------

> From v0.0.5: remove the Alias objects named `crowdsec_blackslists` and
> `crowdsec6_blacklists`, and the rules of the same name.

Download the new version of the plugin, extract and use "pkg upgrade" instead of "pkg add".

You can also use "pkg remove crowdsec crowdsec-firewall-bouncer oscrowdsec"
followed by the three "pkg add", but respect the installation order.


Uninstalling
------------

If you want to completely remove the plugin and all its configuration, uninstall
it from the admin interface, then:

 - `pkg remove crowdsec crowdsec-firewall-bouncer`
 - `rm -rf /var/log/crowdsec /usr/local/etc/crowdsec`


Changelog
---------

v0.1

 - fixed packet tags with ipv6
 - custom `crowdsec_flags`, `crosdsec_firewall_flags`

v0.0.9

 - fixed the javascript, 0.0.8 had a syntax error
 - new option: rules_tag
 - new option: lapi_manual_configuration
 - ipv4/ipv6 validation with regexp

v0.0.8

 - crowdsec update 1.3.2
 - configurable `rules_log` and LAPI address/port

v0.0.7

 - automated removal of Alias objects when the plugin is uninstalled

v0.0.6

 - crowdsec update 1.3.1.r1
 - bouncer update to 0.0.23.r1
 - automated creation of Alias and Rule objects

v0.0.5

 - fixed an issue that prevented the bouncer from banning IPs on opnsense
 - fixed support for notification plugins

