from __future__ import annotations

from docutils import nodes

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata


class PlatDirective(SphinxDirective):
    """A directive to write plat dependent content."""

    required_arguments = 1
    has_content = True
    option_spec = {
        'vers': lambda x: x,
    }

    __plats = {
        'macos': 'macOS',
        'windows': 'Windows',
        'centos': 'CentOS',
        'ubuntu': 'Ubuntu',
        'linux': 'Linux',
        'msys2': 'MSYS2',
    }

    def run(self) -> list[nodes.Node]:
        plat = self.arguments[0]
        if not plat in self.__plats:
            raise self.error(f'Unknown plat "{plat}"')
        platName = self.__plats[plat]
        node = nodes.admonition(rawsource='\n'.join(self.content), classes=['plat', plat])
        self.state.nested_parse(self.content, self.content_offset, node)
        node.insert(0, nodes.title(text=f'The contents are applicable to {platName}'))
        if 'vers' in self.options:
            vers = str(self.options['vers']).split(',')
            p = nodes.paragraph(text=f'Typical versions: ')
            count = 0
            for s in vers:
                if count > 0:
                    p.append(nodes.Text(', '))
                p.append(nodes.strong(rawsource=s, text=s))
                count += 1
            node.insert(1, p)
        return [ node ]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive('plat', PlatDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
