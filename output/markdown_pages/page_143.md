### 5.2 Ensure IBM 10Cloudant encryption is enabled with customer managed dkeys (Manual)

##  Profile Applicability:

• Level 1

## Description:

IBM Cloudant encrypts all client data at-rest by default. For customers using a Dedicated Hardware plan instance, it is optional to use the service's integration with IBM Key Protect for customers to bring their own encryption key at provision time for the instance.



To provision a Cloudant Dedicated Hardware plan instance using Bring-Your-Own-Key with Key Protect, first ensure you are logged into your IBM Cloud account at https://cloud.ibm.com/. Note a paid account is required to provision a Cloudant Dedicated Hardware plan instance.



Before provisioning the Dedicated Hardware plan instance with BYOK with Key Protect,follow the authorization instructions between Key Protect and Cloudant:

1.Open your IBM Cloud dashboard.

2.From the menu bar, click Manage > Access (IAM).

3.In the side navigation, click Authorizations.

4.Click Create.

5.In the Source service menu, select the cloudant in Account.

6.In the Source service instance menu, select all instances.

7.In the Target service menu, select Key Protect in Account, and leave Instance ID of string equals All instances.



8.Enable the Reader role by checking the checkbox.

9.Click Authorize.

Ensure the necessary encryption key(s) in Key Protect have been created. (See IBM Key Protect documentation for those steps.)



 Next provision a Cloudant Dedicated Hardware plan instance and choose the BYOK with Key Protect option during the provisioning process:

## V ia Ul:

●1.From the IBM Cloud Dashboard,click on Create resource.

22.[Te_m]



Selectcoliofforins 

4.[Ta]

5.[Tabl 

6.公司添

