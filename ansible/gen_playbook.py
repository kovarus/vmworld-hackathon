import yaml
import json
#
# ---
# - hosts: lb
#   remote_user: root
#
#   vars:
#     haproxy_backend_servers:
#       - name: app1
#         address: 127.0.0.1:8080
#       - name: app2
#         address: 127.0.0.2:8080
#   roles:
#     - ansible-role-haproxy

def main():
    backend_servers = [{
                        "name": "app1",
                        "address": "127.0.0.1:8080"
                        },
                        {
                            "name": "app2",
                            "address": "127.0.0.2:8080"
                        },
                        {
                            "name": "app3",
                            "address": "127.0.0.3:8080"
                        }]

    new_server = {"name": "foo1", "address": "100.1.1.1:8080"}

    backend_servers.append(new_server)



    lb_configuration = [
                        {
                            "remote_user": "root",
                            "hosts": "lb",
                            "vars": {
                                "haproxy_backend_servers":
                                  backend_servers

                            },
                            "roles": [
                                "ansible-role-haproxy"
                            ]
                        }
                    ]

    print(yaml.dump(lb_configuration))
    # print "*" * 80
    # print(json.dumps(lb_configuration, indent=4))

if __name__ == "__main__":
    main()