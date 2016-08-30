import pyVim
from pyVmomi import vim, vmodl
from pyVim import connect

import ssl

folderName = 'Autoscale'
host = '192.168.1.205'
user = 'administrator@vsphere.local'
pwd = 'VMware1!'


def Connect(host, user, pwd, context=None):
    if context is None:
        context = ssl._create_unverified_context()

    service_instance = connect.SmartConnect(host=host,
                                            user=user,
                                            pwd=pwd,
                                            sslContext=context)

    return service_instance.RetrieveContent()

def GetAllVMInFolder(content, folderName):
    # Get folders
    folders = content.rootFolder.childEntity[0].vmFolder.childEntity

    vmFolder = None

    for f in folders:
        if isinstance(f, vim.Folder):
            if f.name == folderName:
                vmFolder = f
                break

    if vmFolder is None:
        raise Exception("Unable to locate folder")

    return f.childEntity
