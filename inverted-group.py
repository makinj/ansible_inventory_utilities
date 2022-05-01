#!/bin/env python


  
DOCUMENTATION = '''
    name: inverted-group Inventory
    plugin_type: inventory
    author:
      - Joshua Makinen (@joshuamakinen)
    short_description: Inverts the normal Ansible inventory group relationship to list the parents of a host/group instead of listing the group's children.
    description:
        - "n/a"
    version_added: "n/a"
    inventory: inverted-group
    options:
        plugin:
            description: Token that ensures this is a source file for the plugin.
            required: True
            choices: ['inverted-group']
        hosts:
            description:
                - Same as normal Ansible inventories, but now you can specify parents of hosts as well
            required: False
        groups:
            description:
                - Same as normal Ansible inventories, but now you can specify parents of groups as well
            required: False
    requirements:
        - python >= 2.7
'''
EXAMPLES = r'''
# example inverted-group.yml file
---
plugin: inverted-group
hosts:
    example-host:
        parents:
            dev_tmux_installed
groups:
    dev_tmux_installed:
        parents:
            dev
            tmux_installed
'''

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseFileInventoryPlugin

class InventoryModule(BaseFileInventoryPlugin):

    NAME = 'inverted-group'

    def verify_file(self, path):
      super(InventoryModule, self).verify_file(path)
      return path.endswith(('igroup.yml', 'igroup.yaml','inverted-group.yml', 'inverted-group.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)

        hosts_in = self.get_option('hosts')
        if hosts_in:
            for host, hostdata in hosts_in.items():
                for parent in hostdata['parents']:
                    self.inventory.add_group(parent)
                    self.inventory.add_host(host,parent)

        groups_in = self.get_option('groups')
        if groups_in:
            for group, groupdata in groups_in.items():
                self.inventory.add_group(group)
                for parent in groupdata['parents']:
                    self.inventory.add_group(parent)
                    self.inventory.add_child(parent,group)

