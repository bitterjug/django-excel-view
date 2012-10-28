from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin

from excel_response import ExcelResponse

from col_spec import ColSpec, Col


class ExcelView(View, MultipleObjectMixin):
    file_name = "spreadsheet"
    colspec = None

    def get(self, *args, **kwargs):
        """
        Returns an ExcelResponse containing the data
        specified by self.colspec, which must exist.
        """
        return ExcelResponse(
            self.get_data(),
            self.file_name)

    def get_data(self, *args, **kwargs):
        if not self.colspec or \
                not isinstance(self.colspec, ColSpec):
            raise ImproperlyConfigured(
                "{0} must define 'colspec'".format(
                    self.__class__.__name__))
        dataset = self.get_queryset()\
            .select_related(*self.colspec.related())\
            .values(*self.colspec.inputs())
        return [self.colspec.headers()] +\
               [self.colspec.values(row) for row in dataset]
