salas_comuns = [
    "Sala de Aula 01", "Sala de Aula 02", "Sala de Aula 03",
    "Sala de Aula da Pós 01", "Sala de Aula da Pós 02",
    "Sala de Aula 207", "Sala de Aula 206", "Sala de Aula 205", "Sala de Aula 204"
]

laboratorios = [
    "Laboratório de Robótica",
    "Laboratório de Graduação 01",
    "Laboratório de Graduação 02",
    "Laboratório de Graduação 03",
    "Lab. de Circ. Elétricos e Eletrônicos",
    "Laboratório da Pós 01",
    "Laboratório da Pós 02"
]

espacos_auxiliares = [
    "Mini-sala 01",
    "Mini-auditório",
    "Sala de Reuniões",
    "Sala de Reuniões do CEPETEC",
    "Auditório"
]

def sala_eh_laboratorio(sala):
    return sala in laboratorios