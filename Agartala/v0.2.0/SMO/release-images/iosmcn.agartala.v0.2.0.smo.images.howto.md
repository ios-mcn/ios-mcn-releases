## This document explains how to use the pre-built images for deployment 

OAM deployment is about runing multiple containers. The source-code of oam has 2 simple steps to run OAM containers.

In the OAM source code, you will find .env file. Currently, the .env file already refers to the pre-built images as summarized in the below table.

Step 1 : Unzip the SMO/OAM source code

Download the [SMO Source](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.2.0/SMO/source-code/iosmcn.agartala.v0.2.0.smo.source.tar.gz)

```sh
tar -xvzf iosmcn.agartala.v0.2.0.smo.source.tar.gz
cd iosmcn.agartala.v0.2.0.smo.source/
tar -xzvf oam-0.2.0.iosmcn.smo.oam.tar.gz
cd oam-0.2.0.iosmcn.smo.oam
```

Step 2: Open the .env and ensure the images listed below are correctly referenced.

```sh
cd oam-0.2.0.iosmcn.smo.oam
vi .env
```

|Image|Image Download URL |Docker command|
|--|--|--|
|pm-file-converter|https://github.com/orgs/ios-mcn/packages/container/package/pm-file-converter|docker pull ghcr.io/ios-mcn/pm-file-converter:1.2.1|
|datafile-collector|https://github.com/orgs/ios-mcn/packages/container/package/datafile-collector|docker pull ghcr.io/ios-mcn/datafile-collector:0.0.2|
|nonrtric-controlpanel|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-controlpanel|docker pull ghcr.io/ios-mcn/nonrtric-controlpanel:2.5.1|
|nonrtric-plt-auth-token-fetch|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-auth-token-fetch|docker pull ghcr.io/ios-mcn/nonrtric-plt-auth-token-fetch:1.1.2|
|nonrtric-gateway|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-gateway|docker pull ghcr.io/ios-mcn/nonrtric-gateway:1.2.1|
|nonrtric-plt-dmaapadapter|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-dmaapadapter|docker pull ghcr.io/ios-mcn/nonrtric-plt-dmaapadapter:1.4.1|
|nonrtric-plt-a1policymanagementservice|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-a1policymanagementservice|docker pull ghcr.io/ios-mcn/nonrtric-plt-a1policymanagementservice:2.8.2|
|nonrtric-plt-pmproducer|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-pmproducer|docker pull ghcr.io/ios-mcn/nonrtric-plt-pmproducer:1.0.2|
|nonrtric-plt-informationcoordinatorservice|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-informationcoordinatorservice|docker pull ghcr.io/ios-mcn/nonrtric-plt-informationcoordinatorservice:1.5.1|
|ves-collector|https://github.com/orgs/ios-mcn/packages/container/package/ves-collector|docker pull ghcr.io/ios-mcn/ves-collector:1.12.4|
|nonrtric-plt-pmlog|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-pmlog|docker pull ghcr.io/ios-mcn/nonrtric-plt-pmlog:1.0.1|

### Building custom images and using it.

Please refer to the oam developer guide that you will find in the SMO documentation.
