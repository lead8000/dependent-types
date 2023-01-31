Implementación de un nuevo tipo dependiente
==============================================

Se necesita importar la metaclase :py:class:`~dependent_types.DependentType` del paquete y declararla como metaclase del tipo dependiente que se quiere implementar. A continuación se muestra un breve ejemplo:

.. code-block:: python

    from dependent_types import DependentType

    class Matrix(metaclass=DependentType):

        def __init__(self, l):
            self.list = l
            self.amount_rows = len(l)
            self.amount_cols = len(l[0])
            self.len = len(self)
        
        def __len__(self):
            return sum([len(row) for row in self.list])

Hasta este momento se tiene declarada la clase :py:class:`Matrix` como tipo dependiente, pero no se tiene especificado cuáles son los atibutos dependientes de este tipo. Para esto se utiliza el operador `|=` que sirve para anotar los attributos que será dependientes, de la clase :py:class:`Matrix`.

.. code-block:: python

    Matrix |= 'amount_rows'
    Matrix |= 'amount_cols'


**OJO**: hay que tener en cuenta de aquí en adelante, el orden establecido de los atributos dependientes. A partir de ahora cuando se haga referencia al primer atributo dependiente se estará refiriendo al atributo ``amount_rows``, cuando se refiera al segundo a ``amount_cols``, etc.
