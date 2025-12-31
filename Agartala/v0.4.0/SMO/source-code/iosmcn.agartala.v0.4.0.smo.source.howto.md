## This document explains how to use the source-code and build OAM images, if required.

The SMO source code has mainly 3 parts - FOCOM, NFO and OAM.

### Using OAM.

Step 1 : untar the iosmcn.agartala.v0.4.0.smo.source.tar.gz

```sh
tar -xvzf iosmcn.agartala.v0.4.0.smo.source.tar.gz

```

Step 2 : untar the oam-0.0.2.iosmcn.smo.oam.tar.gz

```sh
cd iosmcn.agartala.v0.4.0.smo.source
tar -xvzf oam-0.4.0.iosmcn.smo.oam.tar.gz
cd oam-0.4.0.iosmcn.smo.oam
```

Step 3: Ensure the system is ready for OAM deployment.

Please refer to the pre-requisites section in the OAM deployment guide that is part of the SMO documentation.

Step 4: Adapt to this release (this step applies only to the 0.4.0 release)

```sh
sed -i -e 's/ios-mcn-smo/ios-mcn/g' -e 's/1.2.2/1.2.1/g' .env
```

Step 5: Deploy OAM

Please refer to the Usage section in the OAM deployment guide that is part of the SMO documentation.
You need to run just 2 commands

```sh
python3 adapt_to_environment.py --i <IP-ADDR-OF-THE-SYSTEM> --d <DOMAIN-NAME>
./docker-setup.sh
```

### Using FOCOM
Step 1 : untar the iosmcn.agartala.v0.2.0.smo.source.tar.gz

```sh
tar -xvzf iosmcn.agartala.v0.4.0.smo.source.tar.gz

```

Step 2 : untar the focom-0.0.1.iosmcn.smo.focom.tar.gz

```sh
cd iosmcn.agartala.v0.4.0.smo.source
tar -xvzf focom-0.4.0.iosmcn.smo.focom.tar.gz
cd focom-0.4.0.iosmcn.smo.focom
```

Step 3: Use Ansible Roles/Playbooks
If you prefer to deploy kubernetes cluster

```sh
cd docker/roles/ansible-role-docker
```
Follow the steps mentioned in README.md

If you prefer to prepare system for docker and docker compose

```sh
cd kubernetes
```
Follow the steps mentioned in README.md

### Using NFO
Step 1 : untar the iosmcn.agartala.v0.1.0.smo.source.tar.gz

```sh
tar -xvzf iosmcn.agartala.v0.4.0.smo.source.tar.gz

```

Step 2 : untar the nfo-0.0.1.iosmcn.smo.nfo.tar.gz

```sh
cd iosmcn.agartala.v0.4.0.smo.source
tar -xvzf nfo-0.4.0.iosmcn.smo.focom.tar.gz
cd focom-0.4.0.iosmcn.smo.nfo
```

Step 3: Deploy Workloads

If you want to deploy RAN distributed, follow the steps in ``docker/ran-distributed/README.md``.
If you want to deploy CORE, follow the steps in ``kubernetes/aether-5gc/README.md``

### Building OAM images

Please refer to the Developer Guide, which is present in the SMO documentation.
