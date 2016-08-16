from __future__ import print_function

# import argparse
import atexit
import getpass
import datetime

import requests.packages.urllib3 as urllib3
import ssl

from pyVim import connect
from pyVmomi import vmodl, vim
#
# def getargs():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('positional',
#                         required=True,
#                         action='store',
#                         help='This is an example of a positional argument')
#     parser.add_argument('-s', '--stuff',
#                         required=True,
#                         action='store',
#                         help='Placeholder for help')
#     parser.add_argument('-t', '--test',
#                         required=True,
#                         action='store',
#                         help='more sample help',
#                         dest='test_var')
#     args = parser.parse_args()
#     return args


def GetProperties(content, viewType, props, specType):
    # Build a view and get basic properties for all Virtual Machines
    objView = content.viewManager.CreateContainerView(content.rootFolder, viewType, True)
    tSpec = vim.PropertyCollector.TraversalSpec(name='tSpecName', path='view', skip=False, type=vim.view.ContainerView)
    pSpec = vim.PropertyCollector.PropertySpec(all=False, pathSet=props, type=specType)
    oSpec = vim.PropertyCollector.ObjectSpec(obj=objView, selectSet=[tSpec], skip=False)
    pfSpec = vim.PropertyCollector.FilterSpec(objectSet=[oSpec], propSet=[pSpec], reportMissingObjectsInResults=False)
    retOptions = vim.PropertyCollector.RetrieveOptions()
    totalProps = []
    retProps = content.propertyCollector.RetrievePropertiesEx(specSet=[pfSpec], options=retOptions)
    totalProps += retProps.objects
    while retProps.token:
        retProps = content.propertyCollector.ContinueRetrievePropertiesEx(token=retProps.token)
        totalProps += retProps.objects
    objView.Destroy()
    # Turn the output in retProps into a usable dictionary of values
    gpOutput = []
    for eachProp in totalProps:
        propDic = {}
        for prop in eachProp.propSet:
            propDic[prop.name] = prop.val
        propDic['moref'] = eachProp.obj
        gpOutput.append(propDic)
    return gpOutput

def main():
    # args = get_args()


    host = "hq-l-lvc2.kpsc.lan"
    user = "svc.vmware@kpsc.lan"
    password = "!Passw0rd"

    port=443

    urllib3.disable_warnings()
    service_instance = None
    context = None
    if hasattr(ssl, 'SSLContext'):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE

    try:
        service_instance = connect.SmartConnect(host=host,
                                                port=port,
                                                user=user,
                                                pwd=password,
                                                sslContext=context)
        if not service_instance:
            print("Could not connect to the specified host using specified "
                  "username and password")


        atexit.register(connect.Disconnect, service_instance)

        content = service_instance.RetrieveContent()

        search_index = content.searchIndex

        virtual_machine = "hq-l-ccm1.kpsc.lan"

        # quick/dirty way to find an ESXi host


        vchtime = service_instance.CurrentTime()

        vm = search_index.FindByDnsName(dnsName=virtual_machine, vmSearch=True)

        # Get all the performance counters
        perf_dict = {}
        performance_counters = content.perfManager.perfCounter
        for counter in performance_counters:
            counter_full = "{}.{}.{}".format(counter.groupInfo.key, counter.nameInfo.key, counter.rollupType)
            perf_dict[counter_full] = counter.key


        retProps = GetProperties(content, [vim.VirtualMachine], ['name', 'runtime.powerState'], vim.VirtualMachine)

        # Find VM supplied as arg and use Managed Object Reference (moref) for the PrintVmInfo
        for vm in retProps:
            if (vm['name'] in vmnames) and (vm['runtime.powerState'] == "poweredOn"):
                PrintVmInfo(vm['moref'], content, vchtime, 15, perf_dict)
            elif vm['name'] in vmnames:
                print('ERROR: Problem connecting to Virtual Machine.  {} is likely powered off or suspended'.format(
                    vm['name']))

        perfManager = content.perfManager
        metricId = vim.PerformanceManager.MetricId(counterId=4, instance="*")
        startTime = datetime.datetime.now() - datetime.timedelta(hours=1)
        endTime = datetime.datetime.now()

        query = vim.PerformanceManager.QuerySpec(maxSample=1,
                                                 entity=host,
                                                 metricId=[metricId],
                                                 startTime=startTime,
                                                 endTime=endTime)

        print(perfManager.QueryPerf(querySpec=[query]))

    except vmodl.MethodFault as e:
        print("Caught vmodl fault : " + e.msg)
        return -1
    except Exception as e:
        print("Caught exception : " + str(e))
        return -1

    return 0

if __name__ == '__main__':
    main()
