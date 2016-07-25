from ssis_dss.trees.abstract_tree import AbstractTree

class AutosendTree(AbstractTree):
    _branches = 'ssis_dss.branches.branches.AutosendBranches'

class AutosendFirstrunTree(AbstractTree):
	_branches = 'ssis_dss.branches.branches.AutosendFirstrunBranches'