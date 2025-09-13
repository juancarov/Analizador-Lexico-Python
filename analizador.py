import sys

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

def es_letra(c):
    return c.isalpha() or c == "_"

def es_digito(c):
    return c.isdigit()

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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python analizador.py entrada.py salida.txt")
    else:
        analizar_archivo(sys.argv[1], sys.argv[2])
