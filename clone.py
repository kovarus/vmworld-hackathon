# Code shamelessly stolen from https://github.com/vmware/pyvmomi/blob/master/sample/poweronvm.py

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from vmware_vmfork import fork

import sys
import ssl
import atexit


user = 'pyvmomi@vsphere.local'
password = 'VMware1!'
host = '10.10.10.10'

def Connect():
	# Setup SSL context. I use self-signed certs, so unverified it is
	context = ssl._create_unverified_context()

	try:
		si = SmartConnect(host=host,
						  user=user,
						  pwd=password,
						  sslContext=context)
	except IOError:
		pass
	if not si:
		print("Cannot connect. Check host, user, pass.")
		sys.exit()

	atexit.register(Disconnect, si)

	return si

def WaitForTasks(tasks, si):
   """
   Given the service instance si and tasks, it returns after all the
   tasks are complete
   """

   pc = si.content.propertyCollector

   taskList = [str(task) for task in tasks]

   # Create filter
   objSpecs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                                                            for task in tasks]
   propSpec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                         pathSet=[], all=True)
   filterSpec = vmodl.query.PropertyCollector.FilterSpec()
   filterSpec.objectSet = objSpecs
   filterSpec.propSet = [propSpec]
   filter = pc.CreateFilter(filterSpec, True)

   try:
      version, state = None, None

      # Loop looking for updates till the state moves to a completed state.
      while len(taskList):
         update = pc.WaitForUpdates(version)
         for filterSet in update.filterSet:
            for objSet in filterSet.objectSet:
               task = objSet.obj
               for change in objSet.changeSet:
                  if change.name == 'info':
                     state = change.val.state
                  elif change.name == 'info.state':
                     state = change.val
                  else:
                     continue

                  if not str(task) in taskList:
                     continue

                  if state == vim.TaskInfo.State.success:
                     # Remove task from taskList
                     taskList.remove(str(task))
                  elif state == vim.TaskInfo.State.error:
                     raise task.info.error
         # Move to next version
         version = update.version
   finally:
      if filter:
         filter.Destroy()


def GetVM(si, vmname):
	content = si.content

	objView = content.viewManager.CreateContainerView(content.rootFolder,
													  [vim.VirtualMachine],
													  True)
	vmList = objView.view
	objView.Destroy()

	for vm in vmList:
		if vm.name == vmname:
			return vm

def CloneVM(vm):
	if isinstance(vm, vim.VirtualMachine) == False:
		# Argument 'vm' is not a virtual machine.
		raise Exception("Argument 'vm' is not an instance of vim.VirtualMachine'", vm)
	
	if vm.runtime.powerState != 'poweredOn':
		raise Exception("VM not powered on", vm)

	child = fork.CreateChildVm(vm, 'Photon-Child', persistent=False)
	if not child:
		raise Exception("Error cloning VM", child)

	return child

if __name__ == "__main__":
	si = Connect()
	vm = GetVM(si, 'Photon')
	print("VM found: " + vm.name)
	print("Attempting to tag as clonable...")
	task = vm.EnableForkParent()
	WaitForTasks([task], si)
	print("VM forking enabled")
	print("Attempting to clone vm...")
	child = CloneVM(vm)
	print("Child cloned: " + child.name)
