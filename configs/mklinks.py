import errno
import os
import os.path

def link(target_dir, node_dir):
    linked = set()
    for f in os.listdir(target_dir):
        if f.startswith('.'):
            # private item; not to be linked
            continue

        target = os.path.join(target_dir, f)
        node_link = os.path.join(node_dir, f)
        if os.path.isdir(target):
            try:
                os.mkdir(node_link)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            link(target, node_link)
            linked.add(f)

        else:
            node_target = '../' * node_link.count('/') + target
            try:
                found_link = os.readlink(node_link)
                if found_link == node_target:
                    linked.add(f)
                    continue
            except OSError:
                pass
            os.symlink(node_target, node_link)
            linked.add(f)

    to_delete = set(os.listdir(node_dir)) - linked
    if to_delete:
        print(f'Need to delete {len(to_delete)} items from {node_dir}')
    for item in to_delete:
        os.unlink(os.path.join(node_dir, item))

for node in os.listdir('.'):
    if not os.path.isdir(node):
        continue
    if node in ('swift-node', 'worker'):
        continue
    link('swift-node', node)
