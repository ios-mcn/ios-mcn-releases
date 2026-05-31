# IOS-MCN-IMS – API Guide

This document describes the REST APIs supported by the **IOS-MCN-IMS** platform.

The APIs primarily expose:

1. **N5 → NRF/PCF Interface APIs**
2. **P-CSCF → N5 Interface APIs**
3. **I-CSCF → UDR Interface APIs**
3. **S-CSCF → UDR Interface APIs**

These APIs enable seamless integration with 5G Core network functions including NRF, SCP, PCF, UDR, and UDM while providing centralized configuration management capabilities.

---

# 1. N5 → NRF/PCF Interface API Guide

The N5 Interface acts as a 3GPP Application Function (AF) and communicates with:

- NRF
- SCP
- PCF

for Network Function registration and policy authorization.

The N5 Interface supports:

- NF Registration
- NF Heartbeat
- Audio Session Creation (VoNR)
- Video Session Creation (ViNR)
- Session Modification
- Session Deletion

---

## 1.1 NF Registration API

### Endpoint

```http
POST /nnrf-nfm/v1/nf-instances
```

### Description

Registers the N5 Interface as an Application Function (AF) with the Network Repository Function (NRF).

### Purpose

- Advertises AF capabilities
- Enables NF discovery
- Establishes service availability
- Maintains registration through heartbeat updates

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "nfInstanceId": "##{UUID}",
  "nfType": "AF",
  "nfStatus": "REGISTERED",
  "ipv4Addresses": [
    "##{AFIP}"
  ],
  "allowedNfTypes": [
    "SCP",
    "PCF"
  ],
  "priority": 0,
  "capacity": 100,
  "load": 0,
  "nfServiceList": {
    "##{UUID}": {
      "serviceInstanceId": "##{UUID}",
      "serviceName": "npcf-policyauthorization",
      "versions": [
        {
          "apiVersionInUri": "v2",
          "apiFullVersion": "2.0.0"
        }
      ],
      "scheme": "http",
      "nfServiceStatus": "REGISTERED",
      "ipEndPoints": [
        {
          "ipv4Address": "##{AFIP}",
          "port": 7777
        }
      ],
      "allowedNfTypes": [
        "PCF"
      ]
    }
  }
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 201 | Successfully Registered |
| 200 | Already Registered |
| 400 | Invalid Request |
| 500 | NRF Error |

---

## 1.2 NF Heartbeat API

### Endpoint

```http
PATCH /nnrf-nfm/v1/nf-instances/{nfInstanceId}
```

### Description

Maintains AF registration state and updates runtime information within the NRF.

### Purpose

- Keeps AF registration active
- Updates NRF load information
- Prevents NF deregistration

### Request Headers

```http
Content-Type: application/json-patch+json
```

### Request Body

```json
[
  {
    "op": "replace",
    "path": "/nfStatus",
    "value": "REGISTERED"
  },
  {
    "op": "replace",
    "path": "/load",
    "value": 0
  }
]
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 204 | Heartbeat Accepted |
| 404 | NF Instance Not Found |
| 500 | NRF Error |

---

## 1.3 Audio Session Creation API (VoNR)

### Endpoint

```http
POST /npcf-policyauthorization/v1/app-sessions
```

### Description

Creates a policy authorization session for Voice over New Radio (VoNR).

### Purpose

- Requests QoS authorization from PCF
- Creates audio media policy session
- Establishes RTP and RTCP QoS flows

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "ascReqData": {
    "afAppId": "+g.3gpp.icsi-ref=\"urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel\"",
    "dnn": "ims",
    "medComponents": {
      "0": {
        "medCompN": 1,
        "qosReference": "qosVoNR",
        "medType": "AUDIO",
        "codecs": ["downlink\noffer\n", "uplink\nanswer\n"],
        "medSubComps": {
          "0": {
            "fNum": 1,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UEAUDIOPORT}",
              "permit in 17 from ##{UEIP} ##{UEAUDIOPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "128 Kbps",
            "marBwUl": "128 Kbps",
            "flowUsage": "NO_INFO"
          },
          "1": {
            "fNum": 2,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UERTCPPORT}",
              "permit in 17 from ##{UEIP} ##{UERTCPPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "128 Kbps",
            "marBwUl": "128 Kbps",
            "flowUsage": "RTCP"
          }
        }
      }
    },
    "evSubsc": {
      "events": [
        {
          "event": "QOS_NOTIF",
          "notifMethod": "PERIODIC"
        },
        {
          "event": "ANI_REPORT",
          "notifMethod": "ONE_TIME"
        }
      ]
    },
    "notifUri": "http://##{AFIP}:##{AFPORT}",
    "sponStatus": "SPONSOR_DISABLED",
    "gpsi": "msisdn-##{UEMSISDN}",
    "suppFeat": "5",
    "ueIpv4": "##{UEIP}"
  }
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 201 | Session Created |
| 400 | Invalid Request |
| 403 | Policy Denied |
| 500 | PCF Error |

---

## 1.4 Video Session Creation API (ViNR)

### Endpoint

```http
POST /npcf-policyauthorization/v1/app-sessions
```

### Description

Creates a policy authorization session for Video over New Radio (ViNR).

### Purpose

- Requests video QoS authorization from PCF
- Creates audio and video media policy sessions
- Establishes RTP and RTCP QoS flows

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "ascReqData": {
    "afAppId": "+g.3gpp.icsi-ref=\"urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel\"",
    "dnn": "ims",
    "medComponents": {
      "0": {
        "medCompN": 1,
        "qosReference": "qosVoNR",
        "medType": "AUDIO",
        "codecs": ["downlink\noffer\n", "uplink\nanswer\n"],
        "medSubComps": {
          "0":{
            "fNum": 1,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UEAUDIOPORT}",
              "permit in 17 from ##{UEIP} ##{UEAUDIOPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "128 Kbps",
            "marBwUl": "128 Kbps",
            "flowUsage": "NO_INFO"
          },
          "1": {
            "fNum": 2,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UERTCPPORT}",
              "permit in 17 from ##{UEIP} ##{UERTCPPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "128 Kbps",
            "marBwUl": "128 Kbps",
            "flowUsage": "RTCP"
          }
        }
      },
      "1": {
        "medCompN": 2,
        "qosReference": "qosViNR",
        "medType": "VIDEO",
        "codecs": ["downlink\noffer\n", "uplink\nanswer\n"],
        "medSubComps": {
          "0":{
            "fNum": 1,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UEVIDEOPORT}",
              "permit in 17 from ##{UEIP} ##{UEVIDEOPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "2048 Kbps",
            "marBwUl": "2048 Kbps",
            "flowUsage": "NO_INFO"
          },
          "1": {
            "fNum": 2,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UEVIDEORTCPPORT}",
              "permit in 17 from ##{UEIP} ##{UEVIDEORTCPPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "128 Kbps",
            "marBwUl": "128 Kbps",
            "flowUsage": "RTCP"
          }
        }
      }
    },
    "evSubsc": {
      "events": [
        { "event": "QOS_NOTIF", "notifMethod": "PERIODIC" },
        { "event": "ANI_REPORT", "notifMethod": "ONE_TIME" }
      ]
    },
    "notifUri": "http://##{AFIP}:##{AFPORT}",
    "sponStatus": "SPONSOR_DISABLED",
    "gpsi": "msisdn-##{UEMSISDN}",
    "suppFeat": "5",
    "ueIpv4": "##{UEIP}"
  }
}

```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 201 | Session Created |
| 400 | Invalid Request |
| 403 | Policy Denied |
| 500 | PCF Error |

---

## 1.5 Session Modification API

### Endpoint

```http
PATCH /npcf-policyauthorization/v1/app-sessions/{appSessionId}
```

### Description

Modifies an existing policy authorization session by adding a video media component.

### Purpose

- Upgrades VoNR session to ViNR session
- Adds video media components
- Updates policy association

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "ascReqData": {
    "afAppId": "+g.3gpp.icsi-ref=\"urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel\"",
    "dnn": "ims",
    "medComponents": {
      "1": {
        "medCompN": 2,
        "qosReference": "qosViNR",
        "medType": "VIDEO",
        "codecs": [
          "downlink\noffer\n",
          "uplink\nanswer\n"
        ],
        "medSubComps": {
          "0": {
            "fNum": 1,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UEVIDEOPORT}",
              "permit in 17 from ##{UEIP} ##{UEVIDEOPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "2048 Kbps",
            "marBwUl": "2048 Kbps",
            "flowUsage": "NO_INFO"
          },
          "1": {
            "fNum": 2,
            "fDescs": [
              "permit out 17 from any to ##{UEIP} ##{UEVIDEORTCPPORT}",
              "permit in 17 from ##{UEIP} ##{UEVIDEORTCPPORT} to any"
            ],
            "fStatus": "ENABLED",
            "marBwDl": "128 Kbps",
            "marBwUl": "128 Kbps",
            "flowUsage": "RTCP"
          }
        }
      }
    },
    "evSubsc": {
      "events": [
        {
          "event": "QOS_NOTIF",
          "notifMethod": "PERIODIC"
        },
        {
          "event": "ANI_REPORT",
          "notifMethod": "ONE_TIME"
        }
      ]
    },
    "notifUri": "http://##{AFIP}:##{AFPORT}",
    "sponStatus": "SPONSOR_DISABLED",
    "gpsi": "msisdn-##{UEMSISDN}",
    "suppFeat": "5",
    "ueIpv4": "##{UEIP}"
  }
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Session Modified |
| 400 | Invalid Request |
| 404 | Session Not Found |
| 500 | PCF Error |

---

## 1.6 Session Deletion API

### Endpoint

```http
POST /npcf-policyauthorization/v1/app-sessions/{appSessionId}/delete
```

### Description

Deletes an existing policy authorization session.

### Purpose

- Releases QoS resources
- Removes PCF policy association
- Terminates media authorization

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Session Deleted Ok Response |
| 204 | Session Deleted |
| 404 | Session Not Found |
| 500 | PCF Error |

---


# 2. P-CSCF → N5 Interface APIs

The P-CSCF communicates with the N5 Interface to request policy authorization and QoS enforcement for IMS multimedia sessions.

---

## 2.1 Create Audio PDU Session API

### Endpoint

```http
POST /api/n5/createAudio
```

### Description

Creates an Audio PDU Session and requests Voice QoS authorization from the N5 Interface.

### Purpose

- Create Voice QoS Session
- Request VoNR Policy Authorization
- Establish Audio RTP Flows
- Establish Audio RTCP Flows

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "fromUEMSISDN": "919876543210",
  "fromUEIP": "192.168.1.10",
  "fromUEAUDIOPORT": "49152"
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Audio PDU Session Created |
| 400 | Invalid Request |
| 500 | Internal Error |

---

## 2.2 Create Video PDU Session API

### Endpoint

```http
POST /api/n5/createVideo
```

### Description

Creates Audio and Video PDU Sessions and requests Video QoS authorization from the N5 Interface.

### Purpose

- Create Audio QoS Session
- Create Video QoS Session
- Request ViNR Policy Authorization
- Establish RTP and RTCP Flows

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "fromUEMSISDN": "919876543210",
  "fromUEIP": "192.168.1.10",
  "fromUEAUDIOPORT": "49152",
  "fromUEVIDEOPORT": "49154"
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Video PDU Session Created |
| 400 | Invalid Request |
| 500 | Internal Error |

---

## 2.3 Patch Video PDU Session API

### Endpoint

```http
POST /api/n5/patchVideo
```

### Description

Upgrades an existing Audio PDU Session by adding Video Media Components.

### Purpose

- Upgrade VoNR Session to ViNR
- Add Video QoS Components
- Update Existing Policy Session

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "fromUEMSISDN": "919876543210",
  "fromUEIP": "192.168.1.10",
  "fromUEAUDIOPORT": "49152",
  "fromUEVIDEOPORT": "49154"
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Session Modified |
| 400 | Invalid Request |
| 500 | Internal Error |

---

## 2.4 Delete PDU Session API

### Endpoint

```http
POST /api/n5/deleteSession
```

### Description

Deletes an existing PDU Session and releases associated QoS resources.

### Purpose

- Release QoS Resources
- Remove Policy Association
- Cleanup Session State

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "fromUEMSISDN": "919876543210"
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Session Deleted |
| 404 | Session Not Found |
| 500 | Internal Error |

---

# 3. I-CSCF → UDR Interface APIs

The I-CSCF communicates with the UDR to validate subscriber existence before IMS registration and routing procedures.

---

## 3.1 Subscriber Existence Check API

### Endpoint

#### IOS-MCN Core Mode

```http
GET /nudr-dr/v2/subscription-data/imsi-{IMSI}/authentication-data/authentication-subscription
```

#### Standard UDR Mode

```http
GET /nudr-dr/v1/subscription-data/imsi-{IMSI}/authentication-data/authentication-subscription
```

### Description

Retrieves Authentication Subscription information for a subscriber and validates whether the IMSI exists within the UDR.

### Purpose

- Validate Subscriber Existence
- Verify IMSI Provisioning
- Prevent Routing Requests for Unknown Subscribers
- Support IMS Registration Processing

### Request Headers

```http
Content-Type: application/json
```

### Path Parameters

| Parameter | Description |
|------------|-------------|
| IMSI | Subscriber IMSI Identifier |

### Example Request

#### IOS-MCN Core Mode

```http
GET /nudr-dr/v2/subscription-data/imsi-001010123456789/authentication-data/authentication-subscription
```

#### Standard UDR Mode

```http
GET /nudr-dr/v1/subscription-data/imsi-001010123456789/authentication-data/authentication-subscription
```

### Success Response

| HTTP Code | Description |
|------------|-------------|
| 200 | Subscriber Exists |

### Failure Response

| HTTP Code | Description |
|------------|-------------|
| 404 | Subscriber Not Found |
| 500 | UDR Error |
| 503 | UDR Unreachable |

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Subscriber Exists |
| 404 | Subscriber Not Found |
| 500 | Internal Error |
| 503 | UDR Unreachable |

---

## Internal Processing Logic

The I-CSCF performs subscriber validation using:

```java
checkSubscriberExists(String imsi)
```

### Processing Flow

1. Receive IMS Registration Request.
2. Extract Subscriber IMSI.
3. Query UDR Authentication Subscription Data.
4. Validate HTTP Response.
5. Continue IMS Processing if Subscriber Exists.
6. Reject Registration if Subscriber Does Not Exist.

### Success Criteria

The subscriber is considered valid when:

```http
HTTP 200 OK
```

is returned by the UDR.

### Failure Criteria

The subscriber is considered invalid when:

```http
HTTP 404 Not Found
```

or any UDR communication failure is returned.

---

## UDR Integration Modes

### IOS-MCN Core Mode

Uses:

```http
/nudr-dr/v2/subscription-data/
```

### Standard UDR Mode

Uses:

```http
/nudr-dr/v1/subscription-data/
```

The mode is selected using:

```text
IOSMCNCORE=TRUE/FALSE
```

within the I-CSCF configuration.

---

# 4. S-CSCF → UDR Interface APIs

The S-CSCF communicates with the UDR to retrieve subscriber authentication data required for IMS AKA authentication.

---

## 4.1 Authentication Subscription Retrieval API

### Endpoint

#### IOS-MCN Core Mode

```http
GET /nudr-dr/v2/subscription-data/imsi-{IMSI}/authentication-data/authentication-subscription
```

#### Standard UDR Mode

```http
GET /nudr-dr/v1/subscription-data/imsi-{IMSI}/authentication-data/authentication-subscription
```

### Description

Retrieves subscriber authentication data from the UDR for IMS AKA authentication processing. :contentReference[oaicite:0]{index=0}

### Purpose

- Retrieve Subscriber Authentication Data
- Retrieve Permanent Key (K)
- Retrieve Operator Key (OPc)
- Retrieve Authentication Management Field (AMF)
- Retrieve Sequence Number (SQN)
- Generate Authentication Vectors

### Request Headers

```http
Accept: application/json
```

### Path Parameters

| Parameter | Description |
|------------|-------------|
| IMSI | Subscriber IMSI Identifier |

### Example Request

```http
GET /nudr-dr/v2/subscription-data/imsi-001010123456789/authentication-data/authentication-subscription
```

### Response Body

#### IOS-MCN Core Format

```json
{
  "authenticationManagementField": "8000",
  "encPermanentKey": "465B5CE8B199B49FAA5F0A2EE238A6BC",
  "encOpcKey": "E8ED289DEBA952E4283B54E88E6183CA",
  "sequenceNumber": {
    "sqn": "000000000001"
  }
}
```

#### Standard UDR Format

```json
{
  "authenticationManagementField": "8000",
  "permanentKey": {
    "permanentKeyValue": "465B5CE8B199B49FAA5F0A2EE238A6BC"
  },
  "opc": {
    "opcValue": "E8ED289DEBA952E4283B54E88E6183CA"
  },
  "sequenceNumber": "000000000001"
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Authentication Data Retrieved |
| 404 | Subscriber Not Found |
| 500 | UDR Error |
| 503 | UDR Unreachable |

---

## 4.2 IMS AKA Authentication Vector Generation

### Description

After retrieving authentication data from UDR, the S-CSCF generates IMS AKA authentication vectors using the MILENAGE algorithm. :contentReference[oaicite:1]{index=1}

### Purpose

- Generate RAND
- Generate AUTN
- Generate RES
- Generate CK
- Generate IK
- Generate Nonce

### Generated Parameters

| Parameter | Description |
|------------|-------------|
| RAND | Random Challenge |
| AUTN | Authentication Token |
| RES | Expected Authentication Response |
| CK | Cipher Key |
| IK | Integrity Key |
| NONCE | IMS Digest Nonce |

---

# 5. S-CSCF → UDR Interface APIs

The S-CSCF communicates with the UDR to retrieve subscriber identity(MSISDN) information.

---

## 5.1 Subscriber MSISDN Retrieval API

### Endpoint

#### IOS-MCN Core Mode

```http
GET /nudr-dr/v2/subscription-data/imsi-{IMSI}/{PLMN-ID}/provisioned-data/am-data
```

#### Standard UDR Mode

```http
GET /nudr-dr/v1/subscription-data/imsi-{IMSI}/{PLMN-ID}/provisioned-data/am-data
```

### Description

Retrieves subscriber Access and Mobility Subscription data and extracts the associated MSISDN. :contentReference[oaicite:2]{index=2}

### Purpose

- Retrieve Subscriber MSISDN
- Retrieve GPSI Information
- Support IMS Registration
- Support SIP URI Resolution

### Request Headers

```http
Accept: application/json
3gpp-sbi-target-apiroot: <api-root>
3gpp-sbi-max-rsp-time: <timeout>
```

### Path Parameters

| Parameter | Description |
|------------|-------------|
| IMSI | Subscriber IMSI Identifier |
| PLMN-ID | Mobile Network Identifier |

### Example Request

```http
GET /nudr-dr/v2/subscription-data/imsi-001010123456789/00101/provisioned-data/am-data
```

### Example Response

```json
{
  "gpsis": [
    "msisdn-919876543210"
  ]
}
```

### Response Codes

| HTTP Code | Description |
|------------|-------------|
| 200 | Subscriber Data Retrieved |
| 404 | Subscriber Not Found |
| 500 | UDM Error |
| 503 | UDM Unreachable |

---