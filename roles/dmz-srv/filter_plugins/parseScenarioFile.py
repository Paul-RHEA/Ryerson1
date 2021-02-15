#!/usr/bin/python3

import json

class FilterModule(object):

    def filters(self):
        return {
            'getMcnIP': self.getMcnIP,
            'getUserLayerIP': self.getUserLayerIP
            }


    def getMcnIP(self, nics):

        mcnIP = 'Unable to get IP'
        for nic in nics:
            if ((nic['isMCN'] == True) and (nic['isManagement'] == True)):
                mcnIP = nic['ip']

        return mcnIP

    def getUserLayerIP(self, nics):
        userLayerIP = ''
        for nic in nics:
            if ((nic['isMCN'] == False ) and (nic['isManagement'] == False )):
                userLayerIP = nic['ip']

        return userLayerIP
