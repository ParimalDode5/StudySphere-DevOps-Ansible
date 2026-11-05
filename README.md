# StudySphere — DevOps Case Study & Ansible Automation

StudySphere is a sample online learning website used to demonstrate a basic DevOps workflow and configuration management with Ansible on Ubuntu through WSL2.

## Project contents

```text
StudySphere-DevOps-Ansible/
├── website/                 # Static website source
├── ansible/
│   ├── inventory.ini        # Local WSL host inventory
│   ├── deploy.yml           # Nginx installation and deployment playbook
│   └── templates/
│       └── studysphere.conf.j2
├── documentation/
│   ├── architecture.md
│   └── devops-lifecycle.md
├── screenshots/             # Add your own execution screenshots here
└── README.md
```

## Requirements

- Windows 11 with WSL2 enabled
- An Ubuntu WSL distribution
- Ansible installed inside Ubuntu
- Internet access while installing Ansible and Nginx

## 1. Install or open Ubuntu in WSL2

In Windows PowerShell, check installed distributions:

```powershell
wsl --list --verbose
```

If Ubuntu is not installed, install Ubuntu 24.04 LTS:

```powershell
wsl --install Ubuntu-24.04
```

Complete the first-launch setup by creating a Linux username and password. Then open Ubuntu and confirm that it is running as WSL version 2:

```powershell
wsl --set-version Ubuntu-24.04 2
wsl --list --verbose
```

## 2. Prepare Ubuntu

Run inside the Ubuntu terminal:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y software-properties-common git curl
```

Install Ansible from the Ansible project PPA:

```bash
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible
ansible --version
```

## 3. Get the project files

Clone your GitHub repository after you create it, or copy this project folder into your Ubuntu home directory. Keep the project in the Linux filesystem (for example, `~/StudySphere-DevOps-Ansible`) rather than under `/mnt/c` for better Linux filesystem performance.

If you downloaded the ZIP in Windows, it is commonly available under `/mnt/c/Users/<WindowsUser>/Downloads/`. Extract it, then copy the project folder into your Ubuntu home directory.

## 4. Enable systemd in WSL if needed

Check whether systemd is PID 1:

```bash
ps -p 1 -o comm=
```

If the output is `systemd`, continue to the next step. If not, enable it for this Ubuntu distribution:

```bash
sudo nano /etc/wsl.conf
```

Add:

```ini
[boot]
systemd=true
```

Save the file, then run this in Windows PowerShell:

```powershell
wsl --shutdown
```

Reopen Ubuntu and verify again with `ps -p 1 -o comm=`. WSL systemd support is documented by Microsoft; if your existing configuration already uses systemd, do not change it.

## 5. Validate and run the playbook

From the project root in Ubuntu:

```bash
cd ~/StudySphere-DevOps-Ansible
ansible -i ansible/inventory.ini webservers -m ping
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --syntax-check
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-become-pass
```

Enter the Linux account password when Ansible asks for the become password. This is the password used with `sudo` in Ubuntu, not your Windows password.

## 6. Verify the deployment

Open `http://localhost` in a Windows browser. You can also run:

```bash
sudo systemctl status nginx --no-pager
curl -I http://localhost
curl http://localhost | head
```

Expected HTTP result: `HTTP/1.1 200 OK` (or an equivalent HTTP 200 response).

## 7. Demonstrate idempotency

Run the same playbook one more time:

```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-become-pass
```

When there are no source or configuration changes, the second run should ideally show `changed=0` and `failed=0`. If it reports changes, inspect the task that changed and explain the reason rather than editing the screenshot.

## 8. Useful troubleshooting

- `UNREACHABLE`: confirm the inventory uses `ansible_connection=local` and that you are running the command inside the Ubuntu project directory.
- `Missing sudo password`: include `--ask-become-pass` and enter your Ubuntu Linux password.
- `System has not been booted with systemd`: complete the optional systemd setup above, then run `wsl --shutdown` from PowerShell and reopen Ubuntu.
- Port 80 already in use: inspect with `sudo ss -ltnp | grep ':80'` and stop the conflicting service before rerunning the playbook.
- HTTP response is not 200: inspect `sudo nginx -t`, `sudo systemctl status nginx` and the StudySphere Nginx error log.

## Evidence to capture for the assignment

1. `ansible --version`
2. Ansible ping result for `webservers`
3. Playbook syntax-check result
4. First successful playbook run and recap
5. `sudo systemctl status nginx --no-pager`
6. StudySphere page opened at `http://localhost`
7. Second playbook run showing idempotency (`changed=0`, when applicable)
8. GitHub repository page with project files

Save only screenshots from your own actual execution in `screenshots/`.

## Scope note

This implementation deploys a static website to one local WSL2 Ubuntu host. It demonstrates configuration management and a local web-server deployment. It does not implement a production CI/CD pipeline, cloud infrastructure, user authentication, real course enrolment or a database.


## Activity 3: Jenkins CI/CD and Terraform

This project now includes an automated Jenkins CI/CD pipeline
with Checkout, Build, Test and Deploy stages.

Terraform provisions the Docker infrastructure required
to run StudySphere using Nginx.

Application deployment:
- Jenkins and Nginx: http://localhost
- Terraform and Docker: http://localhost:8082