# **IOS MCN v0.3.0 Agartala Release - API Guide v3.0**

## **Introduction**

This REST APIs are used to configure subscribers, device groups and network slice of IOSMCN-Core.

## **Purpose and Audience**
This guide is for the developers to interface using API 

## **API Specification**


### API 1 
**Subscriber Configuration**
Below example configures subscriber 208014567891209 in the IOSMCN-Core. You can any number of subscribers using these APIs. IOSMCN-Core takes care of configuring Network Function responsible for authentication with the below details.

- Post:
  URL: `http://<config-service-name-or-ip>:<port>/api/subscriber/<imsi-xxx>`
  Ex: `http://<config-service-name-or-ip>:<port>/api/subscriber/<imsi-208014567891209>`
  
  Request Body:
      {
          "UeId":"208014567891209",
          "plmnId":"20801",
          "opc":"d4416644f6154936193433dd20a0ace0",
          "key":"465b5ce8b199b49faa5f0a2ee238a6bc",
          "sequenceNumber":"96"
      }
      
- Delete:
  URL: `http://<config-service-name-or-ip>:<port>/api/subscriber/<imsi-xxx>`
   Ex: `http://<config-service-name-or-ip>:<port>/api/subscriber/<imsi-208014567891209>`

### API 2 
**Device Group Configuration**
Below example groups multiple IMSIs under one IP domain. IP domain is close match with APN in 4G & dnn in case of 5G. Along with UE IP pool, there is also configuration of QoS for the users in this group.
- Post:
  URL: `http://<config-service-name-or-ip>:<port>/device-group/<group-name>`
  Ex: `http://config5g:8080/device-group/iot-camera`

  Request Body:
  {
      "imsis":
      [
          "123456789123456"
          "123456789123457"
          "123456789123458"
      ],
      "site-info": "menlo",
      "ip-domain-name": "pool1",
      "ip-domain-expanded":
      {
          "dnn": "internet",
          "ue-ip-pool": "10.91.0.0/16",
          "dns-primary": "8.8.8.8",
          "dns-secondary": "8.8.4.4",
          "mtu": 1460,
          "ue-dnn-qos":
          {
              "dnn-mbr-uplink": 4000000,
              "dnn-mbr-downlink": 20000000,
              "bitrate-unit": "Mbps",
              "traffic-class":
              {
                  "qci": 9,
                  "arp": 1,
                  "pdb": 2,
                  "pelr": 1,
                  "name": "platinum"
              }
          }
      }
  }

- Delete
  URL: `http://<config-service-name-or-ip>:<port>/device-group/<group-name>`
  Ex: `http://config5g:8080/device-group/iot-camera`
  
REST API can use PUT Method to modify/replace the device group configuration. IMSIs can be added, removed through PUT Method.
If UPF is used to allocate UE address allocation then even if you have specified UE address pool in the slice config, you still need to add the address pool configuration in the UPF deployment.

### API 3

**Network Slice Configuration**

Below example creates Network Slice with set of eNBs, UPF and device groups.

- Post:
  URL: `http://<config-service-name-or-ip>:<port>/network-slice/<slice-name>`
  Ex: `http://config5g:8080/network-slice/slice1`


  Request Body:
  {
      "slice-id":
      {
          "sst": "1",
          "sd": "010203"
      },
      "qos":
      {
          "uplink": 4000000,
          "downlink": 20000000,
          "bitrate-unit": "Mbps",
          "traffic-class":
          {
              "qci": 9,
              "arp": 1,
              "pdb": 2,
              "pelr": 1,
              "name": "platinum"
          }
      },
      "site-device-group":
      [
          "iot-camera"
      ],
      "site-info":
      {
          "site-name": "menlo",
          "plmn":
          {
              "mcc": "315",
              "mnc": "010"
          },
          "gNodeBs":
          [
              {
              "name": "menlo-gnb1",
              "tac": 1
              }
          ],
          "upf":
          {
          "upf-name": "upf.menlo.iosmcn.org",
          "upf-port": 8805
          }
      },
  }

- Delete
  URL: `http://<config-service-name-or-ip>:<port>/network-slice/<slice-name>`
  Ex: `http://config5g:8080/network-slice/slice1`

Slice needs to have single UPF. Multiple UPFs can not be added in single Slice. One or more access nodes can be added in slice. For now IOSMCN-Core does not do any validation of access nodes connecting to MME/AMF, but TAC & PLMN validation is done in Core Network.


### API 4
**Network Slice + Application filtering Configuration**

Below example creates Network Slice with set of eNBs, UPF and device groups. Note that this slice only allows traffic to single application hosted at address 10.91.1.3 .. code-block

- Post:
  URL: `http://<config-service-name-or-ip>:<port>/network-slice/<slice-name>`
  Ex: `http://config5g:8080/network-slice/slice1`


  Request Body:
  {
      "slice-id":
      {
          "sst": "1",
          "sd": "010203"
      },
      "qos":
      {
          "uplink": 4000000,
          "downlink": 20000000,
          "bitrate-unit": "Mbps",
          "traffic-class":
          {
              "qci": 9,
              "arp": 1,
              "pdb": 2,
              "pelr": 1,
              "name": "platinum"
          }
      },
      "site-device-group":
      [
          "iot-camera"
      ],
      "site-info":
      {
          "site-name": "menlo",
          "plmn":
          {
              "mcc": "315",
              "mnc": "010"
          },
          "gNodeBs":
          [
              {
              "name": "menlo-gnb1",
              "tac": 1
              }
          ],
          "upf":
          {
          "upf-name": "upf.menlo.iosmcn.org",
          "upf-port": 8805
          }
      },
      "application-filtering-rules":
        [
           {
              "rule-name": rule-1,
              "priority": 5,
              "action" : permit,
              "endpoint": "10.91.1.3",
              "traffic-class":
              {
                "name": “platinum”,
                "qci": 9,
                "arp": 125,
                "pdb": 300,
                "pelr": 6
              }
          }
        ]
  }

- Delete
  URL: `http://<config-service-name-or-ip>:<port>/network-slice/<slice-name>`
  Ex: `http://config5g:8080/network-slice/slice1`

## Related Artifacts & links

| **Document Name** | **Purpose** | **Link** |
|--|--|--|
| Installation Guide | Installation of IOSMCN-Core | [Click here](./IOS-MCN%20CORE%20Installation%20Guide.md) |
| Troubleshooting Guide  | Troubleshooting guide for IOSMCN-Core | [Click here](./IOS-MCN%20CORE%20Troubleshooting%20Guide.md)|
| Developer Guide | Guide for IOSMCN-Core developers | [Click Here](./IOS-MCN%20CORE%20Developer%20Guide.md)|
| User Guide | Quick user guide | [Click Here](./IOS-MCN%20CORE%20User%20Guide.md)  |
| API Guide | API guide | [Click here](./IOS-MCN%20CORE%20API%20Guide.md)|
