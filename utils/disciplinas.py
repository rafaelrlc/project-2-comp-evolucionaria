disciplinas = [
    # obrigatorias
    {"codigo": "COMP359", "nome": "Programação 1", "periodo": 1, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP360", "nome": "Lógica para Computação", "periodo": 1, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP361", "nome": "Computação, Sociedade e Ética", "periodo": 1, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP362", "nome": "Matemática Discreta", "periodo": 1, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP363", "nome": "Cálculo Diferencial e Integral", "periodo": 1, "carga_horaria": 144, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP364", "nome": "Estrutura de Dados", "periodo": 2, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP359"]},
    {"codigo": "COMP365", "nome": "Banco de Dados", "periodo": 2, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP366", "nome": "Organização e Arquitetura de Computadores", "periodo": 2, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP367", "nome": "Geometria Analítica", "periodo": 2, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP368", "nome": "Redes de Computadores", "periodo": 3, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP359"]},
    {"codigo": "COMP369", "nome": "Teoria dos Grafos", "periodo": 3, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP364", "COMP362"]},
    {"codigo": "COMP370", "nome": "Probabilidade e Estatística", "periodo": 3, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP363"]},
    {"codigo": "COMP371", "nome": "Álgebra Linear", "periodo": 3, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP367"]},
    {"codigo": "COMP372", "nome": "Programação 2", "periodo": 4, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP364", "COMP365", "COMP368"]},
    {"codigo": "COMP373", "nome": "Programação 3", "periodo": 4, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP372"]},
    {"codigo": "COMP374", "nome": "Projeto e Análise de Algoritmos", "periodo": 4, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP369"]},
    {"codigo": "COMP376", "nome": "Teoria da Computação", "periodo": 4, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP378", "nome": "Sistemas Operacionais", "periodo": 5, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP366"]},
    {"codigo": "COMP379", "nome": "Compiladores", "periodo": 5, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP376"]},
    {"codigo": "COMP380", "nome": "Inteligência Artificial", "periodo": 5, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP374"]},
    {"codigo": "COMP381", "nome": "Computação Gráfica", "periodo": 5, "carga_horaria": 72, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": ["COMP371"]},
    {"codigo": "COMP382", "nome": "Projeto e Desenvolvimento de Sistemas", "periodo": 6, "carga_horaria": 288, "laboratorio": True, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP386", "nome": "Metodologia de Pesquisa e Trabalho Individual", "periodo": 7, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},
    {"codigo": "COMP387", "nome": "Noções de Direito", "periodo": 7, "carga_horaria": 72, "laboratorio": False, "tipo": "Obrigatória", "enfase": None, "prerequisitos": []},

    # enfases
    # sistemas de computação
    {"codigo": "COMP388", "nome": "Sistemas Embarcados", "periodo": 7, "carga_horaria": 72, "laboratorio": True, "tipo": "Ênfase", "enfase": ["Sistemas de Computação"], "prerequisitos": ["COMP366"]},
    {"codigo": "COMP389", "nome": "Sistemas Distribuídos", "periodo": 8, "carga_horaria": 72, "laboratorio": False, "tipo": "Ênfase", "enfase": ["Sistemas de Computação"], "prerequisitos": ["COMP378"]},

    # sistemas de informação
    {"codigo": "COMP390", "nome": "Engenharia de Software", "periodo": 7, "carga_horaria": 72, "laboratorio": False, "tipo": "Ênfase", "enfase": ["Sistemas de Informação"], "prerequisitos": ["COMP382"]},
    {"codigo": "COMP391", "nome": "Mineração de Dados", "periodo": 8, "carga_horaria": 72, "laboratorio": False, "tipo": "Ênfase", "enfase": ["Sistemas de Informação"], "prerequisitos": ["COMP370", "COMP365"]},

    # computação visual
    {"codigo": "COMP392", "nome": "Processamento de Imagens", "periodo": 7, "carga_horaria": 72, "laboratorio": True, "tipo": "Ênfase", "enfase": ["Computação Visual"], "prerequisitos": ["COMP381"]},
    {"codigo": "COMP400", "nome": "Visão Computacional", "periodo": 8, "carga_horaria": 72, "laboratorio": True, "tipo": "Ênfase", "enfase": ["Computação Visual"], "prerequisitos": ["COMP392"]},

    # sistemas inteligentes
    {"codigo": "COMP393", "nome": "Redes Neurais e Aprendizado Profundo", "periodo": 7, "carga_horaria": 72, "laboratorio": False, "tipo": "Ênfase", "enfase": ["Sistemas Inteligentes"], "prerequisitos": ["COMP380"]},
    {"codigo": "COMP394", "nome": "Raciocínio Automático", "periodo": 8, "carga_horaria": 72, "laboratorio": False, "tipo": "Ênfase", "enfase": ["Sistemas Inteligentes"], "prerequisitos": ["COMP393"]}
]
