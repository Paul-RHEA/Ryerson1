#!/usr/bin/python3

import json

class FilterModule(object):

    def filters(self):
        return {
            'getEmailDomainsAndAccounts': self.getEmailDomainsAndAccounts,
            'getCampaigns': self.getCampaigns
            }


    def getCampaigns(self, campaigns):

        camps = (campaigns.split('-/-'))

        results = []
        for c  in camps:
            c = c[1:-1]
            c = c.split(',')
            camp = {}

            camp['name'] = c[0]

            template = {}
            template['name'] = c[1]
            camp['template'] = template

            page = {}
            page['name'] = c[2]
            camp['page'] = page

            camp['url'] = c[3]

            sProf = {}
            sProf['name'] = c[4]
            camp['smtp'] = sProf

            camp['send_by_date'] = "null"

            grps = []
            grp = {}
            grp['name'] = c[5]
            grps.append(grp)
            camp['groups'] = grps

            results.append(camp)

        return results

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
