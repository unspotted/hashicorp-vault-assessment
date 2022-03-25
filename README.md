# hashicorp-vault-assessment

## Preparation and Setup
- Installed and troubleshooted WSL and Ubuntu distribution package.
- Installed Vault.
- Completed Vault CLI quick start tutorial.

## Technical Task
1. Set up AWS secrets engine using personal AWS account credentials. No troubleshooting was needed.
2. Used the provided option for converting CLI commands into curl strings. Command and output:
```bash
$ vault write -output-curl-string aws/roles/my-role \
> credential_type=iam_user \
> policy_document=-<<EOF
> {
> "Version": "2012-10-17",
> "Statement": [
> {
> "Effect": "Allow",
> "Action": "ec2:*",
> "Resource": "*"
> }
> ]
> }
> EOF
curl -X PUT -H "X-Vault-Request: true" -H "X-Vault-Token: $(vault print token)" -d '{"credential_type":"iam_user","policy_document":"{\n\"Version\": \"2012-10-17\",\n\"Statement\": [\n{\n\"Effect\": \"Allow\",\n\"Action\": \"ec2:*\",\n\"Resource\": \"*\"\n}\n]\n}\n"}' http://127.0.0.1:8200/v1/aws/roles/my-role
```
3. Policy included in `aws-policy.hcl`.
Commands:

Upload policy.
```bash
$ vault policy write aws-policy - << aws-policy.hcl
Success! Uploaded policy: aws-policy
```
Create token using policy.
```bash
$ vault token create -policy='aws-policy'
Key                  Value
---                  -----
token                hvs.CAESIKqkrvQkz76WvVkVMsZD5isT7aM3KugRuN3u82aHUeHkGh4KHGh2cy55eUU3bGpONksxN0xqU2xQUVdVd0w3Tzg
token_accessor       T7ron1EEOtVxLzSQluQtG0fK
token_duration       768h
token_renewable      true
token_policies       ["aws-policy" "default"]
identity_policies    []
policies             ["aws-policy" "default"]
```
Log into Vault using newly created token.
```bash
$ vault login
```
Write role.
```bash
$ curl -X PUT -H "X-Vault-Request: true" -H "X-Vault-Token: $(vault print token)" -d '{"credential_type":"iam_user","policy_document":"{\n\"Version\": \"2012-10-17\",\n\"Statement\": [\n{\n\"Effect\": \"Allow\",\n\"Action\": \"ec2:*\",\n\"Resource\": \"*\"\n}\n]\n}\n"}' http://127.0.0.1:8200/v1/aws/roles/my-role
```
Generate AWS credentials.
```bash
$ curl -H "X-Vault-Request: true" -H "X-Vault-Token: $(vault print token)" http://127.0.0.1:8200/v1/aws/creds/my-role
{"request_id":"1aff925c-8560-d794-7275-babff5b792e2","lease_id":"aws/creds/my-role/NBkTu5aE7slLV21Zh3ljrf7Z","renewable":true,"lease_duration":2764800,"data":{"access_key":"######","secret_key":"######","security_token":null},"wrap_info":null,"warnings":null,"auth":null}
```
Test using AWS CLI.
```bash
$ aws iam list-users{
    "Users": [
        snip
        {
            "Path": "/",
            "UserName": "vault-token-my-role-1648235253-wr11bVrRyYwKAJ1L0GsH",
            "UserId": "AIDAUPSKXGRBVR4KYNMAU",
            "Arn": "arn:aws:iam::308320613443:user/vault-token-my-role-1648235253-wr11bVrRyYwKAJ1L0GsH",
            "CreateDate": "2022-03-25T19:07:34+00:00"
        }
    ]
}
```
