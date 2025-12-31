.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

Cluster API BYOH: Bare Metal Kubernetes Automation
==================================================

This project provides a fully automated solution for provisioning
Kubernetes clusters on bare metal servers using Cluster API (CAPI) and
the Bring Your Own Host (BYOH) provider. It leverages Ansible for
orchestration and configuration management, allowing you to turn raw
Linux servers into production-ready Kubernetes clusters with a single
JSON configuration file.

📋 Features & Support
---------------------

-  **Supported OS:** Ubuntu 20.04, 22.04, 24.04
-  **Kubernetes Versions:** Up to v1.34
-  **Architecture:** Linux AMD64
-  **Orchestration:** Automated via Ansible & Cluster API
-  **Networking:** Calico CNI, Kube-Vip for Control Plane HA

✅ Prerequisites
----------------

Before starting, ensure your Management Machine and Target Hosts meet
the following requirements.

1. Target Server Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The target servers (the machines that will become your workload
clusters) must have:

-  **SSH Access:** Password-less sudo or a known user/password
   (configured in ``input.json``)
-  **Internet Access:** Required to fetch K8s binaries and manifests
-  **Hostname Rule:** Hostnames MUST be lowercase. Kubernetes does not
   support uppercase characters in server names.

   -  ✅ Correct: ``hpe-server-01``
   -  ❌ Incorrect: ``HPE-Server-01``

2. Configure Ansible Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You must configure one of the following authentication methods for
Ansible to connect to your target servers:

💡 Recommendation
^^^^^^^^^^^^^^^^^

**Use Option A (SSH Keys).** It is the standard way to manage Linux
servers. It prevents issues where ``sshpass`` might hang or fail due to
“Host Key Verification” prompts. Since you already have access to all
servers, running ``ssh-copy-id`` 5 times will take you less than 2
minutes and save you headaches later.

**Option A: Use SSH Keys (Recommended & Best)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the “Critical Pre-Requisite” mentioned. It is better because it
is more secure and Ansible doesn’t get stuck on password prompts.

**How to do it:**

1. **SSH into your Management server:**

   .. code:: bash

      ssh username@management-server-ip
      # Enter your password when prompted

2. **Generate a Key Pair on your Management server** *(Do not enter a
   passphrase when asked, just press Enter)*:

   .. code:: bash

      ssh-keygen -t rsa

3. **Copy this Key to ALL serverw (including itself):** You will run
   this command from your management server. It will ask for the
   password one last time for each server.

   .. code:: bash

      # Copy to target server
      ssh-copy-id username@server-01-ip
      ssh-copy-id username@server-02-ip
      ssh-copy-id username@server-03-ip
      # ... repeat for all target servers

4. **Test it:** From your management server, try
   ``ssh username@server-01-ip``. If it logs in without a password, you
   are ready!

**Config Change:**

-  Leave ``host_pwd`` **empty** ``""`` in your ``input.json``
-  Keep the ``# ansible_password`` line **commented out** in
   ``site.yaml``

--------------

**Option B: Use Passwords (If you skip Keys)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do **not** want to generate keys and just want to use passwords,
you can configure Ansible to use it.

**How to do it:**

1. **Install** ``sshpass`` **on** ``hpe18``: Ansible needs this tool to
   handle text passwords.

   .. code:: bash

      sudo apt update
      sudo apt install sshpass

2. **Update** ``input.json``: You must put the password in the file for
   every host.

   .. code:: json

      {
        "host_id": 1,
        "host_name": "server-01",
        "host_ip": "192.168.1.10",
        "host_user": "ubuntu",
        "host_pwd": "your-password"  
      }

3. **Update** ``site.yaml``: You must **uncomment** the password line in
   ``site.yaml``.

   **Current:**

   .. code:: yaml

      # ansible_password: "{{ item.host_pwd }}"

   **Change to:**

   .. code:: yaml

      ansible_password: "{{ item.host_pwd }}"

3. Connectivity Check
~~~~~~~~~~~~~~~~~~~~~

Run the following commands on ALL target servers to verify they can
reach the necessary repositories:

.. code:: bash

   ping -c3 raw.githubusercontent.com
   nslookup raw.githubusercontent.com

If these fail, check your DNS or Firewall settings before proceeding.

📂 Project Structure
--------------------

::

   .
   ├── mgmt.sh            # Setup script for the Management Cluster (Clusterctl, ArgoCD, etc.)
   ├── site.yaml          # Main Ansible playbook for provisioning and cluster creation
   ├── input.json         # Configuration file defining Hosts and Cluster topology
   ├── templates/
   │   └── cluster.yaml.j2 # Jinja2 template for generating CAPI Cluster manifests
   └── README.md

🚀 Getting Started
------------------

Step 1: Initialize Management Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the ``mgmt.sh`` script on your bootstrap machine (e.g., your laptop
or a dedicated bastion host). This script installs dependencies
(Docker/Containerd, Kubectl, Ansible) and initializes the CAPI
management cluster.

.. code:: bash

   chmod +x mgmt.sh
   ./mgmt.sh

**What this does:**

-  Installs system dependencies and Kubernetes binaries
-  Bootstraps a local Kubernetes management cluster using kubeadm
-  Installs Cluster API, BYOH Provider, Cert Manager, and ArgoCD
-  Patches the BYOH controller to use the enhanced image
   (``rehanfazal47/byoh-controller:controller-enhancced``)

Step 2: Define Infrastructure (input.json)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Edit the ``input.json`` file to define your available physical hosts and
how you want to group them into clusters.

**Strict Rules for input.json:**

-  ``host_name``: Must match the actual hostname of the machine
   (lowercase)
-  ``host_id``: Must be unique for every host
-  ``host_ip``: Must be resolvable or a direct IP address

**Example input.json:**

.. code:: json

   {
     "hosts": [
       {
         "host_id": 1,
         "host_name": "server-01",
         "host_ip": "192.168.1.10",
         "host_user": "ubuntu",
         "host_pwd": "password123"
       },
       {
         "host_id": 2,
         "host_name": "server-02",
         "host_ip": "192.168.1.11",
         "host_user": "ubuntu",
         "host_pwd": "password123"
       }
     ],
     "clusters": [
       {
         "cluster_name": "production-cluster",
         "cluster_masters": [ { "host_id": 1 } ],
         "cluster_workers": [ { "host_id": 2 } ]
       }
     ]
   }

Step 3: Provision and Deploy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the Ansible playbook to prepare the hosts, install the BYOH agent,
and deploy the defined clusters.

.. code:: bash

   ansible-playbook site.yaml

**What happens next:**

-  **Keys & Inventory:** Ansible rotates the bootstrap tokens and
   creates an in-memory inventory from ``input.json``
-  **Host Prep:** Connects to hosts, disables swap, loads kernel
   modules, installs containerd and K8s binaries (v1.34 or version
   specified in playbook)
-  **Agent Deployment:** Starts the ``byoh-hostagent`` on the targets
-  **Cluster Creation:** Generates manifests from ``cluster.yaml.j2``
   and applies them to the management cluster
-  **Pinning:** Automatically labels the agents so the specific physical
   host is assigned to the specific cluster role defined in your JSON

⚙️ Operations Guide
-------------------

How to Add New Clusters or Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To scale your infrastructure, you do not need to start over.

1. **Edit input.json:**

   -  To add a node: Add a new entry to the ``"hosts"`` array and assign
      its ``host_id`` to a cluster’s ``cluster_workers`` list
   -  To add a cluster: Add a new object to the ``"clusters"`` array

2. **Re-run Ansible:**

   .. code:: bash

      ansible-playbook site.yaml

Ansible is idempotent; it will skip already configured hosts and only
provision the new ones.

How to Delete Clusters
~~~~~~~~~~~~~~~~~~~~~~

To remove a workload cluster (this will wipe the nodes associated with
it):

.. code:: bash

   # List all clusters
   kubectl get clusters

   # Delete a specific cluster
   kubectl delete cluster <cluster_name>

**Note:** This deletes the Kubernetes cluster object. The physical
machines will remain running but will be released by the BYOH
controller. To reuse them, you may need to clean up the
``byoh-hostagent`` process on the target server.

Changing Kubernetes Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To change the version of Kubernetes being deployed:

1. Open ``site.yaml``
2. Locate ``target_k8s_version: "1.34.0"`` (under Play 2 variables)
3. Update it to your desired version (e.g., ``1.30.0``)
4. Ensure ``cluster_k8s_version`` (under Play 3 variables) matches
   (e.g., ``v1.30.0``)

🛠 Troubleshooting
-----------------

1. Ansible fails to connect to hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Ensure SSH keys are copied (``ssh-copy-id user@host``) or the
   password in ``input.json`` is correct
-  Check if ``python3`` is installed on the target

2. Cluster(or Nodes) stuck in “Provisioning” state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check the agent logs on the target host:

.. code:: bash

   tail -f /var/log/byoh.log

Ensure the host ID labeling worked by running
``kubectl get byohosts --show-labels`` on the management machine.

3. “Hostname not found”
~~~~~~~~~~~~~~~~~~~~~~~

Verify that ``hostname`` command on the target server returns a
lowercase name that exactly matches ``host_name`` in ``input.json``.
