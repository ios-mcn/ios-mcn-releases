## This document explains how to use the pre-built images for deployment 

OAM deployment is about runing multiple containers. The source-code of oam has 2 simple steps to run OAM containers.

In the OAM source code, you will find .env file. Currently, the .env file already refers to the pre-built images as summarized in the below table.

Step 1 : Unzip the SMO/OAM source code

Download the [SMO Source](https://github.com/ios-mcn/ios-mcn-releases/blob/main/Agartala/v0.4.0/SMO/source-code/iosmcn.agartala.v0.4.0.smo.source.tar)

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
|a1-simulator|https://github.com/orgs/ios-mcn-smo/packages/container/package/a1-simulator|docker pull ghcr.io/ios-mcn-smo/a1-simulator:2.8.1
| nonrtric-controlpanel | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-controlpanel | docker pull ghcr.io/ios-mcn-smo/nonrtric-controlpanel:2.6.0
| nonrtric-gateway | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-gateway |docker pull ghcr.io/ios-mcn-smo/nonrtric-gateway:1.2.2
| nonrtric-plt-a1policymanagementservice | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-a1policymanagementservice|docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-a1policymanagementservice:2.10.1
| nonrtric-plt-auth-token-fetch | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-auth-token-fetch | docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-auth-token-fetch:1.1.3
| nonrtric-plt-dmaapadapter | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-dmaapadapter | docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-dmaapadapter:1.5.0
| nonrtric-plt-informationcoordinatorservice | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-informationcoordinatorservice | docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-informationcoordinatorservice:1.7.0
|nonrtric-plt-participant-impl-dme| https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-participant-impl-dme | docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-participant-impl-dme:0.4.0
| nonrtric-plt-pmlog | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-pmlog |docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-pmlog:1.2.0
| nonrtric-plt-pmproducer | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-pmproducer |docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-pmproducer:1.2.0
|nonrtric-plt-ranpm-datafilecollector| https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-ranpm-datafilecollector |docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-ranpm-datafilecollector:1.2.1
| pm-file-converter | https://github.com/orgs/ios-mcn-smo/packages/container/package/pm-file-converter |docker pull ghcr.io/ios-mcn-smo/pm-file-converter:1.2.2
| nonrtric-plt-rappmanager | https://github.com/orgs/ios-mcn-smo/packages/container/package/nonrtric-plt-rappmanager | docker pull ghcr.io/ios-mcn-smo/nonrtric-plt-rappmanager:0.4.0
|servicemanager| https://github.com/orgs/ios-mcn-smo/packages/container/package/servicemanager |docker pull ghcr.io/ios-mcn-smo/servicemanager:0.2.2
| smo-ncmp-to-teiv-adapter|https://github.com/orgs/ios-mcn-smo/packages/container/package/smo-ncmp-to-teiv-adapter |docker pull ghcr.io/ios-mcn-smo/smo-ncmp-to-teiv-adapter:0.0.1
|smo-teiv-exposure|https://github.com/orgs/ios-mcn-smo/packages/container/package/smo-teiv-exposure |docker pull ghcr.io/ios-mcn-smo/smo-teiv-exposure:0.2.0
|smo-teiv-ingestion|https://github.com/orgs/ios-mcn-smo/packages/container/package/smo-teiv-ingestion |docker pull ghcr.io/ios-mcn-smo/smo-teiv-ingestion:0.2.0
|capifcore| https://github.com/orgs/ios-mcn-smo/packages/container/package/capifcore |docker pull ghcr.io/ios-mcn-smo/capifcore:1.4.0
| cps-and-ncmp| https://github.com/orgs/ios-mcn-smo/packages/container/package/cps-and-ncmp |docker pull ghcr.io/ios-mcn-smo/cps-and-ncmp:3.6.5
| ves-collector | https://github.com/orgs/ios-mcn-smo/packages/container/package/ves-collector |docker pull ghcr.io/ios-mcn-smo/ves-collector:1.12.5
|policy-apex-pdp| https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-apex-pdp | docker pull ghcr.io/ios-mcn-smo/policy-apex-pdp:4.2.0
|policy-api| https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-api | docker pull ghcr.io/ios-mcn-smo/policy-api:4.2.0
|policy-clamp-ac-a1pms-ppnt| https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-clamp-ac-a1pms-ppnt |docker pull ghcr.io/ios-mcn-smo/policy-clamp-ac-a1pms-ppnt:8.2.0
|policy-clamp-ac-http-ppnt | https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-clamp-ac-http-ppnt |docker pull ghcr.io/ios-mcn-smo/policy-clamp-ac-http-ppnt:8.2.0
|policy-clamp-ac-k8s-ppnt | https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-clamp-ac-k8s-ppnt |docker pull ghcr.io/ios-mcn-smo/policy-clamp-ac-k8s-ppnt:8.2.0
|policy-clamp-ac-kserve-ppnt| https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-clamp-ac-kserve-ppnt |docker pull ghcr.io/ios-mcn-smo/policy-clamp-ac-kserve-ppnt:8.2.0
| policy-clamp-ac-pf-ppnt| https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-clamp-ac-pf-ppnt |docker pull ghcr.io/ios-mcn-smo/policy-clamp-ac-pf-ppnt:8.2.0
| policy-clamp-runtime-acm| https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-clamp-runtime-acm |docker pull ghcr.io/ios-mcn-smo/policy-clamp-runtime-acm:8.2.0
|policy-db-migrator| https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-db-migrator | docker pull ghcr.io/ios-mcn-smo/policy-db-migrator:4.2.0
|policy-pap | https://github.com/orgs/ios-mcn-smo/packages/container/package/policy-pap | docker pull ghcr.io/ios-mcn-smo/policy-pap:4.2.0
| sdnc-ansible-server-image| https://github.com/orgs/ios-mcn-smo/packages/container/package/sdnc-ansible-server-image |docker pull ghcr.io/ios-mcn-smo/sdnc-ansible-server-image:3.1.1
|sdnc-image | https://github.com/orgs/ios-mcn-smo/packages/container/package/sdnc-image | docker pull ghcr.io/ios-mcn-smo/sdnc-image:3.1.1
|sdnc-web-image| https://github.com/orgs/ios-mcn-smo/packages/container/package/sdnc-web-image | docker pull ghcr.io/ios-mcn-smo/sdnc-web-image:3.1.1
|it-dep-secret| https://github.com/orgs/ios-mcn-smo/packages/container/package/it-dep-secret | docker pull ghcr.io/ios-mcn-smo/it-dep-secret:0.0.2
|ric-app-qp| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-app-qp | docker pull ghcr.io/ios-mcn-smo/ric-app-qp:0.0.5
|ric-app-rc| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-app-rc | docker pull ghcr.io/ios-mcn-smo/ric-app-rc:1.0.1
| ric-app-ts| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-app-ts | docker pull ghcr.io/ios-mcn-smo/ric-app-ts:1.2.5
| ric-plt-o1| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-o1 | docker pull ghcr.io/ios-mcn-smo/ric-plt-o1:0.6.3
| ric-plt-alarmmanager| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-alarmmanager | docker pull ghcr.io/ios-mcn-smo/ric-plt-alarmmanager:0.5.16
|ric-plt-appmgr| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-appmgr |docker pull ghcr.io/ios-mcn-smo/ric-plt-appmgr:0.5.8
| ric-plt-dbaas|https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-dbaas |docker pull ghcr.io/ios-mcn-smo/ric-plt-dbaas:0.6.5
| ric-plt-e2| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-e2 | docker pull ghcr.io/ios-mcn-smo/ric-plt-e2:6.0.6
| ric-plt-e2mgr| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-e2mgr |docker pull ghcr.io/ios-mcn-smo/ric-plt-e2mgr:6.0.6
| ric-plt-a1| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-a1 |docker pull ghcr.io/ios-mcn-smo/ric-plt-a1:3.2.3
|ric-plt-rtmgr| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-rtmgr |docker pull ghcr.io/ios-mcn-smo/ric-plt-rtmgr:0.9.6
 | ric-plt-submgr|https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-submgr| |docker pull ghcr.io/ios-mcn-smo/ric-plt-submgr:0.10.2
 | ric-plt-vespamgr| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-plt-vespamgr |docker pull ghcr.io/ios-mcn-smo/ric-plt-vespamgr:0.7.5
 | ric-app-bouncer| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-app-bouncer| docker pull ghcr.io/ios-mcn-smo/ric-app-bouncer:2.0.0
 |ric-app-kpimon-go | https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-app-kpimon-go|docker pull ghcr.io/ios-mcn-smo/ric-app-kpimon-go:1.0.1
 | xapp-onboarder| https://github.com/orgs/ios-mcn-smo/packages/container/package/xapp-onboarder | docker pull ghcr.io/ios-mcn-smo/xapp-onboarder:1.0.0
 | ric-app-ad| https://github.com/orgs/ios-mcn-smo/packages/container/package/ric-app-ad |docker pull ghcr.io/ios-mcn-smo/ric-app-ad:1.0.1
 | a1-policy-producer | https://github.com/orgs/ios-mcn-smo/packages/container/package/a1-policy-producer | docker pull ghcr.io/ios-mcn-smo/a1-policy-producer:1.0.0
 | load-monitoring-rapp | https://github.com/orgs/ios-mcn-smo/packages/container/package/load-monitoring-rapp | docker pull ghcr.io/ios-mcn-smo/load-monitoring-rapp:1.0.0
 |ue-management-rapp | https://github.com/orgs/ios-mcn-smo/packages/container/package/ue-management-rapp | docker pull ghcr.io/ios-mcn-smo/ue-management-rapp:1.0.0
 | darpan | https://github.com/orgs/ios-mcn-smo/packages/container/package/darpan |docker pull ghcr.io/ios-mcn-smo/darpan:latest




### Building custom images and using it.

Please refer to the oam developer guide that you will find in the SMO documentation.
