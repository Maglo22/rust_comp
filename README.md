# rust_comp
Interprete del lenguaje Rust hecho con PLY.

Dentro de la carpeta _rust_ se encuentra: 
- **rust_lex** - léxico del lenguaje.
- **rust_yacc** - gramática y analizador.
- **pyrust** - archivo principal.

Para ejecutar utilizar el archivo _pyrust.py_ -> `python pyrust.py [archivo_entrada]`.

Ejemplo: `python pyrust.py ../tests/data_types.rs`

Al ejecutarse se escribirá el árbol de sintaxis abstracto (AST) generado por el analizador en un archivo "AST.txt", siempre y cuando no haya un error de sintaxis.
