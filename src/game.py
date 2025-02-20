class Game:
    def __init__(self):
        # Lista de escenarios (puedes agregar más o modificar los existentes)
        self.scenarios = [
            # Escenario 0: Introducción
            {
                "scenario": "Tu barco ha sido sacudido por una tormenta y nadie ha sobrevivido, más que tú y tu compañero. " +
                "Perdiste al resto de tus compañeros durante el incidente. Cuando recuperas el conocimiento, " +
                "ambos están varados en la orilla de una isla desconocida. El sol se acerca al horizonte y la incertidumbre " +
                "se cierne sobre ustedes. Tienen que actuar rápido: buscar comida (1) o buscar refugio (2).",
                "choices": [1, 2]
            },
            # Escenario 1A: Ambos buscan comida
            {
                "scenario": "Deciden buscar comida juntos. Encuentran algunos frutos en los árboles cercanos, pero algunos parecen venenosos. " +
                "¿Comer los frutos (1) o buscar otra fuente de alimento (2)?",
                "choices": [1, 2]
            },
            # Escenario 1B: Uno busca comida, otro refugio
            {
                "scenario": "Uno de ustedes busca comida, mientras el otro busca refugio. El que busca comida encuentra frutos sospechosos, " +
                "mientras que el otro descubre una cueva con señales de peligro. ¿Deciden comer los frutos (1) o explorar la cueva (2)?",
                "choices": [1, 2]
            },
            # Escenario 1C: Ambos buscan refugio
            {
                "scenario": "Deciden buscar refugio juntos. Encuentran una cueva que parece ser segura, pero escuchan ruidos dentro. " +
                "¿Entrar a la cueva (1) o buscar otro lugar (2)?",
                "choices": [1, 2]
            },
            # Escenario 2A: Comer los frutos - Viene de 1A y 1B
            {
                "scenario": "Comen los frutos. Uno de ellos resulta ser venenoso y tu compañero comienza a sentirse mal. " +
                "¿Buscar ayuda en la isla (1) o intentar encontrar un antídoto en la naturaleza (2)?",
                "choices": [1, 2]
            },
            # Escenario 2B: Uno come los frutos otro busca otra fuente de alimento - Viene de 1A
            {
                "scenario": "Algunos frutos resultan ser venenosos, al ingerirlos quedas envenendado e incapaz de hacer nada. Al intentar buscar otra fuente de alimentos no te das cuenta de que tu compañero esta en grave estado, por tanto muere solo. Al seguir buscando alimento caes por un barranco sin darte cuenta y mueres " +
                "Final del juego 1",
                "choices": []
            },

            # Escenario 2C: Buscar otra fuente de alimento - Viene de 1A
            {
                "scenario": "Deciden buscar otra fuente de alimento. Encuentran un río con peces, pero no tienen herramientas para pescar. " +
                "¿Intentar pescar con las manos (1) o seguir buscando (2)?",
                "choices": [1, 2]
            },
            # Escenario 3A: Ambos buscan ayuda en la isla - Viene de 2A
            {
                "scenario": "Ambos deciden buscar ayuda en la isla. Después de caminar un rato, encuentran una choza de un hombre solitario. El hombre les ofrece medicina para el veneno, pero les advierte que tiene un precio. " +
                "¿Aceptar la oferta del hombre y ayudarle a recolectar hierbas en un pantano peligroso (1) o Rechazar la oferta y seguir buscando una forma alternativa de curarse (2)?",
                "choices": [1, 2]
            },
            # Escenario 3B: Uno busca ayuda, otro antídoto - Viene de 2A
            {
                "scenario": "Al intentar buscar ayuda, se pierde en la jungla y desaparece para siempre. El que buscaba un antidoto natural, cae por un barranco sin darse cuenta y muere" +
                "Final del juego 2",
                "choices": []
            },
            # Escenario 3C: Ambos buscan antídoto - Viene de 2A
            {
                "scenario": "Ambos se adentran en el bosque buscando plantas curativas. Tras varias horas de búsqueda, uno de los personajes cae en un pozo venenoso y el veneno se propaga rápidamente. " +
                "¿Intentar salir del pozo a toda prisa, incluso si eso pone en riesgo tu vida (1) o Quedarte en el pozo, esperando encontrar una salida más segura mientras los efectos del veneno avanzan (2)?",
                "choices": [1, 2]
            },
            # Escenario 2D: Entrar a la cueva - Viene de 1B y 1C
            {
                "scenario": "Entran a la cueva y descubren que está habitada por un oso. El oso los ataca. " +
                "¿Intentar defenderse (1) o huir (2)?",
                "choices": [1, 2]
            },
            # Escenario 2E: Buscar otro lugar - Viene de 1C
            {
                "scenario": "Deciden buscar otro lugar para refugiarse. Encuentran un árbol grande con ramas gruesas. " +
                "¿Construir un refugio en el árbol (1) o seguir buscando (2)?",
                "choices": [1, 2]
            },
            # Escenario 4A: Ambos intentan salir del pozo - Viene de 3C
            {
                "scenario": "Consiguen salir del pozo juntos, pero uno ya se encuentra infectado" +
                "¿Intentar quemar madera y hacer señales en la playa para ser salvados rapidamente (1) o priorizar construir un refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 5A: Viene de 4A, ambos elijen refugio
            {
                "scenario": "El veneno se propaga, y sin antídoto, ambos mueren al amanecer." +
                "Final del juego 4",
                "choices": []
            },
            # Escenario 5B: Viene de 4A, buscan cosas distintas
            {
                "scenario": "Uno cae en una trampa natural y muere en el acto, mientras que el otro, al no conseguir antidoto, muere debido al veneno" +
                "Final del juego 5",
                "choices": []
            },
            # Escenario 5C: Viene de 4A, ambos buscan plantas curativas
            {
                "scenario": "Encuetran una cura natural en una planta y mientras exploran la isla, descubren unas antiguas ruinas cubiertas de inscripciones extrañas. " +
                "Una fuerza misteriosa parece emanar del lugar. " +
                "¿Explorar las ruinas (1) o alejarse y seguir buscando supervivencia (2)?",
                "choices": [1, 2]
            },
            # Escenario 4B: Viene de 3C, Ambos se quedan en el pozo
            {
                "scenario": "Se quedan en el pozo y descubren un pasadizo oculto con símbolos antiguos. " +
                "¿explorar el pasadizo (1) o ignorarlo y esperar ayuda (2)?",
                "choices": [1, 2]
            },
            # Escenario 5D: Viene de 4B, ambos elijen explorar pasadizo
            {
                "scenario": "El pasadizo los lleva a un templo donde una entidad les ofrece inmortalidad... a cambio de sus almas" +
                "La entidad del templo exige un sacrificio. ¿Aceptar el trato (1) o rechazarlo y huir (2)?",
                "choices": [1, 2]
            },
            # Escenario 5E: Viene de 4B, ambos elijen esperar
            {
                "scenario": "Ambos mueren debido al veneno y a la espera" +
                "Final del juego 8",
                "choices": []
            },
            # Escenario 5F: Viene de 4B, ambos elijen distintas opciones
            {
                "scenario": "Uno muere debido al veneno y a la espera, el otro muere en extrañas condiciones al comenzar a adentrarse al pasadizo" +
                "Final del juego 9",
                "choices": []
            },
            # Escenario 6A: Viene de 5D, ambos elijen aceptar
            {
                "scenario": "Uno de ustedes muere, pero el otro obtiene poderes sobrenaturales... y una maldición eterna que le hara vagar por la isla como un fantasma eternamente" +
                "Final del juego 6",
                "choices": []
            },
            # Escenario 6B: Viene de 5D, ambos elijen huir
            {
                "scenario": "La entidad se enfada por pertubar su gran letargo y huir, y los convierte en jabalis salvajes de la isla sin recuerdos" +
                "Final del juego 7",
                "choices": []
            },
            # Escenario 5E: Viene de 4B, buscan cosas distintas
            {
                "scenario": "Uno cae en una trampa natural y muere en el acto, mientras que el otro, al no conseguir antidoto, muere debido al veneno" +
                "Final del juego 5",
                "choices": []
            },
            # Escenario 5F: Viene de 4B, ambos buscan plantas curativas
            {
                "scenario": "Encuetran una cura natural en una planta y mientras exploran la isla, descubren unas antiguas ruinas cubiertas de inscripciones extrañas. " +
                "Una fuerza misteriosa parece emanar del lugar. " +
                "¿Explorar las ruinas (1) o alejarse y seguir buscando supervivencia (2)?",
                "choices": [1, 2]
            },
            # Escenario 6C:Viene de 5C, Ambos eliejn explorar las ruinas
            {
                "scenario": "Al explorar las ruinas, una voz surge en sus mentes, ofreciendo conocimiento prohibido a cambio de permanecer en la isla. " +
                "Sienten un poder oscuro envolviéndolos. " +
                "¿Aceptar el trato (1) o rechazarlo y huir (2)?",
                "choices": [1, 2]
            },
            # Escenario 6D: Viene de 5C, Ambos deciden seguir explorando
            {
                "scenario": "Deciden seguir explorando. Encuentran un sendero que parece llevar a una zona más alta de la isla. " +
                "¿Seguir el sendero (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 6E: Viene de 5C, Ambos deciden cosas distintas
            {
                "scenario": "Al separar vuestros caminos, uno desaparece en extrañas condiciones en las ruinas y otro es atacado por un oso en el bosque llevando a su muerte " +
                "Final del juego 10",
                "choices": []
            },
            # Escenario 7A: Viene de 6D, Ambos deciden regresar al refugio
            {
                "scenario": "Regresan al refugio y deciden mejorar su estructura. Con el tiempo, se sienten más seguros. Acaban optando por quedarse a vivir en la isla" +
                "Final del juego 11",
                "choices": []
            },
            # Escenario 7B: Viene de 6D, Ambos deciden seguir explorando
            {
                "scenario": "Deciden descansar mientras exploran y curar las heridas. Mientras descansan, encuentran un manantial de agua fresca. " +
                "¿Quedarse cerca del manantial (1) o seguir explorando (2)?",
                "choices": [1, 2]
            },
            # Escenario 7C: Viene de 6D, Eligen opciones distintas
            {
                "scenario": "Al separar vuestros caminos, uno refuerza mejor el refugio, llegando a adaptarse a este y a la isla y quedandose a vivir para siempre. El que decide explorar, logra encontrar un barco que lo ayuda a salir de la isla y ser rescatado en alta mar semanas despues" +
                "Final del juego 12",
                "choices": []
            },

            # Escenario 8A:Viene de 7B, Ambos eligen Quedarse cerca del manantial
            {
                "scenario": "Se quedan cerca del manantial y construyen un refugio temporal. El agua fresca les da energía, " +
                "pero la comida sigue siendo escasa. ¿Buscar comida en los alrededores (1) o intentar pescar (2)?",
                "choices": [1, 2]
            },
            # Escenario 8B:Viene de 7B, Ambos eligen seguir explorando
            {
                "scenario": "Al seguir explorando encontrais un barco barado en otra playa, después de varios intentos, logran zarpar y ser rescatados a las pocas semanas en alta mar. " +
                "Final del juego 27",
                "choices": []
            },
            # Escenario 9A: Viene de 8A, Ambos eligen Buscar comida en los alrededores
            {
                "scenario": "Buscan comida en los alrededores y encuentran un árbol con frutas desconocidas. " +
                "¿Arriesgarse a comerlas (1) o buscar otra fuente de alimento (2)?",
                "choices": [1, 2]
            },
            # Escenario 9B:Viene de 8A, Ambos elijen Intentar pescar
            {
                "scenario": "Intentan pescar en el manantial, pero no hay peces. Sin embargo, encuentran un arroyo cercano. " +
                "¿Seguir el arroyo (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 9C:Viene de 8A, Ambos eligen opciones distintas
            {
                "scenario": "Al separar vuestros caminos, uno logra adaptarse mejor a la isla mediante la pesca y el uso de utensilios creados a partir de madera, llegando a adaptarse a la isla y quedandose a vivir para siempre. El que decide buscar en los alrededores, logra encontrar un barco que lo ayuda a salir de la isla y ser rescatado en alta mar semanas despues" +
                "Final del juego 16º",
                "choices": []
            },
            # Escenario 10A:Viene de 9A, Arriesgarse a comer frutas desconocidas
            {
                "scenario": "Comen las frutas desconocidas. Lo que les provoca alucionaciones y matarse entre ambos" +
                "Final del juego 13",
                "choices": []
            },
            # Escenario 10B: Viene de 9A, Ambos elijen, Buscar otra fuente de alimento
            {
                "scenario": "Acaban encontrando unos huevos cerca de un nido de pájaros, la experiencia que vais adquiriendo os hace adaptaros a la isla y quedaros a sobrevivir" +
                "Final del juego 14",
                "choices": []
            },
            # Escenario 10C: Viene de 9A, Ambos elijen cosas distintas
            {
                "scenario": "El que decide comer los frutos, sufre grandes alucionaciones, lo que le provoca matar a su compañero y suicidarse despues" +
                "Final del juego 15",
                "choices": []
            },
            # Escenario 10D:Viene de 9B, Ambos eligen Seguir el arroyo
            {
                "scenario": "Siguen el arroyo y encuentran una cascada. Detrás de la cascada, hay una cueva oculta. " +
                "¿Explorar la cueva (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 10E:Viene de 9B, Ambos eligen opciones distintas
            {
                "scenario": "Al separar vuestros caminos, uno logra adaptarse mejor a la isla al volver al refugio, llegando a adaptarse a la isla y quedandose a vivir para siempre. El que decide seguir el arroyo, logra encontrar un barco que lo ayuda a salir de la isla y ser rescatado en alta mar semanas despues" +
                "Final del juego 17",
                "choices": []
            },
            # Escenario 10F: vienen de 9B, Ambos elijen regresar al refugio
            {
                "scenario": "Deciden quedarse en la playa y construir una vida en la isla. Con el tiempo, aprenden a sobrevivir y encuentran paz en su nuevo hogar." +
                "Final del juego 18",
                "choices": []
            },
            # Escenario 11A: vienen de 10D, Ambos elijen Explorar la cueva
            {
                "scenario": "Exploran la cueva y encuentran un antiguo altar con símbolos extraños. " +
                "¿Tocar el altar (1) o ignorarlo (2)?",
                "choices": [1, 2]
            },
            # Escenario 11B:Viene de 10D, Ambos eligen Opciones distintas
            {
                "scenario": "Al separar vuestros caminos, uno logra adaptarse mejor a la isla al volver al refugio, llegando a adaptarse a la isla y quedandose a vivir para siempre. El que decide explorar la cueva, desaparece para siempre" +
                "Final del juego 19",
                "choices": []
            },

            # Escenario 12A: Viene de 11A ,ambos eligen tocar el altar
            {
                "scenario": "Al tocar el altar, una luz brillante los envuelve. Una voz les ofrece conocimiento infinito a cambio de quedarse. ¿Aceptar (1) o rechazar (2)?",
                "choices": [1, 2],
            },

            # Escenario 12B: Viene de 11A, ambos eligen ignorar el altar
            {
                "scenario": "Deciden ignorar el altar. Al salir ven un barco en el horizonte. ¿Hacer fogata (1) o esperar (2)?",
                "choices": [1, 2],
            },

            # Escenario 12C: Viene de 11A (decisiones distintas)
            {
                "scenario": "Uno toca el altar y desaparece. El otro intenta ayudarlo y cae en una trampa mortal. Final del juego 21",
                "choices": []
            },

            # Escenario 13A: Viene de 12A , ambos aceptan trato
            {
                "scenario": "Son transportados a una dimensión de conocimiento eterno. Donde descubren secretos cósmicos pero pierden su humanidad y se convierten en entidades inmortales" +
                "Final del juego 22",
                "choices": [],
            },

            # Escenario 13B: Viene de 12A , ambos rechazan trato
            {
                "scenario": "La entidad se enfurece. La cueva colapsa. ¿Correr (1) o buscar salida alternativa (2)?",
                "choices": [1, 2],
            },
            # Escenario 13C: Viene de 12B, ambos hacen fogata
            {
                "scenario": "El barco los ve y consiguen ser rescatados. " +
                "Final del juego 23",
                "choices": [],
            },

            # Escenario 14A: Viene de 13B , ambos corren
            {
                "scenario": "Logran escapar pero el exterior ahora es un desierto árido, sin rastros de vida. " +
                "Final del juego 24",
                "choices": [],
            },
            # Escenario 14B: Viene de 13B , ambos buscan salida alternativa
            {
                "scenario": "Buscan otra salida y encuentran un túnel que los lleva a una playa desierta. " +
                "Intentan construir una balsa con los restos del naufragio. Después de varios intentos, logran zarpar y ser rescatados a las pocas semanas en alta mar."+
                "Final del juego 26",
                "choices": []
            },
            # Escenario 14C: Viene de 13B , ambos elijen distintas opciones
            {
                "scenario": "Al no ponerse de acuerdo son sepultados por las piedras que van cayendo, dejando sus cuerpos sellados con la cueva" +
                "Final del juego 25",
                "choices": []
            },
            









            # Escenario 4A: Pescar con las manos
            {
                "scenario": "Intentan pescar con las manos, pero los peces son demasiado rápidos. " +
                "Después de varios intentos fallidos, uno de ustedes encuentra una lanza improvisada en la orilla. " +
                "¿Intentar pescar con la lanza (1) o seguir buscando otra fuente de alimento (2)?",
                "choices": [1, 2]
            },
            # Escenario 5A: Defenderse del oso
            {
                "scenario": "Deciden enfrentar al oso con ramas y piedras. La criatura se muestra agresiva, pero con esfuerzo logran ahuyentarlo. " +
                "Sin embargo, uno de ustedes queda herido. ¿Descansar y recuperarse (1) o seguir explorando la cueva (2)?",
                "choices": [1, 2]
            },
        ]

        self.current_scenario = 0  # Escenario actual
        self.player_decision = None  # Decisión del jugador 1
        self.other_player_decision = None  # Decisión del jugador 2

    def get_scenario(self, index):
        """Devuelve el escenario en la posición `index`."""
        return self.scenarios[index]

    def both_players_responded(self):
        """Verifica si ambos jugadores han respondido."""
        return self.player_decision is not None and self.other_player_decision is not None

    def reset_decisions(self):
        """Reinicia las decisiones para el siguiente escenario."""
        self.player_decision = None
        self.other_player_decision = None

    def process_decisions(self):
        """
        Define aquí la lógica de transición entre escenarios.
        Puedes modificar esta función para que las decisiones de los jugadores
        lleven a escenarios específicos.
        """
        if self.current_scenario == 0:
            # Escenario 0: Construir refugio (1) o buscar comida (2)
            if self.player_decision == self.other_player_decision:
                self.current_scenario = 1  # Ambos eligen lo mismo: ir al escenario 1
            else:
                self.current_scenario = 2  # Decisiones distintas: ir al escenario 2

        elif self.current_scenario == 1:
            # Escenario 1: Enfrentar animal (1) o huir (2)
            if self.player_decision == self.other_player_decision:
                self.current_scenario = 3  # Ambos eligen lo mismo: ir al escenario 3
            else:
                self.current_scenario = 4  # Decisiones distintas: ir al escenario 4

        elif self.current_scenario == 2:
            # Escenario 2: Entrar a la cueva (1) o buscar comida (2)
            if self.player_decision == self.other_player_decision:
                self.current_scenario = 5  # Ambos eligen lo mismo: ir al escenario 5
            else:
                self.current_scenario = 6  # Decisiones distintas: ir al escenario 6

        elif self.current_scenario == 3:
            # Escenario 3: Reparar bote (1) o quedarse (2)
            if self.player_decision == self.other_player_decision:
                self.current_scenario = 7  # Ambos eligen lo mismo: ir al escenario 7
            else:
                self.current_scenario = 8  # Decisiones distintas: ir al escenario 8

        elif self.current_scenario == 4:
            # Escenario 4: Señalar barco (1) o ignorarlo (2)
            if self.player_decision == self.other_player_decision:
                self.current_scenario = 9  # Ambos eligen lo mismo: ir al escenario 9
            else:
                self.current_scenario = 10  # Decisiones distintas: ir al escenario 10

        elif self.current_scenario == 5:
            # Escenario 5: Ser rescatado (1) o explorar más (2)
            if self.player_decision == self.other_player_decision:
                self.current_scenario = 11  # Ambos eligen lo mismo: ir al escenario 11
            else:
                self.current_scenario = 12  # Decisiones distintas: ir al escenario 12

        # Añade más condiciones para los demás escenarios...
        else:
            # Si no hay más escenarios, termina el juego
            self.current_scenario = -1  # Fin del juego

    def get_results(self):
        """Genera los resultados basados en las decisiones de ambos jugadores."""
        return f"Your decision: {self.player_decision}, Other player's decision: {self.other_player_decision}"
