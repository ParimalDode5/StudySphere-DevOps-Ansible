# 5–7 minute demonstration outline

## 0:00–0:40 — Introduction

"Hello. My project is StudySphere, a sample online learning platform. The objective is to demonstrate a DevOps workflow and automate web-server configuration and website deployment using Ansible on Ubuntu running in WSL2."

## 0:40–1:35 — Lifecycle and architecture

"The lifecycle includes planning, coding, version control, testing, release, deployment, operation, monitoring and feedback. The website is built with HTML, CSS and JavaScript. Git and GitHub provide version control. Ansible runs from the Ubuntu WSL2 control node and configures the local host. Nginx serves the website on port 80."

## 1:35–2:20 — Inventory and playbook

"The inventory defines a webservers group with localhost as its host. The local connection plugin is used because the control node and managed host are the same Ubuntu environment. The playbook updates the package index, installs Nginx, copies the website files, configures an Nginx virtual host, validates the configuration, starts the service and checks the HTTP response."

## 2:20–4:15 — Execute automation

Show the inventory, run the Ansible ping, run the syntax check and execute the playbook. Explain the tasks as the output appears. Do not skip or fabricate command output.

## 4:15–5:15 — Verify the website and service

Show `systemctl status nginx`, `curl -I http://localhost` and the StudySphere page in a browser.

## 5:15–5:55 — Idempotency

Run the same playbook again. Explain that Ansible aims to keep the host in the desired state without making unnecessary changes. Point out `changed=0` if that is the actual result.

## 5:55–6:30 — Repository and conclusion

Show the GitHub repository and explain that the project demonstrates repeatable configuration and local website deployment. State honestly that cloud deployment and a complete CI/CD pipeline are outside this implementation's scope.
