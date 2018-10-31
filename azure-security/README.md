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

From Azure Cloud Shell on [Azure Portal](https://portal.azure.com), perform the following steps:

![AzureCloudShell](media/azurecloudshell.png)

#### Create a [Resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups).

```console
$ az group create --name myVMRG --location eastus2
```

Output:
```console
{
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myVMRG",
  "location": "eastus2",
  "managedBy": null,
  "name": "myVMRG",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null
}
```

**Note:** You will need your Azure Subscription ID for some of the steps below. To get the subscription ID, run the command "az account list" from the Cloud Shell prompt.


#### Create a Virtual Machine on the resource group that was created in the previous steps

```console
az vm create \
  --resource-group myVMRG \
  --name myMSIVM1 \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys
```

**Note:** The command "--generate-ssh-keys" will use the existing SSH files ~/.ssh/id_rsa and ~/.ssh/id_rsa.pub. In case these files do not exist, they will be created as part of the "az vm create" command execution.

Output:

```console
{
  "fqdns": "",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myVMRG/providers/Microsoft.Compute/virtualMachines/myMSIVM1",
  "location": "eastus2",
  "macAddress": "AA-BB-CC-DD-EE-FF",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "1.1.1.1",
  "resourceGroup": "myVMRG",
  "zones": ""
}
```
**Note:** We will use the publicIpAddress from the output above in order to login into the VM.


#### Grant permission to read your Azure Resource Group

Use az vm identity assign with the identity assign command enable the system-assigned identity to an existing VM:

```console
az vm identity assign --resource-group myVMRG --name myMSIVM1
```

**Note:** We could create the VM with its identity assigned by adding the parameter "--assign-identity", as explained [here](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-cli-windows-vm#system-assigned-managed-identity).

Output:

```console
{
  "systemAssignedIdentity": "aa5a8fa2-4e31-4bc7-99ea-4af10269d783",
  "userAssignedIdentities": {}
}
```

**Note:** The UUID aa5a8fa2-4e31-4bc7-99ea-4af10269d783 is an example and you may use your information.

List the VM MSI Identity (principalId) that will be used to assign a role to the VM, which should match the "systemAssignedIdentity" from the previous output:

```console
MSIdentity=`az resource list -n myMSIVM1 --query [*].identity.principalId -o json | jq .[0] -r`
```

Assign "Reader" role to the VM for the resource group scope:

```console
az role assignment create --assignee $MSIdentity --role reader --scope /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myVMRG
```

Output:

```console
{
  "canDelegate": null,
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myVMRG/providers/Microsoft.Authorization/roleAssignments/aa5a8fa2-4e31-4bc7-99ea-4af10269d783",
  "name": "fa0c59bb-08f7-4a20-a4b3-2186a7c6d358",
  "principalId": "aa5a8fa2-4e31-4bc7-99ea-4af10269d783",
  "resourceGroup": "myVMRG",
  "roleDefinitionId": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
  "scope": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myVMRG",
  "type": "Microsoft.Authorization/roleAssignments"
}
```

**Note:** We are using system-assigned identity in this example. Be sure to review the [difference between a system-assigned and user-assigned managed identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview#how-does-it-work).

#### Go through the following steps in order to validate MSI


1. Login into the VM using the "publicIpAddress" information from the output after the VM creation

```console
ssh azureuser@1.1.1.1
```

2. Request Access Token:

```console 
response=$(curl -H Metadata:true "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fmanagement.azure.com/")
```

3. Parse Access Token Value:

```console 
access_token=$(echo $response | python -c 'import sys, json; print (json.load(sys.stdin)["access_token"])') 
```

4. Use the Token:

```console
SubID="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
RG="myVMRG"

url="https://management.azure.com/subscriptions/$SubID/resourceGroups/$RG?api-version=2016-09-01"

curl $url -H "x-ms-version: 2017-11-09" -H "Authorization: Bearer $access_token"
```

Output:
```console
{"id":"/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myVMRG","name":"myVMRG","location":"eastus2","properties":{"provisioningState":"Succeeded"}}
```

**Note:** In case you want to validate how MSI works, you can remove the role previously assigned and run the tests again.

```console
az role assignment delete --assignee XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX --role reader --scope /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myVMRG
```

Now, run the 4th step again (curl $url -H "x-ms-version: 2017-11-09" -H "Authorization: Bearer $access_token") from within the VM we configured, and you may notice an error message due to the access removal.

Output:

```console
{"error":{"code":"AuthorizationFailed","message":"The client 'f4011a26-1eec-4083-a2c2-ce173dca00bc' with object id 'f4011a26-1eec-4083-a2c2-ce173dca00bc' does not have authorizationto perform action 'Microsoft.Resources/subscriptions/resourceGroups/read' over scope '/subscriptions/30ec953a-f038-4636-b9b6-4ff8ba87b572/resourceGroups/myVMRG'."}}
```

#### Lab resources cleanup:

To delete the resources that were created as part of this lab, you can run the following command:

```console
$ az group delete --name myVMRG
```

## Lab 3: Data Access Management

## Lab 4: Governance

## Lab 5: Unified Visibility Control

## Lab 6: Operational Security Controls
