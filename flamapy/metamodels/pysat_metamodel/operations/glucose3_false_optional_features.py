from typing import Any

from pysat.solvers import Solver

from flamapy.core.operations import FalseOptionalFeatures
from flamapy.metamodels.pysat_metamodel.models.pysat_model import PySATModel
from flamapy.metamodels.fm_metamodel.models.feature_model import FeatureModel


class Glucose3FalseOptionalFeatures(FalseOptionalFeatures):

    def __init__(self, feature_model: FeatureModel) -> None:
        self.result: list[Any] = []
        self.feature_model = feature_model
        self.solver = Solver(name='glucose3')

    def execute(self, model: PySATModel) -> 'Glucose3FalseOptionalFeatures':
        self.result = _get_false_optional_features(model, self.feature_model)
        return self

    def get_false_optional_features(self) -> list[list[Any]]:
        return self.get_result()

    def get_result(self) -> list[Any]:
        return self.result


    def _get_false_optional_features(self, sat_model: PySATModel, feature_model: FeatureModel) -> list[Any]:
        real_optional_features = [f for f in feature_model.get_features() 
                                  if not f.is_root() and not f.is_mandatory()]

        result = []
        for clause in sat_model.get_all_clauses():
            self.solver.add_clause(clause)
    
        for feature in real_optional_features:
            variable = sat_model.variables.get(feature.name)
            parent_variable = sat_model.variables.get(feature.get_parent().name)
            assert variable is not None
            satisfiable = self.solver.solve(assumptions=[parent_variable, -variable])
            if not satisfiable:
                result.append(feature.name)
        self.solver.delete()
        return result
