<?php

// SPDX-License-Identifier: MIT
// SPDX-FileCopyrightText: © 2021 CrowdSec <info@crowdsec.net>

use OPNsense\Core\Config;

function bouncer_enabled()
{
    global $config;

    return isset($config['OPNsense']['crowdsec']['general']['firewall_bouncer_enabled']) &&
    $config['OPNsense']['crowdsec']['general']['firewall_bouncer_enabled'] == 1;
}

function add_alias_if_not_exist($name, $description, $proto) {
    $model = new OPNsense\Firewall\Alias();
    foreach ($model->aliases->alias->iterateItems() as $alias) {
        if ((string)$alias->name == $name) {
            return;
        }
    }

    $new_alias = $model->aliases->alias->Add();
    $new_alias->name = $name;
    $new_alias->description = $description;
    $new_alias->proto = $proto;
    $new_alias->type = 'external';
    $model->serializeToConfig();
    Config::getInstance()->save();
}

function crowdsec_firewall(\OPNsense\Firewall\Plugin $fw)
{
    if (!bouncer_enabled()) {
        return;
    }

    add_alias_if_not_exist('crowdsec_blacklists', 'CrowdSec (IPv4)', 'IPv4');

    $fw->registerFilterRule(
        1, /* priority */
        array(
            'ipprotocol'     => 'inet',
            'descr'          => 'CrowdSec (IPv4)',
            'from'           => '$crowdsec_blacklists',     # $ to reference an alias
            'type'           => 'block',
            'quick'          => true
        ),
        null
    );

    add_alias_if_not_exist('crowdsec6_blacklists', 'CrowdSec (IPv6)', 'IPv6');

    $fw->registerFilterRule(
        1, /* priority */
        array(
            'ipprotocol'     => 'inet6',
            'descr'          => 'CrowdSec (IPv6)',
            'from'           => '$crowdsec6_blacklists',    # $ to reference an alias
            'type'           => 'block',
            'quick'          => true
        ),
        null
    );
}

function crowdsec_services()
{
    $services[] = array(
        'description' => 'CrowdSec',
        'configd' => array(
            'restart' => array('crowdsec restart'),
            'start' => array('crowdsec start'),
            'stop' => array('crowdsec stop'),
        ),
        'name' => 'crowdsec'
    );

    return $services;
}
