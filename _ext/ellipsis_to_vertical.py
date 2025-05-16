from docutils import nodes

def replace_ellipsis_in_codeblocks(app, doctree, fromdocname):
    for node in doctree.traverse(nodes.literal_block):
        if node.attributes.get("language") == 'console':
            replaced = False
            for child in node.traverse(nodes.Text):
                if '...' in child:
                    child.parent.replace(child, nodes.Text(child.astext().replace('...', '️⋮')))
                    replaced = True
            # It seems problematic if the rawsource does not match the text
            if replaced:
                node.rawsource = node.astext()

def setup(app):
    app.connect('doctree-resolved', replace_ellipsis_in_codeblocks)
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
