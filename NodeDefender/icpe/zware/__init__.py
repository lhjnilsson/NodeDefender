from NodeDefender.icpe.zware import network, role, config

def system_status(icpe, payload):
    network.operation(icpe, *payload['stat'].split(','))
    network.including_state(icpe, payload['addstat'])
    network.excluding_state(icpe, payload['delstat'])
    network.aborting_state(icpe, payload['abtstat'])
    network.removing_state(icpe, payload['remstat'])
    network.replacing_state(icpe, payload['repstat'])
    network.learning_state(icpe, payload['learnstat'])
    network.updating_state(icpe, payload['udtstat'])
    network.transmitting_state(icpe, payload['txstat'])

    role.home_id(icpe, payload['netid'])
    role.controller_id(icpe, payload['controllerid'])
    role.nodebmp(icpe, payload['nodebmp'])
    role.supported_role(icpe, payload['role'])
    role.current_role(icpe, payload['zwaverole'])
    role.learnable(icpe, payload['learnable'])
    role.lifeline(icpe, payload['lifeline'])

    config.automatic_polling(icpe, payload['awpoll'])
    config.always_reporting(icpe, payload['awrpt'])
    config.general_wakeup(icpe, payload['acwkup'])
    config.forward_unsolicited(icpe, payload['unsolicit'])
    config.auto_reboot(icpe, payload['armask'])
    config.auto_isolate(icpe, payload['autoisolate'])
    config.battery_warning(icpe, payload['bnlevel'])
    config.health_check_interval(icpe, payload['hcinterval'])
    return True
