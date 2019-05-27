"""
Created on May 20 2019
@author: Paulo Renato
Version: 0.1beta
"""
import adal
import requests
import json
import pprint
import sys
import re

def run_RemoveVMFromLBBEPool():
    # Service Principal info
    tenant_id= '12345678-1234-1234-1234-123456789abc'
    application_id= '12345678-1234-1234-1234-123456789abc'
    application_secret= 'FakePassW0rd!'

    # Azure Environment
    # Replace with your own information about Subscription, RG, VMSS Name
    subscription_id= '12345678-1234-1234-1234-123456789abc'
    authentication_endpoint = 'https://login.microsoftonline.com/'
    resource_endpoint  = 'https://management.core.windows.net/'
    azure_endpoint = 'https://management.azure.com'
    resource_group = 'rg-vmss-lab1'
    VMSS_name = 'vmsslab1'
    VMSS_endpoint = azure_endpoint + '/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group + '/providers/Microsoft.Compute/virtualMachineScaleSets/' + VMSS_name

    def parse_parameter():
        # this function parses the Webhookdata payload received from Action Group
        # there is opportunity to optimize it
        input_data=(sys.argv[1:])
        parsed_data=((re.split(r'vmsslab1_',str(input_data))))
        return (parsed_data[1][0])

    VMSSinstanceId = parse_parameter()

    def access_token():
        # get an Azure access token using the adal library
        context = adal.AuthenticationContext(authentication_endpoint + tenant_id)
        token_response = context.acquire_token_with_client_credentials(resource_endpoint, application_id, application_secret)
        access_token = token_response.get('accessToken')
        return access_token

    # print(access_token())

    def VMSS_instanceview():
        # show VMSS configuration
        headers = {"Authorization": 'Bearer ' + access_token()}
        json_output = requests.get(azure_endpoint,headers=headers).json()
        VMSSep_instanceview = VMSS_endpoint + "/instanceView?api-version=2019-03-01"
        VMSSresponse = requests.get(VMSSep_instanceview,headers=headers).json()
        pprint.pprint(VMSSresponse)

    # VMSS_instanceview()

    def VMSS_instanceIdview():
        # show VMSS instance configuration
        headers = {"Authorization": 'Bearer ' + access_token()}
        json_output = requests.get(azure_endpoint,headers=headers).json()
        VMSSep_instance = VMSS_endpoint+"/virtualMachines/" + VMSSinstanceId + "?api-version=2019-03-01"
        VMSSresponse = requests.get(VMSSep_instance,headers=headers).json()
        return VMSSresponse

    # VMSS_instanceIdview()

    def VMSS_removefromLB():
        # Remove VM instance from the load balancer
        VMSSconfigdata=VMSS_instanceIdview()
        try:
            del VMSSconfigdata['properties']['networkProfileConfiguration']['networkInterfaceConfigurations'][0]['properties']['ipConfigurations'][0]['properties']['loadBalancerBackendAddressPools']
            headers = {"Authorization": 'Bearer ' + access_token(),"Content-Type": 'application/json'}
            VMSSep_instance = VMSS_endpoint+"/virtualMachines/" + VMSSinstanceId + "?api-version=2019-03-01"
            VMSSUpdateresponse = requests.put(VMSSep_instance,headers=headers,data=json.dumps(VMSSconfigdata))
            print(VMSSUpdateresponse)
            pprint.pprint("Load Balancer removed from the instance "+VMSSinstanceId+" network profile.")
        except KeyError:
            pprint.pprint("VM Instance does not have Load Balancer Backend Pool config in Network Profile")
    
    VMSS_removefromLB()

if __name__ == "__main__":
    run_RemoveVMFromLBBEPool()