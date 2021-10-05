operaciones = ['MOV','ADD','SUB','AND','OR','NOT','XOR','SHL','SHR','INC',
            'RST','CMP','JMP','JEQ','JNE','JGT','JLT','JGE','JLE','JCR','JOV',
            'CALL','RET','PUSH','POP']

def hex_a_dec(string):
    if type(string) == str:
        if  "#" in string:
            string = string.replace("#", "")
            return int(string, 16)
        else:
            return int(string)
    return string

def opcodes(operaciones):
    dic_ins = {}
    cont = 0
    aux = ""
    stringaux = ""
    check = True
    archivo = open("instrucciones.txt")
    for linea in archivo:
        if linea=="\n":
            check = True
            continue

        linea = linea.replace("\n","")

        if linea in operaciones and check:
            aux = linea
            check = False
            continue

        cont+=1
        if cont==1:
            stringaux=aux+" "+linea

        if cont==2:
            dic_ins[stringaux]=linea
            stringaux=""
            cont = 0
    return dic_ins

def lectura(nombre):
    archivo = open(nombre, 'r')
    lineas = archivo.readlines()
    cant = len(lineas)
    inCode = False
    instructions = []

    for i in lineas:
        inCode = True
        i = i.split()
        if inCode:
            try:
                if len(i) == 2:
                    if ',' in i[1]:
                        i[1] = i[1].split(',')
                    instructions.append(i)
                elif len(i) == 1:
                    instructions.append(i)
            except:
                pass
    return instructions, cant

def validar_ins(instruction, opc, cant):

    ins_trans = instruction[0]+' '

    if instruction[0] == 'RET':
        if len(instruction) != 1:
            arg = ','.join(instruction[1])
            return f'Instruccion invalida: {ins_trans}{arg}' 
        if len(instruction) == 1:
            return True  

    if len(instruction) < 2:
        inst = ','.join(instruction)
        if instruction[0] in operaciones:
            return f'Instruccion incompleta: {inst}'
        else:
            return f'Instruccion no existe: {inst}'

    if type(instruction[1]) is list:
        if len(instruction[1]) > 2:
            arg = instruction[1]
            arg = ','.join(arg)
            return f'La instruccion {ins_trans}{arg} es invalida, recibe argumentos extra'
        else:
            arg = instruction[1]
            if arg[0]!="A" and arg[0]!="B" and arg[0]!="(B)" and arg[0]!="(A)":
                if '(' in arg[0]:
                    ins_trans += '(Dir)'
                else:
                    ins_trans += 'Lit'
            else:
                ins_trans += arg[0]
            
            ins_trans += ','

            if arg[1]!="A" and arg[1]!="B" and arg[1]!="(B)" and arg[1]!="(A)":
                if '(' in arg[1]:
                    ins_trans += '(Dir)'
                else:
                    ins_trans += 'Lit'
            else:
                ins_trans += arg[1]

    else:
        if 'J' in instruction[0]:
            #JUMPS
            arg = instruction[1]
            if '#' in arg:
                arg = hex_a_dec(arg)
                if arg > cant:
                    return f'Direccion fuera de rango en instruccion {ins_trans}{instruction[1]}'
            ins_trans += 'Dir'
        else:
            #INC, RST
            arg = instruction[1]
            if arg!="A" and arg!="B" and arg!="(B)" and arg!="(A)":
                if '(' in arg:
                    ins_trans += '(Dir)'
                else:
                    ins_trans += 'Lit'
            else:
                ins_trans += arg

    if ins_trans in opc.keys():
        return True
    else:
        return f'Instruccion no existe: {ins_trans}'
        
def main():
    opc = opcodes(operaciones)
    instructions, cant= lectura('../p3-ej_incorrecto.ass')
    cont = 1
    for ins in instructions:
        val = validar_ins(ins, opc, cant)
        if val != True:
            print(f'Error en la linea {cont} -> {val}') 
        cont += 1  
        
main()