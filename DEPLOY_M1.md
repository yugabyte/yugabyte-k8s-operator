### Getting YugabyteDB-K8s-Operator running on M1 Mac for local development.

Getting YugabyteDB-K8s-Operator running on M1 Mac for local development.
This guide will help us set up and run Colima with specific configurations on a Mac M1/M2 (Apple Silicon) and then deploy Kubernetes on it. Once Kubernetes cluster is up and running we will follow the install instructions for yugabyte-k8s-operator to get it to run and create yugabyte-db universes

#### Prerequisites
- Mac M1 with macOS
- Homebrew installed
- Colima installed
- kubectl installed

### Step 1: Install Homebrew
If no homebrew is installed lets install homebrew, open the terminal and run:
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Colima
Install Colima using Homebrew:
```sh
brew install colima
```

### Step 3: Install kubectl
Install kubectl using Homebrew:
```sh
brew install kubectl
```

### Step 4: Start Colima with Specified Arguments
Open the terminal and start Colima with the specified arguments:
```sh
colima start -p amd64 --arch x86_64 --cpu 8 --memory 12 --cpu-type max,+avx,+avx2 --disk 20 --kubernetes
```
This command configures Colima to use an x86_64 architecture, allocates 8 CPUs, 12GB of memory, enables AVX and AVX2 CPU features, and sets a disk size of 20GB.

### Step 5: Install Docker (if not already installed)
Colima uses Docker, so we need Docker installed on our system:
```sh
brew install docker
```

### Step 6: Set Up Docker Context <optional>
Configure Docker to use the Colima context:
```sh
docker context use colima
```

### Step 7: Verify Kubernetes Installation
Ensure that Kubernetes is running:
```sh
kubectl version --short
```
We should see the Client and Server versions of Kubernetes.

### Step 8: Test Kubernetes Deployment
Deploy a test application to ensure Kubernetes is functioning correctly:
```sh
kubectl create deployment hello-world --image=k8s.gcr.io/echoserver:1.4
kubectl expose deployment hello-world --type=LoadBalancer --port=8080
```
Check the status of the deployment:
```sh
kubectl get services
```
Access the application using the IP address and port listed under the services.

### Step 9: Colima is up
We have successfully set up and run Colima with Kubernetes on our Mac  using the specified configurations. 
We can now manage and deploy our applications within this environment.
  
### Step 10: Edit Kubernetes Nodes metadata
Once colima is deployed, next thing to do is add zone and region lables to the kuberntes nodes.

```sh
kubectl edit node
```
Add these labels
```
  failure-domain.beta.kubernetes.io/region: region-1
  failure-domain.beta.kubernetes.io/zone: region-1-zone-1
```

### Step 11: Deploy Kubernetes Operator
Once these are added, we can follow the yugabyte-k8s-operator installation instructions mentioned at 
https://github.com/yugabyte/yugabyte-k8s-operator/blob/main/README.md#installing-the-operator-with-rbac-permissions


### Note Since we are deploying x86_64 VMs on arm64, some things are slower. 
This may cause some startup jobs to timeout, however these jobs are retried by the helm post install hook.  
  
### Step 12: Deploy Kubernetes Custom Resources
At this point operator should be up, at this point we can start creating custom resources based on this or a similar CR
```
kubectl apply -f ./miniKubeSampleCr.yaml -n operator-test
```


anijhawan@Amans-MacBook-Pro chart % cat  ./miniKubeSampleCr.yaml
```
apiVersion: operator.yugabyte.io/v1alpha1
kind: YBUniverse
metadata:
  name: oss-demo-test-20
spec:
  numNodes:    1  
  replicationFactor:  1 
  enableYSQL: true
  enableNodeToNodeEncrypt: true
  enableClientToNodeEncrypt: true
  enableLoadBalancer: false 
  ybSoftwareVersion: "2.20.1.3-b3"
  enableYSQLAuth: false 
  enableYCQL: true
  enableYCQLAuth: false 
  gFlags:
    tserverGFlags: {}
    masterGFlags: {}
  deviceInfo:
    volumeSize: 10 
    numVolumes: 1
    storageClass: "local-path"
  kubernetesOverrides:
    resource:
      master:
        requests:
          cpu: 1 
          memory: 1Gi 
        limits:
          cpu: 1
          memory: 1Gi
      tserver:
        requests:
          cpu:  1 
          memory: 1Gi 
        limits:
          cpu: 1 
          memory: 1Gi
```
    
