# dependent-types

Se quiere hacer un DSL que contenga el concepto de tipo dependiente, es decir un tipo que depende de otros tipos para existir. El siguiente ejemplo modela la situación más sencilla que se quisiera modelar con este DSL.

Se tiene una función anotada como axioma, que representa uno de los tipos más básicos en este programa y no es cuestionable si es consistente la dependencia de tipos, se asume como verdad. Entonces lo que se quisiera validar es que aquellas otras funciones que no son axiomas son consistentes con la dependencia de tipos.

Este es un ejemplo sencillo donde se crea un función que recibe una lista de tamaño `N` y un elemento, y devuelve una lista de tamaño `N+1`. Como esta función es un axioma del programa el validador no la chequea.

Luego se encuentra otra función que recibe dos listas, una de tamaño `N` y otra de `M`, y devuelve una lista de `N+M`. Como esta función no está anotada como axioma, el validador está encargado de chequear si se cumple la consistencia de tipos. En este caso esta función cumple correctamente el concepto de tipo dependiente que se quiere abarcar en el DSL; el tipo resultante de esta función es un tipo de tamaño `N` y tamaño `M` ya que cada elemento de la lista `m` es añadido a la lista `n` y luego esta es devuelta.

```python
@axiom
def add_something(n: List[N], item) -> List[N + 1]:
    n.append(item)
    return n

def concatenate_list(n: List[N], m: List[M]) -> List[N + M]:    
    for item in m:
        n = add_something(n, item)
    return n
```
