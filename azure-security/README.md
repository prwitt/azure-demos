# Azure Security Labs

In this tutorial, we have a series of mini labs related to different Azure security topics that are discussed as part of the "Azure Security Overview" session delivered by [Paulo Renato](https://www.linkedin.com/in/paulorenato/). The presentation can be obtained upon contact. The areas we chose for this tutorial are described as follow: 

* Azure Networking
* Identity & Access Management
* Data Access Management
* Governance
* Unified Visibility Control
* Operational Security Controls

## Before you begin

* Make sure you have access to an [Azure Account](https://azure.microsoft.com/en-us/free/).
* The tutorial is wholly based on [Azure Cloud Shell](https://azure.microsoft.com/en-us/features/cloud-shell/) and the Azure Portal and does not require additional software installation on the client side.

## Lab 1: Azure Networking

## Lab 2: Identity & Access Management

* Create Azure VM
* Enable AAD MSI for the VM
* Grant permission to read Azure Resource Manager (as Reader)
* Learn how to use MSI on a VM to talk to ARM

1. Request Access Token:

```console 
response=$(curl -H Metadata:true "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fmanagement.azure.com/")
```
2. Parse Access Token Value:

```console 
access_token=$(echo $response | python -c 'import sys, json; print (json.load(sys.stdin)["access_token"])') 
```
3. Use the Token:

```console
url="https://management.azure.com/subscriptions/1ad652b3-4cc2-40fd-991d-2d2a6910d22b/resourceGroups/tmpMS_MSItest?api-version=2016-09-01"curl $url -H "x-ms-version: 2017-11-09" -H "Authorization: Bearer $access_token"
```


## Lab 3: Data Access Management

## Lab 4: Governance

## Lab 5: Unified Visibility Control

## Lab 6: Operational Security Controls
