from flask import Blueprint


class Blueprint(Blueprint):
    def __init__(self, package, **kwargs):
        kwargs.setdefault('cli_group', None)
        kwargs['url_prefix'] = kwargs.pop('prefix', None)
        super().__init__(
            package.replace('.', '_'),
            package,
            **kwargs,
        )
