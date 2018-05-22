
# Azure Kubernetes Services (AKS) and Nirmata Hackathon

In this tutorial, you will learn how to deploy a Kubernetes Cluster utilizing Azure Kubernetes Services (AKS), and how to deploy multi-tier applications on this Cluster utilizing Nirmata. The following steps will help you to accomplish the following:

* Configure AKS via Azure CLI
* Deploy a Managed Kubernetes cluster
* Configure Nirmata
* Manage Multi-tier Application


## Before you begin

* Make sure you have access to an [Azure Account](https://azure.microsoft.com/en-us/free/).
* The tutorial is wholly based on [Azure Cloud Shell](https://azure.microsoft.com/en-us/features/cloud-shell/) and the Azure Portal and does not require additional software installation on the client side.

## Azure Kubernetes Services Configuration

From Azure Cloud Shell on Azure Portal, perform the following steps:

![AzureCloudShell](media/azurecloudshell.png)

* Create a [Resource Group](https://azure.microsoft.com/en-us/updates/resource-groups-in-azure-preview-portal/). Make sure you deploy it in a supported region for the Azure resource type 'Microsoft.ContainerService/managedClusters'. Using this command, ```az provider list --query "[?namespace=='Microsoft.ContainerService'].resourceTypes[]|[?contains(resourceType,'managedClusters')]"```, you can get more information on the regions that are currently supported.

```console
$ az group create --name myK8sRG --location centralus
```

Output:
```console
{
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourceGroups/myK8sRG",
  "location": "centralus",
  "managedBy": null,
  "name": "myK8sRG",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null
}
```

**Note:** The example above creates a resource group in Central US. As of mid May/2018, AKS is available on the following regions: East US (eastus), West Europe (westeurope), Central US (centralus), Canada Central (canadacentral), Canada East (canadaeast). Other regions will be available during GA.

* Before creating the AKS Cluster on the Resource Group created on the previous step, in case it is the first time you use this service on your Azure Subscription, you need to make sure the [Resource Provider](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-supported-services) is registered. The following command shows the status of your resource provider:

```console
az provider show --name "Microsoft.ContainerService" --query "{registrationState:registrationState}"
```

Output in case it is registered:
```console
{
  "registrationState": "Registered"
}
```

In case it is ot registered, the "registrationState" object will show as "NotRegistered", and you should register it with the following command before proceeding:

```console
az provider register --namespace Microsoft.ContainerService --wait
```

Repeat the command to verify the registration status, and if it shows as "Registered", we are good to proceed.


* Deploy a Managed Kubernetes Cluster on [AKS](https://azure.microsoft.com/en-us/services/container-service/). This process will take 5 minutes approximately.

```console
$ az aks create --resource-group myK8sRG --name myK8sCluster --node-count 1 --generate-ssh-keys
```

Output:
```console
{
  "additionalProperties": {},
  "agentPoolProfiles": [
    {
      "additionalProperties": {},
      "count": 1,
      "dnsPrefix": null,
      "fqdn": null,
      "name": "nodepool1",
      "osDiskSizeGb": null,
      "osType": "Linux",
      "ports": null,
      "storageProfile": "ManagedDisks",
      "vmSize": "Standard_DS1_v2",
      "vnetSubnetId": null
    }
  ],
  "dnsPrefix": "myK8sClust-myK8sRG-30ec95",
  "fqdn": "myk8sclust-myk8srg-30ec95-407988ed.hcp.centralus.azmk8s.io",
  "id": "/subscriptions/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resourcegroups/myK8sRG/providers/Microsoft.ContainerService/managedClusters/myK8sCluster",
  "kubernetesVersion": "1.9.6",
  "linuxProfile": {
    "additionalProperties": {},
    "adminUsername": "azureuser",
    "ssh": {
      "additionalProperties": {},
      "publicKeys": [
        {
          "additionalProperties": {},
          "keyData": "ssh-rsa XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXfkmmlWld7JKNdc7GwbxWbTFDu/4/Qe8X67+PBWNfPK3ywYpBNTYLjWzQx2BO/N97JwLW6HNfk/TpSFC3wASTcZnPIE4gbQ2bCHyPpyPSB+kv/RIwnwfohNrvoj5j8qRayRcHQuJe2rv+lRIpM0UEcaL7wOjOt50Pa0+oncvgOqxXLh67XpEf4sGhaBkE1AftJ/X/vjSXJB3YmZUMA7/Z4UtJv0+jXozOE3iw8U6nu2CTSDagXnf7/339w5MG/RtPlvLlF0NpBkvusaAutgPo74EkX"
        }
      ]
    }
  },
  "location": "centralus",
  "name": "myK8sCluster",
  "provisioningState": "Succeeded",
  "resourceGroup": "myK8sRG",
...
}
```

* Get credential

``` console
$ az aks get-credentials --resource-group myK8sRG --name myK8sCluster

```

Output:
```console
Merged "myK8sCluster" as current context in /home/<your-home-dir>/.kube/config
```

* Make sure you can access your cluster, and the STATUS is Ready

```console
$ kubectl get nodes
```

Output:
```console
NAME                       STATUS    ROLES     AGE       VERSION
aks-nodepool1-84578568-0   Ready     agent     8m        v1.9.6
```

Note that at the time this tutorial was written, the default version for the AKS cluster is v1.9.6. One of the benefits of managed K8s on Azure, is that you can upgrade it easily. We don't need to do it at this time.

## Nirmata Configuration

## Manage Multi-tier App


## Clean Up

To delete the resources that were created, you can run the following command:

```console
$ az group delete --name myK8sRG
```

For questions or suggestions about this tutorial, you can reach out to [Paulo Renato](https://www.linkedin.com/in/paulorenato/) on the Azure section, and [Jim Bugwadia](https://www.linkedin.com/in/jimbugwadia/) on the Nirmata section.
