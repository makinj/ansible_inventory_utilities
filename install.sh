mkdir -p  ~/.ansible/plugins/inventory
ln -sf "$(pwd)/combined-groups.py" ~/.ansible/plugins/inventory
ln -sf "$(pwd)/inverted-group.py" ~/.ansible/plugins/inventory
