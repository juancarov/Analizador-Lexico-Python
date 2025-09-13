# Analizador-Lexico-Python

### Introducción.

Este proyecto implementa un analizador léxico escrito en Python puro (sin `re`, `ply` ni `flex`). El programa recibe un archivo `.py` como entrada y produce un archivo de salida con los tokens detectados.  

#### 1. Definicion de Tokens

Palabras reservadas de Python (class, def, if, return, etc.).

Símbolos y operadores con nombres (tk_par_izq, tk_par_der, tk_asig, tk_distinto, etc.). Esto se guardó en dos estructuras: un conjunto RESERVADAS y un diccionario SIMBOLOS.

<par>

RESERVADAS = {"class", "def", "if", "return", "print", "True", "False", "None"}
SIMBOLOS = {"(": "tk_par_izq", ")": "tk_par_der", ":": "tk_dos_puntos", "=": "tk_asig", "!=": "tk_distinto"}

</par>
