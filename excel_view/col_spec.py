class Col(object):

    def __init__(self, header, *input_keys, **kwargs):
        """
        :Header is text for the spreadsheet header row.
        :Keys are a list of input data keys required in the
        context dictionary to produce the out put value
        :reduce is an optional function to reduce a list
        of values into one
        :function is an optional transformation function
        to perform on the reduced value
        :default is an optional value to use instead of
        null if an input key is not found in the context
        dictionary. Note that if the key is there with value
        None, then you still get None, not this default.
        """
        self.fn = kwargs.get('function', lambda x: x)
        self.rx = kwargs.get('reduce', list.pop)
        self.default = kwargs.get('default')
        self.header = header
        self.keys = list(input_keys) if input_keys else [header]

    def inputs(self):
        return self.keys

    def value(self, context):
        return self.fn(
                self.rx(
                    [context.get(key, self.default) for key in self.keys]))


class ColSpec(object):
    """
    Columns specification for spreadsheet export.
    Spreadsheet wants list of lists with headers in first row.
    We can easily get a dictionary of data using queryset.values(...)
    These classes enable a declarative style specification of the
    mapping from these dicts to the spreadsheet rows.
    """

    def __init__(self, *cols):
        """
        Expects a list of Col() objects as parameters
        """
        self.cols = cols

    def inputs(self):
        """
        Returns a flat list of the input keys required in the
        context dictionary to satisfy all the cols
        """
        return sum([col.inputs() for col in self.cols], [])

    def values(self, context):
        """
        Returns the spreadsheet data row
        """
        return [col.value(context) for col in self.cols]

    def headers(self):
        """
        Returns the spreadsheet header row
        """
        return [col.header for col in self.cols]

    def related(self):
        """
        Returns the set of field names leading to relatd models
        to be included in the queryset. (derived from the prefixes
        up to double-underscore in the input keys)
        """
        sep = '__'
        return set([key.partition(sep)[0]
            for key in self.inputs()
            if key.find(sep) >= 0])
