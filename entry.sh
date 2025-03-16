#!/bin/bash

python -m ovpn_idpass_plugin /home/ryo/development/Private/ovpn-password-plugin/ovpn_idpass_plugin/assets/ovpn_id_pass.txt $1
exit $?
