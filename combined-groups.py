#!/bin/env python


  
DOCUMENTATION = '''
    name: combined-groups Inventory
    plugin_type: inventory
    author:
      - Joshua Makinen (@joshuamakinen)
    short_description: TKTK
    description:
        - TKTK
    version_added: "n/a"
    inventory: combined-groups
    options:
        plugin:
            description: Token that ensures this is a source file for the plugin.
            required: True
            choices: ['combined-groups']
        dimensions:
            description:
                - TKTK
            required: True
    requirements:
        - python >= 2.7
'''
EXAMPLES = r'''
# example combined-groups.yml file
---
plugin: combined-groups
dimensions:
- [dev,prod]
- [PCLT02,Ulfgar]
- [vagrant_hypervisors, vagrant_guests, vagrant_virtualbox_guests]
'''

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseFileInventoryPlugin
from itertools import combinations

def combine_lists(dimensions):
    results=[]
    if len(dimensions)>=1:
        for dimval,dimchild in dimensions[0].items():
            results.append([{dimval:dimchild}])
    if len(dimensions)>1:
        recurse_results=combine_lists(dimensions[1:])
        results+=recurse_results
        for dimval,dimchild in dimensions[0].items():
            for recurse_result in recurse_results:
                results.append([{dimval:dimchild}]+recurse_result)
    return results


class InventoryModule(BaseFileInventoryPlugin):

    NAME = 'combined-groups'

    def verify_file(self, path):
      super(InventoryModule, self).verify_file(path)
      return path.endswith(('cgroups.yml', 'cgroups.yaml','combined-groups.yml', 'combined-groups.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)
        results = self.fetch()
        self.populate(results)


    def fetch(self):
        results={}

        dimensions_in = self.get_option('dimensions')
        results=combine_lists(dimensions_in)
        return results
    
    def traverse_elements(self, elements, callback,parent='',child=''):
        if isinstance(elements,dict):
            for child_name, child_data in elements.items():
                callback(child_name, child_data, parent,child)
                if child_data and 'children' in child_data:
                    self.traverse_elements(child_data['children'],callback,child_name)
                if child_data and 'parents' in child_data:
                    self.traverse_elements(child_data['parents'],callback,child=child_name)
        elif isinstance(elements[0],str):
            callback(elements, {})

    def add_combination_groups(self, combo, prefix=[]):
        #print(repr(combo),prefix)
        if len(combo)>=1:
            cur_elem=combo[0]
            def add_element_groups(name,data,parent='',child=''):
                #print(parent,name,repr(data))
                full_group=prefix+[name]
                if len(combo)>1:
                    self.add_combination_groups(combo[1:],full_group)
                else:
                    #print(repr(prefix),repr(name),repr(full_group))
                    full_group_name='_'.join(full_group)
                    self.inventory.add_group(full_group_name)
                    if parent:
                        parent_name='_'.join(prefix+[parent])
                        self.inventory.add_child(parent_name, full_group_name)
                    if child:
                        child_name='_'.join(prefix+[child])
                        self.inventory.add_child(full_group_name, child_name)
                    if len(full_group)>1:
                        for n in range(1,len(full_group)):
                            for parent in combinations(full_group, n):
                                parent_name='_'.join(parent)

                                self.inventory.add_group(parent_name)
                                self.inventory.add_child(parent_name,full_group_name)

            self.traverse_elements(cur_elem, add_element_groups)


    def populate(self, results):
        for combo in results:
            self.add_combination_groups(combo)

