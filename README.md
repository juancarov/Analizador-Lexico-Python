# Analizador-Lexico-Python

### Introducción

Este proyecto implementa un analizador léxico escrito en Python puro (sin `re`, `ply` ni `flex`). El programa recibe un archivo `.py` como entrada y produce un archivo de salida con los tokens detectados.  

---

### 1. Definición de Tokens

**Palabras reservadas de Python:** `class`, `def`, `if`, `return`, etc.  

**Símbolos y operadores con nombres** (`tk_par_izq`, `tk_par_der`, `tk_asig`, `tk_distinto`, etc.) se guardaron en dos estructuras: un conjunto `RESERVADAS` y un diccionario `SIMBOLOS`.

```python
RESERVADAS = {
    "class", "def", "if", "else", "elif", "while", "for", "in",
    "return", "print", "True", "False", "None", "and", "or", "not",
    "break", "continue", "pass", "import", "from", "as", "with",
    "try", "except", "finally", "raise", "global", "nonlocal",
    "lambda", "yield", "assert", "del", "is"
}

SIMBOLOS = {
    "==": "tk_igual",
    "!=": "tk_distinto",
    "<=": "tk_menor_igual",
    ">=": "tk_mayor_igual",
    "->": "tk_ejecuta",
    "(": "tk_par_izq",
    ")": "tk_par_der",
    ":": "tk_dos_puntos",
    ",": "tk_coma",
    ".": "tk_punto",
    "=": "tk_asig",
    "+": "tk_suma",
    "-": "tk_resta",
    "*": "tk_mult",
    "/": "tk_div",
    "<": "tk_menor",
    ">": "tk_mayor",
}
``` 

#### 2. Funciones Auxiliares

Se escribieron funciones pequeñas para reconocer caracteres:

es_letra(c) → devuelve True si es letra o _.

es_digito(c) → devuelve True si es dígito.

Estas ayudan a construir identificadores y números sin usar expresiones regulares.

```python
def es_letra(c):
    return c.isalpha() or c == "_"

def es_digito(c):
    return c.isdigit()
``` 

#### 3. Tokenización con un puntero

La función principal es tokenize_line.
Usa un puntero i que avanza carácter por carácter en la línea, y según el caso:

Ignora espacios y comentarios.

Reconoce cadenas ("...", '...').

Reconoce enteros.

Reconoce identificadores o palabras reservadas.

Reconoce símbolos y operadores (aplicando el principio de subcadena más larga).

Si encuentra algo no definido → error léxico.

```python
def tokenizar_linea(linea, num_linea):
    i = 0
    tokens = []
    while i < len(linea):
        c = linea[i]

        # espacios
        if c.isspace():
            i += 1
            continue

        # comentarios
        if c == "#":
            break

        # cadenas
        if c in ('"', "'"):
            inicio = i
            i += 1
            while i < len(linea) and linea[i] != c:
                i += 1
            if i >= len(linea):
                raise Exception(f">>> Error léxico(linea:{num_linea},posicion:{inicio+1})")
            lexema = linea[inicio:i+1]
            tokens.append(("tk_cadena", lexema, num_linea, inicio+1))
            i += 1
            continue

        # números
        if es_digito(c):
            inicio = i
            while i < len(linea) and es_digito(linea[i]):
                i += 1
            lexema = linea[inicio:i]
            tokens.append(("tk_entero", lexema, num_linea, inicio+1))
            continue

        # identificadores / reservadas
        if es_letra(c):
            inicio = i
            while i < len(linea) and (es_letra(linea[i]) or es_digito(linea[i])):
                i += 1
            lexema = linea[inicio:i]
            if lexema in RESERVADAS:
                tokens.append((lexema, num_linea, inicio+1))
            else:
                tokens.append(("id", lexema, num_linea, inicio+1))
            continue

        # símbolos (subcadena más larga primero)
        encontrado = False
        for simb in sorted(SIMBOLOS, key=lambda x: -len(x)):
            if linea.startswith(simb, i):
                tokens.append((SIMBOLOS[simb], num_linea, i+1))
                i += len(simb)
                encontrado = True
                break
        if encontrado:
            continue

        # si no encaja, error
        raise Exception(f">>> Error léxico(linea:{num_linea},posicion:{i+1})")

    return tokens
```

#### 4. Lectura del archivo

La función analizar_archivo abre el archivo de entrada, recorre sus líneas y llama a tokenizar_linea. 

Cada token se escribe en el archivo de salida en el formato requerido:

```python
def analizar_archivo(entrada, salida):
    with open(entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    with open(salida, "w", encoding="utf-8") as out:
        for num_linea, linea in enumerate(lineas, start=1):
            try:
                tokens = tokenizar_linea(linea, num_linea)
                for t in tokens:
                    if t[0] in RESERVADAS:   # reservada
                        out.write(f"<{t[0]},{t[1]},{t[2]}>\n")
                    elif t[0] == "id":       # identificador
                        out.write(f"<id,{t[1]},{t[2]},{t[3]}>\n")
                    elif t[0] in ("tk_cadena", "tk_entero"):
                        out.write(f"<{t[0]},{t[1]},{t[2]},{t[3]}>\n")
                    else:                    # símbolo
                        out.write(f"<{t[0]},{t[1]},{t[2]}>\n")
            except Exception as e:
                out.write(str(e) + "\n")
                break
```

#### 5. Pruebas Realizadas

Ejemplo del PDF (Cow/Animal) → salida igual al enunciado.

Calculadora con math.pi → reconoció import, funciones y números.

Errores intencionales:

90.00.50 → enteros y puntos separados.

1¬23948998 → error en ¬.

!== → error léxico.

!=¿ → <tk_distinto> y error en ¿.

Cadenas sin cerrar → error léxico.

##### Ejemplo Dado

```python
class Animal(object):
    makes_noise: bool = False

    def make_noise(self: "Animal") -> object:
        if (self.makes_noise):
            print(self.sound())

    def sound(self: "Animal") -> str:
        return "???"

class Cow(Animal):
    def __init__(self: "Cow"):
        self.makes_noise = True

    def sound(self: "Cow") -> str:
        return "moo"

c: Animal = None
c = Cow()
c.make_noise()   # Prints "moo"
```

##### Salida:

<img width="658" height="706" alt="image" src="https://github.com/user-attachments/assets/8d009f62-55b1-48b4-826d-7cb152ae8279" />

##### Calculadora Básica:

```python
import math

def calc_angle(x: float) -> float:
    y = math.sin(x) + math.cos(x)
    return y

angle = math.pi / 2
result = calc_angle(angle)
print(result)
```
##### Salida:

<img width="799" height="868" alt="image" src="https://github.com/user-attachments/assets/64ddb27c-36e8-4ebd-8589-af6fb866c8f7" />

##### Forzado de Errores 

```python

# Esto es un comentario y no debería generar tokens
class Test:
    x = 90.00.50    # número con puntos intermedios (debe tokenizar como enteros y puntos)
    y = 1¬23948998  # carácter inválido ¬ → debe dar error léxico

def broken_code():
    text = "hola
    number = 123abc   # identificador mal formado, pero en léxico será id
    z = 2 ** 3        # si no agregaste ** a los símbolos, esto debería romper
    if z !== 10:      # operador !== no existe → debería fallar
        print("ok")
```

##### Salida:

<img width="769" height="237" alt="image" src="https://github.com/user-attachments/assets/563629dd-26a7-4f53-9f18-bb94edf40bbb" />

#### Conclusión:

En conclusión, el analizador léxico desarrollado cumple con el objetivo de reconocer correctamente palabras reservadas, identificadores, enteros, cadenas y símbolos de Python sin apoyarse en librerías externas como re o ply. A partir de las pruebas realizadas —con código válido y con entradas que generan errores léxicos— se comprobó que el sistema es capaz de tokenizar de forma adecuada y también de detectar inconsistencias (operadores inválidos, cadenas sin cerrar, caracteres no reconocidos, etc.). Esto demuestra que la implementación es funcional y extensible, constituyendo una base sólida para futuros componentes de un compilador o intérprete más completo.




