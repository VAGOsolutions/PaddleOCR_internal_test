「

"deployment: {"id": "crn:vl:staging:public:databases-for-enterprisedb:us
df0dd7e706c8::","name":"crn:vl:staging:public:databases-for-enterprisedb:us
south:a/b9552134280015ebfde430a819fa4bb3:5589ecbf-de5f-4eac-9917
df0dd7e706c8::",
"type": "enterprisedb",
"platform_options": {

"disk_encryption_key_crn": "",
"backup_encryption_key_crn": ""
"version": "12",
'admin usernames":「

"database": "admin"
"enable private_endpoints": false,
"enable_public_endpoints: true,
"disablements": []

}

1

5. The lack of text in "disk_encryption_key_crn": and"backup_encryption_key_crn":means that your deployment is encrypted at rest with IBM managed encryption keys. If there is text after "crn" then that will be the unique identifier of the encryption key that is customer-managed for encryption at rest or for backups.

## Remediation:

 No remediation procedure. lmpossible for end-user to impact this control in a negatie way.



## Default Value:

By default all objects stored on IBM Cloud Databases are encrypted at-rest.


<div style="text-align: center;"><html><body><table border="1"><tr><td>Controls Version</td><td>Control</td><td>IG 1</td><td>IG2</td><td>IG3</td></tr><tr><td>v8</td><td>3.11 Encrypt Sensitive Data at Rest Encrypt sensitive data at rest on servers, applications, and databases containing sensitive data. Storage-layer encryption, also known as server-side encryption, meets the minimum requirement of this Safeguard. Additional encryption methods may include application-layer encryption, also known as client-side encryption, where access to the data storage device(s) does not permit accesstothe plain-text data.</td><td></td><td></td><td></td></tr></table></body></html></div>


## CIS Controls: