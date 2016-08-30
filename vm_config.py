#!/usr/bin/env python
import time



configuration_dict = {"Application":
                          [{"name":"Autoscale",
                            "min_nodes": 1,
                            "max_nodes": 4,
                            "cpu_threshold_lower": 15,
                            "cpu_threshold_upper": 25,
                            "polling_interval": 20,
                            "metric_count": 3}]}

# here is my fancy database; a python dictionary!
# We need to update this to a data structure that supports multiple applications
cpu_monitor = [1,1,1,1,1,1,1,1]



def main():

    # min_nodes = "CODEHERE TO GET CURRENT NODES"


    for app in configuration_dict["Application"]:
        current_nodes = "CODETOGETCURRENT"
        if current_nodes < app["min_nodes"]:
            # code to build at least 1 node
            pass
        else:
            pass

    while True:
        try:
            print("Foo")
            # Code to get current CPU utilization

            # code to update cpu_monitor


            for app in configuration_dict["Application"]:
                # Get CPU utilzation

                # Change below to get last 3 intervals
                start = len(cpu_monitor) - 3

                cpu_total = None
                for i in cpu_monitor[start:]:
                    cpu_total += i

                # average last 3 intervals
                cpu_average = cpu_total / 3

                if cpu_average >= app["cpu_threshold_max"]:
                    # run code to scale up
                    pass
                elif cpu_average < app["cpu_threshold_lower"]:
                    # run code to remove all but one nstance
                    pass

            time.sleep(20)

        except KeyboardInterrupt:
            raise




if __name__ == "__main__":
    main()
