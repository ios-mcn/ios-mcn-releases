## IOS MCN IMS n5 v0.3.0 Release
Welcome to the v0.3.0 Release of IOS MCN IMS n5

# Version Summary
Version Number : v0.3.0
Version Name:  v0.3.0
Date: 29-03-2025

Projects / Repos Included in this release:
| Project | version| Release image Link |
|--|--|--|
 |[N5](https://github.com/ios-mcn-ims/n5.git)|v0.3.0| [link](https://github.com/ios-mcn-ims/n5/releases/tag/v0.3.0.iosmcn.ims.n5)|

## Release Summary :
**N5 agartala v0.3.0** is released with features supporting Audio and Video PDU session creation, and deletion, with support of registering P-CSCF as a Network Function.


## Highlights:
- NF Register:
   - Heartbeat timer to maintain register status
- Audio PDU Session Creation
- Video PDU Session Creation
- PDU Session Deletion

## Changelog v0.3.0
- Inclusion of SBI interface for P-CSCF
- Support for HTTP/1.1 for smoother NFRegister function.
- Removal of pseudo headers from request to clear the clunk.

#### Test Reports:
[link](ttps://github.com/ios-mcn-ims/qa/tree/main/01.releases/v0.3.0/test%20report)

## How to use the Release:
### Environment Requirements and Pre-requisites:

### Steps to Use:
#### Build

From source code folder run 

docker build -t n5-service .

#### Run

docker run -d --name n5-container -p 8080:8080 n5-service

#### Run Tests
docker exec -it n5-container mvn test -Dserver.port=8081 -Dapp.config=/app/config/iosmcn-ims-n5.test

```plaintext
[INFO] Results:
[INFO]
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  2.627 s
[INFO] Finished at: 2025-03-29T14:11:44Z
[INFO] ------------------------------------------------------------------------```
```

#### Gain access
docker exec -it n5-container /bin/bash

## License 
| Library | License |
| ------ | ------- |
| Spring Framework | Apache License 2.0 |
| Spring Boot | Apache License 2.0 |
| Apache Log4j | Apache License 2.0 |
| OkHttp | Apache License 2.0 |
| Okio | Apache License 2.0 |
| INI4J | Apache License 2.0 |
| Jakarta Annotations | Eclipse Public License - v 2.0 |
| Javax Annotation | Eclipse Public License - v 2.0 |
 
## Issues and Suggestions
For all issues/suggestions related to specific projects, please raise here - [link](https://github.com/ios-mcn-ims/ios-mcn-ims/issues)