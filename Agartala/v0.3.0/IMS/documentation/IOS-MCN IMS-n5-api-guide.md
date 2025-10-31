
# N5 Interface – API Guide

This API Guide provides detailed information about the two primary interfaces used in the **N5 Interface – Agartala v0.3.0**:

1. **NRF API** – For Network Function (NF) Registration
2. **PCF API** – For Application Session (PDU Session) Management

These APIs follow 3GPP-compliant specifications and are designed to interact with the 5G Core Network’s NRF and PCF functions.

---

## 1. NRF API – NF Registration

### Endpoint
```
POST /nnrf-nfm/v1/nf-instances
```

### Description
Registers the **P-CSCF** or other Application Function (AF) as a Network Function (NF) with the **Network Repository Function (NRF)**.

### Purpose
- Advertises AF capabilities to NRF
- Allows discoverability by other 5G Core functions
- Maintains registration with periodic heartbeats

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
  "ipv4Addresses": ["##{AFIP}"],
  "allowedNfTypes": ["SCP", "PCF"],
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
      "allowedNfTypes": ["PCF"],
      "priority": 0,
      "capacity": 100,
      "load": 0
    }
  },
  "nfProfileChangesSupportInd": true
}

```

### Response
- `201 Created`: Successfully registered
- `200 OK`: NF instance already registered
- `400 Bad Request`: Invalid body
- `500 Internal Server Error`: NRF error

---

## 2. PCF API – App Session Management

### Endpoint
```
POST /npcf-policyauthorization/v1/app-sessions
```

### Description
Requests policy control for establishing an application session via the **Policy Control Function (PCF)**. This is used to initiate **Audio** and **Video** PDU sessions with appropriate QoS parameters.

### Purpose
- Creates new Application Sessions
- Notifies PCF of media type (Audio/Video)
- Requests appropriate QoS policies for each session

### Request Headers
```http
Content-Type: application/json
```

### Audio Session – Request Body

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

---

### Video Session – Request Body

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
        "medCompN": 1,
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

### Response
- `201 Created`: Policy session created successfully
- `403 Forbidden`: Request denied by PCF policy
- `400 Bad Request`: Invalid body
- `500 Internal Server Error`: PCF failure

---

## Delete Session

### Endpoint
```
DELETE /npcf-policyauthorization/v1/app-sessions/{appSessionId}
```

### Description
Terminates an existing application session and releases policy control for that media flow.

---

## 3GPP Technical Specifications Referred
| Specification Number | Release | Title | Purpose |
| ------ | ------- |  ------ | ------- |
| 29.510 | Release 16 | Network function repository services | To register a new NF Instance |
| 29.514 | Release 16 | Policy Authorization Service | To manage Audio/Video PDUs |