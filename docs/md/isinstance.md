# Restricciones de un tipo dependiente

Para saber si una instancia concreta cumple con las restricciones del tipo dependiente se utiliza la función built-in `isinstance(_ins, _cls)`.

```python
from dependent_types import Attr, _

N = Attr('amount_rows')
M = Attr('amount_cols')

m = Matrix(
    [[43,23,54,22],
     [13,65,54,34],
     [84,23,54,23],
     [29,49,23,53]]
)

assert not isinstance(m, Matrix[ _, M | ( M > 50 ) ])
```

Fíjese como se utiliza un underscore('_') para indicar que el primer atributo dependiente puede tomar cualquier valor. Tenga en cuenta que para poder utilizar el underscore para esta función, debe importarlo del paquete, como se hizo anteriormente.

[Atrás](introduction.md)
