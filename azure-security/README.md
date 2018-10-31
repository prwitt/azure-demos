# Azure Security Labs

In this lab tutorial, we have a series of mini labs related to different Azure security topics that are discussed as part of the "Azure Security Overview" session delivered by [Paulo Renato](https://www.linkedin.com/in/paulorenato/). The presentation can be obtained upon contact. The areas we chose for this tutorial are described as follow: 

* [Azure Networking](#azure-networking)
* [Identity & Access Management](#identity-and-access)
* [Data Access Management](#data-access)
* [Governance](#governance)
* [Unified Visibility Control](#unified-control)
* [Operational Security Controls](#operational-controls)

## Before you begin

* Make sure you have access to an [Azure Account](https://azure.microsoft.com/en-us/free/).
* The tutorial is wholly based on [Azure Cloud Shell](https://azure.microsoft.com/en-us/features/cloud-shell/) and the Azure Portal, and does not require additional software installation on the client side.

## <a name="azure-networking"></a>Lab 1: Azure Networking

This mini lab will focus on the capabilities to filter network traffic with network security group.

From Azure Cloud Shell on [Azure Portal](https://portal.azure.com), perform the following steps:

![AzureCloudShell](media/azurecloudshell.png)

#### Create a [Resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups).

```console
$ az group create --name myLab1RG --location eastus2
```

Output:
```console
{
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG",
  "location": "eastus2",
  "managedBy": null,
  "name": "myLab1RG",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null
}
```

#### Create a an application security group

An application security group enables you to group servers with similar port filtering requirements.

```console
az network asg create \
  --resource-group myLab1RG \
  --name myAsgWebServers \
  --location eastus2
```

Output:

```console
{
  "etag": "W/\"5064b9a2-e0d6-4b3b-ae96-752914501417\"",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/applicationSecurityGroups/myAsgWebServers",
  "location": "eastus2",
  "name": "myAsgWebServers",
  "provisioningState": "Succeeded",
  "resourceGroup": "myLab1RG",
  "resourceGuid": null,
  "tags": null,
  "type": "Microsoft.Network/applicationSecurityGroups"
}
```

```console
az network asg create \
  --resource-group myLab1RG \
  --name myAsgMgmtServers \
  --location eastus2
```

Output:

```console
{
  "etag": "W/\"e729b06a-6279-4b2c-9516-76e35b4831ee\"",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/applicationSecurityGroups/myAsgMgmtServers",
  "location": "eastus2",
  "name": "myAsgMgmtServers",
  "provisioningState": "Succeeded",
  "resourceGroup": "myLab1RG",
  "resourceGuid": null,
  "tags": null,
  "type": "Microsoft.Network/applicationSecurityGroups"
}
```

#### Create a network security group

```console
az network nsg create \
  --resource-group myLab1RG \
  --name myLab1Nsg
```

#### Create security rules

The following example creates a rule that allows traffic inbound from the internet to the myWebServers application security group over ports 80 and 443:

```console
az network nsg rule create \
  --resource-group myLab1RG \
  --nsg-name myLab1Nsg \
  --name Allow-Web-All \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --priority 100 \
  --source-address-prefix Internet \
  --source-port-range "*" \
  --destination-asgs "myAsgWebServers" \
  --destination-port-range 80 443
```

Output:

```console
{
  "access": "Allow",
  "description": null,
  "destinationAddressPrefix": "",
  "destinationAddressPrefixes": [],
  "destinationApplicationSecurityGroups": [
    {
      "etag": null,
      "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/applicationSecurityGroups/myAsgWebServers",
      "location": null,
      "name": null,
      "provisioningState": null,
      "resourceGroup": "myLab1RG",
      "resourceGuid": null,
      "tags": null,
      "type": null
    }
  ],
  "destinationPortRange": null,
  "destinationPortRanges": [
    "80",
    "443"
  ],
  "direction": "Inbound",
  "etag": "W/\"843bca9d-e93e-4b22-9896-1eeb888848e9\"",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/networkSecurityGroups/myLab1Nsg/securityRules/Allow-Web-All",
  "name": "Allow-Web-All",
  "priority": 100,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "resourceGroup": "myLab1RG",
  "sourceAddressPrefix": "Internet",
  "sourceAddressPrefixes": [],
  "sourceApplicationSecurityGroups": null,
  "sourcePortRange": "*",
  "sourcePortRanges": [],
  "type": "Microsoft.Network/networkSecurityGroups/securityRules"
}

```

The following example creates a rule that allows traffic inbound from the Internet to the myMgmtServers application security group over port 22:

```console
az network nsg rule create \
  --resource-group myLab1RG \
  --nsg-name myLab1Nsg \
  --name Allow-SSH-All \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --priority 110 \
  --source-address-prefix Internet \
  --source-port-range "*" \
  --destination-asgs "myAsgMgmtServers" \
  --destination-port-range 22
  ```

  Output:

```console
{
  "access": "Allow",
  "description": null,
  "destinationAddressPrefix": "",
  "destinationAddressPrefixes": [],
  "destinationApplicationSecurityGroups": [
    {
      "etag": null,
      "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/applicationSecurityGroups/myAsgMgmtServers",
      "location": null,
      "name": null,
      "provisioningState": null,
      "resourceGroup": "myLab1RG",
      "resourceGuid": null,
      "tags": null,
      "type": null
    }
  ],
  "destinationPortRange": "22",
  "destinationPortRanges": [],
  "direction": "Inbound",
  "etag": "W/\"cb999cef-4c90-4997-9515-74402ba00bba\"",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/networkSecurityGroups/myLab1Nsg/securityRules/Allow-SSH-All",
  "name": "Allow-SSH-All",
  "priority": 110,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "resourceGroup": "myLab1RG",
  "sourceAddressPrefix": "Internet",
  "sourceAddressPrefixes": [],
  "sourceApplicationSecurityGroups": null,
  "sourcePortRange": "*",
  "sourcePortRanges": [],
  "type": "Microsoft.Network/networkSecurityGroups/securityRules"
}
```

>**Note:** In this lab, SSH (port 22) is exposed to the internet for the myAsgMgmtServers VM. For production environments, instead of exposing port 22 to the internet, it's recommended that you connect to Azure resources that you want to manage using a VPN or private network connection.

#### Create a Virtual Network

The following example creates a virtual named myLab1VNet:

```console
az network vnet create \
  --name myLab1VNet \
  --resource-group myLab1RG \
  --address-prefixes 192.168.0.0/16
```

>**Note:** Here we are using the network address `192.168.0.0/16`, but you can use an address that fits better your environment.

Output:

```console
{
  "newVNet": {
    "addressSpace": {
      "addressPrefixes": [
        "192.168.0.0/16"
      ]
    },
    "ddosProtectionPlan": null,
    "dhcpOptions": {
      "dnsServers": []
    },
    "enableDdosProtection": false,
    "enableVmProtection": false,
    "etag": "W/\"b7d145a6-16ac-4df9-9965-57be8eee125b\"",
    "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/virtualNetworks/myLab1VNet",
    "location": "eastus2",
    "name": "myLab1VNet",
    "provisioningState": "Succeeded",
    "resourceGroup": "myLab1RG",
    "resourceGuid": "9caec3b3-b2ca-4584-8628-b3d45694752c",
    "subnets": [],
    "tags": {},
    "type": "Microsoft.Network/virtualNetworks",
    "virtualNetworkPeerings": []
  }
}
```

The following example adds a subnet named myLab1Subnet to the virtual network and associates the myLab1Nsg network security group to it:

```console
az network vnet subnet create \
  --vnet-name myLab1VNet \
  --resource-group myLab1RG \
  --name myLab1Subnet \
  --address-prefix 192.168.0.0/24 \
  --network-security-group myLab1Nsg
```

Output:

```console
{
  "addressPrefix": "192.168.0.0/24",
  "addressPrefixes": null,
  "delegations": [],
  "etag": "W/\"df7935ae-e23a-41ff-afd5-e1948b4333aa\"",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/virtualNetworks/myLab1VNet/subnets/myLab1Subnet",
  "interfaceEndpoints": null,
  "ipConfigurationProfiles": null,
  "ipConfigurations": null,
  "name": "myLab1Subnet",
  "networkSecurityGroup": {
    "defaultSecurityRules": null,
    "etag": null,
    "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Network/networkSecurityGroups/myLab1Nsg",
    "location": null,
    "name": null,
    "networkInterfaces": null,
    "provisioningState": null,
    "resourceGroup": "myLab1RG",
    "resourceGuid": null,
    "securityRules": null,
    "subnets": null,
    "tags": null,
    "type": null
  },
  "provisioningState": "Succeeded",
  "purpose": null,
  "resourceGroup": "myLab1RG",
  "resourceNavigationLinks": null,
  "routeTable": null,
  "serviceAssociationLinks": null,
  "serviceEndpointPolicies": null,
  "serviceEndpoints": null,
  "type": "Microsoft.Network/virtualNetworks/subnets"
}
```

#### Create a Virtual Machine on the resource group that was created in the previous steps

The following example creates a VM that will serve as a web server. The `--asgs myAsgWebServers` option causes Azure to make the network interface it creates for the VM a member of the myAsgWebServers application security group.

The `--nsg ""` option is specified to prevent Azure from creating a default network security group for the network interface Azure creates when it creates the VM. To streamline this article, a password is used.

```console
$ az vm create \
  --resource-group myLab1RG \
  --name myLab1VmWeb \
  --image UbuntuLTS \
  --vnet-name myLab1VNet \
  --subnet myLab1Subnet \
  --nsg "" \
  --asgs myAsgWebServers \
  --admin-username azureuser \
  --generate-ssh-keys
```

>**Note:** The command `--generate-ssh-keys` will use the existing SSH files `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`. In case these files do not exist, they will be created as part of the `az vm create` command execution.

Output:

```console
{
  "fqdns": "",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Compute/virtualMachines/myLab1VmWeb",
  "location": "eastus2",
  "macAddress": "00-0D-3A-0E-E8-6A",
  "powerState": "VM running",
  "privateIpAddress": "192.168.0.4",
  "publicIpAddress": "40.70.210.77",
  "resourceGroup": "myLab1RG",
  "zones": ""
}
```

>**Note:** We will use the `publicIpAddress` from the output above in order to login into the VM.

Create a VM to serve as a management server:

```console
$ az vm create \
  --resource-group myLab1RG \
  --name myLab1VmMgmt \
  --image UbuntuLTS \
  --vnet-name myLab1VNet \
  --subnet myLab1Subnet \
  --nsg "" \
  --asgs myAsgMgmtServers \
  --admin-username azureuser \
  --generate-ssh-keys
```

Output:

```console
{
  "fqdns": "",
  "id": "/subscriptions/30ec953a-f038-4636-b9b6-4ff8ba87b572/resourceGroups/myLab1RG/providers/Microsoft.Compute/virtualMachines/myLab1VmMgmt",
  "location": "eastus2",
  "macAddress": "00-0D-3A-04-7B-5D",
  "powerState": "VM running",
  "privateIpAddress": "192.168.0.5",
  "publicIpAddress": "40.70.204.109",
  "resourceGroup": "myLab1RG",
  "zones": ""
}
```

#### Test traffic filters

Copy the your SSH keys to the `myLab1VmMgmt` VM as it will be used for you to login into the `myLab1VmWeb` VM later:

```console
$ scp ~/.ssh/id_rsa* azureuser@40.70.204.109:~/.ssh/
```

Output:

```
id_rsa                                             100% 1679     1.6KB/s   00:00
id_rsa.pub                                         100%  380     0.4KB/s   00:00
```

Use the command that follows to create an SSH session with the myLab1VmMgmt VM. Replace with the public IP address of your VM. In the example above, the IP address is 40.70.204.109.

```console
$ ssh azureuser@40.70.204.109
```

>**Note:** The connection succeeds, because port 22 is allowed inbound from the `Internet` to the `myAsgMgmtServers` application security group that the network interface attached to the `myLab1VmMgmt` VM is in.

Use the following command to SSH to the myLab1VmWeb VM from the myLab1VmMgmt VM:

```console
$ ssh azureuser@MyLab1VmWeb
```

>**Note:** The connection succeeds because a default security rule within each network security group allows traffic over all ports between all IP addresses within a virtual network. You can't SSH to the myVmWeb VM from the Internet because the security rule for the myAsgWebServers doesn't allow port 22 inbound from the Internet.

Use the following commands to install the nginx web server on the myVmWeb VM:

```console
# Update package source
sudo apt-get -y update

# Install NGINX
sudo apt-get -y install nginx
```

>**Note:** The myLab1VmWeb VM is allowed outbound to the Internet to retrieve nginx because a default security rule allows all outbound traffic to the Internet. Exit the myLab1VmWeb SSH session, which leaves you at the `azureuser@myLab1VmMgmt:~$` prompt of the `myLab1VmMgmt` VM. To retrieve the nginx welcome screen from the `myLab1VmWeb` VM, enter the following command:

```console
curl myLab1VMWeb
```

Output:
```console
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
...
```

Logout of the `myLab1VmMgmt` VM. To confirm that you can access the `myLab1VmWeb` web server from outside of Azure, enter `curl <publicIpAddress>` from your own computer. The connection succeeds, because port 80 is allowed inbound from the Internet to the `myAsgWebServers` application security group that the network interface attached to the `myLab1VmWeb` VM is in. You can try to access `myLab1VmWeb` via SSH and you will notice that it is not working, as it is allowed only from the `myLab1VmMgmt`.

#### Lab resources cleanup:

To delete the resources that were created as part of this lab, you can run the following command:

```console
$ az group delete --name myLab1RG
```

## <a name="identity-and-access"></a>Lab 2: Identity & Access Management

This mini lab will focus on [Managed Identities](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview).

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

>**Note:** You will need your Azure Subscription ID for some of the steps below. To get the subscription ID, run the command `az account list` from the Cloud Shell prompt.


#### Create a Virtual Machine on the resource group that was created in the previous steps

```console
$ az vm create \
  --resource-group myVMRG \
  --name myMSIVM1 \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys
```

>**Note:** The command `--generate-ssh-keys` will use the existing SSH files `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`. In case these files do not exist, they will be created as part of the `az vm create` command execution.

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
>**Note:** We will use the `publicIpAddress` from the output above in order to login into the VM.


#### Grant permission to read your Azure Resource Group

Use az vm identity assign with the identity assign command enable the system-assigned identity to an existing VM:

```console
$ az vm identity assign --resource-group myVMRG --name myMSIVM1
```

>**Note:** We could create the VM with its identity assigned by adding the parameter `--assign-identity`, as explained [here](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-cli-windows-vm#system-assigned-managed-identity).

Output:

```console
{
  "systemAssignedIdentity": "aa5a8fa2-4e31-4bc7-99ea-4af10269d783",
  "userAssignedIdentities": {}
}
```

>**Note:** The UUID `aa5a8fa2-4e31-4bc7-99ea-4af10269d783` is an example and you may use your information.

List the VM MSI Identity (`principalId`) that will be used to assign a role to the VM, which should match the `systemAssignedIdentity` from the previous output:

```console
$ MSIdentity=`az resource list -n myMSIVM1 --query [*].identity.principalId -o json | jq .[0] -r`
```

Assign "Reader" role to the VM for the resource group scope:

```console
$ az role assignment create --assignee $MSIdentity --role reader --scope /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myVMRG
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

>**Note:** We are using system-assigned identity in this example. Be sure to review the [difference between a system-assigned and user-assigned managed identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview#how-does-it-work).

#### Go through the following steps in order to validate MSI


1. Login into the VM using the `publicIpAddress` information from the output after the VM creation

```console
$ ssh azureuser@1.1.1.1
```

2. Request Access Token:

```console 
$ response=$(curl -H Metadata:true "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fmanagement.azure.com/")
```

3. Parse Access Token Value:

```console 
$ access_token=$(echo $response | python -c 'import sys, json; print (json.load(sys.stdin)["access_token"])') 
```

4. Use the Token:

```console
$ SubID="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
$ RG="myVMRG"

$ url="https://management.azure.com/subscriptions/$SubID/resourceGroups/$RG?api-version=2016-09-01"

$ curl $url -H "x-ms-version: 2017-11-09" -H "Authorization: Bearer $access_token"
```

Output:
```console
{"id":"/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myVMRG","name":"myVMRG","location":"eastus2","properties":{"provisioningState":"Succeeded"}}
```

>**Note:** In case you want to validate how MSI works, you can remove the role previously assigned and run the tests again.

```console
$ az role assignment delete --assignee XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX --role reader --scope /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myVMRG
```

Now, run the 4th step again (`curl $url -H "x-ms-version: 2017-11-09" -H "Authorization: Bearer $access_token"`) from within the VM we configured, and you may notice an error message due to the access removal.

Output:

```console
{"error":{"code":"AuthorizationFailed","message":"The client 'f4011a26-1eec-4083-a2c2-ce173dca00bc' with object id 'f4011a26-1eec-4083-a2c2-ce173dca00bc' does not have authorizationto perform action 'Microsoft.Resources/subscriptions/resourceGroups/read' over scope '/subscriptions/30ec953a-f038-4636-b9b6-4ff8ba87b572/resourceGroups/myVMRG'."}}
```

#### Lab resources cleanup:

To delete the resources that were created as part of this lab, you can run the following command:

```console
$ az group delete --name myVMRG
```

## <a name="data-access"></a>ab 3: Data Access Management

## <a name="governance"></a>Lab 4: Governance

## <a name="unified-control"></a>Lab 5: Unified Visibility Control

## <a name="operational-controls"></a>Lab 6: Operational Security Controls
