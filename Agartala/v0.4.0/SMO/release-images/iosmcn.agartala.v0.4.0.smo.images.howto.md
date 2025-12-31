## This document explains how to use the pre-built images for deployment 

OAM deployment is about runing multiple containers. The source-code of oam has 2 simple steps to run OAM containers.

In the OAM source code, you will find .env file. Currently, the .env file already refers to the pre-built images as summarized in the below table.

Step 1 : Unzip the SMO/OAM source code

Download the [SMO Source](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.2.0/SMO/source-code/ios-mcn-ran-0.4.0.iosmcn.ran.tar.gz)

```sh
tar -xvzf iosmcn.agartala.v0.4.0.smo.source.tar.gz
cd iosmcn.agartala.v.4.0.smo.source/
tar -xzvf oam-0.4.0.iosmcn.smo.oam.tar.gz
cd oam-0.4.0.iosmcn.smo.oam
```

Step 2: Open the .env and ensure the images listed below are correctly referenced.

```sh
cd oam-0.4.0.iosmcn.smo.oam
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
|onap/sdnc-image|https://github.com/orgs/ios-mcn/packages/container/package/onap/sdnc-image|docker pull ghcr.io/ios-mcn/onap/sdnc-image:3.0.3-snapshot-latest|
|onap/sdnc-web-image|https://github.com/orgs/ios-mcn/packages/container/package/onap/sdnc-web-image|docker pull ghcr.io/ios-mcn/onap/sdnc-web-image:3.0.3-snapshot-latest|
|tabx|https://github.com/orgs/ios-mcn/packages/container/package/tabx|docker pull ghcr.io/ios-mcn/tabx:1.0|
|nonrtric-plt-rappcatalogue-enhanced|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-rappcatalogue-enhanced|docker pull ghcr.io/ios-mcn/nonrtric-plt-rappcatalogue-enhanced:1.2.0|
|pm-rapp|https://github.com/orgs/ios-mcn/packages/container/package/pm-rapp|docker pull ghcr.io/ios-mcn/pm-rapp:1.0|
|nonrtric-plt-dmaapmediatorproducer|https://github.com/orgs/ios-mcn/packages/container/package/nonrtric-plt-dmaapmediatorproducer|docker pull ghcr.io/ios-mcn/nonrtric-plt-dmaapmediatorproducer:1.2.0|
|ric-plt-e2mgr|https://github.com/orgs/ios-mcn/packages/container/package/ric-plt-e2mgr|docker pull ghcr.io/ios-mcn/ric-plt-e2mgr:6.0.4|
|ric-plt-a1|https://github.com/orgs/ios-mcn/packages/container/package/ric-plt-a1|docker pull ghcr.io/ios-mcn/ric-plt-a1:3.2.2|
|ric-plt-dbaas|https://github.com/orgs/ios-mcn/packages/container/package/ric-plt-dbaas|docker pull ghcr.io/ios-mcn/ric-plt-dbaas:0.6.4|
|ric-plt-e2|https://github.com/orgs/ios-mcn/packages/container/package/ric-plt-e2|docker pull ghcr.io/ios-mcn/ric-plt-e2:6.0.4|
|onap/ccsdk-odlsli-alpine-image|https://github.com/orgs/ios-mcn/packages/container/package/onap/ccsdk-odlsli-alpine-image|docker pull ghcr.io/ios-mcn/onap/ccsdk-odlsli-alpine-image:1.7.1-snapshot-latest|
|rtmgr-sim|https://github.com/orgs/ios-mcn/packages/container/package/rtmgr-sim|docker pull ghcr.io/ios-mcn/rtmgr-sim:i-release|
|ric-plt-appmgr|https://github.com/orgs/ios-mcn/packages/container/package/ric-plt-appmgr|docker pull ghcr.io/ios-mcn/ric-plt-appmgr:0.5.7|
|sa-rapp|https://github.com/orgs/ios-mcn/packages/container/package/sa-rapp|docker pull ghcr.io/ios-mcn/sa-rapp:1.0|
|oru-rapp|https://github.com/orgs/ios-mcn/packages/container/package/oru-rapp|docker pull ghcr.io/ios-mcn/oru-rapp:1.0|
|ric-plt-submgr|https://github.com/orgs/ios-mcn/packages/container/package/ric-plt-submgr|docker pull ghcr.io/ios-mcn/ric-plt-submgr:0.10.1|

### Building custom images and using it.

Please refer to the oam developer guide that you will find in the SMO documentation.
