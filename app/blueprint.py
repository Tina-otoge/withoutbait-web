from flask import Blueprint


class Blueprint(Blueprint):
    def __init__(self, package, prefix=None):
        super().__init__(package.replace('.', '_'), package, url_prefix=prefix)
