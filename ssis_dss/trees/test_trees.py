from dss.datastore.tree import DataStoreTree

class MoodleTree(DataStoreTree):
    _branches = 'ssis_dss.branches.test_branches.MoodleBranches'
    _template = 'ssis_dss.templates.templates.MoodleTemplate'

class AutosendTree(DataStoreTree):
    _branches = 'ssis_dss.branches.test_branches.AutosendBranches'