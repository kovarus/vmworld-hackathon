# from https://github.com/vmware/pyvmomi/issues/307

import ssl
import time

import requests
from com.vmware.cis.tagging_client import (
    Category, Tag, TagAssociation, CategoryModel)
from com.vmware.cis_client import Session
from com.vmware.vapi.std_client import DynamicID
from pyVim import connect
from pyVmomi import vim
from vmware.vapi.lib.connect import get_requests_connector
from vmware.vapi.security.session import create_session_security_context
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory

server = '<server_ip>'
url = 'https://{}/api'.format(server)
username = '<username>'
password = '<password>'
category_name = 'sample category'
category_desc = 'sample category description'
tag_name = 'sample tag'
tag_desc = 'sample tag description'
cluster_name = 'cluster'
vm_name = 'vm1'


def create_tag_category(name, description, cardinality):
    """create a category. User who invokes this needs create category privilege."""
    create_spec = category_svc.CreateSpec()
    create_spec.name = name
    create_spec.description = description
    create_spec.cardinality = cardinality
    associableTypes = set()
    create_spec.associable_types = associableTypes
    return category_svc.create(create_spec)


def delete_tag_category(category_id):
    """Deletes an existing tag category; User who invokes this API needs
    delete privilege on the tag category.
    """
    category_svc.delete(category_id)


def create_tag(name, description, category_id):
    """Creates a Tag"""
    create_spec = tag_svc.CreateSpec()
    create_spec.name = name
    create_spec.description = description
    create_spec.category_id = category_id
    return tag_svc.create(create_spec)


def update_tag(tag_id, description):
    """Update the description of an existing tag.
    User who invokes this API needs edit privilege on the tag.
    """
    update_spec = tag_svc.UpdateSpec()
    update_spec.setDescription = description
    tag_svc.update(tag_id, update_spec)


def delete_tag(tag_id):
    """Delete an existing tag.
    User who invokes this API needs delete privilege on the tag."""
    tag_svc.delete(tag_id)


def get_cluster_id(name):
    """Find cluster id by given name using pyVmomi."""
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()

    si = connect.Connect(host=server, user=username, pwd=password,
                         sslContext=context)
    content = si.content
    container = content.rootFolder
    viewType = [vim.ClusterComputeResource]
    recursive = True
    clusterView = content.viewManager.CreateContainerView(container,
                                                          viewType,
                                                          recursive)
    clusters = clusterView.view
    for cluster in clusters:
        if cluster.name == name:
            return cluster._GetMoId()
    raise Exception('Cluster with name {} could not be found'.format(name))


def get_vm_id(name):
    """Find vm id by given name using pyVmomi."""
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()

    si = connect.Connect(host=server, user=username, pwd=password,
                         sslContext=context)
    content = si.content
    container = content.rootFolder
    viewType = [vim.VirtualMachine]
    recursive = True
    vmView = content.viewManager.CreateContainerView(container,
                                                     viewType,
                                                     recursive)
    vms = vmView.view
    for vm in vms:
        if vm.name == name:
            return vm._GetMoId()
    raise Exception('VM with name {} could not be found'.format(name))


"""
Create an authenticated stub configuration object that can be used to issue
requests against vCenter.
Returns a stub_config that stores the session identifier that can be used
to issue authenticated requests against vCenter.
"""
session = requests.Session()
session.verify = False
connector = get_requests_connector(session=session, url=url)
stub_config = StubConfigurationFactory.new_std_configuration(connector)

# Pass user credentials (user/password) in the security context to authenticate.
# login to vAPI endpoint
user_password_security_context = create_user_password_security_context(username,
                                                                       password)
stub_config.connector.set_security_context(user_password_security_context)

# Create the stub for the session service and login by creating a session.
session_svc = Session(stub_config)
session_id = session_svc.create()

# Successful authentication.  Store the session identifier in the security
# context of the stub and use that for all subsequent remote requests
session_security_context = create_session_security_context(session_id)
stub_config.connector.set_security_context(session_security_context)

# Create Tagging services
tag_svc = Tag(stub_config)
category_svc = Category(stub_config)
tag_association = TagAssociation(stub_config)

print('List all the existing categories user has access to...')
categories = category_svc.list()
if len(categories) > 0:
    for category in categories:
        print('Found Category: {0}'.format(category))
else:
    print('No Tag Category Found...')

print('List all the existing tags user has access to...')
tags = tag_svc.list()
if len(tags) > 0:
    for tag in tags:
        print('Found Tag: {0}'.format(tag))
else:
    print('No Tag Found...')

print('creating a new tag category...')
category_id = create_tag_category(category_name,
                                  category_desc,
                                  CategoryModel.Cardinality.MULTIPLE)
assert category_id is not None
print('Tag category created; Id: {0}'.format(category_id))

print("creating a new Tag...")
tag_id = create_tag(tag_name, tag_desc, category_id)
assert tag_id is not None
print('Tag created; Id: {0}'.format(tag_id))

print('updating the tag...')
date_time = time.strftime('%d/%m/%Y %H:%M:%S')
update_tag(tag_id, 'Server Tag updated at ' + date_time)
print('Tag updated; Id: {0}'.format(tag_id))

print('finding the cluster {0}'.format(cluster_name))
cluster_moid = get_cluster_id(cluster_name)
assert cluster_moid is not None
print('Found cluster:{0} mo_id:{1}'.format('vAPISDKCluster', cluster_moid))

print('finding the vm {0}'.format(vm_name))
vm_moid = get_vm_id(vm_name)
assert vm_moid is not None
print('Found vm:{0} mo_id:{1}'.format('vAPISDKVM', vm_moid))

print('Tagging the cluster {0}...'.format(cluster_name))
dynamic_id = DynamicID(type='ClusterComputeResource', id=cluster_moid)
tag_association.attach(tag_id=tag_id, object_id=dynamic_id)
for tag_id in tag_association.list_attached_tags(dynamic_id):
    if tag_id == tag_id:
        tag_attached = True
        break

assert tag_attached
print('Tagged cluster: {0}'.format(cluster_moid))

print('Tagging the vm {0}...'.format(vm_moid))
dynamic_id = DynamicID(type='VirtualMachine', id=vm_moid)
tag_association.attach(tag_id=tag_id, object_id=dynamic_id)
for tag_id in tag_association.list_attached_tags(dynamic_id):
    if tag_id == tag_id:
        tag_attached = True
        break

assert tag_attached
print('Tagged vm: {0}'.format(vm_moid))
