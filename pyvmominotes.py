
# forgot to just bring in 'connect'
>>> import pyVim


# Figured who cares so I'm going to just use the pyVim namespace:

>>> service_instance = pyVim.connect.SmartConnect(host=host, port=port, user=user, pwd=password, sslContext=context)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute 'connect'
'module' object has no attribute 'connect'

# Boggle! Lets just import connect!

>>> from pyVim import connect

>>> service_instance = connect.SmartConnect(host=host, port=port, user=user, pwd=password, sslContext=context)

# This worked? 

# So when I do this:

>>> content = service_instance.RetrieveContent()

>>> dir(content) 
['Array', '_GetPropertyInfo', '_GetPropertyList', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_propInfo', '_propList', '_version', '_wsdlName', 'about', 'accountManager', 'alarmManager', 'authorizationManager', 'certificateManager', 'clusterProfileManager', 'complianceManager', 'customFieldsManager', 'customizationSpecManager', 'datastoreNamespaceManager', 'diagnosticManager', 'dvSwitchManager', 'dynamicProperty', 'dynamicType', 'eventManager', 'extensionManager', 'fileManager', 'guestOperationsManager', 'hostProfileManager', 'ioFilterManager', 'ipPoolManager', 'licenseManager', 'localizationManager', 'overheadMemoryManager', 'ovfManager', 'perfManager', 'propertyCollector', 'rootFolder', 'scheduledTaskManager', 'searchIndex', 'serviceManager', 'sessionManager', 'setting', 'snmpSystem', 'storageResourceManager', 'taskManager', 'userDirectory', 'viewManager', 'virtualDiskManager', 'virtualizationManager', 'vmCompatibilityChecker', 'vmProvisioningChecker']

>>> search_index = content.searchIndex
>>> print search_index
'vim.SearchIndex:SearchIndex'

# What is this actually doing?


# Couldn't find by DNS name so tried to find by IP instead

>>> vm = search_index.FindByIp(ip="10.1.2.135", vmSearch=True)

>>> print vm
'vim.VirtualMachine:vm-2188'

>>> perf_dict = {}

>>> performance_counters = content.perfManager.perfCounter 

# got a list of all performance counters

# this will put counters in a dictionary:
>>> for counter in performance_counters:
...     counter_full = "{}.{}.{}".format(counter.groupInfo.key, counter.nameInfo.key, counter.rollupType)
...     perf_dict[counter_full] = counter.key

# In this case you'd see this:
  "cpu.usage.maximum": 4

  # Which is derived from this info (via content.perfManager.perfCounter)

     (vim.PerformanceManager.CounterInfo) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      key = 4,																# Actual value here in the dictionary
      nameInfo = (vim.ElementDescription) {
         dynamicType = <unset>,
         dynamicProperty = (vmodl.DynamicProperty) [],
         label = 'Usage',
         summary = 'CPU usage as a percentage during the interval',
         key = 'usage'														# Here's the middle key (counter.nameInfo.key)
      },
      groupInfo = (vim.ElementDescription) {
         dynamicType = <unset>,
         dynamicProperty = (vmodl.DynamicProperty) [],
         label = 'CPU',
         summary = 'CPU',
         key = 'cpu'														# Here's the first key (groupInfo.key)
      },
      unitInfo = (vim.ElementDescription) {
         dynamicType = <unset>,
         dynamicProperty = (vmodl.DynamicProperty) [],
         label = '%',
         summary = 'Percentage',
         key = 'percent'
      },
      rollupType = 'maximum',												# Here's the last key (counter.rollupType)
      statsType = 'rate',
      level = 4,
      perDeviceLevel = 4,
      associatedCounterId = (int) []
   }
