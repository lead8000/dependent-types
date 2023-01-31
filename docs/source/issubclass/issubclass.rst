Conformidad de tipos dependientes
=================================

Para saber cuál es la relación de conformidad entre dos tipos dependientes se utiliza la función built-in :py:func:`issubclass(_subcls, _cls)`.

Primeramente se obtiene una referencia a los atributos dependientes de la clase :py:class:`Matrix` de la siguiente forma:

.. code-block:: python
    from dependent_types import Attr

    N = Attr('amount_rows')
    M = Attr('amount_cols')

Luego se escriben los tipos dependientes de los que se quiere verificar su conformidad:

.. code-block:: python
    assert issubclass(Matrix[ N, M | (((N < 100) & ( N > 50)) & (M > 100))  ], Matrix[ N, M | ( M > 50 ) ])
