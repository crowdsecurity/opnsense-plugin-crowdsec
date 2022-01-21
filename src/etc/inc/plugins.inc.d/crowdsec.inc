<?php

// SPDX-License-Identifier: MIT
// SPDX-FileCopyrightText: © 2021 CrowdSec <info@crowdsec.net>

function crowdsec_enabled()
{
    global $config;

    return isset($config['OPNsense']['crowdsec']['general']['firewall_bouncer_enabled']) &&
    $config['OPNsense']['crowdsec']['general']['firewall_bouncer_enabled'] == 1;
}

function crowdsec_firewall($fw)
{
    if (!crowdsec_enabled()) {
        return;
    }

    $fw->registerAnchor('crowdsec', 'fw');
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
