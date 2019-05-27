# Solution Overview

The purpose of this content is to describe how **"Alert Rule"** and **"Action Group"** on Azure Monitor for VMSS can trigger an API call to remove a VM instance out of the Azure Load Balancer backend pool.

Details on the APIs used to accomplish this can be found on the [Azure VMSS documentation](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets)

To demonstrate how the solution works, a test environment with a VMSS configured with two VM instances was set up. Every time a monitoring rule condition was satisfied, e.g., high CPU (several metrics are supported), Azure Monitor called a VMSS API to remove the particular VM instance from the Load Balancer backend pool. Alert Rules, Action Groups, and Automation Runbooks were used to accomplish the task.

The solution works as follow: the alert rule monitors a host-based metric (e.g., CPU utilization) and once the threshold is met, the rule acts based on what is defined in the Action Group, which in our tests it sent an e-mail, and triggered an Automation Runbook. Action group sends a payload called "Webhookdata", which contains information about the rules, the resource ID, and the VM instance where the potential issue occurred. By parsing this parameter, we ran the Python script to call the VMSS API to act towards the specific instance.

I used the following API to GET the VM instance configuration, and to change (PUT) its configuration, e.g., modifying the "networkProfileConfiguration" of a VMSS Instance:

```console
HTTP Verb:  GET and PUT

URL https://<endpoint>/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachineScaleSets/{vMScaleSetName}/virtualMachines/{instance-id}?api-version={api-version}
```

**There are three "simple" steps you need to do to accomplish this configuration, as follow:**

1. Configure Azure Automation Runbook with your Python Script
2. Configure Action Group
3. Configure Alert Rule

**1)** [Here](https://docs.microsoft.com/en-us/azure/automation/automation-quickstart-create-account) you can read more on how to configure the Azure Automation Runbook. The following Python Script performs the necessary tasks to remove a VM instance from the Load Balancer backend pool. Note that it is just a prototype and there are several points to be optimized, e.g., parsing the ["Webhookdata"](https://docs.microsoft.com/en-us/azure/automation/automation-first-runbook-textual-python2#use-input-parameters) sent as an input parameter as a JSON object to the Python script at the Automation Runbook via the Action Group, and simplify the authentication piece as the Automation Runbook makes it simpler. The prototype still work though.

On VMSS, we had to configure the following:

**2)** Create "Action Group"

* Under the VMSS blade, go to Monitor > Alerts
* Under Alerts, click on "Manage actions"
* Click on "Add action group"

In the testing scenario, we created an Action group that will send an e-mail and trigger an Automation Runbook, as you can see below under Actions. Use the Runbook you created previously with the Python script discussed earlier.

Here you have more information on how to Create an Action Group.

**3)** Create a "New alert rule"

* Under the VMSS blade, go to Monitor > Alerts
* Under Alerts, click on "New alert rule". The "Resource" will be selected by default. Create a condition by configuring a signal logic. There are dozens of "Signal Type" for you to choose.
* Under actions, select the "Action Group" previously created.

For questions or suggestions about this content, you can reach out to [Paulo Renato](https://www.linkedin.com/in/paulorenato/).