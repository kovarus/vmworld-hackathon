import pyVim
from pyVmomi import vim, vmodl
from pyVim import connect
from vmware_vmfork import fork

import uuid
import ssl

folderName = 'Autoscale'
host = '192.168.1.205'
user = 'administrator@vsphere.local'
pwd = 'VMware1!'


def _createHash(list, attr):
    ###
    Creates a hash with the key being the specified attr
    ###
    hash = {}
    for e in list:
        hash[getattr(e, attr)] = e

    return hash

def _createPerfHash(content):
    # Creates a perf hash based on the key of the performance counter
    return _createHash(content.perfManager.perfCounter)

def Connect(host, user, pwd, context=None):
    if context is None:
        context = ssl._create_unverified_context()

    service_instance = connect.SmartConnect(host=host,
                                            user=user,
                                            pwd=pwd,
                                            sslContext=context)

    return service_instance.RetrieveContent()

def GetVMInFolder(content, folderName):
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

    return vmFolder.childEntity

def GetPerfByKey(content, perfKey):
    # This is dirty, but easy
    perfs = content.perfManager.perfCounter
    for p in perfs:
        if p.key = perfKey:
            return p

def ValidatePerf(content, entity, targetPerfCounter):
    ###
    Checks if a perf counter is valid for the current service instance
    ###
    available = content.perfManager.QueryAvailablePerfMetric(entity=[entity])
    hash = _createHash(available, 'counterId')

    try:
        return hash[targetPerfCounter] is not None
    except KeyError:
        return False


def CloneVM(vm, user, pwd, scriptLocation=None):
  uid = str(uuid.uuid4())[:8]
  childName = vm.name + '-' + uid
  uid = str(uuid.uuid4())[:8]
  if vm is None or vm.guest.toolsVersion == 0:
    raise Exception('VM with valid tools version is required')

  # Check to see if our parent is already quiesced.
  # If it is, there's no reason to enable it for forking again.
  if not vm.runtime.quiescedForkParent:
    if vm.runtime.powerState is not \
       vm.runtime.powerState.poweredOn:
      task = vm.PowerOn()
      fork.WaitForTask(task)
  
    # Poll until we can SSH. 
    timeout = 10 * 60
    tick = 5 
    elapsed = 0
    quiesced = False
    while vm.guest.ipAddress is None:
      if elapsed > timeout:
        raise Exception('Timed out waiting for ip address from guest')
      elapsed += tick
      sleep(tick)
      
      # We could have enabled quiescing on a previous call.
      if vm.runtime.quiescedForkParent:
        quiesced = True
        break
        
    if not quiesced:
      if scriptLocation is None:
          success = fork.LoadGuestCustomizationScript(vm, user, pwd)
      else:
          success = fork.LoadGuestCustomizationScript(vm, user, pwd, script=scriptLocation)
      if not success:
        raise Exception('Error loading customization script onto parent')
      
  assert vm.runtime.quiescedForkParent
  child = fork.CreateChildVm(vm, childName)
  task = child.PowerOn()
  fork.WaitForTask(task)
  
  task = vm.RetrieveForkChildren()
  fork.WaitForTask(task)
  
  result = task.info.result
  children = len(result) > 0
                                                                                                     
  return child
