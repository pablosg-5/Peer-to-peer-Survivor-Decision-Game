
class Game:
    def __init__(self):
        self.scenarios = [ 
            # NIVEL 0: INTRODUCCIÓN
            {
                "scenario": "Tu barco ha sido sacudido por una tormenta y nadie ha sobrevivido, más que tú y tu compañero. Perdiste al resto de tus compañeros durante el incidente. Cuando recuperas el conocimiento, ambos están varados en la orilla de una isla desconocida. El sol se acerca al horizonte y la incertidumbre se cierne sobre ustedes. Tienen que actuar rápido: buscar comida (1) o buscar refugio (2).",
                "choices": [1, 2]
            },
# ------------------------------
# NIVEL 1
# ------------------------------

            # NIVEL 1A: Ambos buscan comida - Viene de Nivel 0
            {
                "scenario": "Deciden buscar comida juntos. Encuentran algunos frutos en los árboles cercanos, pero algunos parecen venenosos. ¿Comer los frutos (1) o buscar otra fuente de alimento (2)?",
                "choices": [1, 2]
            },

            # NIVEL 1B: Uno busca comida, otro refugio - Viene de Nivel 0
            {
                "scenario": "Uno de ustedes busca comida, mientras el otro busca refugio. El que busca comida encuentra frutos sospechosos, mientras que el otro descubre una cueva con señales de peligro. ¿Deciden comer los frutos (1) o explorar la cueva (2)?",
                "choices": [1, 2]
            },

            # NIVEL 1C: Ambos buscan refugio - Viene de Nivel 0
            {
                "scenario": "Deciden buscar refugio juntos. Encuentran una cueva que parece ser segura, pero escuchan ruidos dentro. ¿Entrar a la cueva (1) o buscar otro lugar (2)?",
                "choices": [1, 2]
            },
# ------------------------------
# NIVEL 2
# ------------------------------

            # NIVEL 2A: Comer los frutos - Viene de Nivel 1A y 1B
            {
                "scenario": "Comen los frutos. Uno de ellos resulta ser venenoso y tu compañero comienza a sentirse mal. ¿Buscar ayuda en la isla (1) o intentar encontrar un antídoto en la naturaleza (2)?",
                "choices": [1, 2]
            },

            # NIVEL 2B: Muerte por envenenamiento - Viene de Nivel 1A
            {
                "scenario": "Algunos frutos resultan ser venenosos. Al ingerirlos quedas envenenado e incapaz de hacer nada. Al intentar buscar otra fuente de alimentos no te das cuenta de que tu compañero está en grave estado, por lo que muere solo. Al seguir buscando alimento caes por un barranco sin darte cuenta y mueres. Final del juego 1",
                "choices": []
            },

            # NIVEL 2C: Buscar otra fuente de alimento - Viene de Nivel 1A
            {
                "scenario": "Deciden buscar otra fuente de alimento. Encuentran un río con peces, pero no tienen herramientas para pescar. ¿Intentar pescar con las manos (1) o seguir buscando (2)?",
                "choices": [1, 2]
            },

            # NIVEL 2D: Entrar a la cueva - Viene de Nivel 1B y 1C
            {
                "scenario": "Entran a la cueva y descubren que está habitada por un oso. El oso los ataca. ¿Intentar defenderse (1) o huir (2)?",
                "choices": [1, 2]
            },

            # NIVEL 2E: Muerte por separación - Viene de Nivel 1C
            {
                "scenario": "El que entra a la cueva es asesinado por un oso, mientras que el otro se pierde en el bosque y fallece en misteriosas condiciones. Final del juego 2",
                "choices": []
            },

            # NIVEL 2F: Muerte dual - Viene de Nivel 1B
            {
                "scenario": "El que entra a la cueva es asesinado por un oso, mientras que el que se come los frutos es envenenado de muerte. Final del juego 3",
                "choices": []
            },

            # NIVEL 2G: Rescate por radio - Viene de Nivel 1C
            {
                "scenario": "Al buscar otro lugar encuentran una especie de refugio abandonado. En él encuentran una radio que los ayuda a comunicar lo sucedido y ser rescatados. Final del juego 4",
                "choices": []
            },
# ------------------------------
# NIVEL 3
# ------------------------------

            # NIVEL 3A: Buscar ayuda - Viene de Nivel 2A
            {
                "scenario": "Ambos deciden buscar ayuda en la isla. Después de caminar un rato, encuentran una choza de un hombre solitario. El hombre les ofrece medicina para el veneno, pero les advierte que tiene un precio. ¿Aceptar la oferta del hombre y ayudarle a recolectar hierbas en un pantano peligroso (1) o rechazar la oferta y seguir buscando una forma alternativa de curarse (2)?",
                "choices": [1, 2]
            },

            # NIVEL 3B: Muerte por barranco - Viene de Nivel 2A
            {
                "scenario": "Al intentar buscar ayuda, se pierde en la jungla y desaparece para siempre. El que buscaba un antídoto natural cae por un barranco sin darse cuenta y muere. Final del juego 5",
                "choices": []
            },

            # NIVEL 3C: Buscar antídoto - Viene de Nivel 2A
            {
                "scenario": "Ambos se adentran en el bosque buscando plantas curativas. Tras varias horas de búsqueda, uno de los personajes cae en un pozo venenoso y el veneno se propaga rápidamente. ¿Intentar salir del pozo a toda prisa, incluso si eso pone en riesgo tu vida (1) o quedarte en el pozo, esperando encontrar una salida más segura mientras los efectos del veneno avanzan (2)?",
                "choices": [1, 2]
            },
            # NIVEL 3D: Pescar con las manos - Viene de Nivel 2C
            {
                "scenario": "Intentan pescar con las manos, pero los peces son demasiado rápidos. Después de varios intentos fallidos, uno de ustedes encuentra una lanza improvisada en la orilla. ¿Intentar pescar con la lanza (1) o seguir buscando otra fuente de alimento (2)?",
                "choices": [1, 2]
            },

            # NIVEL 3E: Muerte por discusión - Viene de Nivel 2C
            {
                "scenario": "Mientras discuten sobre qué hacer, son atacados por un oso que los mata. Final del juego 6",
                "choices": []
            },

            # NIVEL 3F: Muerte por trampa natural - Viene de Nivel 2C
            {
                "scenario": "Ambos caen en una trampa natural mientras exploran y mueren. Final del juego 7",
                "choices": []
            },

            # NIVEL 3G: Defensa exitosa - Viene de Nivel 2D
            {
                "scenario": "Deciden enfrentar al oso con ramas y piedras. La criatura se muestra agresiva, pero con esfuerzo logran ahuyentarlo. Esto les permite encontrar en la cueva una pistola de bengalas que les ayuda a ser rescatados en la playa por un barco. Final del juego 8",
                "choices": []
            },

            # NIVEL 3H: Muerte por huida - Viene de Nivel 2D
            {
                "scenario": "Intentan huir del oso, pero son alcanzados y asesinados brutalmente. Final del juego 9",
                "choices": []
            },

            # NIVEL 3I: Muerte por separación - Viene de Nivel 2D
            {
                "scenario": "Al intentar uno defenderse solo, es asesinado por el oso. El otro, al intentar huir, se tropieza con un hoyo y muere debido al golpe en la cabeza. Final del juego 10",
                "choices": []
            },

# ------------------------------
# NIVEL 4
# ------------------------------

            # NIVEL 4A: Salir del pozo - Viene de Nivel 3C
            {
                "scenario": "Consiguen salir del pozo juntos, pero uno ya se encuentra infectado. ¿Intentar quemar madera y hacer señales en la playa para ser salvados rápidamente (1) o priorizar construir un refugio (2)?",
                "choices": [1, 2]
            },

            # NIVEL 4B: Quedarse en el pozo - Viene de Nivel 3C
            {
                "scenario": "Se quedan en el pozo y descubren un pasadizo oculto con símbolos antiguos. ¿Explorar el pasadizo (1) o ignorarlo y esperar ayuda (2)?",
                "choices": [1, 2]
            },

            # NIVEL 4C: Muerte por opciones distintas - Viene de Nivel 3C
            {
                "scenario": "Al salir del pozo solo, muere al no poder sobrevivir solo en la isla. El que intenta encontrar una salida más segura, muere afectado por el veneno. Final del juego 11",
                "choices": []
            },

            # NIVEL 4D: Muerte en el pantano - Viene de Nivel 3A
            {
                "scenario": "Ambos mueren en el pantano debido a las criaturas que lo habitan y a la falta de conocimiento de la zona. Final del juego 12",
                "choices": []
            },

            # NIVEL 4E: Muerte por veneno - Viene de Nivel 3A
            {
                "scenario": "Al rechazar la oferta del hombre, deciden seguir buscando una forma alternativa de curarse. Sin embargo, el veneno se propaga rápidamente y ambos mueren al amanecer. Final del juego 13",
                "choices": []
            },

            # NIVEL 4F: Muerte por separación - Viene de Nivel 3A
            {
                "scenario": "Al decidir separarse, uno de ustedes cae en una trampa natural y muere en el acto, mientras que el otro, al no conseguir antídoto, muere debido al veneno. Final del juego 14",
                "choices": []
            },

            # NIVEL 4G: Adaptación a la isla - Viene de Nivel 3D
            {
                "scenario": "Consiguen pescar un pez grande y lo cocinan en una fogata improvisada. El alimento les da energía para explorar la isla. Algo que les hace acabar adaptándose a la isla y, debido a la imposibilidad de lograr ser rescatados, acaban quedándose a vivir. Final del juego 15",
                "choices": []
            },

            # NIVEL 4H: Muerte en la jungla - Viene de Nivel 3D
            {
                "scenario": "Al separar vuestros caminos, uno desaparece en extrañas condiciones en la jungla y el otro es atacado por un oso en el bosque, llevando a su muerte. Final del juego 16",
                "choices": []
            },
            # Escenario 4I: Ambos eligen cosas distintas - Viene de 3D
            {
                "scenario": " Al separar vuestros caminos, uno desaparece en extrañas condiciones en la jungla y el otro es atacado por un oso en el bosque llevando a su muerte " +
                "Final del juego 3",
                "choices": []
            },

# ------------------------------
# NIVEL 5
# ------------------------------

            # NIVEL 5A: Muerte por veneno - Viene de Nivel 4A
            {
                "scenario": "El veneno se propaga, y sin antídoto, ambos mueren al amanecer. Final del juego 17",
                "choices": []
            },

            # NIVEL 5B: Muerte por trampa - Viene de Nivel 4A
            {
                "scenario": "Uno cae en una trampa natural y muere en el acto, mientras que el otro, al no conseguir antídoto, muere debido al veneno. Final del juego 18",
                "choices": []
            },

            # NIVEL 5C: Explorar ruinas - Viene de Nivel 4A
            {
                "scenario": "Encuentran una cura natural en una planta y, mientras exploran la isla, descubren unas antiguas ruinas cubiertas de inscripciones extrañas. Una fuerza misteriosa parece emanar del lugar. ¿Explorar las ruinas (1) o alejarse y seguir buscando supervivencia (2)?",
                "choices": [1, 2]
            },

            # NIVEL 5D: Explorar pasadizo - Viene de Nivel 4B
            {
                "scenario": "El pasadizo los lleva a un templo donde una entidad les ofrece inmortalidad... a cambio de sus almas. La entidad del templo exige un sacrificio. ¿Aceptar el trato (1) o rechazarlo y huir (2)?",
                "choices": [1, 2]
            },

            # NIVEL 5E: Muerte por espera - Viene de Nivel 4B
            {
                "scenario": "Ambos mueren debido al veneno y a la espera. Final del juego 19",
                "choices": []
            },

            # NIVEL 5F: Muerte en el pasadizo - Viene de Nivel 4B
            {
                "scenario": "Uno muere debido al veneno y a la espera, el otro muere en extrañas condiciones al comenzar a adentrarse al pasadizo. Final del juego 20",
                "choices": []
            },

# ------------------------------
# NIVEL 6
# ------------------------------

            # NIVEL 6A: Aceptar trato de la entidad - Viene de Nivel 5D
            {
                "scenario": "Uno de ustedes muere, pero el otro obtiene poderes sobrenaturales... y una maldición eterna que le hará vagar por la isla como un fantasma eternamente. Final del juego 21",
                "choices": []
            },

            # NIVEL 6B: Rechazar trato de la entidad - Viene de Nivel 5D
            {
                "scenario": "La entidad se enfada por perturbar su gran letargo y huir, y los convierte en jabalíes salvajes de la isla sin recuerdos. Final del juego 22",
                "choices": []
            },

            # NIVEL 6C: Explorar ruinas - Viene de Nivel 5C
            {
                "scenario": "Al explorar las ruinas, una voz surge en sus mentes, ofreciendo conocimiento prohibido a cambio de permanecer en la isla. Sienten un poder oscuro envolviéndolos. ¿Aceptar el trato (1) o rechazarlo y huir (2)?",
                "choices": [1, 2]
            },

            # NIVEL 6D: Seguir explorando - Viene de Nivel 5C
            {
                "scenario": "Deciden seguir explorando. Encuentran un sendero que parece llevar a una zona más alta de la isla. ¿Seguir el sendero (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },

            # NIVEL 6E: Muerte en las ruinas - Viene de Nivel 5C
            {
                "scenario": "Al separar vuestros caminos, uno desaparece en extrañas condiciones en las ruinas y el otro es atacado por un oso en el bosque, llevando a su muerte. Final del juego 23",
                "choices": []
            },

# ------------------------------
# NIVEL 7
# ------------------------------

            # NIVEL 7A: Aceptar trato de la voz - Viene de Nivel 6C
            {
                "scenario": "Se convierten en guardianes de la isla con todos los conocimientos y secretos de esta. Por tanto, aprenden a vivir en la isla y quedarse para siempre. Final del juego 24",
                "choices": []
            },

            # NIVEL 7B: Rechazar trato de la voz - Viene de Nivel 6C
            {
                "scenario": "Al rechazar el trato, ambos sufren una muerte súbita para poder proteger los secretos de la isla. Final del juego 25",
                "choices": []
            },

            # NIVEL 7C: Traición del guardián - Viene de Nivel 6C
            {
                "scenario": "Al aceptar el trato solo uno, se convierte en el guardián de la isla y asesina a su compañero para proteger los secretos de esta. Final del juego 26",
                "choices": []
            },

            # NIVEL 7D: Seguir el sendero - Viene de Nivel 6D
            {
                "scenario": "Deciden seguir el sendero y encuentran un manantial de agua fresca. ¿Quedarse cerca del manantial (1) o seguir explorando (2)?",
                "choices": [1, 2]
            },

            # NIVEL 7E: Regresar al refugio - Viene de Nivel 6D
            {
                "scenario": "Regresan al refugio y deciden mejorar su estructura. Con el tiempo, se sienten más seguros. Acaban optando por quedarse a vivir en la isla. Final del juego 27",
                "choices": []
            },

            # NIVEL 7F: Explorar y adaptarse - Viene de Nivel 6D
            {
                "scenario": "Al separar vuestros caminos, uno refuerza mejor el refugio, llegando a adaptarse a este y a la isla y quedándose a vivir para siempre. El que decide explorar logra encontrar un barco que lo ayuda a salir de la isla y ser rescatado en alta mar semanas después. Final del juego 28",
                "choices": []
            },

# ------------------------------
# NIVEL 8
# ------------------------------

            # NIVEL 8A: Quedarse cerca del manantial - Viene de Nivel 7D
            {
                "scenario": "Se quedan cerca del manantial y construyen un refugio temporal. El agua fresca les da energía, pero la comida sigue siendo escasa. ¿Buscar comida en los alrededores (1) o intentar pescar (2)?",
                "choices": [1, 2]
            },

            # NIVEL 8B: Rescate final - Viene de Nivel 7D
            {
                "scenario": "Al seguir explorando, encontráis un barco varado en otra playa. Después de varios intentos, logran zarpar y ser rescatados a las pocas semanas en alta mar. Final del juego 29",
                "choices": []
            },

# ------------------------------
# NIVEL 9
# ------------------------------

            # NIVEL 9A: Buscar comida - Viene de Nivel 8A
            {
                "scenario": "Buscan comida en los alrededores y encuentran un árbol con frutas desconocidas. ¿Arriesgarse a comerlas (1) o buscar otra fuente de alimento (2)?",
                "choices": [1, 2]
            },

            # NIVEL 9B: Intentar pescar - Viene de Nivel 8A
            {
                "scenario": "Intentan pescar en el manantial, pero no hay peces. Sin embargo, encuentran un arroyo cercano. ¿Seguir el arroyo (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },

            # NIVEL 9C: Adaptación y rescate - Viene de Nivel 8A
            {
                "scenario": "Al separar vuestros caminos, uno logra adaptarse mejor a la isla mediante la pesca y el uso de utensilios creados a partir de madera, llegando a adaptarse a la isla y quedándose a vivir para siempre. El que decide buscar en los alrededores logra encontrar un barco que lo ayuda a salir de la isla y ser rescatado en alta mar semanas después. Final del juego 30",
                "choices": []
            },

# ------------------------------
# NIVEL 10
# ------------------------------

            # NIVEL 10A: Alucinaciones mortales - Viene de Nivel 9A
            {
                "scenario": "Comen las frutas desconocidas. Lo que les provoca alucinaciones y matarse entre ambos. Final del juego 31",
                "choices": []
            },

            # NIVEL 10B: Adaptación definitiva - Viene de Nivel 9A
            {
                "scenario": "Acaban encontrando unos huevos cerca de un nido de pájaros. La experiencia que vais adquiriendo os hace adaptaros a la isla y quedaros a sobrevivir. Final del juego 32",
                "choices": []
            },

            # NIVEL 10C: Suicidio por alucinaciones - Viene de Nivel 9A
            {
                "scenario": "El que decide comer los frutos sufre grandes alucinaciones, lo que le provoca matar a su compañero y suicidarse después. Final del juego 33",
                "choices": []
            },

            # NIVEL 10D: Explorar cueva oculta - Viene de Nivel 9B
            {
                "scenario": "Siguen el arroyo y encuentran una cascada. Detrás de la cascada, hay una cueva oculta. ¿Explorar la cueva (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },

            # NIVEL 10E: Vida pacífica - Viene de Nivel 9B
            {
                "scenario": "Deciden quedarse en la playa y construir una vida en la isla. Con el tiempo, aprenden a sobrevivir y encuentran paz en su nuevo hogar. Final del juego 34",
                "choices": []
            },
            # Escenario 10F: Ambos elijen regresar al refugio - Viene de 9B
            {
                "scenario": "Deciden quedarse en la playa y construir una vida en la isla. Con el tiempo, aprenden a sobrevivir y encuentran paz en su nuevo hogar. Final del juego 18",                
                "choices": []
            },

# ------------------------------
# NIVEL 11
# ------------------------------

            # NIVEL 11A: Tocar el altar - Viene de Nivel 10D
            {
                "scenario": "Exploran la cueva y encuentran un antiguo altar con símbolos extraños. ¿Tocar el altar (1) o ignorarlo (2)?",
                "choices": [1, 2]
            },

            # NIVEL 11B: Muerte en la cueva - Viene de Nivel 10D
            {
                "scenario": "Al separar vuestros caminos, uno logra adaptarse mejor a la isla al volver al refugio, llegando a adaptarse a la isla y quedándose a vivir para siempre. El que decide explorar la cueva desaparece para siempre. Final del juego 35",
                "choices": []
            },

# ------------------------------
# NIVEL 12
# ------------------------------

            # NIVEL 12A: Conocimiento infinito - Viene de Nivel 11A
            {
                "scenario": "Al tocar el altar, una luz brillante los envuelve. Una voz les ofrece conocimiento infinito a cambio de quedarse. ¿Aceptar (1) o rechazar (2)?",
                "choices": [1, 2]
            },

            # NIVEL 12B: Rescate por fogata - Viene de Nivel 11A
            {
                "scenario": "Deciden ignorar el altar. Al salir ven un barco en el horizonte. ¿Hacer fogata (1) o esperar (2)?",
                "choices": [1, 2]
            },

            # NIVEL 12C: Trampa mortal - Viene de Nivel 11A
            {
                "scenario": "Uno toca el altar y desaparece. El otro intenta ayudarlo y cae en una trampa mortal. Final del juego 36",
                "choices": []
            },

# ------------------------------
# NIVEL 13
# ------------------------------

            # NIVEL 13A: Inmortalidad cósmica - Viene de Nivel 12A
            {
                "scenario": "Son transportados a una dimensión de conocimiento eterno. Donde descubren secretos cósmicos pero pierden su humanidad y se convierten en entidades inmortales. Final del juego 37",
                "choices": []
            },

            # NIVEL 13B: Escape de la cueva - Viene de Nivel 12A
            {
                "scenario": "La entidad se enfurece. La cueva colapsa. ¿Correr (1) o buscar salida alternativa (2)?",
                "choices": [1, 2]
            },

            # NIVEL 13C: Rescate final - Viene de Nivel 12B
            {
                "scenario": "El barco los ve y consiguen ser rescatados. Final del juego 38",
                "choices": []
            },

# ------------------------------
# NIVEL 14
# ------------------------------

            # NIVEL 14A: Desierto árido - Viene de Nivel 13B
            {
                "scenario": "Logran escapar, pero el exterior ahora es un desierto árido, sin rastros de vida. Final del juego 39",
                "choices": []
            },

            # NIVEL 14B: Rescate en alta mar - Viene de Nivel 13B
            {
                "scenario": "Buscan otra salida y encuentran un túnel que los lleva a una playa desierta. Intentan construir una balsa con los restos del naufragio. Después de varios intentos, logran zarpar y ser rescatados a las pocas semanas en alta mar. Final del juego 40",
                "choices": []
            },

            # NIVEL 14C: Muerte en la cueva - Viene de Nivel 13B
            {
                "scenario": "Al no ponerse de acuerdo, son sepultados por las piedras que van cayendo, dejando sus cuerpos sellados con la cueva. Final del juego 41",
                "choices": []
            }
        ]
        
        self.current_scenario = 0
        self.player_decision = None
        self.other_player_decision = None
        self.game_over = False
        self.game_result = None

    def process_decisions(self):
        if self.game_over:
            return

        # Verificar si es escenario final
        if not self.scenarios[self.current_scenario]["choices"]:
            self.game_result = self.scenarios[self.current_scenario]["scenario"]
            self.game_over = True
            return

        # Diccionario de transiciones CORREGIDO
        transitions = {
            # NIVEL 0
            0: {
                (1, 1): 1, (2, 2): 3, (1, 2): 2, (2, 1): 2
            },
            # NIVEL 1A
            1: {
                (1, 1): 4, (2, 2): 6, (1, 2): 5, (2, 1): 5
            },
            # NIVEL 1B
            2: {
                (1, 1): 4, (2, 2): 7, (1, 2): 9, (2, 1): 9
            },
            # NIVEL 1C
            3: {
                (1, 1): 7, (2, 2): 10, (1, 2): 8, (2, 1): 8
            },
            # NIVEL 2A
            4: {
                (1, 1): 11, (2, 2): 13, (1, 2): 12, (2, 1): 12
            },
            # NIVEL 2C
            6: {
                (1, 1): 14, (2, 2): 16, (1, 2): 15, (2, 1): 15
            },
            # NIVEL 2D
            7: {
                (1, 1): 17, (2, 2): 18, (1, 2): 19, (2, 1): 19
            },
            # NIVEL 3A
            11: {
                (1, 1): 23, (2, 2): 24, (1, 2): 25, (2, 1): 25
            },
            # NIVEL 3C
            13: {
                (1, 1): 20, (2, 2): 21, (1, 2): 22, (2, 1): 22
            },
            # NIVEL 3D
            14: {
                (1, 1): 26, (2, 2): 27, (1, 2): 28, (2, 1): 28
            },
            # NIVEL 4A
            20: {
                (1, 1): 29, (2, 2): 30, (1, 2): 31, (2, 1): 31
            },
            # NIVEL 4B
            21: {
                (1, 1): 32, (2, 2): 33, (1, 2): 34, (2, 1): 34
            },
            # NIVEL 5C
            31: {
                (1, 1): 37, (2, 2): 38, (1, 2): 39, (2, 1): 39
            },
            # NIVEL 5D
            32: {
                (1, 1): 35, (2, 2): 36, (1, 2): 36, (2, 1): 36
            },
            # NIVEL 6C
            37: {
                (1, 1): 40, (2, 2): 41, (1, 2): 42, (2, 1): 42
            },
            # NIVEL 6D
            38: {
                (1, 1): 43, (2, 2): 44, (1, 2): 45, (2, 1): 45
            },
            # NIVEL 7D
            43: {
                (1, 1): 46, (2, 2): 47, (1, 2): 45, (2, 1): 45
            },
            # NIVEL 8A
            46: {
                (1, 1): 48, (2, 2): 49, (1, 2): 50, (2, 1): 50
            },
            # NIVEL 9A
            48: {
                (1, 1): 51, (2, 2): 52, (1, 2): 53, (2, 1): 53
            },
            # NIVEL 9B
            49: {
                (1, 1): 54, (2, 2): 55, (1, 2): 56, (2, 1): 56
            },
            # NIVEL 10D
            54: {
                (1, 1): 57, (2, 2): 58, (1, 2): 59, (2, 1): 59
            },
            # NIVEL 11A
            57: {
                (1, 1): 60, (2, 2): 61, (1, 2): 62, (2, 1): 62
            },
            # NIVEL 12A
            59: {
                (1, 1): 63, (2, 2): 64, (1, 2): 65, (2, 1): 65
            },
            # NIVEL 13B
            63: {
                (1, 1): 69, (2, 2): 70, (1, 2): 71, (2, 1): 71
            }
        }

        key = (self.player_decision, self.other_player_decision)
        next_scenario = transitions.get(self.current_scenario, {}).get(key, -1)

        # Verificar si el escenario es válido
        if next_scenario == -1 or next_scenario >= len(self.scenarios):
            self.game_result = "Error: Transición no válida"
            self.game_over = True
        else:
            self.current_scenario = next_scenario

        # Verificar si es final
        if not self.scenarios[self.current_scenario]["choices"]:
            self.game_result = self.scenarios[self.current_scenario]["scenario"]
            self.game_over = True

        self.reset_decisions()


    def get_scenario(self, index=None):
        """Devuelve el escenario actual o resultado final"""
        if self.game_over:
            return {
                "scenario": self.game_result,
                "choices": [],
                "final": True
            }
        return self.scenarios[self.current_scenario]
    
    def _get_valid_decision(self, choices):
        """Valida la entrada del usuario (método faltante)"""
        while True:
            try:
                decision = int(input(f"Elige una opción {choices}: "))
                if decision in choices:
                    return decision
                print(f"Opción inválida. Por favor elige entre {choices}")
            except ValueError:
                print("Entrada inválida. Debes ingresar un número.")

    def reset_decisions(self):
        """Reinicia las decisiones para el siguiente escenario"""
        self.player_decision = None
        self.other_player_decision = None

    def input_decision(self, is_player=True):
        """Maneja la entrada del jugador con validación"""
        if self.game_over:
            return
        
        current = self.scenarios[self.current_scenario]
        choices = current["choices"]
        
        if not choices:  # Escenario final
            return
        
        decision = self._get_valid_decision(choices)
        
        if is_player:
            self.player_decision = decision
        else:
            self.other_player_decision = decision

    def get_game_state(self):
        """Devuelve el estado actual del juego"""
        return {
            "current_scenario": self.current_scenario,
            "game_over": self.game_over,
            "result": self.game_result
        }