# ansible_inventory_utilities
Combine and invert group relationships to simplify complex and repetitive Ansible inventories

## Invert groups

Inverts the normal group relationship where you can list the parents of a host/group instead of you list all of the children of a group.

Example:

```yaml
plugin: inverted-group
hosts:
  example-host:
    parents:
    - devops_tools_installed
groups:
  devops_tools_installed:
    parents:
    - dev_tools_installed
    - ops_tools_installed
```
Having the above in a file ending in `igroups.yml`, `igroups.yaml`,`inverted-groups.yml`, or `inverted-groups.yaml` in your inventory
Results in:
```
@all:
  |--@dev_tools_installed:
  |  |--@devops_tools_installed:
  |  |  |--example-host
  |--@ops_tools_installed:
  |  |--@devops_tools_installed:
  |  |  |--example-host
  |--@ungrouped:
```

## Combine groups

Takes a number of dimensions of groups and combines their names while retaining the inner structure so you can have the same pattern of groupings replicated and target specific group combinations. input groups can have children and parents (from inverted groups) and 

Example:
```yaml
plugin: combined-groups
dimensions:
- dev:
  prod:
- hypervisor:
  guest:
    children:
      headless_guest:
      gui_guest:
```

Having the above in a file ending in `cgroups.yml`, `cgroups.yaml`,`combined-groups.yml`, or `combined-groups.yaml` in your inventory
Results in:

```
@all:
  |--@dev:
  |  |--@dev_guest:
  |  |  |--@dev_gui_guest:
  |  |  |--@dev_headless_guest:
  |  |--@dev_gui_guest:
  |  |--@dev_headless_guest:
  |  |--@dev_hypervisor:
  |--@guest:
  |  |--@dev_guest:
  |  |  |--@dev_gui_guest:
  |  |  |--@dev_headless_guest:
  |  |--@gui_guest:
  |  |  |--@dev_gui_guest:
  |  |  |--@prod_gui_guest:
  |  |--@headless_guest:
  |  |  |--@dev_headless_guest:
  |  |  |--@prod_headless_guest:
  |  |--@prod_guest:
  |  |  |--@prod_gui_guest:
  |  |  |--@prod_headless_guest:
  |--@hypervisor:
  |  |--@dev_hypervisor:
  |  |--@prod_hypervisor:
  |--@prod:
  |  |--@prod_guest:
  |  |  |--@prod_gui_guest:
  |  |  |--@prod_headless_guest:
  |  |--@prod_gui_guest:
  |  |--@prod_headless_guest:
  |  |--@prod_hypervisor:
  |--@ungrouped:
```

