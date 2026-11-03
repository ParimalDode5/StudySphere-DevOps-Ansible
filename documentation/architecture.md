# StudySphere — architecture and automation notes

## Application architecture

StudySphere is a static three-file front end:

- `website/index.html` — semantic page structure and course content.
- `website/style.css` — responsive layout and visual styling.
- `website/script.js` — course filtering, search and course-overview dialog.

No application server or database is required for this demonstration. Nginx serves the static files to the browser.

## Deployment architecture

- Control node: Ubuntu running in WSL2.
- Managed host: the same Ubuntu WSL2 instance, addressed as `localhost` with Ansible's `local` connection.
- Configuration management: Ansible inventory and playbook.
- Web server: Nginx listening on TCP port 80.
- Deployment directory: `/var/www/studysphere`.
- Nginx site configuration: `/etc/nginx/sites-available/studysphere`, enabled through `/etc/nginx/sites-enabled/studysphere`.

## Why Ansible?

Ansible describes the desired system state in YAML and uses modules such as `apt`, `file`, `copy`, `template`, `service` and `uri` to apply and verify configuration. These modules are designed to be idempotent: running the playbook again should not make changes when the host already matches the declared state.

## Monitoring and verification

The playbook validates the Nginx configuration with `nginx -t`, checks the service state through the service module and performs an HTTP GET request to `http://127.0.0.1/` expecting status 200. Operational checks can also be run manually:

```bash
sudo systemctl status nginx
curl -I http://localhost
sudo tail -n 20 /var/log/nginx/studysphere_access.log
sudo tail -n 20 /var/log/nginx/studysphere_error.log
```
