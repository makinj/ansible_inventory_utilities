# ansible_inventory_utilities
Combine and invert group relationships to simplify complex and repetitive Ansible inventories

## Invert groups

Inverts the normal group relationship where you can list the parents of a host/group instead of you list all of the children of a group.

Example:

```
plugin: inverted-group
hosts:
  myPC:
    parents:
      - install_dev_tools
      - install_ops_tools
```
Having the above in a file ending in `igroups.yml`, `igroups.yaml`,`inverted-groups.yml`, or `inverted-groups.yaml` in your inventory
Results in:
```
@all:
  |--@install_dev_tools:
  |  |--myPC
  |--@install_ops_tools:
  |  |--myPC
  |--@ungrouped:
```

## Combine groups

Takes a number of dimensions of groups and combines their names while retaining the inner structure so you can have the same pattern of groupings replicated and target specific group combinations. input groups can have children and parents (from inverted groups) and 

Example:
```yaml
plugin: combined-groups
dimensions:
- myPC:
- dev:
  prod:
- hypervisor:
  guest:
```

Having the above in a file ending in `cgroups.yml`, `cgroups.yaml`,`combined-groups.yml`, or `combined-groups.yaml` in your inventory
Results in:

```
@all:
  |--@dev:
  |  |--@dev_guest:
  |  |  |--@myPC_dev_guest:
  |  |--@dev_hypervisor:
  |  |  |--@myPC_dev_hypervisor:
  |  |--@myPC_dev:
  |  |  |--@myPC_dev_guest:
  |  |  |--@myPC_dev_hypervisor:
  |  |--@myPC_dev_guest:
  |  |--@myPC_dev_hypervisor:
  |--@guest:
  |  |--@dev_guest:
  |  |  |--@myPC_dev_guest:
  |  |--@myPC_dev_guest:
  |  |--@myPC_guest:
  |  |  |--@myPC_dev_guest:
  |  |  |--@myPC_prod_guest:
  |  |--@myPC_prod_guest:
  |  |--@prod_guest:
  |  |  |--@myPC_prod_guest:
  |--@hypervisor:
  |  |--@dev_hypervisor:
  |  |  |--@myPC_dev_hypervisor:
  |  |--@myPC_dev_hypervisor:
  |  |--@myPC_hypervisor:
  |  |  |--@myPC_dev_hypervisor:
  |  |  |--@myPC_prod_hypervisor:
  |  |--@myPC_prod_hypervisor:
  |  |--@prod_hypervisor:
  |  |  |--@myPC_prod_hypervisor:
  |--@myPC:
  |  |--@myPC_dev:
  |  |  |--@myPC_dev_guest:
  |  |  |--@myPC_dev_hypervisor:
  |  |--@myPC_dev_guest:
  |  |--@myPC_dev_hypervisor:
  |  |--@myPC_guest:
  |  |  |--@myPC_dev_guest:
  |  |  |--@myPC_prod_guest:
  |  |--@myPC_hypervisor:
  |  |  |--@myPC_dev_hypervisor:
  |  |  |--@myPC_prod_hypervisor:
  |  |--@myPC_prod:
  |  |  |--@myPC_prod_guest:
  |  |  |--@myPC_prod_hypervisor:
  |  |--@myPC_prod_guest:
  |  |--@myPC_prod_hypervisor:
  |--@prod:
  |  |--@myPC_prod:
  |  |  |--@myPC_prod_guest:
  |  |  |--@myPC_prod_hypervisor:
  |  |--@myPC_prod_guest:
  |  |--@myPC_prod_hypervisor:
  |  |--@prod_guest:
  |  |  |--@myPC_prod_guest:
  |  |--@prod_hypervisor:
  |  |  |--@myPC_prod_hypervisor:
  |--@ungrouped:
```

