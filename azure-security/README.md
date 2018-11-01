# Azure Security Labs

In this tutorial, we have a series of mini labs related to different Azure security topics that are discussed as part of the "Azure Security Overview" session delivered by [Paulo Renato](https://www.linkedin.com/in/paulorenato/). The presentation can be obtained upon contact. The areas we chose for this tutorial are described as follow: 

* [Azure Networking](#azure-networking)
* [Identity & Access Management](#identity-and-access)
* [Data Access Management](#data-access)
* [Governance](#governance)
* [Unified Visibility Control](#unified-control)
* [Operational Security Controls](#operational-controls)

## Before you begin

* Make sure you have access to an [Azure Account](https://azure.microsoft.com/en-us/free/).
* The tutorial is wholly based on [Azure Cloud Shell](https://azure.microsoft.com/en-us/features/cloud-shell/) and the [Azure Portal](https://portal.azure.com), and does not require additional software installation on the client side.

# <a name="azure-networking"></a>Lab 1: Azure Networking

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
$ az network asg create \
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
$ az network asg create \
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
$ az network nsg create \
  --resource-group myLab1RG \
  --name myLab1Nsg
```

#### Create security rules

The following example creates a rule that allows traffic inbound from the internet to the `myWebServers` application security group over ports 80 and 443:

```console
$ az network nsg rule create \
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

The following example creates a rule that allows traffic inbound from the Internet to the `myMgmtServers` application security group over port 22:

```console
$ az network nsg rule create \
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

>**Note:** In this lab, SSH (port 22) is exposed to the internet for the `myAsgMgmtServers` VM. For production environments, instead of exposing port 22 to the internet, it's recommended that you connect to Azure resources that you want to manage using a VPN or private network connection.

#### Create a Virtual Network

The following example creates a virtual named `myLab1VNet`:

```console
$ az network vnet create \
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

The following example adds a subnet named myLab1Subnet to the virtual network and associates the `myLab1Nsg` network security group to it:

```console
$ az network vnet subnet create \
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

The following example creates a VM that will serve as a web server. The `--asgs myAsgWebServers` option causes Azure to make the network interface it creates for the VM a member of the `myAsgWebServers` application security group.

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
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab1RG/providers/Microsoft.Compute/virtualMachines/myLab1VmMgmt",
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

Use the command that follows to create an SSH session with the `myLab1VmMgmt` VM. Replace with the public IP address of your VM. In the example above, the IP address is 40.70.204.109.

```console
$ ssh azureuser@40.70.204.109
```

>**Note:** The connection succeeds, because port 22 is allowed inbound from the `Internet` to the `myAsgMgmtServers` application security group that the network interface attached to the `myLab1VmMgmt` VM is in.

Use the following command to SSH to the myLab1VmWeb VM from the `myLab1VmMgmt` VM:

```console
$ ssh azureuser@MyLab1VmWeb
```

>**Note:** The connection succeeds because a default security rule within each network security group allows traffic over all ports between all IP addresses within a virtual network. You can't SSH to the myVmWeb VM from the Internet because the security rule for the `myAsgWebServers` doesn't allow port 22 inbound from the Internet.

Use the following commands to install the nginx web server on the myVmWeb VM:

```console
# Update package source
sudo apt-get -y update

# Install NGINX
sudo apt-get -y install nginx
```

>**Note:** The `myLab1VmWeb` VM is allowed outbound to the Internet to retrieve nginx because a default security rule allows all outbound traffic to the Internet. Exit the myLab1VmWeb SSH session, which leaves you at the `azureuser@myLab1VmMgmt:~$` prompt of the `myLab1VmMgmt` VM. To retrieve the nginx welcome screen from the `myLab1VmWeb` VM, enter the following command:

```console
$ curl myLab1VMWeb
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

# <a name="identity-and-access"></a>Lab 2: Identity & Access Management

This mini lab will focus on [Managed Identities](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview).

From Azure Cloud Shell on [Azure Portal](https://portal.azure.com), perform the following steps:

![AzureCloudShell](media/azurecloudshell.png)

#### Create a [Resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups).

```console
$ az group create --name myLab2RG --location eastus2
```

Output:
```console
{
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab2RG",
  "location": "eastus2",
  "managedBy": null,
  "name": "myLab2RG",
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
  --resource-group myLab2RG \
  --name myLab2VM1 \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys
```

>**Note:** The command `--generate-ssh-keys` will use the existing SSH files `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`. In case these files do not exist, they will be created as part of the `az vm create` command execution.

Output:

```console
{
  "fqdns": "",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myVMRG/providers/Microsoft.Compute/virtualMachines/myLab2VM1",
  "location": "eastus2",
  "macAddress": "AA-BB-CC-DD-EE-FF",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "40.70.131.116",
  "resourceGroup": "myLab2RG",
  "zones": ""
}
```
>**Note:** We will use the `publicIpAddress` from the output above in order to login into the VM.


#### Grant permission to read your Azure Resource Group

Use az vm identity assign with the identity assign command enable the system-assigned identity to an existing VM:

```console
$ az vm identity assign --resource-group myLab2RG --name myLab2VM1
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
$ MSIdentity=`az resource list -n myLab2VM1 --query [*].identity.principalId -o json | jq .[0] -r`
```

Assign "Reader" role to the VM for the resource group scope. Make sure you replace `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` with your real subscription id.

```console
$ az role assignment create --assignee $MSIdentity --role reader --scope /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myLab2RG
```

Output:

```console
{
  "canDelegate": null,
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myLab2RG/providers/Microsoft.Authorization/roleAssignments/aa5a8fa2-4e31-4bc7-99ea-4af10269d783",
  "name": "fa0c59bb-08f7-4a20-a4b3-2186a7c6d358",
  "principalId": "aa5a8fa2-4e31-4bc7-99ea-4af10269d783",
  "resourceGroup": "myLab2RG",
  "roleDefinitionId": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
  "scope": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myLab2RG",
  "type": "Microsoft.Authorization/roleAssignments"
}
```

>**Note:** We are using system-assigned identity in this example. Be sure to review the [difference between a system-assigned and user-assigned managed identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview#how-does-it-work).

#### Go through the following steps in order to validate MSI


1. Login into the VM using the `publicIpAddress` information from the output after the VM creation

```console
$ ssh azureuser@40.70.131.116
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
$ RG="myLab2RG"

$ url="https://management.azure.com/subscriptions/$SubID/resourceGroups/$RG?api-version=2016-09-01"

$ curl $url -H "x-ms-version: 2017-11-09" -H "Authorization: Bearer $access_token"
```

Output:
```console
{"id":"/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab2RG","name":"myLab2RG","location":"eastus2","properties":{"provisioningState":"Succeeded"}}
```

>**Note:** In case you want to validate how MSI works, you can remove the role previously assigned and run the tests again.

```console
$ az role assignment delete --assignee XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX --role reader --scope /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/ResourceGroups/myLab2RG
```

Now, run the 4th step again (`curl $url -H "x-ms-version: 2017-11-09" -H "Authorization: Bearer $access_token"`) from within the VM we configured, and you may notice an error message due to the access removal.

Output:

```console
{"error":{"code":"AuthorizationFailed","message":"The client 'f4011a26-1eec-4083-a2c2-ce173dca00bc' with object id 'f4011a26-1eec-4083-a2c2-ce173dca00bc' does not have authorizationto perform action 'Microsoft.Resources/subscriptions/resourceGroups/read' over scope '/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab2RG'."}}
```

#### Lab resources cleanup:

To delete the resources that were created as part of this lab, you can run the following command:

```console
$ az group delete --name myLab2RG
```

# <a name="data-access"></a>Lab 3: Data Access Management

This mini lab will focus on [Shared Access Signature](https://docs.microsoft.com/en-us/azure/storage/common/storage-dotnet-shared-access-signature-part-1).

From Azure Cloud Shell on [Azure Portal](https://portal.azure.com), perform the following steps:

![AzureCloudShell](media/azurecloudshell.png)

#### Create a [Resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups).

```console
$ az group create --name myLab3RG --location eastus2
```

Output:
```console
{
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myLab3RG",
  "location": "eastus2",
  "managedBy": null,
  "name": "myLab3RG",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null
}
```

#### Create Storage Account

>**Important:** The Storage account name is global and unique, so you need to use a random name. In the following example we are using `mylab3stgacct`. Note that it accepts between 3-24 characters and all lower-case.

```console
$ az storage account create --name mylab3stgacct --resource-group myLab3RG --sku Standard_LRS --location eastus2
```

Output:

```console
{
  "accessTier": null,
  "creationTime": "2018-10-31T18:17:51.904889+00:00",
  "customDomain": null,
  "enableHttpsTrafficOnly": false,
  "encryption": {
    "keySource": "Microsoft.Storage",
    "keyVaultProperties": null,
    "services": {
      "blob": {
        "enabled": true,
        "lastEnabledTime": "2018-10-31T18:17:52.108026+00:00"
      },
      "file": {
        "enabled": true,
        "lastEnabledTime": "2018-10-31T18:17:52.108026+00:00"
      },
      "queue": null,
      "table": null
    }
    ...
    <removed output>
}
```

#### Create a storage container to store blobs

```console
$ az storage container create --name mylab3stgcontainer --account-name mylab3stgacct
```

Output:

```console
{
  "created": true
}
```

#### Create Stored Access Policy for the container

First, let us see if there is any policy associated to the storage container recently created:

```console
$ az storage container policy list --container mylab3stgcontainer --account-name mylab3stgacct
```

Output:

```console
{}
```

As we could see, no stored policy is associated with the container created above. Now, let us create the `Stored Access Policy` for the container:

```console
$ start=`date -d "-30 minutes" '+%Y-%m-%dT%H:%MZ'`
$ end=`date -d "30 minutes" '+%Y-%m-%dT%H:%MZ'`
$ az storage container policy create --name mylab3policy1 --container-name mylab3stgcontainer --account-name mylab3stgacct --permissions dwrl --start $start --expiry $end
```

Output:

```console
{
  "etag": "\"0x8D63F5F5F4222C3\"",
  "lastModified": "2018-10-31T18:33:37+00:00"
}
```

Execute the command below to liste the pol

```console
$ az storage container policy list --container mylab3stgcontainer --account-name mylab3stgacct
```

Output:

```console
{
  "mylab3policy1": {
    "expiry": null,
    "permission": "rwdl",
    "start": null
  }
}
```

#### Create a SAS key based on Stored Access Policy

```console
$ az storage container generate-sas --name mylab3stgcontainer --account-name mylab3stgacct --policy-name mylab3policy1
```

Output:

```console
"sv=2018-03-28&si=mylab3policy1&sr=c&sig=71zzMlgFsRhNiqiBirNlWNAN8zQVdv0Xi36Q2SKoKNo%3D"
```

#### Test Access to the Storage Container

Upload a file to the storage account:

```console
$ sas="sv=2018-03-28&si=mylab3policy1&sr=c&sig=71zzMlgFsRhNiqiBirNlWNAN8zQVdv0Xi36Q2SKoKNo%3D"

$ echo "MyLab3 Upload Test" > MyLab3File.txt

$ az storage blob upload --name MyLab3File.txt --container-name mylab3stgcontainer --account-name mylab3stgacct --file MyLab3File.txt --sas-token $sas 
```

Validate you can access the blob as follow:

```console
$ curl "https://mylab3stgacct.blob.core.windows.net/mylab3stgcontainer/MyLab3File.txt?"$sas
```

>**Note:** As you append the SAS key value to the URL, it will look like this:  `https://storage account name and Azure URL/the container name/the filename?the sas-key value`.


Update the `Stored Access Policy` expiring date and try to access it again, as follow:

```console
$ start=`date -d "-30 minutes" '+%Y-%m-%dT%H:%MZ'`
$ end=`date -d "-30 minutes" '+%Y-%m-%dT%H:%MZ'`
$ az storage container policy update --name mylab3policy1 --container-name mylab3stgcontainer --account-name mylab3stgacct --permissions dwrl --start $start --expiry $end
```

Output:

```console
{
  "etag": "\"0x8D63F75B3FE941A\"",
  "lastModified": "2018-10-31T21:13:28+00:00"
}
```

If you try to access the same blob, you should get an error message, as follow:

```console
$ curl "https://mylab3stgacct.blob.core.windows.net/mylab3stgcontainer/MyLab3File.txt?"$sas
```

Output:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error>
   <Code>AuthenticationFailed</Code>
   <Message>Server failed to authenticate the request. Make sure the value of Authorization header is formed correctly including the signature.
RequestId:4c9acbf6-601e-00b1-455e-714e6b000000
Time:2018-10-31T21:14:09.2705135Z</Message>
   <AuthenticationErrorDetail>Signed expiry time [Wed, 31 Oct 2018 20:43:00 GMT] has to be after signed start time [Wed, 31 Oct 2018 20:43:00 GMT]</AuthenticationErrorDetail>
</Error>
```

>**Note:** If you update the `start` and `end` dates on the policy, the access can be restablished.


#### Lab resources cleanup:

To delete the resources that were created as part of this lab, you can run the following command:

```console
$ az group delete --name myLab3RG
```

# <a name="governance"></a>Lab 4: Governance

This mini lab will focus on [Azure Resource Manager Policy](https://docs.microsoft.com/en-us/azure/governance/policy/overview). Here you will see how to restrict a deployment to a given region.
You can find other policy samples [here](https://docs.microsoft.com/en-us/azure/governance/policy/samples/).

From Azure Cloud Shell on [Azure Portal](https://portal.azure.com), perform the following steps:

![AzureCloudShell](media/azurecloudshell.png)

#### Create a [Resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups).

```console
$ az group create --name myLab4RG --location eastus2
```

#### Prerequesites

Register the Policy Insights resource provider using Azure CLI. Registering the resource provider makes sure that your subscription works with it. To register a resource provider, you must have permission to perform the register action operation for the resource provider. This operation is included in the Contributor and Owner roles. Run the following command to register the resource provider:

```console
$ az provider register --namespace 'Microsoft.PolicyInsights'
```

#### Define and Assign the ARM Policy

In our example, we will define a policy that restricts deployment to West US 2 region. Create a policy definition with the following command.

```console
$ az policy definition create --name MyallowedLocations --display-name MyallowedLocations --rules '{
                            "if": {
                                "not": {
                                    "field": "location",
                                    "in": ["westus2"] 
                                }
                            },
                            "then": {
                                "effect": "deny"
                            }
                        }'
```

Output:

```console
{
  "description": null,
  "displayName": null,
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/policyDefinitions/MyallowedLocations",
  "metadata": null,
  "mode": null,
  "name": "MyallowedLocations",
  "parameters": {},
  "policyRule": {
    "if": {
      "not": {
        "field": "location",
        "in": [
          "westus2"
        ]
      }
    },
    "then": {
      "effect": "deny"
    }
  },
  "policyType": "Custom",
  "type": "Microsoft.Authorization/policyDefinitions"
}
```

Now, let's assign the policy to the subscription scope. Don't forget to replace `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` with your subscription ID.

```console
$ az policy assignment create --policy MyallowedLocations --name MyallowedLocations --display-name MyallowedLocations --scope /subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

Output:

```console
{
  "description": null,
  "displayName": null,
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/policyAssignments/4a5cdb94-7b3a-4d5d-9efa-a3f1dd7c5ddb",
  "metadata": null,
  "name": "4a5cdb94-7b3a-4d5d-9efa-a3f1dd7c5ddb",
  "notScopes": null,
  "parameters": null,
  "policyDefinitionId": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/policyDefinitions/MyallowedLocations",
  "scope": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "sku": {
    "name": "A0",
    "tier": "Free"
  },
  "type": "Microsoft.Authorization/policyAssignments"
}
```

#### Test the policy

Let's try to create a resource (VM) in in the resource group `myLab4RG`:

```console
$ az vm create \
  --resource-group myLab4RG \
  --name myLab4Vm \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys
```

If the policy was applied correctly, the deployment will fail with the following error message:

```console
Azure Error: InvalidTemplateDeployment
Message: The template deployment failed with multiple errors. Please see details for more information.
Exception Details:
	Error Code: RequestDisallowedByPolicy
	Message: Resource 'myLab4VmVNET' was disallowed by policy. Policy identifiers: '[{"policyAssignment":{"name":"2469dc55-706d-4cef-8a17-ad6076e8160a","id":"/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/policyAssignments/2469dc55-706d-4cef-8a17-ad6076e8160a"},"policyDefinition":{"name":"MyallowedLocations","id":"/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/policyDefinitions/MyallowedLocations"}},{"policyAssignment":{"name":"4a5cdb94-7b3a-4d5d-9efa-a3f1dd7c5ddb","id":"/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/policyAssignments/4a5cdb94-7b3a-4d5d-9efa-a3f1dd7c5ddb"},"policyDefinition":{"name":"MyallowedLocations","id":"/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/providers/Microsoft.Authorization/policyDefinitions/MyallowedLocations"}}]'.
	Target: myLab4VmVNET
```

>**Note:** The resource group `myLab4RG` was created in the `East US 2` region, while the policy restricts the deployment at `West US 2`.


#### Lab resources cleanup:

To delete the resources that were created as part of this lab, you can run the following commands:

```console
$ az group delete --name myLab4RG

$ az policy assignment delete --name MyallowedLocations

$ az policy definition delete --name MyallowedLocations 
```

# <a name="unified-control"></a>Lab 5: Unified Visibility Control

# <a name="operational-controls"></a>Lab 6: Operational Security Controls
