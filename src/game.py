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
            # Escenario 2A: Comer los frutos
            {
                "scenario": "Comen los frutos. Uno de ellos resulta ser venenoso y tu compañero comienza a sentirse mal. " +
                "¿Buscar ayuda en la isla (1) o intentar encontrar un antídoto en la naturaleza (2)?",
                "choices": [1, 2]
            },
            # Escenario 2B: Uno come los frutos otro busca otra fuente de alimento
            {
                "scenario": "Algunos frutos resultan ser venenosos, al ingerirlos quedas envenendado e incapaz de hacer nada. Al intentar buscar otra fuente de alimentos no te das cuenta de que tu compañero esta en grave estado, por tanto muere solo. Al seguir buscando alimento caes por un barranco sin darte cuenta y mueres " +
                "Final del juego 1",
                "choices": []
            },

            # Escenario 2C: Buscar otra fuente de alimento
            {
                "scenario": "Deciden buscar otra fuente de alimento. Encuentran un río con peces, pero no tienen herramientas para pescar. " +
                "¿Intentar pescar con las manos (1) o seguir buscando (2)?",
                "choices": [1, 2]
            },
            # Escenario 3A: Ambos buscan ayuda en la isla
            {
                "scenario": "Ambos deciden buscar ayuda en la isla. Después de caminar un rato, encuentran una choza de un hombre solitario. El hombre les ofrece medicina para el veneno, pero les advierte que tiene un precio. " +
                "¿Aceptar la oferta del hombre y ayudarle a recolectar hierbas en un pantano peligroso (1) o Rechazar la oferta y seguir buscando una forma alternativa de curarse (2)?",
                "choices": [1, 2]
            },
            # Escenario 3B: Uno busca ayuda, otro antídoto
            {
                "scenario": "Al intentar buscar ayuda, se pierde en la jungla y desaparece para siempre. El que buscaba un antidoto natural, cae por un barranco sin darse cuenta y muere" +
                "Final del juego 2",
                "choices": []
            },
            # Escenario 3C: Ambos buscan antídoto
            {
                "scenario": "Ambos se adentran en el bosque buscando plantas curativas. Tras varias horas de búsqueda, uno de los personajes cae en un pozo venenoso y el veneno se propaga rápidamente. " +
                "¿Intentar salir del pozo a toda prisa, incluso si eso pone en riesgo tu vida (1) o Quedarte en el pozo, esperando encontrar una salida más segura mientras los efectos del veneno avanzan (2)?",
                "choices": [1, 2]
            },
            # Escenario 3A: Entrar a la cueva
            {
                "scenario": "Entran a la cueva y descubren que está habitada por un oso. El oso los ataca. " +
                "¿Intentar defenderse (1) o huir (2)?",
                "choices": [1, 2]
            },
            # Escenario 3B: Buscar otro lugar
            {
                "scenario": "Deciden buscar otro lugar para refugiarse. Encuentran un árbol grande con ramas gruesas. " +
                "¿Construir un refugio en el árbol (1) o seguir buscando (2)?",
                "choices": [1, 2]
            },
            # Escenario 4A: Pescar con las manos
            {
                "scenario": "Intentan pescar con las manos, pero los peces son demasiado rápidos. " +
                "Después de varios intentos fallidos, uno de ustedes encuentra una lanza improvisada en la orilla. " +
                "¿Intentar pescar con la lanza (1) o seguir buscando otra fuente de alimento (2)?",
                "choices": [1, 2]
            },
            # Escenario 4B: Descubrimiento sobrenatural
            {
                "scenario": "Mientras exploran la isla, descubren unas antiguas ruinas cubiertas de inscripciones extrañas. " +
                "Una fuerza misteriosa parece emanar del lugar. " +
                "¿Explorar las ruinas (1) o alejarse y seguir buscando supervivencia (2)?",
                "choices": [1, 2]
            },
            # Escenario 5A: Defenderse del oso
            {
                "scenario": "Deciden enfrentar al oso con ramas y piedras. La criatura se muestra agresiva, pero con esfuerzo logran ahuyentarlo. " +
                "Sin embargo, uno de ustedes queda herido. ¿Descansar y recuperarse (1) o seguir explorando la cueva (2)?",
                "choices": [1, 2]
            },
            # Escenario 5B: Supervivencia exitosa
            {
                "scenario": "Con esfuerzo y buenas decisiones, logran construir un refugio seguro, conseguir suficiente comida " +
                "y, eventualmente, son rescatados por un barco que pasaba. Han superado la prueba.",
                "choices": []
            },
            # Escenario 6A: Trato con la entidad
            {
                "scenario": "Al explorar las ruinas, una voz surge en sus mentes, ofreciendo conocimiento prohibido a cambio de permanecer en la isla. " +
                "Sienten un poder oscuro envolviéndolos. " +
                "¿Aceptar el trato (1) o rechazarlo y huir (2)?",
                "choices": [1, 2]
            },
            # Escenario 6B: Destino trágico
            {
                "scenario": "Tomaron demasiadas malas decisiones. La falta de cooperación y los peligros de la isla " +
                "los han llevado al borde de la inanición y la desesperación. Finalmente, el destino los alcanza. " +
                "El juego termina aquí.",
                "choices": []
            }
            # Escenario 7A: Descansar y recuperarse
            {
                "scenario": "Deciden descansar y curar las heridas. Mientras descansan, encuentran un manantial de agua fresca. " +
                "¿Quedarse cerca del manantial (1) o seguir explorando (2)?",
                "choices": [1, 2]
            },
            # Escenario 7B: Seguir explorando la cueva
            {
                "scenario": "Deciden seguir explorando la cueva. Encuentran un pasadizo secreto que lleva a una cámara oculta. " +
                "¿Entrar a la cámara (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 8A: Quedarse cerca del manantial
            {
                "scenario": "Se quedan cerca del manantial y construyen un refugio temporal. El agua fresca les da energía, " +
                "pero la comida sigue siendo escasa. ¿Buscar comida en los alrededores (1) o intentar pescar (2)?",
                "choices": [1, 2]
            },
            # Escenario 8B: Seguir explorando
            {
                "scenario": "Deciden seguir explorando. Encuentran un sendero que parece llevar a una zona más alta de la isla. " +
                "¿Seguir el sendero (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 9A: Buscar comida en los alrededores
            {
                "scenario": "Buscan comida en los alrededores y encuentran un árbol con frutas desconocidas. " +
                "¿Arriesgarse a comerlas (1) o buscar otra fuente de alimento (2)?",
                "choices": [1, 2]
            },
            # Escenario 9B: Intentar pescar
            {
                "scenario": "Intentan pescar en el manantial, pero no hay peces. Sin embargo, encuentran un arroyo cercano. " +
                "¿Seguir el arroyo (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 10A: Arriesgarse a comer frutas desconocidas
            {
                "scenario": "Comen las frutas desconocidas. Uno de ustedes comienza a sentirse mareado. " +
                "¿Buscar ayuda en la isla (1) o esperar a ver qué pasa (2)?",
                "choices": [1, 2]
            },
            # Escenario 10B: Buscar otra fuente de alimento
            {
                "scenario": "Deciden buscar otra fuente de alimento. Encuentran un nido de pájaros con huevos. " +
                "¿Tomar los huevos (1) o dejarlos (2)?",
                "choices": [1, 2]
            },
            # Escenario 11A: Seguir el arroyo
            {
                "scenario": "Siguen el arroyo y encuentran una cascada. Detrás de la cascada, hay una cueva oculta. " +
                "¿Explorar la cueva (1) o regresar al refugio (2)?",
                "choices": [1, 2]
            },
            # Escenario 11B: Regresar al refugio
            {
                "scenario": "Regresan al refugio y deciden mejorar su estructura. Con el tiempo, se sienten más seguros. " +
                "¿Explorar más la isla (1) o enfocarse en ser rescatados (2)?",
                "choices": [1, 2]
            },
            # Escenario 12A: Explorar la cueva detrás de la cascada
            {
                "scenario": "Exploran la cueva y encuentran un antiguo altar con símbolos extraños. " +
                "¿Tocar el altar (1) o ignorarlo (2)?",
                "choices": [1, 2]
            },
            # Escenario 12B: Ignorar el altar
            {
                "scenario": "Deciden ignorar el altar y salir de la cueva. Afuera, encuentran un barco en el horizonte. " +
                "¿Hacer una fogata para llamar su atención (1) o esperar a que se acerquen (2)?",
                "choices": [1, 2]
            },
            # Escenario 13A: Tocar el altar
            {
                "scenario": "Al tocar el altar, una luz brillante los envuelve. Una voz les ofrece un trato: " +
                "conocimiento infinito a cambio de quedarse en la isla. ¿Aceptar (1) o rechazar (2)?",
                "choices": [1, 2]
            },
            # Escenario 13B: Hacer una fogata
            {
                "scenario": "Hacen una fogata y el barco los ve. Sin embargo, el barco parece estar en mal estado. " +
                "¿Intentar llegar al barco (1) o esperar a que se acerquen (2)?",
                "choices": [1, 2]
            },
            # Escenario 14A: Aceptar el trato del altar
            {
                "scenario": "Aceptan el trato y son transportados a una dimensión desconocida. La isla desaparece, " +
                "y ahora están en un lugar lleno de conocimiento, pero también de peligros. " +
                "¿Explorar la nueva dimensión (1) o intentar regresar (2)?",
                "choices": [1, 2]
            },
            # Escenario 14B: Rechazar el trato del altar
            {
                "scenario": "Rechazan el trato y el altar se desvanece. La cueva comienza a colapsar. " +
                "¿Correr hacia la salida (1) o buscar otra salida (2)?",
                "choices": [1, 2]
            },
            # Escenario 15A: Explorar la nueva dimensión
            {
                "scenario": "Exploran la nueva dimensión y encuentran un portal que parece llevar a casa. " +
                "¿Entrar al portal (1) o quedarse en la dimensión (2)?",
                "choices": [1, 2]
            },
            # Escenario 15B: Intentar regresar
            {
                "scenario": "Intentan regresar, pero el portal se cierra. Ahora están atrapados en la dimensión. " +
                "¿Buscar otra salida (1) o aceptar su destino (2)?",
                "choices": [1, 2]
            },
            # Escenario 16A: Correr hacia la salida
            {
                "scenario": "Corren hacia la salida y logran escapar justo antes de que la cueva colapse. " +
                "Afuera, encuentran un barco que los rescata. Han sobrevivido, pero la isla aún guarda secretos.",
                "choices": []
            },
            # Escenario 16B: Buscar otra salida
            {
                "scenario": "Buscan otra salida y encuentran un túnel que los lleva a una playa desierta. " +
                "El barco que los rescató ya se ha ido. Ahora deben decidir si quedarse o intentar construir una balsa.",
                "choices": [1, 2]
            },
            # Escenario 17A: Quedarse en la playa
            {
                "scenario": "Deciden quedarse en la playa y construir una vida en la isla. Con el tiempo, aprenden a sobrevivir " +
                "y encuentran paz en su nuevo hogar.",
                "choices": []
            },
            # Escenario 17B: Intentar construir una balsa
            {
                "scenario": "Intentan construir una balsa con los restos del naufragio. Después de varios intentos, logran zarpar. " +
                "Sin embargo, el mar es traicionero. ¿Lograrán llegar a tierra firme?",
                "choices": []
            }
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
