#!/usr/bin/env python

#

configuration_dict = {"Application":
                          [{"name":"Autoscale",
                            "min_nodes": 1,
                            "max_nodes": 4,
                            "cpu_threshold_lower": 15,
                            "cpu_threshold_upper": 25,
                            "polling_interval": 20,
                            "metric_count": 3}]}

