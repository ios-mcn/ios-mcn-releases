
# **IOS MCN v0.1.0 Agartala Release: CORE Developer Guide**

# Introduction

This guide mentions the options to work with IOS-MCN github repository for the software development for IOSMCN-Core.

# Purpose and Audience

This document is intended only for the core developers for the 5G platform.

# How to build from source code

Step 1: Create a directory for IOSMCN-Core-Source in home directory.
```
cd
mkdir IOSMCN-Core-Source
cd IOSMCN-Core-Source
```

Step 2: Download the source code tar file.

```sh
wget https://github.com/ios-mcn/ios-mcn-releases/raw/refs/heads/main/Agartala/v0.1.0/CORE/source-code/iosmcn.agartala.v0.1.0.core.source.tar.gz
```

Step 3: Untar the iosmcn.agartala.v0.1.0.core.source.tar.gz.

```sh
tar -xvzf iosmcn.agartala.v0.1.0.core.source.tar.gz
cd iosmcn.agartala.v0.1.0.core.source
```

Step 4: Untar the network functions -  *\<nf>*-0.0.*\<nf-version>*.iosmcn.core.*\<nf>*.tar.gz.

```sh
tar -xvzf amf-0.0.10.iosmcn.core.amf.tar.gz
cd amf-0.0.10.iosmcn.core.amf
```
or

```sh
tar -xvzf smf-0.0.6.iosmcn.core.smf.tar.gz
cd smf-0.0.6.iosmcn.core.smf
```
...

*\<nf>* can be amf, smf, ausf, nrf, pcf, udm, udr, simapp, nssf, upf, metricfunc, bess.

Step 5: Create a new repository in [GitHub](https://github.com/new). Name the repository as any one of the network functions - amf, smf, ausf, nrf, pcf, udm, udr, simapp, nssf, upf, metricfunc, bess.

Step 6: Create a new branch named _iosmcnmaster_ and set is as default branch.

Step 7: Push the extracted network function code to the newly created repository. Follow the [GitHub documentation](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github) for detailed steps. Make sure the code is pushed to the _iosmcnmaster_ branch.

Step 8: A GitHub workflow is already set up for building the release image. Modify the workflow to build and push the image to the container registry.

Step 9: For building amf, smf, ausf, nrf, pcf, udm, udr, simapp, nssf, metricfunc - open the workflow file **\.github\workflows\iosmcn-release-push.yml** and make the following modifications from Step 12  - Step 13.

Step 10: For building bess - open the workflow file **\.github\workflows\iosmcn-master.yml** and make the following modifications from Step 12 - Step 13. Before that, apply the modifications from Step 10.1 to Step 10.2:

- Step 10.1: Remove the following line in each jobs of the _iosmcn-master.yml_ workflow:
  > if: github.repository_owner == 'ios-mcn-core'

- Step 10.2: Open the python file _env\rebuild_images_iosmcn.py_ and modify the container registry path to the one created by the user (line number 43).
  > TARGET_REPO = '\<registry.io>/\<registry-username>/bess_build'
  
  Eg.,
  > TARGET_REPO = 'docker.io/iosmcncorereg/bess_build'

Step 11: For building upf - make sure that bess is already built. Open the workflow file **\.github\workflows\iosmcn-release-push.yml** and make the following modifications from Step 12 - Step 13. Before that, apply the modifications from Step 11.1 to Step 11.3:
 - Step 11.1: Open the _Makefile_IOSMCN_ file and modify the GitHub UPF repository path to the user created one (line number 58).

    >--label org.opencontainers.image.source="https://github.com\/\<github-username>/upf" \

	Eg.,
	>--label org.opencontainers.image.source="https://github.com/iosmcncoregit/upf" \
 - Step 11.2: Open the _Dockerfile_IOSMCN_ file and modify the Bess container registry repository path to the user created one (line number 6).
    >FROM \<registry.io>/\<registry-username>/bess_build:latest AS bess-build

    Eg.,
	>FROM docker.io/iosmcncorereg/bess_build:latest AS bess-build

 - Step 11.3: Open the _Dockerfile_IOSMCN_ file and modify the Bess GitHub repository path to the user created one (line number 26).
    >FROM RUN git clone https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com\/\<github-username>/bess.git . && \

    Eg.,
	>RUN git clone https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/iosmcncoregit/bess.git . && \

Step 12: Update the container registry values in the variables - *REGISTRY*, *DOCKER_REGISTRY* (docker.io, ghcr.io).

Step 13: Update the container registry repository username value in the variable - *DOCKER_REPOSITORY*.

Step 14: Create Secrets for container registry repository username and password with key named - GHCRUSER & GHCRPASS. Refer the [GitHub documentation](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions).

Step 15: Go to **Actions tab** in the GitHub repository. Select the IOSMCN Release Workflow or IOSMCN Master Workflow(based on the network function).

Step 16: Click on **Run workflow** to manually trigger the workflow.

Step 17: Once the workflow completes successfully, the built image will be pushed to the configured container registry.

**Note**: If you want to tag the bess image as the release image, use the **\.github\workflows\iosmcn-release-push.yml** worflow. Modify the _STABLE_TAG_ variable with the newly built image tag(non-release) of bess. The bess release image has no dependency with the upf build process.

## Deployment

- If the core is not installed, follow the [installation guide](./Installation%20Guide.md).

- After the core installation, open _IOSMCN-CoreDpm_ directory and edit iosmcn-5g-values.yaml file located in the below mentioned location:

>IOSMCN-CoreDpm/deps/5gc/roles/core/templates/iosmcn-5g-values.yaml

- Update the image name to the newly built image under the _tags_ section of the yaml file:

```
5g-control-plane:
  enable5G: true
  images:
	repository: ""    # defaults to Docker Hub
	tags:
	  amf: docker.io/iosmcncorereg/5gc-amf:release-0.0.10
	  smf: docker.io/iosmcncorereg/5gc-smf:release-0.0.6
	  pcf: docker.io/iosmcncorereg/5gc-pcf:release-0.0.4
	  nrf: docker.io/iosmcncorereg/5gc-nrf:release-0.0.5
	  ausf: docker.io/iosmcncorereg/5gc-ausf:release-0.0.4
	  nssf: docker.io/iosmcncorereg/5gc-nssf:release-0.0.4
	  udm: docker.io/iosmcncorereg/5gc-udm:release-0.0.4
	  udr: docker.io/iosmcncorereg/5gc-udr:release-0.0.4
	  webui: docker.io/iosmcncorereg/5gc-webui:release-0.0.4
	  metricfunc: docker.io/iosmcncorereg/metricfunc:release-0.0.4

...

omec-sub-provision:
  enable: true
  images:
    repository: ""    # defaults to Docker Hub
    tags:
      simapp: docker.io/iosmcncorereg/simapp:release-0.0.3

...

omec-user-plane:
  enable: true
  nodeSelectors:
    enabled: true
  resources:
    enabled: false
  images:
    repository: ""    # defaults to Docker Hub
    # following two lines pull busybox from Docker Hub instead of Aether Registry
    tags:
      tools: omecproject/busybox:stable
    # uncomment following section to add update bess image tag
    tags:
      bess: docker.io/iosmcncorereg/upf-epc-bess:release-ivybridge-0.0.4
      pfcpiface: docker.io/iosmcncorereg/upf-epc-pfcpiface:release-ivybridge-0.0.4
```

- If the core is installed and you want to update the pod with the new images and reset the core, run the following command:
	_cd ~/IOSMCN-Core/iosmcn.agartala.v0.1.0.core.images/IOSMCN-CoreDpm_
	_make aether-resetcore_

- Check the pod status using the command:
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