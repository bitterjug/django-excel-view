django-excel-view
=================

A wraper for django-excel-response_ for DRY simple spreadsheets including a class-based view.

.. _django-excel-response: https://bitbucket.org/kmike/django-excel-response

Use
-----

Django-excel-response makes it easy to make spreadsheets. 
As you can see from its readme, it likes to get a queryset
or a list of lists. If you give it a list of lists, its up 
to you to make the headers line up with the content. 
Its up to you to fetch the data and marshall it into lists too. 
Specifying the column headings and content
separately felt too un-DRY. 

My data comes from a  queryset. I join the related models using
``select_related()``, and fetch out a dictionary of the fields I'm
interested in, with their values, using ``values()``. 
I can give these dictionaries directly to django-excel-response,
and it will use the keys as column headings.
Sometimes, however, I want to include values derived from 
other values, or to do post-processing on the values. Somtiems
I want better column headings.  So I make a column specification::

    from excel_view import ColSpec, Col

    colspec = ColSpec(
        Col('id'),
        Col('Business', 'business_name'),
        Col('Name', 'user__name', 'user__oname', 'user__sname',
            reduce=" ".join),
        Col('Full cost', 'price', 'vat', reduce=sum)
        Col('Status', 'status_code',
            function=status_codes.get),
         ...)

- The first column heading is **id** and that's also the dictionary
  key of the id field

- The second column heading is **Business** and contains the ``business_name``

- The **Name** column contains the result of joining together
  three name fields from a related model linked by ``user`` field.
  ``user__name`` fetches the ``name`` field from the related ``user``
  object, etc.  And ``" ".join`` is a function to join strings with spaces,
  it reduces the list of three name values to one string value.

- Similarly the **Full cost** column is the sum of
  two numeric values calculated using the ``sum`` built-in

- **Status*** column values are strings that correspond
  to code values stored in the DB. So we use the ``status_codes``
  dictionary's ``get()`` method, as a function argument,
  to convert them.


So the arguments to ``Col(...)`` are:

1. A mandatory column header.

2. the remainder of ``*args`` are input dictionary keys
   (default = header)

3. optional ``reduce`` is a function to reduce a list
   of values to one -- if you specified more than
   one input key (the default is ``pop()``, i.e. take
   the first)

4. optional ``function`` is a function to transform the
   single result value (the default identity:
   ``lambda x:x``, i.e. no change)

Then ``ColSpec`` provides useful methods:

1. ``inputs()`` gives the full list of input keys expected,
   which you can use as arguments to ``values()`` on a queryset::

      dataset = BusinessPlan.objects.values(*colspec.inputs())

2. ``related()`` lists the related models (derived from keys
   that contain double underscore)::

      dataset = BusinessPlan.objects\
                  .filter(... whatever ...)\
                  .select_related(*colspec.related())\
                  .values(*colspec.inputs())

3. ``values(context_dictionary)`` is a function that takes 
   the dictionary of values corresponding to one entry in 
   the queryset and returns the list of values to go into 
   the spreadsheet::

        data_rows = [colspec.values(row) for row in dataset]

4. ``headers()`` returns the column headers::

    return ExcelResponse(data_rows, headers=colspec.headers())



Testing
--------

The ``testapp`` application sets up enough django context to run the tests::

  $ python manage.py test testapp


