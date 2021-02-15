#!/usr/bin/python3

import os
import random
import vymgmt
import subprocess
from itertools import permutations
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleAction, _AnsibleActionDone, AnsibleActionFail
from ansible.module_utils._text import to_native



###################################################################

def configureCommon(ruleset):

     cmd = []
     cmd.append("firewall name " + ruleset + " default-action drop")

     cmd.append("firewall name " + ruleset + \
                " rule 1 action accept")
     cmd.append("firewall name " + ruleset + \
                " rule 1 state established enable")
     cmd.append("firewall name " + ruleset + \
                " rule 1 state related enable")

     cmd.append("firewall name " + ruleset + \
                " rule 2 action drop")
     cmd.append("firewall name " + ruleset + \
                " rule 2 state invalid enable")
     cmd.append("firewall name " + ruleset + \
                " rule 2 log enable")
     return cmd

def rule10_ALL(ruleset):
     cmd = []
     cmd.append("firewall name " + ruleset + \
                " rule 10 action accept")
     cmd.append("firewall name " + ruleset + \
                " rule 10 log enable")
     return cmd

def rule20_ICMP(ruleset):
     cmd = []
     cmd.append("firewall name " + ruleset + \
                " rule 20 action accept")
     cmd.append("firewall name " + ruleset + \
                " rule 20 protocol icmp")
     cmd.append("firewall name " + ruleset + \
                " rule 20 log enable")
     return cmd

def rule30_SSH(ruleset):
     cmd = []
     cmd.append("firewall name " + ruleset + \
                " rule 30 action accept")
     cmd.append("firewall name " + ruleset + \
                " rule 30 destination port 22")
     cmd.append("firewall name " + ruleset + \
                " rule 30 protocol tcp")
     cmd.append("firewall name " + ruleset + \
                " rule 30 log enable")
     return cmd

def rule40_WEB(ruleset):
     cmd = []
     cmd.append("firewall name " + ruleset + \
                " rule 40 action accept")
     cmd.append("firewall name " + ruleset + \
                " rule 40 destination port http,https")
     cmd.append("firewall name " + ruleset + \
                " rule 40 protocol tcp")
     cmd.append("firewall name " + ruleset + \
                " rule 40 log enable")
     return cmd

def rule50_SMTP(ruleset):
     cmd = []
     cmd.append("firewall name " + ruleset + \
                " rule 50 action accept")
     cmd.append("firewall name " + ruleset + \
                " rule 50 destination port smtp")
     cmd.append("firewall name " + ruleset + \
                " rule 50 protocol tcp")
     cmd.append("firewall name " + ruleset + \
                " rule 50 log enable")
     return cmd

def rule60_DNS(ruleset):
     cmd = []
     cmd.append("firewall name " + ruleset + \
                " rule 60 action accept")
     cmd.append("firewall name " + ruleset + \
                " rule 60 destination port 53")
     cmd.append("firewall name " + ruleset + \
                " rule 60 protocol tcp_udp")
     cmd.append("firewall name " + ruleset + \
                " rule 60 log enable")
     return cmd


def createCustomRule(ruleset, rule_num, accept=True, src_ip=None, dst_ip=None, dst_port=None, dst_proto=None):
     cmd = []

     if accept:
         cmd.append("firewall name " + ruleset + \
                    " rule " + str(rule_num) + " action accept")
     else:
         cmd.append("firewall name " + ruleset + \
                    " rule " + str(rule_num) + " action drop")
     if src_ip is not None:
         cmd.append("firewall name " + ruleset + \
                    " rule " + str(rule_num) + " source address " + str(src_ip))
     if dst_port is not None:
         cmd.append("firewall name " + ruleset + \
                    " rule " + str(rule_num) + " destination port " + str(dst_port))
     if dst_ip is not None:
         cmd.append("firewall name " + ruleset + \
                    " rule " + str(rule_num) + " destination address " + str(dst_ip))
     if dst_proto is not None:
         cmd.append("firewall name " + ruleset + \
                    " rule " + str(rule_num) + " protocol " + str(dst_proto))
     cmd.append("firewall name " + ruleset + \
                " rule " + str(rule_num) + " log enable")
     return cmd

def createRulesetsDefaultRules(rulesets):
     cmd = []

     for ruleset in rulesets:

          cmd.extend(configureCommon(ruleset))

          if (ruleset == 'LAN-DMZ' or
              ruleset == 'LAN-WAN' or
              ruleset == 'DMZ-WAN' or
              ruleset == 'SOC-LAN' or
              ruleset == 'SOC-DMZ' or
              ruleset == 'SOC-OT' or
              ruleset == 'SOC-WAN' or
              ruleset == 'SOC-LOCAL' or
              ruleset == 'LOCAL-LAN' or
              ruleset == 'LOCAL-DMZ' or
              ruleset == 'LOCAL-SOC' or
              ruleset == 'LOCAL-WAN' or
              ruleset == 'LOCAL-OT' or
              ruleset == 'MGT-LOCAL'
              ):
               cmd.extend(rule10_ALL(ruleset))

          if (ruleset == 'SOC-LOCAL'):
               cmd.extend(rule30_SSH(ruleset))
               cmd.extend(rule20_ICMP(ruleset))

          if (ruleset == 'WAN-DMZ'):
               cmd.extend(rule40_WEB(ruleset))
               cmd.extend(rule20_ICMP(ruleset))

          if (ruleset == 'WAN-LAN'):
               cmd.extend(rule50_SMTP(ruleset))

          if (ruleset == 'WAN-LOCAL' or
              ruleset == 'LAN-LOCAL' or
              ruleset == 'LAN-OT'
              ):
               cmd.extend(rule20_ICMP(ruleset))

          if (ruleset == 'OT-LAN'):
               cmd.extend(rule20_ICMP(ruleset))
               cmd.extend(rule60_DNS(ruleset))

     return cmd

def createRulesets(zones):
     comb = permutations(zones,2)
     rulesets = []
     for c in comb:
          rulesets.append(c[0] + '-' + c[1])

     return rulesets

def createZones(ifaces):
     cmd = []
     for iface in ifaces:
          cmd.append("zone-policy zone " + iface['zone'] + \
                     " interface " + iface['adapter'] )

     return cmd

def createZoneLOCAL(ethx):
     cmd = []
     cmd.append("zone-policy zone LOCAL local-zone")

     return cmd
def setZonePolicies(zones):

     cmd = []
     comb = permutations(zones,2)
     rulesets = []
     for co in comb:
          src = co[0]
          dst = co[1]

          cmd.append("zone-policy zone " + dst + " from " + src + \
                     " firewall name " + src + "-" + dst)
     return cmd

def setDefaultGW(defaultGW):
     cmd = []
     cmd.append("protocols static route 0.0.0.0/0 next-hop " + str(defaultGW))
     return cmd

def configureNAT(iface):
     cmd = []
     cmd.append("nat source rule 10 outbound-interface " + iface['adapter'])
     cmd.append("nat source rule 10 translation address 'masquerade'")
     return cmd

def setPortForwarding(ruleset, rule_num, dst_ip, dst_port, prot, in_interface, transl_ip, transl_port):

     cmd = []

     cmd.append("nat destination rule " + str(rule_num) + \
                " destination address " +  str(dst_ip))
     cmd.append("nat destination rule " + str(rule_num) + \
                " destination port " +  str(dst_port))
     cmd.append("nat destination rule " + str(rule_num) + \
                " inbound-interface " +  str(in_interface))
     cmd.append("nat destination rule " + str(rule_num) + \
                " protocol " +  str(prot))
     cmd.append("nat destination rule " + str(rule_num) + \
                " translation address " +  str(transl_ip))
     cmd.append("nat destination rule " + str(rule_num) + \
                " translation port " +  str(transl_port))

     return cmd

########################################################


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)

        try:
            ifaces = self._task.args.get('interfaces')
            defaultGW = self._task.args.get('default_gw')
            #Interface format: {'id': '100', 'adapter': 'eth0', 'ip': '10.0.4.1', 'mask': '24', 'zone': 'SOC'}
            zones = []
            [zones.append(i['zone']) for i in ifaces if i['zone'] not in zones]
            zones.append('LOCAL')
            print(zones)
        except AnsibleError as e:
            raise AnsibleActionFail(to_native(e))


        rulesets = createRulesets(zones)
        cmd = []
        cmd.extend(setDefaultGW(defaultGW))
        #cmd.extend(configureNAT(ifaces[4]))


        cmd.extend(createRulesetsDefaultRules(rulesets))

        try:
            cust_rules = self._task.args.get('custom_rules')
            #Custom rule format: ruleset, rule_num, accept=True, src_ip=None, dst_ip=None, dst_port=None, dst_proto=None
            if cust_rules is not None:
                for rule in cust_rules:
                    cmd.extend(createCustomRule(**rule))
        except AnsibleError as e:
            raise AnsibleActionFail(to_native(e))

        final_cmd=['set ' + v for v in cmd]
        final_cmd.insert(0, 'configure')
        final_cmd.append('commit')

        result1 = self._execute_module(module_name='vyos_command',
                                      module_args={'commands': final_cmd},
                                      task_vars=task_vars,
                                      tmp=tmp)

        cmd=[]
        cmd.extend(createZones(ifaces))
        cmd.extend(createZoneLOCAL('lo'))
        cmd.extend(setZonePolicies(zones))
        final_cmd=['set ' + v for v in cmd]
        final_cmd.append('commit')
        final_cmd.append('exit')

        result2 = self._execute_module(module_name='vyos_command',
                                      module_args={'commands': final_cmd},
                                      task_vars=task_vars,
                                      tmp=tmp)

        return result1
