
# **IOS MCN v0.1.0 Agartala Release Developer Guide: IOSMCN-Core v0.1**

# Introduction

This guide mentions the options to work with IOS-MCN github repository for the software development for IOSMCN-Core.

# Purpose and Audience

This document is intended only for the core developers for the 5G platform.

# How to build from source code

Step 1: Untar the iosmcn.agartala.v0.1.0.core.source.tar.gz

```sh
tar -xvzf iosmcn.agartala.v0.1.0.core.source.tar.gz

```

Step 2: Untar the network functions -  *\<nf>*-0.0.*\<nf-version>*.iosmcn.core.*\<nf>*.tar.gz

```sh
tar -xvzf amf-0.0.10.iosmcn.core.amf.tar.gz

```

```sh
tar -xvzf smf-0.0.6.iosmcn.core.smf.tar.gz

```
...

*\<nf>* can be amf, smf, ausf, nrf, pcf, udm, udr, simapp, nssf, upf, metricfunc, bess.

Step 3: Create a new repository in [GitHub](https://github.com/new).

Step 4: Create a new branch named _iosmcnmaster_ and set is as default branch.

Step 5: Push the extracted code to the newly created repository. Follow the [GitHub documentation](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github) for detailed steps. Make sure the code is pushed to the _iosmcnmaster_ branch.

Step 6: A GitHub workflow is already set up for building the release image. Modify the workflow to build and push the image to the container registry.

Step 7: Open the workflow file **\.github\workflows\iosmcn-release-push.yml** and make the following modifications from Step 8 - Step 10.

Step 8: Update the container registry values in the variables - *REGISTRY*, *DOCKER_REGISTRY* (docker.io, ghcr.io).

Step 9: Update the container registry repository username value in the variable - *DOCKER_REPOSITORY*.

Step 10: Create Secrets for container registry repository username and password with key named - GHCRUSER & GHCRPASS. Refer the [GitHub documentation](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions).

Step 11: Go to **Actions tab** in the GitHub repository. Select the IOSMCN Release Workflow.

Step 12: Click on **Run workflow** to manually trigger the workflow.

Step 13: Once the workflow completes successfully, the built image will be pushed to the configured container registry.

## Deployment

- Open IOSMCN-CoreDpm and edit iosmcn-5g-values.yaml file located in the below mentioned location.

>IOSMCN-CoreDpm/deps/5gc/roles/core/templates/iosmcn-5g-values.yaml

- Update the image name to the newly built image under the tag section of the yaml file.

```
5g-control-plane:
  enable5G: true
  images:
	repository: ""    # defaults to Docker Hub
	tags:
	  amf: docker.io/iosmcnbuildtest/5gc-amf:release-0.0.10

```

- Run the following command to reset the core.

	_make aether-resetcore_

- Check the pod status using the command.

	_kubectl get pods -n iosmcn_

![Figure 13: pods status](../../CORE/documentation/images/devel/fig1-pod-stats.png)

## Related Artifacts & links

| **Document Name** | **Purpose** | **Link** |
|--|--|--|
| User Guide | Quick user guide | [Click Here](./User%20Guide.md)  |
| API Guide | API guide | [Click here](./API%20Guide.md)|
| Troubleshooting Guide  | Troubleshooting guide for IOSMCN-Core | [Click here](./Troubleshooting%20Guide.md)|
| Installation Guide | Installation of IOSMCN-Core | [Click here](./Installation%20Guide.md) |
| Developer Guide | Guide for IOSMCN-Core developers | [Click Here](./Developer%20Guide.md)|