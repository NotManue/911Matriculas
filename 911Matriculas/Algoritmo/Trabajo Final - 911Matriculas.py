# 911Matriculas 

import pandas as pd
import os
import logging
import math as math
from datetime import datetime

Ruta = r'C:\Users\Usuario\Desktop\911Matriculas\Bases_de_Datos' 

# Log

hoy = datetime.today().strftime('%Y%m%d') #Captura de fecha de ejecucion

nombre_archivo_log = f"log_{hoy}.log"

logging.basicConfig(filename=nombre_archivo_log, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.info("911Matriculas comenzo a la carrera fiuummmmmm")

# Directorio de archivos

RutaDeImpresion = r'C:\Users\Usuario\Desktop'

RutaDeImpresion = os.path.join(RutaDeImpresion, 'Archivos911Matriculas')
os.makedirs(RutaDeImpresion, exist_ok=True)

logging.info(f"Directorio de impresión creado: {RutaDeImpresion}")

for i in range(10):
    RutaSemestres = os.path.join(RutaDeImpresion, f"Semestre_{i+1}")
    os.makedirs(RutaSemestres, exist_ok=True)
    logging.info(f"Directorio del semestre {i+1}: {RutaSemestres}")

# Lectura de base de datos 

RutaEstudiantes = os.path.join(Ruta, "Estudiantes.xlsx")

Estudiantes = pd.read_excel(RutaEstudiantes)
logging.info(f"Archivo de estudiantes leido: {RutaEstudiantes}")

# Lectura malla curricular

RutaMallaCurricular = os.path.join(Ruta, "Materias_Semestre_Creditos.xlsx")

MallaCurricular = pd.read_excel(RutaMallaCurricular)
logging.info(f"Archivo de la malla curricular leído: {RutaMallaCurricular}")

# Creacion de codigos de asignatura (6 caracteres maximo)

def CodMat(x: str) -> str: 
    """
    Crea un codigo basado en partes especificas de la cadena de texto dada
    La funcion separa cada input por palabras, y construye un codigo siguiendo 
    las siguientes reglas.
    - Si el input contiene mas de 2 palabras:
       - Toma los primeros 2 caracteres the la primera palabra
       - Toma el primer caracter de la segunda palabra. 
       - Tomas los ultimos 3 caracteres de la ultima palabra.
       - Concatena estos caracteres y crea el codigo. 
    - Si el input contiene 2 palabras o menos: 
       - Toma los primeros 3 caracteres de la primera palabra.
       - Toma los ultimos 3 caracteres de la ultima palabra.
       - Concatena estos caracteres y crea el codigo.
    
    Nota: El codigo generado no posee espacios entre caracteres.
    
    Parameters:
    x (str): La cadena de texto a ser codificada.
    
    Returns:
    str: La cadena de texto (Codigo) generada.
    """
    words = x.split()
    
    if len(words) > 2: 
        first_word = words[0] 
        coded_first_word = first_word[:2] 
        second_word = words[1] 
        coded_second_word = second_word[:1]  
        last_word = words[-1] 
        coded_last_word = last_word[-3:] 
        coded = coded_first_word + coded_second_word + coded_last_word 
        coded_str = ' '.join(coded)
    else:
        first_word = words[0] 
        coded_first_word = first_word[:3] 
        last_word = words[-1] 
        coded_last_word = last_word[-3:] 
        coded = coded_first_word + coded_last_word 
        coded_str = ' '.join(coded)
        
    coded_str = coded_str.replace(" ", "")
    
    return coded_str

MallaCurricular['Codigo'] = MallaCurricular['Asignatura'].apply(CodMat)
print(MallaCurricular.head())
logging.info("Códigos de asignaturas generados")

# Horas de trabajo del docente 

def HTD(x:int):
    """
    Calcula las horas de trabajo por parte del docente según los créditos de la materia.

    Esta función toma como entrada el número de créditos de una materia y devuelve 
    la cantidad correspondiente de horas de trabajo del docente (HTD) basándose 
    en una serie de reglas predefinidas.

    Parameters:
    x (int): El número de créditos de la materia.

    Returns:
    int: La cantidad de horas de trabajo del docente correspondiente a los créditos de la materia.
    """
    if x == 1:
        return 16
    if x == 2:
        return 32
    if x == 3:
        return 64
    if x == 4:
        return 96
    if x == 12:
        return 288

MallaCurricular['HTD'] = MallaCurricular['Creditos'].apply(HTD)
logging.info("Horas de trabajo del docente (HTD) calculadas")

# Horas de trabajo independiente

def HTI(x:int):
    """
    Calcula las horas de trabajo independiente según los créditos de la materia.

    Esta función toma como entrada el número de créditos de una materia y devuelve 
    la cantidad correspondiente de horas de trabajo independiente (HTI) basándose 
    en una serie de reglas predefinidas. 
    
    Parameters:
    x (int): El número de créditos de la materia. 
    
    Returns: 
    int: La cantidad de horas de trabajo independiente correspondiente a los créditos de la materia.
    """
    if x == 1:
        return 32
    if x == 2:
        return 64
    if x == 3:
        return 80
    if x == 4:
        return 120
    if x == 12:
        return 360

MallaCurricular['HTI'] = MallaCurricular['Creditos'].apply(HTI)
logging.info("Horas de trabajo independiente (HTI) calculadas")

# Separacion de las materias por semestre

MallaPorSem = []

for i in range(1,11):
    
    MallaPorSem.append(MallaCurricular[MallaCurricular['Semestre'] == i])
    
logging.info("Materias separadas por semestre")

# Separacion de estudiantes por semestre

EstudiantesPorSem = []

for i in range(1,11):
    
    EstudiantesPorSem.append(Estudiantes[Estudiantes['Semestre'] == i])
    
logging.info("Estudiantes separados por semestre")

# Numero de estudiantes por semestre (NTE)

NTE = []

for i in range(10):
    
    NTE.append(len(EstudiantesPorSem[i]))

logging.info("Número de estudiantes por semestre:")

for i, valor in enumerate(NTE, start=1):
    logging.info(f"{i}. NTE[{i-1}]: {valor}")

# Limites de las aulas de clase 

Limites = [30, 30, 30, 25, 25, 25, 20, 20, 20, 10]

# Numero de cursos que se deben de abrir por semestre (TCA)

TCA = []

for i in range(10):
    
    TCA.append(math.ceil(NTE[i]/Limites[i]))
    
logging.info("Número de cursos a abrir por semestre:")

for i, valor in enumerate(TCA, start=1):
    logging.info(f"{i}. TCA[{i-1}]: {valor}")

# Creacion del Excel por asignatura

# Creacion de los grupos

def split_dataframe(df, Limite):
    """
    Separa un Dataframe en Dataframes mas pequeños de una determinada longitud maxima.

    Parameters:
    df (pandas.DataFrame): DataFrame dado a ser separado.
    Limite (int): Numero maximo de filas que cada split debe tener.

    Returns:
    lista de pandas.DataFrame: Lista de los Dataframes seccionados, cada uno con su "Limite" de filas.
    """
    return [df[i:i + Limite] for i in range(0, df.shape[0], Limite)] 

SplitsDeGrupos = []

for i in range(10):
    
    SplitsDeGrupos.append(split_dataframe(EstudiantesPorSem[i], Limites[i]))
    
    logging.info(f"Grupos del semestre {i+1} creados")

# Asignar las materias a los grupos de cada semestre
        
# Semestre 1

Codigos1erSem = MallaPorSem[0]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[0])):
    
    logging.info(f"Asignando estudiantes Semestre 1: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[0])):
        
        SplitsDeGrupos[0][i][f'Asignatura{j+1}'] = f"{Codigos1erSem[j]}{i+1}"
        
        RutaSem1 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_1'
        
        RutaSem1 = os.path.join(RutaSem1, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem1, exist_ok=True)
         
        carpeta = f"S1_G{i+1}_N{len(SplitsDeGrupos[0][i])}.xlsx"
         
        RutaSem1 = os.path.join(RutaSem1, carpeta)
         
        SplitsDeGrupos[0][i].to_excel(RutaSem1, index=False)
        
        RutaSem1 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_1'
        
        RutaSem1 = os.path.join(RutaSem1, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem1, exist_ok=True)
         
        carpetacsv = f"S1_G{i+1}_N{len(SplitsDeGrupos[0][i])}.csv"
         
        RutaSem1 = os.path.join(RutaSem1, carpetacsv)
        
        SplitsDeGrupos[0][i].to_csv(RutaSem1, index=False)

logging.info("1er Semestre: Completado jeje")
        
# Semestre 2

Codigos2doSem = MallaPorSem[1]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[1])):
    
    logging.info(f"Asignando estudiantes Semestre 2: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[1])):
        
        RutaSem2 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_2'
        
        RutaSem2 = os.path.join(RutaSem2, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem2, exist_ok=True)
        
        SplitsDeGrupos[1][i][f'Asignatura{j+1}'] = f"{Codigos2doSem[j]}{i+1}"
        
        carpeta = f"S2_G{i+1}_N{len(SplitsDeGrupos[1][i])}.xlsx"
        
        RutaSem2 = os.path.join(RutaSem2, carpeta)
         
        SplitsDeGrupos[1][i].to_excel(RutaSem2, index=False)
        
        RutaSem2 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_2' 
        
        RutaSem2 = os.path.join(RutaSem2, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem2, exist_ok=True)
        
        carpetacsv = f"S2_G{i+1}_N{len(SplitsDeGrupos[1][i])}.csv" 
        
        RutaSem2 = os.path.join(RutaSem2, carpetacsv)
        
        SplitsDeGrupos[1][i].to_csv(RutaSem2, index=False)
     
logging.info("2do Semestre: Completado")

# Semestre 3

Codigos3erSem = MallaPorSem[2]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[2])):
    
    logging.info(f"Asignando estudiantes Semestre 3: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[2])):
        
        RutaSem3 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_3'
        
        RutaSem3 = os.path.join(RutaSem3, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem3, exist_ok=True)
        
        SplitsDeGrupos[2][i][f'Asignatura{j+1}'] = f"{Codigos3erSem[j]}{i+1}"
        
        carpeta = f"S3_G{i+1}_N{len(SplitsDeGrupos[2][i])}.xlsx"
        
        RutaSem3 = os.path.join(RutaSem3, carpeta)
         
        SplitsDeGrupos[2][i].to_excel(RutaSem3, index=False) 
        
        RutaSem3 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_3' 
        
        RutaSem3 = os.path.join(RutaSem3, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem3, exist_ok=True)
        
        carpetacsv = f"S3_G{i+1}_N{len(SplitsDeGrupos[2][i])}.csv" 
        
        RutaSem3 = os.path.join(RutaSem3, carpetacsv) 
        
        SplitsDeGrupos[2][i].to_csv(RutaSem3, index=False)
        
logging.info("3er Semestre: Completado")

# Semestre 4

Codigos4toSem = MallaPorSem[3]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[3])):
    
    logging.info(f"Asignando estudiantes Semestre 4: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[3])):
        
        RutaSem4 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_4' 
        
        RutaSem4 = os.path.join(RutaSem4, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem4, exist_ok=True)
        
        SplitsDeGrupos[3][i][f'Asignatura{j+1}'] = f"{Codigos4toSem[j]}{i+1}" 
        
        carpeta = f"S4_G{i+1}_N{len(SplitsDeGrupos[3][i])}.xlsx"
        
        RutaSem4 = os.path.join(RutaSem4, carpeta)
        
        SplitsDeGrupos[3][i].to_excel(RutaSem4, index=False) 
        
        RutaSem4 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_4'
        
        RutaSem4 = os.path.join(RutaSem4, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem4, exist_ok=True)
        
        carpetacsv = f"S4_G{i+1}_N{len(SplitsDeGrupos[3][i])}.csv" 
        
        RutaSem4 = os.path.join(RutaSem4, carpetacsv) 
        
        SplitsDeGrupos[3][i].to_csv(RutaSem4, index=False)

logging.info("4to Semestre: Completado")

# Semestre 5

Codigos5toSem = MallaPorSem[4]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[4])):
    
    logging.info(f"Asignando estudiantes Semestre 5: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[4])):
        
        RutaSem5 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_5'
        
        RutaSem5 = os.path.join(RutaSem5, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem5, exist_ok=True)
        
        SplitsDeGrupos[4][i][f'Asignatura{j+1}'] = f"{Codigos5toSem[j]}{i+1}" 
        
        carpeta = f"S5_G{i+1}_N{len(SplitsDeGrupos[4][i])}.xlsx"
        
        RutaSem5 = os.path.join(RutaSem5, carpeta)
        
        SplitsDeGrupos[4][i].to_excel(RutaSem5, index=False)
        
        RutaSem5 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_5' 
        
        RutaSem5 = os.path.join(RutaSem5, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem5, exist_ok=True)
        
        carpetacsv = f"S5_G{i+1}_N{len(SplitsDeGrupos[4][i])}.csv" 
        
        RutaSem5 = os.path.join(RutaSem5, carpetacsv) 
        
        SplitsDeGrupos[4][i].to_csv(RutaSem5, index=False)

logging.info("5to Semestre: Completado")

# Semestre 6

Codigos6toSem = MallaPorSem[5]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[5])):
    
    logging.info(f"Asignando estudiantes Semestre 6: Grupo_{i+1}")
   
    for j in range(len(MallaPorSem[5])):
        
        RutaSem6 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_6'
        
        RutaSem6 = os.path.join(RutaSem6, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem6, exist_ok=True)
        
        SplitsDeGrupos[5][i][f'Asignatura{j+1}'] = f"{Codigos6toSem[j]}{i+1}" 
        
        carpeta = f"S6_G{i+1}_N{len(SplitsDeGrupos[5][i])}.xlsx"
        
        RutaSem6 = os.path.join(RutaSem6, carpeta)
        
        SplitsDeGrupos[5][i].to_excel(RutaSem6, index=False)
        
        RutaSem6 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_6'
        
        RutaSem6 = os.path.join(RutaSem6, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem6, exist_ok=True)
        
        carpetacsv = f"S6_G{i+1}_N{len(SplitsDeGrupos[5][i])}.csv" 
        
        RutaSem6 = os.path.join(RutaSem6, carpetacsv) 
        
        SplitsDeGrupos[5][i].to_csv(RutaSem6, index=False)

logging.info("6to Semestre: Completado")

# Semestre 7

RutaSem7 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_7'

Codigos7moSem = MallaPorSem[6]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[6])):
    
    logging.info(f"Asignando estudiantes Semestre 7: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[6])):
        
        RutaSem7 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_7'
        
        RutaSem7 = os.path.join(RutaSem7, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem7, exist_ok=True)
        
        SplitsDeGrupos[6][i][f'Asignatura{j+1}'] = f"{Codigos7moSem[j]}{i+1}"
        
        carpeta = f"S7_G{i+1}_N{len(SplitsDeGrupos[6][i])}.xlsx"
        
        RutaSem7 = os.path.join(RutaSem7, carpeta)
        
        SplitsDeGrupos[6][i].to_excel(RutaSem7, index=False)
        
        RutaSem7 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_7' 
        
        RutaSem7 = os.path.join(RutaSem7, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem7, exist_ok=True)
        
        carpetacsv = f"S7_G{i+1}_N{len(SplitsDeGrupos[6][i])}.csv" 
        
        RutaSem7 = os.path.join(RutaSem7, carpetacsv) 
        
        SplitsDeGrupos[6][i].to_csv(RutaSem7, index=False)

logging.info("7mo Semestre: Completado")

# Semestre 8

Codigos8voSem = MallaPorSem[7]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[7])):
    
    logging.info(f"Asignando estudiantes Semestre 8: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[7])):
        
        RutaSem8 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_8'
        
        RutaSem8 = os.path.join(RutaSem8, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem8, exist_ok=True)
        
        SplitsDeGrupos[7][i][f'Asignatura{j+1}'] = f"{Codigos8voSem[j]}{i+1}" 
        
        carpeta = f"S8_G{i+1}_N{len(SplitsDeGrupos[7][i])}.xlsx"
        
        RutaSem8 = os.path.join(RutaSem8, carpeta)
        
        SplitsDeGrupos[7][i].to_excel(RutaSem8, index=False)
        
        RutaSem8 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_8' 
        
        RutaSem8 = os.path.join(RutaSem8, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem8, exist_ok=True)
        
        carpetacsv = f"S8_G{i+1}_N{len(SplitsDeGrupos[7][i])}.csv" 
        
        RutaSem8 = os.path.join(RutaSem8, carpetacsv) 
        
        SplitsDeGrupos[7][i].to_csv(RutaSem8, index=False)
        
logging.info("8vo Semestre: Completado")

# Semestre 9

Codigos9noSem = MallaPorSem[8]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[8])):
    
    logging.info(f"Asignando estudiantes Semestre 9: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[8])):
        
        RutaSem9 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_9'
        
        RutaSem9 = os.path.join(RutaSem9, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem9, exist_ok=True)
        
        SplitsDeGrupos[8][i][f'Asignatura{j+1}'] = f"{Codigos9noSem[j]}{i+1}"
        
        carpeta = f"S9_G{i+1}_N{len(SplitsDeGrupos[8][i])}.xlsx"
        
        RutaSem9 = os.path.join(RutaSem9, carpeta)
        
        SplitsDeGrupos[8][i].to_excel(RutaSem9, index=False)
        
        RutaSem9 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_9' 
        
        RutaSem9 = os.path.join(RutaSem9, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem9, exist_ok=True)
        
        carpetacsv = f"S9_G{i+1}_N{len(SplitsDeGrupos[8][i])}.csv" 
        
        RutaSem9 = os.path.join(RutaSem9, carpetacsv) 
        
        SplitsDeGrupos[8][i].to_csv(RutaSem9, index=False)
        
logging.info("9no Semestre: Completado")

# Semestre 10

Codigos10moSem = MallaPorSem[9]['Codigo'].tolist()

for i in range(len(SplitsDeGrupos[9])):
    
    logging.info(f"Asignando estudiantes Semestre 10: Grupo_{i+1}")
    
    for j in range(len(MallaPorSem[9])):
        
        RutaSem10 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_10'
        
        RutaSem10 = os.path.join(RutaSem10, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem10, exist_ok=True)
        
        SplitsDeGrupos[9][i][f'Asignatura{j+1}'] = f"{Codigos10moSem[j]}{i+1}" 
        
        carpeta = f"S10_G{i+1}_N{len(SplitsDeGrupos[9][i])}.xlsx"
        
        RutaSem10 = os.path.join(RutaSem10, carpeta)
        
        SplitsDeGrupos[9][i].to_excel(RutaSem10, index=False)
        
        RutaSem10 = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Semestre_10' 
        
        RutaSem10 = os.path.join(RutaSem10, f"Grupo_{i+1}")
        
        os.makedirs(RutaSem10, exist_ok=True)
        
        carpetacsv = f"S10_G{i+1}_N{len(SplitsDeGrupos[9][i])}.csv" 
        
        RutaSem10 = os.path.join(RutaSem10, carpetacsv) 
        
        SplitsDeGrupos[9][i].to_csv(RutaSem10, index=False)
    
logging.info("10mo Semestre: Completado")

# Excel de planificacion total

PlanCompleto = pd.DataFrame()

PlanCompleto['Nivel'] = MallaCurricular['Semestre']

PlanCompleto['CA'] = MallaCurricular['Codigo'] 

PlanCompleto['HTD'] = MallaCurricular['HTD']

PlanCompleto['HTI'] = MallaCurricular['HTI']

PlanCompleto['NTE'] = ''

for i in range(len(PlanCompleto)):
    
    semestre = (PlanCompleto.at[i, 'Nivel']) - 1
    
    PlanCompleto.at[i, 'NTE'] = NTE[semestre]

PlanCompleto['TCA'] = ''

for i in range(len(PlanCompleto)):
    
    semestre = (PlanCompleto.at[i, 'Nivel']) - 1
    
    PlanCompleto.at[i, 'TCA'] = TCA[semestre]

PlanCompleto['Fecha'] = datetime.today()

logging.info("Plan Completo Definido :D")

RutaPlanCompleto = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Plan_Completo'

os.makedirs(RutaPlanCompleto, exist_ok=True)

excel = 'Plan_completo.xlsx'

RutaPlanCompleto = os.path.join(RutaPlanCompleto, excel)

PlanCompleto.to_excel(RutaPlanCompleto, index=False)

logging.info(f"Archivo excel con la planificación total, creado en {RutaPlanCompleto}")

RutaPlanCompleto = r'C:\Users\Usuario\Desktop\Archivos911Matriculas\Plan_Completo'

csv = 'Plan_completo.csv'

RutaPlanCompleto = os.path.join(RutaPlanCompleto, csv)

PlanCompleto.to_csv(RutaPlanCompleto, index=False)

logging.info(f"Archivo plano CSV con la planificación total, creado en {RutaPlanCompleto}")

# Fin del proceso y agradecimiento

logging.info("911Matriculas termino la carrera, y llego de 1ro")

logging.info("Muchas gracias CastilloEnterprises por su gran participacion en el proyecto")

print('Muchas gracias profe, nos vemos en Simulacion jeje')
print(' <3 '*30)
    




