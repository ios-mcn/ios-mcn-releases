
# **IOS MCN v0.1.0 Agartala Release Developer Guide: SD-Core v0.1**

# Introduction

This guide mentions the options to work with IOS-MCN github repository for the software development for SD-Core.

# Purpose and Audience

This document is intended only for the core developers for the 5G platform.

# How to build from source code

Download file: iosmcn.agartala.v0.1.0.core.source.tar.gz

_tar -xvzf iosmcn.agartala.v0.1.0.core.source.tar.gz_

Untar the network functions -  *\<nf>*-0.0.*\<nf-version>*.iosmcn.core.*\<nf>*.tar.gz

```sh
tar -xvzf amf-0.0.10.iosmcn.core.amf.tar.gz

```

```sh
tar -xvzf smf-0.0.6.iosmcn.core.smf.tar.gz

```
...

*\<nf>* can be amf, smf, ausf, nrf, pcf, udm, udr, simapp, nssf, upf, metricfunc, bess.

Step 3: Create a new repository in GitHub.

Step 4: Create a new branch named iosmcnmaster and set is as default branch.

Step 5: Push the extracted code to the newly created repository. Follow the GitHub documentation for detailed steps.

Step 6: A GitHub workflow is already set up for building and testing. Modify the workflow to build and push the image to the container registry.

Step 7: Open the workflow file .github\workflows\iosmcn-master.yml and make the following modifications from Step 8 - Step 10.

Step 8: Remove below mentioned line in each workflow job to remove ownership check:

if: github.repository_owner == 'ios-mcn-core'

Step 9: Update the container registry values in the variables - REGISTRY, DOCKER_REGISTRY (docker.io, ghcr.io).

Step 10: Update the container registry repository username value in the variable - DOCKER_REPOSITORY.

Step 11: Create Secrets for container registry repository username and password with key named - GHCRUSER & GHCRPASS. Refer the GitHub documentation.

Step 12: Go to Actions tab in the GitHub repository. Select the IOSMCN Master workflow.

Step 13: Click on Run workflow.

Step 14: Once the workflow completes successfully, the built image will be pushed to the configured container registry.

## Deployment

- Open 5g-control-plane folder in sdcore and edit values.yaml file

- Change image names in tags to ios-mcn

 - Change 5g-control-plane dependency repository location to above extracted file location

- Run the following commands

	_make reset-5g-test_

	_make 5g-test_

- Check the pod status using the command

	_kubectl get pods -n ios-mcn_

![Figure 13: pods status](./images/devel/fig13-pod-stats.png)

## Related Artifacts & links

| **Document Name** | **Purpose** | **Link** |
|--|--|--|
| User Guide | Quick user guide | [Click Here](./User%20Guide.md)  |
| API Guide | API guide | [Click here](./API%20Guide.md)|
| Troubleshooting Guide  | Troubleshooting guide for SD-Core | [Click here](./Troubleshooting%20Guide.md)|
| Installation Guide | Installation of SD-Core | [Click here](./Installation%20Guide.md) |
| Developer Guide | Guide for SD-Core developers | [Click Here](./Developer%20Guide.md)|