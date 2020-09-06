# Install AWS, kubectl & eksctl CLI's

## Step-00: Introduction
- Install AWS CLI
- Install kubectl CLI
- Install eksctl CLI

## Step-01: Install AWS CLI
# Prerequisites

* Python3 or Python2.7.9+
* Python Pip3 / Pip

# Install awscli
## linux based system

```bash 
pip install --user awscli
export PATH=$PATH:/home/$(whoami)/.local/bin
```

_--user_ is used to install the awscli under your home directory, not to interfere with any existing libraries/installations

create file _~/.aws/credentials_

```bash
[default]
aws_access_key_id=###
aws_secret_access_key=###
region=us-east-1
output=json
```

## Windows, using Anaconda
after Anaconda python distribution, goto "Start" => "Anaconda" => "open anaconda shell"

```
# potentially upgrade pip first
python -m pip install --upgrade pip
pip install --user awscli

set path=%path%;c:\users\<<username>>\appdata\roaming\python\python37\scripts
```

## TEST

```bash
aws --version
```

### Step-01-03: Configure AWS Command Line using Security Credentials
- Go to AWS Management Console --> Services --> IAM
- Select the IAM User: kalyan 
- **Important Note:** Use only IAM user to generate **Security Credentials**. Never ever use Root User. (Highly not recommended)
- Click on **Security credentials** tab
- Click on **Create access key**
- Copy Access ID and Secret access key
- Go to command line and provide the required details
```
aws configure
AWS Access Key ID [None]: ABCDEFGHIAZBERTUCNGG  (Replace your creds when prompted)
AWS Secret Access Key [None]: uMe7fumK1IdDB094q2sGFhM5Bqt3HQRw3IHZzBDTm  (Replace your creds when prompted)
Default region name [None]: us-east-1
Default output format [None]: json
```
- Test if AWS CLI is working after configuring the above
```
aws ec2 describe-vpcs
```

## Step-02: Install kubectl CLI
- **IMPORTANT NOTE:** Kubectl binaries for EKS please prefer to use from Amazon (**Amazon EKS-vended kubectl binary**)
- This will help us to get the exact Kubectl client version based on our EKS Cluster version. You can use the below documentation link to download the binary.
- Reference: https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

### Step-02-01: MAC - Install and configure kubectl
- Kubectl version we are using here is 1.16.8 (It may vary based on Cluster version you are planning use in AWS EKS)

```
# Download the Package
mkdir kubectlbinary
cd kubectlbinary
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/darwin/amd64/kubectl

# Provide execute permissions
chmod +x ./kubectl

# Set the Path by copying to user Home Directory
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile

# Verify the kubectl version
kubectl version --short --client
Output: Client Version: v1.16.8-eks-e16311
```


### Step-02-02: Windows 10 - Install and configure kubectl
- Install kubectl on Windows 10 
```
mkdir kubectlbinary
cd kubectlbinary
curl -o kubectl.exe https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/windows/amd64/kubectl.exe
```
- Update the system **Path** environment variable 
```
C:\Users\KALYAN\Documents\kubectlbinary
```
- Verify the kubectl client version
```
kubectl version --short --client
kubectl version --client
```

## Step-03: Install eksctl CLI
## Installation
for non-Linux OS you can find a binary download here:

https://github.com/weaveworks/eksctl/releases

on Linux, you can just execute:

```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp  

sudo mv /tmp/eksctl /usr/local/bin
```

This utility will use the same _credentials_ file as we explored for the AWS cli, located under '~/.aws/credentials'

## Test
```eksctl version```
