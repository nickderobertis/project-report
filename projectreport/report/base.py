from cached_property import cached_property
import yaml
from projectreport.report.json import to_json


class BaseReport:

    def __str__(self):
        return self.yaml

    @cached_property
    def json(self) -> str:
        return to_json(self.data)

    @cached_property
    def yaml(self) -> str:
        return yaml.dump(self.data, indent=2)

    @cached_property
    def latex(self):
        return str(self.doc)

    #### Scaffolding below, implement these in subclass ########

    @cached_property
    def data(self):
        raise NotImplementedError

    @cached_property
    def doc(self):
        raise NotImplementedError
