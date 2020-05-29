```
Create a nodegroup

Usage: eksctl create nodegroup [flags]

Aliases: nodegroup, ng

General flags:
      --cluster string          name of the EKS cluster to add the nodegroup to
      --tags stringToString     Used to tag the AWS resources. List of comma separated KV pairs "k1=v1,k2=v2" (default [])
  -r, --region string           AWS region
      --version string          Kubernetes version (valid options: 1.13, 1.14, 1.15, 1.16) [for nodegroups "auto" and "latest" can be used to automatically inherit version from the control plane or force latest] (default "auto")
  -f, --config-file string      load configuration from a file (or stdin if set to '-')
      --include strings         nodegroups to include (list of globs), e.g.: 'ng-team-?,prod-*'
      --exclude strings         nodegroups to exclude (list of globs), e.g.: 'ng-team-?,prod-*'
      --update-auth-configmap   Add nodegroup IAM role to aws-auth configmap (default true)
      --timeout duration        maximum waiting time for any long-running operation (default 25m0s)

New nodegroup flags:
  -n, --name string                    name of the new nodegroup (generated if unspecified, e.g. "ng-ea3bc9ad")
  -t, --node-type string               node instance type (default "m5.large")
  -N, --nodes int                      total number of nodes (for a static ASG) (default 2)
  -m, --nodes-min int                  minimum nodes in ASG (default 2)
  -M, --nodes-max int                  maximum nodes in ASG (default 2)
      --node-volume-size int           node volume size in GB
      --node-volume-type string        node volume type (valid options: gp2, io1, sc1, st1) (default "gp2")
      --max-pods-per-node int          maximum number of pods per node (set automatically if unspecified)
      --ssh-access                     control SSH access for nodes. Uses ~/.ssh/id_rsa.pub as default key path if enabled
      --ssh-public-key string          SSH public key to use for nodes (import from local path, or use existing EC2 key pair)
      --node-ami string                Advanced use cases only. If 'ssm' is supplied (default) then eksctl will use SSM Parameter; if 'auto' is supplied then eksctl will automatically set the AMI based on version/region/instance type; if static is supplied (deprecated), then static AMIs will be used; if any other value is supplied it will override the AMI to use for the nodes. Use with extreme care.
      --node-ami-family string         Advanced use cases only. If 'AmazonLinux2' is supplied (default), then eksctl will use the official AWS EKS AMIs (Amazon Linux 2); if 'Ubuntu1804' is supplied, then eksctl will use the official Canonical EKS AMIs (Ubuntu 18.04). (default "AmazonLinux2")
  -P, --node-private-networking        whether to make nodegroup networking private
      --node-security-groups strings   Attach additional security groups to nodes, so that it can be used to allow extra ingress/egress access from/to pods
      --node-labels stringToString     Extra labels to add when registering the nodes in the nodegroup. List of comma separated KV pairs "k1=v1,k2=v2" (default [])
      --node-zones strings             (inherited from the cluster if unspecified)
      --managed                        Create EKS-managed nodegroup

Addons flags:
      --asg-access              enable IAM policy for cluster-autoscaler
      --external-dns-access     enable IAM policy for external-dns
      --full-ecr-access         enable full access to ECR
      --appmesh-access          enable full access to AppMesh
      --alb-ingress-access      enable full access for alb-ingress-controller
      --install-neuron-plugin   Install Neuron plugin for Inferentia nodes (default true)

AWS client flags:
  -p, --profile string        AWS credentials profile to use (overrides the AWS_PROFILE environment variable)
      --cfn-role-arn string   IAM role used by CloudFormation to call AWS API on your behalf

Common flags:
  -C, --color string   toggle colorized logs (valid options: true, false, fabulous) (default "true")
  -h, --help           help for this command
  -v, --verbose int    set log level, use 0 to silence, 4 for debugging and 5 for debugging with AWS debug logging (default 3)

Use 'eksctl create nodegroup [command] --help' for more information about a command.
```

