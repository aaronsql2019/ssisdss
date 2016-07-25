"""
Importers that are used on both sides of the isles, in order to make deriviative branches
"""

from dss.importers.default_importer import DefaultImporter

class UsersImporter(DefaultImporter):

    def readin(self):
        for branch_name in ['students', 'parents', 'staff']:
            branch = getattr(self._tree, branch_name)
            for key in branch.keys():
                item = branch.get(key)
                # 'object' as a key and only idnumber and object indicates immediate substitution
                yield {
                    'idnumber': item.idnumber,
                    'object': item
                }


