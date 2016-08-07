from ssis_dss.trees.abstract_tree import AbstractTree

class MoodleTree(AbstractTree):
    _branches = 'ssis_dss.branches.branches.MoodleBranches'
    _template = 'ssis_dss.templates.templates.MoodleFullTemplate'

class MoodleFirstrunTree(AbstractTree):
    _branches = 'ssis_dss.branches.branches.MoodleFirstrunBranches'
    _template = 'ssis_dss.templates.templates.MoodleFirstRunTemplate'
