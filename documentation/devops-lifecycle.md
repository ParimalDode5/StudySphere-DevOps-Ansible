# StudySphere — DevOps lifecycle and workflow

## 1. Scenario

StudySphere is a sample online learning platform. The demonstration website allows visitors to browse introductory courses, filter courses by category, search the catalogue and open a course overview. It is a static front-end demonstration; it does not provide real user accounts, payments, enrolment or a learning database.

## 2. DevOps lifecycle

| Stage | StudySphere activity | Tools / practices | Evidence or output |
|---|---|---|---|
| Plan | Define the target users, course catalogue and deployment requirements | Requirements notes, task planning | Scope and acceptance criteria |
| Code | Build the HTML, CSS and JavaScript website | HTML5, CSS3, JavaScript | `website/` source files |
| Version control | Track changes and collaborate through commits | Git, GitHub | Versioned repository |
| Build and test | Check the page, browser interactions and Ansible syntax | Browser testing, `ansible-playbook --syntax-check` | Test results and terminal output |
| Release | Keep the reviewed website and deployment files in a repository version | Git tags / GitHub releases (optional for this lab) | Identifiable source revision |
| Deploy | Install Nginx, publish files and apply the web-server configuration | Ansible, Ubuntu, Nginx | Successful playbook output |
| Operate | Serve the website over HTTP | Nginx service | Website at `http://localhost` |
| Monitor | Check service state, HTTP response and server logs | `systemctl`, Ansible `uri`, Nginx logs | Service and HTTP checks |
| Feedback | Review issues and update the source before redeployment | GitHub issues / commits | Follow-up changes |

## 3. Workflow

1. A developer updates the StudySphere source files.
2. Git records the change and GitHub stores the repository.
3. The website is checked in a browser and the Ansible playbook is syntax-checked.
4. Ansible connects to the local Ubuntu WSL host using the local connection plugin.
5. The playbook installs Nginx, copies the website, installs the Nginx site configuration and starts the service.
6. Ansible validates the Nginx configuration and requests the local website, expecting HTTP 200.
7. The operator checks the browser, service state and logs. Any change is committed and redeployed.

## 4. Architecture

```text
Developer
   |
   v
StudySphere source (HTML / CSS / JavaScript)
   |
   v
Git repository  ----->  GitHub repository
   |
   v
Ansible control node (Ubuntu on WSL2)
   |  inventory.ini: localhost in [webservers]
   |  deploy.yml
   |  Nginx configuration template
   v
Local managed host (same Ubuntu WSL2 instance)
   |
   +---- Nginx service (port 80)
   |
   +---- /var/www/studysphere (website files)
   |
   v
Browser: http://localhost
   |
   v
Checks: systemctl status, curl / Ansible uri, Nginx logs
```

## 5. Automation scope and limitations

The implemented automation covers package installation, website-file deployment, Nginx virtual-host configuration, service enablement and an HTTP response check. The inventory targets one local WSL Ubuntu instance. It is a learning-lab implementation, not a multi-node or production deployment.

A full CI/CD pipeline, cloud hosting, TLS certificates, authentication, a database and centralized monitoring are not implemented in this assignment. They can be described as possible future extensions, but must not be presented as completed work.
