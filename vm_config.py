#!/usr/bin/env python
import time



configuration_dict = {"Application":
                          [{"name":"Autoscale",
                            "min_nodes": 1,
                            "max_nodes": 4,
                            "cpu_threshold_lower": 15,
                            "cpu_threshold_upper": 25,
                            "polling_interval": 20,
                            "metric_count": 3,
                            "node_list": []}]}

# here is my fancy database; a python dictionary!
# We need to update this to a data structure that supports multiple applications
# cpu_monitor = [1,1,1,1,1,1,1,1]

import yaml
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

def generate_playbook(node_list):

    backend_servers = []

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

def main():

    # min_nodes = "CODEHERE TO GET CURRENT NODES"


    for app in configuration_dict["Application"]:
        current_nodes = "CODETOGETCURRENT"
        if current_nodes < app["min_nodes"]:
            # code to build at least 1 node
            # update config_dict node_list to include base node
            pass
        else:
            pass

    while True:
        cpu_monitor = []

        try:
            for app in configuration_dict["Application"]:

                # generate node list from list of virtual machines



                # Get CPU utilzation for all instances

                # Change below to get last 3 intervals
                start = len(cpu_monitor) - 3

                cpu_total = None
                for i in cpu_monitor[start:]:
                    cpu_total += i

                # average last 3 intervals
                cpu_average = cpu_total / 3

                if cpu_average >= app["cpu_threshold_max"]:
                    # run code to scale up
                    # Invoke a process to kick off a run with our yaml playbook
                    pass
                elif cpu_average < app["cpu_threshold_lower"]:
                    # run code to remove all but one nstance
                    pass

            time.sleep(20)

        except KeyboardInterrupt:
            raise


if __name__ == "__main__":
    main()
