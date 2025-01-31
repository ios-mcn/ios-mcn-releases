## This document explains how to build the images from source-code.

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

Step 4: Create a new branch named **iosmcnmaster** and set is as [default branch](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/changing-the-default-branch).

Step 5: Push the extracted code to the newly created repository. Follow the GitHub [documentation](https://docs.github.com/en/get-started/start-your-journey/uploading-a-project-to-github) for detailed steps.

Step 6: A GitHub workflow is already set up for building and testing. Modify the workflow to build and push the image to the container registry.

Step 7: Open the workflow file **\.github\workflows\iosmcn-master.yml** and make the following modifications from Step 8 - Step 10.

Step 8: Remove below mentioned line in each workflow job to remove ownership check:
> if: github.repository_owner == 'ios-mcn-core'

Step 9: Update the container registry values in the variables - *REGISTRY*, *DOCKER_REGISTRY* (docker.io, ghcr.io).

Step 10: Update the container registry repository username value in the variable - *DOCKER_REPOSITORY*.

Step 11: Create Secrets for container registry repository username and password with key named - GHCRUSER & GHCRPASS. Refer the [GitHub documentation](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions).

Step 12: Go to **Actions tab** in the GitHub repository. Select the IOSMCN Master workflow.

Step 13: Click on **Run workflow**.

Step 14: Once the workflow completes successfully, the built image will be pushed to the configured container registry.