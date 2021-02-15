#!/usr/bin/python3

import json

class FilterModule(object):

    def filters(self):
        return {
            'getEmailDomainsAndAccounts': self.getEmailDomainsAndAccounts,
            'getMcnIP': self.getMcnIP,
            }


    def getMcnIP(self, nics):

        mcnIP = 'Unable to get IP'
        for nic in nics:
            if ((nic['isMCN'] == True) and (nic['isManagement'] == True)):
                mcnIP = nic['ip']

        return mcnIP

    #Retrieves the accounts and domains to be created in the email server
    #sf: scenario json file
    def getEmailDomainsAndAccounts(self, accounts):

        acc = (accounts.split('-/-'))

        accountsList = []
        domainsList = []
        results = {}
        for l in acc:
            l = l[1:-1]
            l = l.split(',')
            aD = {}
            aD['domain'] = l[0]
            aD['username'] = l[1]
            aD['first_name'] = l[2]
            aD['last_name'] = l[3]
            aD['role'] = l[4]
            aD['password'] = l[5]

            accountsList.append(aD)
            if l[0] not in domainsList:
                domainsList.append(l[0])

        results['domains'] = domainsList
        results['accounts'] = accountsList

        return results


#########################################################
