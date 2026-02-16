class OwnFieldsOnlyMixin:

    def model_dump_own(self):
        data = self.model_dump()
        return {k: v for k, v in data.items() if k in self.model_fields}
