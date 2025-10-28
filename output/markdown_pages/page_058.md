##### 2.1.1.1 E Ensure Cloud Object Storage encryption is done with customer managed keys (Manual)

##  Profile Applicability:

Level 2

## Description:

Users can store objects in IBM Cloud Object Storage buckets by providing their own encryption keys which get applied at a per object level.



## Rationale:

Users can have added security and granular control over the encryption keys at a per object level.



## I mpact:

Users can configure Cloud Object Storage and use their own root keys when uploading objects. For any key rotation (or new key usage) users will have to issue a GET operation with the old key and a PUT operation with the new key.

## Audit:

## Using Console: N/A 

## Using APl/CLl:

[Ea]

by the following steps:



Ta 

following the guidelines on the Using the AWS CLI page 

1. Review the metadata of the object that is encrypted using the customer-provided key. The operation can be performed using an APl call or via a command-line interface. Here is an example call to get the object metadata:

aws --endpoint https://s3.private.au-syd.cloud-objectstorage.appdomain.cloud s3api head-object --bucket <bucket-name> --key <object-name> --sse-customer-algorithm=AES256 --sse-customerkey=<customer-key-used-to encrypt-the-object>



2.The presence of the object headers SSECustomerKeyMD5 and 

SSECustomerAlgorithm from the APl/CLI response should confirm that the object 

is encrypted using the key.

