import random
import itertools

DAYS_OF_WEEK = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
TIME_SLOTS = [
    "7:30-8:20",   # M2
    "9:20-10:10",  # M4
    "11:10-12:00", # M6
    "12:00-12:50", # T1
    "13:30-14:20", # T2
    "15:20-16:10", # T4
    "16:10-17:00",  # T5
    "17:10-18:00",  # T6
]

class Course:
    """Representa um curso com seu nome e o número de sessões semanais necessárias."""
    def __init__(self, name, sessions_per_week):
        self.name = name
        self.sessions_per_week = sessions_per_week

    def __repr__(self):
        return f"Course(name='{self.name}', sessions={self.sessions_per_week})"

class Teacher:
    """Representa um professor com seu nome e os cursos que ele pode lecionar."""
    def __init__(self, name, courses_can_teach):
        self.name = name
        self.courses_can_teach = courses_can_teach # Lista de nomes de cursos (strings)

    def __repr__(self):
        return f"Teacher(name='{self.name}')"

class Room:
    """Representa uma sala de aula com seu nome e capacidade."""
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return f"Room(name='{self.name}', capacity={self.capacity})"

class Slot:
    """Representa um slot de tempo específico em um dia específico."""
    def __init__(self, day, time):
        self.day = day
        self.time = time

    def __repr__(self):
        return f"Slot(day='{self.day}', time='{self.time}')"

    def __eq__(self, other):
        return isinstance(other, Slot) and self.day == other.day and self.time == other.time

    def __hash__(self):
        return hash((self.day, self.time))

class GeneticScheduler:
    """
    Resolve o problema de agendamento escolar usando um Algoritmo Genético.

    Um "cromossomo" (indivíduo na população) é um dicionário representando
    uma agenda completa: {Slot: (Course, Teacher, Room) ou None}.
    """
    def __init__(self, courses, teachers, rooms, days=DAYS_OF_WEEK, time_slots=TIME_SLOTS):
        self.courses = courses
        self.teachers = teachers
        self.rooms = rooms
        self.days = days
        self.time_slots = time_slots
        self.all_slots = [Slot(day, time) for day in days for time in time_slots]
        self.course_names = [c.name for c in courses]
        self.teacher_names = [t.name for t in teachers]
        self.room_names = [r.name for r in rooms]

        # Mapeia nomes de cursos para objetos Course para fácil consulta
        self.course_map = {c.name: c for c in courses}
        # Mapeia nomes de professores para objetos Teacher
        self.teacher_map = {t.name: t for t in teachers}
        # Mapeia nomes de salas para objetos Room
        self.room_map = {r.name: r for r in rooms}

        # Parâmetros para o algoritmo genético
        self.population_size = 100
        self.num_generations = 1000
        self.mutation_rate = 0.05
        self.elitism_rate = 0.1 # Porcentagem dos melhores indivíduos a serem transferidos diretamente

    def _generate_random_chromosome(self):
        """
        Gera uma única agenda aleatória (cromossomo).
        Cada slot é atribuído a uma combinação aleatória (curso, professor, sala) ou deixado vazio.
        """
        chromosome = {}
        possible_assignments = list(itertools.product(self.courses, self.teachers, self.rooms))
        # Adiciona uma opção None para representar um slot vazio
        possible_assignments.append(None)

        for slot in self.all_slots:
            # Atribui aleatoriamente uma combinação válida ou deixa vazio
            assignment = random.choice(possible_assignments)
            if assignment is not None:
                course, teacher, room = assignment
                # Verificação básica de expertise do professor durante a geração inicial
                if course.name not in teacher.courses_can_teach:
                    assignment = None # Invalida se o professor não pode lecionar
            chromosome[slot] = assignment
        return chromosome

    def _initialize_population(self):
        """Cria a população inicial de cromossomos aleatórios."""
        return [self._generate_random_chromosome() for _ in range(self.population_size)]

    def _calculate_fitness(self, chromosome):
        """
        Calcula a aptidão de um dado cromossomo (agenda).
        Uma pontuação de aptidão mais baixa é melhor (menos violações de restrições).

        Critérios de aptidão (penalidades):
        1. Conflito de professor: Mesmo professor atribuído a várias turmas ao mesmo tempo.
        2. Conflito de sala: Mesma sala atribuída a várias turmas ao mesmo tempo.
        3. Expertise do professor: Professor atribuído a um curso que não pode lecionar.
        4. Contagem de sessões do curso: Não atender ao número necessário de sessões para um curso.
        """
        fitness = 0
        teacher_busy_slots = {} # {teacher_name: [slot1, slot2, ...]}
        room_busy_slots = {}    # {room_name: [slot1, slot2, ...]}
        course_session_counts = {course.name: 0 for course in self.courses}

        # Inicializa slots ocupados para todos os professores e salas
        for teacher_name in self.teacher_names:
            teacher_busy_slots[teacher_name] = []
        for room_name in self.room_names:
            room_busy_slots[room_name] = []

        for slot, assignment in chromosome.items():
            if assignment is None:
                continue # Slot vazio, sem penalidades

            course, teacher, room = assignment

            # Penalidade 1: Conflito de professor
            if slot in teacher_busy_slots[teacher.name]:
                fitness += 10 # Alta penalidade para o professor estar em dois lugares
            else:
                teacher_busy_slots[teacher.name].append(slot)

            # Penalidade 2: Conflito de sala
            if slot in room_busy_slots[room.name]:
                fitness += 10 # Alta penalidade para a sala ser usada duas vezes
            else:
                room_busy_slots[room.name].append(slot)

            # Penalidade 3: Expertise do professor
            if course.name not in teacher.courses_can_teach:
                fitness += 5 # Penalidade moderada por expertise errada

            # Atualiza a contagem de sessões do curso
            course_session_counts[course.name] += 1

        # Penalidade 4: Contagem de sessões do curso (restrição suave, pode ser menor ou maior)
        for course in self.courses:
            diff = abs(course_session_counts[course.name] - course.sessions_per_week)
            fitness += diff * 2 # Penalidade por não atender às sessões necessárias

        return fitness

    def _select_parents(self, population_with_fitness):
        """
        Seleciona dois pais usando seleção por torneio.
        Um pequeno grupo de indivíduos é escolhido aleatoriamente, e o melhor desse grupo vence.
        """
        tournament_size = 5
        parents = []
        for _ in range(2): # Seleciona dois pais
            tournament_contenders = random.sample(population_with_fitness, min(tournament_size, len(population_with_fitness)))
            best_contender = min(tournament_contenders, key=lambda x: x[1]) # Seleciona o que tem a menor aptidão
            parents.append(best_contender[0]) # Adiciona o cromossomo (agenda)
        return parents[0], parents[1]

    def _crossover(self, parent1, parent2):
        """
        Realiza o cruzamento de ponto único em dois cromossomos pais.
        Divide a agenda em um ponto aleatório e combina as partes.
        """
        crossover_point = random.randint(1, len(self.all_slots) - 1)
        
        child1 = {}
        child2 = {}

        # Converte dicionários em listas de (slot, atribuição) para facilitar o fatiamento
        parent1_items = list(parent1.items())
        parent2_items = list(parent2.items())

        # Filho 1: primeira parte do pai1, segunda parte do pai2
        for i in range(len(self.all_slots)):
            slot, assignment = parent1_items[i]
            if i < crossover_point:
                child1[slot] = assignment
            else:
                child1[slot] = parent2_items[i][1] # Obtém atribuição do pai2

        # Filho 2: primeira parte do pai2, segunda parte do pai1
        for i in range(len(self.all_slots)):
            slot, assignment = parent2_items[i]
            if i < crossover_point:
                child2[slot] = assignment
            else:
                child2[slot] = parent1_items[i][1] # Obtém atribuição do pai1

        return child1, child2

    def _mutate(self, chromosome):
        """
        Muta um cromossomo alterando aleatoriamente uma atribuição em um slot.
        A atribuição de um slot pode ser alterada para outra atribuição válida aleatória
        ou definida como None (vazia).
        """
        if random.random() < self.mutation_rate:
            # Seleciona um slot aleatório para mutar
            slot_to_mutate = random.choice(self.all_slots)

            # Gera uma nova atribuição aleatória para este slot
            possible_assignments = list(itertools.product(self.courses, self.teachers, self.rooms))
            possible_assignments.append(None) # Opção para deixá-lo vazio

            new_assignment = random.choice(possible_assignments)
            
            # Validação simples para expertise do professor durante a mutação
            if new_assignment is not None:
                course, teacher, room = new_assignment
                if course.name not in teacher.courses_can_teach:
                    new_assignment = None # Se inválido, padrão para vazio

            chromosome[slot_to_mutate] = new_assignment
        return chromosome

    def solve(self):
        """
        Executa o algoritmo genético para encontrar uma agenda escolar ótima.
        Retorna a melhor agenda encontrada ou None se nenhuma agenda satisfatória for encontrada.
        """
        population = self._initialize_population()
        
        # Acompanha a melhor agenda encontrada até agora
        best_schedule = None
        min_fitness = float('inf')

        print(f"Iniciando Algoritmo Genético por {self.num_generations} gerações...")

        for generation in range(self.num_generations):
            # 1. Avalia a aptidão para a população atual
            population_with_fitness = [(chromo, self._calculate_fitness(chromo)) for chromo in population]
            
            # Ordena por aptidão (o menor é o melhor)
            population_with_fitness.sort(key=lambda x: x[1])

            # Atualiza a melhor agenda encontrada
            current_best_fitness = population_with_fitness[0][1]
            if current_best_fitness < min_fitness:
                min_fitness = current_best_fitness
                best_schedule = population_with_fitness[0][0]

            # Se uma agenda perfeita (aptidão 0) for encontrada, retorna-a
            if min_fitness == 0:
                print(f"Agenda ótima encontrada na geração {generation}!")
                return best_schedule

            # Imprime o progresso
            if generation % 100 == 0:
                print(f"Geração {generation}: Melhor Aptidão = {min_fitness}")

            # 2. Elitismo: Transfere os melhores indivíduos diretamente para a próxima geração
            num_elites = int(self.population_size * self.elitism_rate)
            new_population = [chromo for chromo, _ in population_with_fitness[:num_elites]]

            # 3. Gera descendentes para o resto da população
            while len(new_population) < self.population_size:
                parent1, parent2 = self._select_parents(population_with_fitness)
                child1, child2 = self._crossover(parent1, parent2)
                
                # Muta os filhos
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)

            population = new_population

        print(f"Algoritmo Genético finalizado. Melhor aptidão encontrada: {min_fitness}")
        return best_schedule if min_fitness == 0 else None # Retorna apenas se for perfeito, ou modifica para retornar o melhor encontrado

    def print_schedule(self, schedule):
        """Imprime a agenda gerada em um formato legível."""
        if not schedule:
            print("Nenhuma agenda pôde ser gerada ou a melhor encontrada não foi ótima.")
            return

        # Cria uma visualização estruturada da agenda
        daily_schedule = {day: {time: "Livre" for time in self.time_slots} for day in self.days}

        for slot, assignment in schedule.items():
            if assignment:
                course, teacher, room = assignment
                daily_schedule[slot.day][slot.time] = f"{course.name} (Professor: {teacher.name}, Sala: {room.name})"
            else:
                daily_schedule[slot.day][slot.time] = "Livre"

        print("\n--- Horário Escolar Gerado ---")
        for day in self.days:
            print(f"\n{day}:")
            for time in self.time_slots:
                print(f"  {time}: {daily_schedule[day][time]}")
        print("\n---------------------------------")


if __name__ == "__main__":
    all_courses = [
        # 1º Período
        Course("Programação 1", 4),
        Course("Lógica para Computação", 4),
        Course("Computação, Sociedade e Ética", 4),
        Course("Matemática Discreta", 4),
        Course("Cálculo Diferencial e Integral", 8),  # 144h

        # 2º Período
        Course("Estrutura de Dados", 4),
        Course("Banco de Dados", 4),
        Course("Organização e Arquitetura de Computadores", 4),
        Course("Geometria Analítica", 4),

        # 3º Período
        Course("Redes de Computadores", 4),
        Course("Teoria dos Grafos", 4),
        Course("Probabilidade e Estatística", 4),
        Course("Álgebra Linear", 4),

        # 4º Período
        Course("Programação 2", 4),
        Course("Programação 3", 4),
        Course("Projeto e Análise de Algoritmos", 4),
        Course("Teoria da Computação", 4),

        # 5º Período
        Course("Sistemas Operacionais", 4),
        Course("Compiladores", 4),
        Course("Inteligência Artificial", 4),
        Course("Computação Gráfica", 4),

        # 6º Período
        Course("Projeto e Desenvolvimento de Sistemas", 16),  # 288h

        # 7º Período
        Course("Metodologia de Pesquisa e Trabalho Individual", 4),
        Course("Noções de Direito", 4),

        # Ênfases 
        Course("Cálculo 3", 4),
        Course("Conceitos de Linguagem de Programação", 4),
        Course("Aprendizagem de Máquina", 4),
        Course("Sistemas Digitais", 4),
        Course("Sistemas Distribuídos", 4),
        Course("Redes Neurais e Aprendizado Profundo", 4),
        Course("FPGA", 4),
        Course("Interação Homem-Máquina", 4),
        Course("Processamento Digital de Imagens", 4),
        Course("Computação Evolucionária", 4),
        Course("Sistemas Embarcados", 4),
        Course("Gerência de Projeto", 4),
        Course("Visão Computacional", 4),
        Course("Ciência de Dados", 4),
        Course("Microcontroladores e Aplicações", 4),
        Course("Segurança de Sistemas Computacionais", 4),
        Course("Pesquisa Operacional", 4),
    ]

    # 2. Define os professores em uma lista, relacionando apenas aos cursos existentes em all_courses
    all_teachers = [
        Teacher("Almir Pereira Guimarães", [
            "Redes de Computadores", "Sistemas Distribuídos"
        ]),
        Teacher("André Luiz Lins de Aquino", [
            "Redes de Computadores", "Projeto e Análise de Algoritmos"
        ]),
        Teacher("Arturo Hernández Domínguez", [
            "Programação 3", "Projeto e Teoria de Linguagens", "Engenharia de Software", "Compiladores"
        ]),
        Teacher("Aydano Pamponet Machado", [
            "Aprendizagem de Máquina", "Inteligência Artificial", "Introdução à Computação"
        ]),
        Teacher("Baldoino Fonseca dos Santos Neto", [
            "Programação 2", "Lógica para Computação", "Sistemas Digitais", "Inteligência Artificial"
        ]),
        Teacher("Bruno Almeida Pimentel", [
            "Inteligência Artificial", "Aprendizagem de Máquina"
        ]),
        Teacher("Bruno Costa e Silva Nogueira", [
            "Organização e Arquitetura de Computadores", "Pesquisa Operacional"
        ]),
        Teacher("Cid Cavalcanti de Albuquerque", [
            "Noções de Direito", "Introdução à Computação"
        ]),
        Teacher("Davi Bibiano Brito", [
            "Sistemas Digitais"
        ]),
        Teacher("Erick de Andrade Barboza", [
            "Organização e Arquitetura de Computadores", "Microcontroladores e Aplicações"
        ]),
        Teacher("Evandro de Barros Costa", [
            "Inteligência Artificial",
        ]),
        Teacher("Fábio José Coutinho da Silva", [
            "Banco de Dados", "Sistemas Distribuídos", "Ciência de Dados", "Conceitos de Linguagem de Programação"
        ]),
        Teacher("Fábio Paraguaçu Duarte da Costa", [
            "Lógica para Computação", "Teoria da Computação", "Inteligência Artificial", "Interação Homem-Máquina"
        ]),
        Teacher("Glauber Rodrigues Leite", [
           "Álgebra Linear"
        ]),
        Teacher("Ig Ibert Bittencourt Santana Pinto", [
            "Introdução à Computação"
        ]),
        Teacher("Leandro Dias da Silva", [
            "Sistemas Operacionais", "Redes de Computadores", "Sistemas Embarcados"
        ]),
        Teacher("Leandro Melo de Sales", [
            "Redes de Computadores", "Sistemas Operacionais", "Sistemas Distribuídos"
        ]),
        Teacher("Marcelo Costa Oliveira", [
            "Processamento Digital de Imagens", "Computação Gráfica", "Ciência de Dados"
        ]),
        Teacher("Márcio de Medeiros Ribeiro", [
            "Estrutura de Dados"
        ]),
        Teacher("Mário Hozano Lucas de Souza", [
            "Programação 3"
        ]),
        Teacher("Petrúcio Antônio Medeiros Barros", [
           "Probabilidade e Estatística", "Computação, Sociedade e Ética"
        ]),
        Teacher("Ranilson Oscar Araújo Paiva", [
          "Programação 3", "Projeto e Desenvolvimento de Sistemas", "Programação 1"
        ]),
        Teacher("Rafael de Amorim Silva", [
            "Gerência de Projeto", "Computação, Sociedade e Ética", "Introdução à Computação", "Conceitos de Linguagem de Programação"
        ]),
        Teacher("Rian Gabriel Santos Pinheiro", [
            "Projeto e Análise de Algoritmos", "Teoria dos Grafos", "Pesquisa Operacional", "Teoria da Computação"
        ]),
        Teacher("Roberta Vilhena Vieira Lopes", [
            "Projeto e Teoria de Linguagens", "Introdução à Computação", "Computação Evolucionária"
        ]),
        Teacher("Rodrigo de Barros Paes", [
            "Programação 1", "Programação 3", "Projeto e Desenvolvimento de Sistemas"
        ]),
        Teacher("Thales Miranda de Almeida Vieira", [
            "Aprendizagem de Máquina", "Redes Neurais e Aprendizado Profundo", "Visão Computacional"
        ]),
        Teacher("Tiago Alves de Almeida", [
            "Cálculo Diferencial e Integral", "Geometria Analítica"
        ]),
        Teacher("Xu Yang", [
            "Cálculo Diferencial e Integral", "Teoria dos Grafos"
        ]),
        Teacher("Willy Carvalho Tiengo", [
            "Sistemas Operacionais", "Engenharia de Software", "Redes de Computadores", "Projeto e Desenvolvimento de Sistemas"
        ]),
        Teacher("LUCAS BENEVIDES VIANA DE AMORIM", [
            "Organização e Arquitetura de Computadores", 
        ]),
        Teacher("TIAGO FIGUEIREDO VIEIRA", [
            "Redes Neurais e Aprendizado Profundo", "Processamento Digital de Imagens"
        ]),
        Teacher("MARIA CRISTINA TENORIO CAVALCANTE ESCARPINI", [
            "Banco de Dados", "Computação Evolucionária", 
        ]),
    ]

    cursos_primeiros_4_periodos = [
        c.name for c in all_courses[:17] 
    ]

    # Adiciona cursos dos primeiros 4 períodos a todos os professores
    for prof in all_teachers:
        prof.courses_can_teach = list(set(prof.courses_can_teach) | set(cursos_primeiros_4_periodos))

    # 3. Define suas salas
    sala_1 = Room("Sala 1", 30)
    sala_2 = Room("Sala 2", 30)
    lab_1 = Room("Laboratório 1", 65)
    lab_2 = Room("Laboratório 2", 35)
    auditorio = Room("Auditório", 50)

    all_rooms = [sala_1, sala_2, lab_1, auditorio]

    # 4. Cria a instância do agendador
    # Podem ajustar os parâmetros do algoritmo genético aqui
    scheduler = GeneticScheduler(all_courses, all_teachers, all_rooms)
    scheduler.population_size = 200 
    scheduler.num_generations = 2000 
    scheduler.mutation_rate = 0.1 

    # 5. Resolve a agenda
    print("Tentando gerar agenda usando Algoritmo Genético...")
    found_schedule = scheduler.solve()

    # 6. Imprime o resultado
    if found_schedule:
        print("\nAlgoritmo Genético: Horário gerado com sucesso!")
        scheduler.print_schedule(found_schedule)
    else:
        print("\nAlgoritmo Genético: Falha ao encontrar um horário ótimo (aptidão 0).")
        print("Considere ajustar os cursos, professores, salas, horários ou parâmetros do GA.")
        # Opcionalmente, imprime a melhor agenda não ótima encontrada
        # print("\nMelhor horário não ótimo encontrado:")
        # scheduler.print_schedule(scheduler.best_schedule_overall) # Precisa armazenar isso em solve()
