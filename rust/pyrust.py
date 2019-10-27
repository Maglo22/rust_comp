# run -> python pyrust.py [archivo_entrada]
#     -> python pyrust.py ../tests/data_types.rs
#     -> python pyrust.py ../tests/errors/error_var.rs

# Imprime en un archivo 'AST.txt' un AST

import sys
if ".." not in sys.path: sys.path.insert(0,"..")

import rust_yacc

if len(sys.argv) != 2:
    print("Uso: python pyrust.py [archivo de entrada]")
    exit()
else:
    inFile = sys.argv[1] # archivo de entrada

# Leer archivo de entrada
try:
    with open(inFile,'r') as file:
        data = file.read()

    result = rust_yacc.parse(data, 0, True) # generar resultado (AST)
    
    file.close()

    if result != None:
        # Escribir AST generado en archivo 'AST.txt'
        r = open("AST.txt", 'w+')
        r.write(str(result))
        r.close()

        print("AST generado en 'AST.txt'")

except FileNotFoundError:
    print("El archivo de entrada no existe")
    exit()