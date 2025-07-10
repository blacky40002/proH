from testMy import testEqual, testEccezione
from classi import Data, Prenotazione
from stanze import Singola, Doppia, Suite, Stanza
from hotel import Hotel


def run_additional_tests():
    risultati = []

    # === Data edge cases ===
    risultati.append(testEccezione(1, ValueError, Data, 32, 1))  # Giorno fuori range
    risultati.append(testEccezione(2, ValueError, Data, 0, 1))   # Giorno zero
    risultati.append(testEccezione(3, ValueError, Data, 1, 13))  # Mese fuori range
    risultati.append(testEccezione(4, TypeError, Data, "1", "a"))  # Tipi errati

    # === Suite validation ===
    risultati.append(testEccezione(5, ValueError, Suite, 200, 3, ["TV"], 100.0))  # posti < 4

    # === Prenotazione validation ===
    d1 = Data(1, 1)
    d2 = Data(5, 1)
    risultati.append(testEccezione(6, ValueError, Prenotazione, None, 101, d2, d1, "Mario", 2))  # partenza < arrivo

    # === Hotel advanced scenarios ===
    h = Hotel()
    s = Doppia(110, 80.0)
    h.aggiungi_stanza(s)
    idx = h.prenota(110, d1, d2, "Mario", 2)
    # Tentativo di rimuovere stanza con prenotazioni attive deve eliminare le prenotazioni
    h.rimuovi_stanza(110)
    risultati.append(testEqual(len(h.get_prenotazioni()), 0))
    risultati.append(testEqual(len(h.stanze), 0))

    # Dopo il salvataggio e caricamento lo stato deve rimanere consistente
    h2 = Hotel()
    s2 = Singola(120, 40.0)
    h2.aggiungi_stanza(s2)
    idx2 = h2.prenota(120, Data(10, 2), Data(12, 2), "Luigi", 1)
    h2.salva("hotell.txt")
    h3 = Hotel()
    h3.carica("hotell.txt")
    risultati.append(testEqual(h2, h3))

    # Stanza price calculations for long stays
    risultati.append(testEqual(s2.calcola_prezzo(10), 400.0))

    if all(risultati):
        print("\nTutti i test aggiuntivi SUPERATI (", len(risultati), "/", len(risultati), ")")
    else:
        fail = [i+1 for i, r in enumerate(risultati) if not r]
        print("\nTest aggiuntivi FALLITI:", fail)

    return risultati


if __name__ == "__main__":
    run_additional_tests()