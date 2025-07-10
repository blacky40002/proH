#!/usr/bin/env python3
"""
Test più approfonditi per il sistema di gestione hotel
Test delle funzionalità avanzate e casi limite
"""

from testMy import *
from hotel import Hotel
from stanze import Singola, Doppia, Suite
from classi import Data, Prenotazione

def test_data_avanzati():
    """Test approfonditi per la classe Data"""
    print("=== Test avanzati per la classe Data ===")
    risultati = []
    
    # Test costruttore con valori limite
    try:
        d1 = Data(31, 1)  # Ultimo giorno gennaio
        d2 = Data(28, 2)  # Ultimo giorno febbraio
        d3 = Data(30, 4)  # Ultimo giorno aprile
        risultati.append(True)
        print("✓ Date ai limiti create correttamente")
    except Exception as e:
        print(f"✗ Errore creazione date limite: {e}")
        risultati.append(False)
    
    # Test valori invalidi
    try:
        Data(32, 1)  # Giorno troppo alto
        risultati.append(False)
        print("✗ Non ha rilevato giorno invalido")
    except (ValueError, TypeError):
        risultati.append(True)
        print("✓ Rilevato correttamente giorno invalido")
    
    try:
        Data(29, 2)  # Febbraio non bisestile
        risultati.append(False)
        print("✗ Non ha rilevato giorno invalido per febbraio")
    except (ValueError, TypeError):
        risultati.append(True)
        print("✓ Rilevato correttamente giorno invalido per febbraio")
    
    # Test differenze tra mesi
    d_gen = Data(15, 1)
    d_feb = Data(15, 2)
    d_dic = Data(15, 12)
    
    risultati.append(testEqual(d_feb - d_gen, 31))
    risultati.append(testEqual(d_dic - d_gen, 349))  # 31+28+31+30+31+30+31+31+30+31+30+14
    print(f"✓ Differenze tra mesi calcolate correttamente")
    
    return risultati

def test_prenotazioni_avanzate():
    """Test approfonditi per le prenotazioni"""
    print("\n=== Test avanzati per le Prenotazioni ===")
    risultati = []
    
    # Test nomi clienti con spazi
    try:
        p1 = Prenotazione(1, 101, Data(1,1), Data(5,1), "Mario Rossi", 2)
        p2 = Prenotazione(2, 102, Data(1,1), Data(5,1), "   Ana   ", 1)  # Con spazi
        risultati.append(testEqual(p2.nome_cliente, "Ana"))
        print("✓ Gestione spazi nel nome cliente corretta")
    except Exception as e:
        print(f"✗ Errore gestione spazi: {e}")
        risultati.append(False)
    
    # Test nome troppo corto/lungo
    try:
        Prenotazione(3, 103, Data(1,1), Data(5,1), "AB", 1)  # Troppo corto
        risultati.append(False)
        print("✗ Non ha rilevato nome troppo corto")
    except (ValueError, TypeError):
        risultati.append(True)
        print("✓ Rilevato nome troppo corto")
    
    try:
        nome_lungo = "a" * 25  # Troppo lungo
        Prenotazione(4, 104, Data(1,1), Data(5,1), nome_lungo, 1)
        risultati.append(False)
        print("✗ Non ha rilevato nome troppo lungo")
    except (ValueError, TypeError):
        risultati.append(True)
        print("✓ Rilevato nome troppo lungo")
    
    return risultati

def test_stanze_avanzate():
    """Test approfonditi per le stanze"""
    print("\n=== Test avanzati per le Stanze ===")
    risultati = []
    
    # Test Suite con extra vuoti
    try:
        s1 = Suite(101, 4, [], 200.0)  # Nessun extra
        risultati.append(testEqual(s1.calcola_prezzo(1), 300.0))  # 200 * 1.5
        print("✓ Suite senza extra gestita correttamente")
    except Exception as e:
        print(f"✗ Errore Suite senza extra: {e}")
        risultati.append(False)
    
    # Test Suite con molti extra
    try:
        extra_list = ["TV", "WiFi", "Minibar", "Jacuzzi", "Balcone", "Vista mare"]
        s2 = Suite(102, 6, extra_list, 300.0)
        prezzo_atteso = (300.0 * 1.5 + 10 * len(extra_list)) * 2  # 2 notti
        risultati.append(testEqual(s2.calcola_prezzo(2), prezzo_atteso))
        print("✓ Suite con molti extra calcolata correttamente")
    except Exception as e:
        print(f"✗ Errore Suite con molti extra: {e}")
        risultati.append(False)
    
    # Test rappresentazione stringa
    risultati.append(testEqual(str(s2), "Suite 102, 6 posti, con TV, WiFi, Minibar, Jacuzzi, Balcone, Vista mare"))
    print("✓ Rappresentazione stringa Suite corretta")
    
    # Test che Suite non può avere meno di 4 posti
    try:
        Suite(103, 3, ["TV"], 200.0)
        risultati.append(False)
        print("✗ Non ha rilevato posti insufficienti per Suite")
    except ValueError:
        risultati.append(True)
        print("✓ Rilevato correttamente posti insufficienti per Suite")
    
    return risultati

def test_hotel_avanzato():
    """Test approfonditi per l'Hotel"""
    print("\n=== Test avanzati per l'Hotel ===")
    risultati = []
    
    hotel = Hotel()
    
    # Aggiungi diverse tipologie di stanze
    s1 = Singola(101, 50.0)
    s2 = Doppia(102, 80.0)
    s3 = Suite(103, 4, ["TV", "Minibar"], 200.0)
    
    for stanza in [s1, s2, s3]:
        hotel.aggiungi_stanza(stanza)
    
    # Test get_stanze_tipo
    risultati.append(testEqual(len(hotel.get_stanze_tipo("Singola")), 1))
    risultati.append(testEqual(len(hotel.get_stanze_tipo("Doppia")), 1))
    risultati.append(testEqual(len(hotel.get_stanze_tipo("Suite")), 1))
    print("✓ Filtro per tipo stanza funziona correttamente")
    
    # Test prenotazioni sovrapposte
    hotel.prenota(101, Data(1,1), Data(5,1), "Cliente1", 1)
    
    try:
        hotel.prenota(101, Data(3,1), Data(7,1), "Cliente2", 1)  # Sovrapposta
        risultati.append(False)
        print("✗ Non ha rilevato sovrapposizione date")
    except ValueError:
        risultati.append(True)
        print("✓ Rilevata correttamente sovrapposizione date")
    
    # Test prenotazione valida dopo la prima
    try:
        id_pren = hotel.prenota(101, Data(6,1), Data(10,1), "Cliente2", 1)
        risultati.append(True)
        print("✓ Prenotazione consecutiva accettata")
    except Exception as e:
        print(f"✗ Errore prenotazione consecutiva: {e}")
        risultati.append(False)
    
    # Test get_stanze_sopra_prezzo
    stanze_costose = hotel.get_stanze_sopra_prezzo(1, 100)
    risultati.append(testEqual(len(stanze_costose), 2))  # Doppia e Suite
    print("✓ Filtro stanze per prezzo funziona")
    
    # Test persone che superano capacità stanza
    try:
        hotel.prenota(101, Data(15,1), Data(20,1), "Cliente3", 3)  # Singola per 3 persone
        risultati.append(False)
        print("✗ Non ha rilevato eccesso capacità")
    except ValueError:
        risultati.append(True)
        print("✓ Rilevato eccesso capacità stanza")
    
    return risultati

def test_calcoli_prezzi():
    """Test specifici per i calcoli dei prezzi"""
    print("\n=== Test calcoli prezzi ===")
    risultati = []
    
    hotel = Hotel()
    s1 = Singola(101, 50.0)
    s2 = Doppia(102, 100.0)
    s3 = Suite(103, 4, ["TV", "Minibar"], 200.0)
    
    for stanza in [s1, s2, s3]:
        hotel.aggiungi_stanza(stanza)
    
    # Prenotazioni di test
    id1 = hotel.prenota(101, Data(1,1), Data(3,1), "Cliente1", 1)  # 2 notti
    id2 = hotel.prenota(102, Data(1,1), Data(4,1), "Cliente2", 2)  # 3 notti, 2 persone
    id3 = hotel.prenota(103, Data(1,1), Data(2,1), "Cliente3", 3)  # 1 notte, 3 persone
    
    # Test calcoli
    # Singola: 50 * 2 notti * 1 persona = 100
    risultati.append(testEqual(hotel.prezzo_prenotazione(id1), 100.0))
    
    # Doppia: 100 * 1.2 * 3 notti * 2 persone = 720
    risultati.append(testEqual(hotel.prezzo_prenotazione(id2), 720.0))
    
    # Suite: (200 * 1.5 + 10 * 2 extra) * 1 notte * 3 persone = 320 * 3 = 960
    risultati.append(testEqual(hotel.prezzo_prenotazione(id3), 960.0))
    
    print("✓ Calcoli prezzi corretti per tutte le tipologie")
    
    return risultati

def test_salvataggio_caricamento():
    """Test del salvataggio e caricamento"""
    print("\n=== Test salvataggio e caricamento ===")
    risultati = []
    
    # Crea hotel di test
    hotel1 = Hotel()
    hotel1.aggiungi_stanza(Singola(101, 50.0))
    hotel1.aggiungi_stanza(Doppia(102, 80.0))
    hotel1.prenota(101, Data(1,1), Data(5,1), "TestClient", 1)
    
    # Salva
    try:
        hotel1.salva("test_hotel.txt")
        risultati.append(True)
        print("✓ Salvataggio completato")
    except Exception as e:
        print(f"✗ Errore salvataggio: {e}")
        risultati.append(False)
        return risultati
    
    # Carica in nuovo hotel
    try:
        hotel2 = Hotel()
        hotel2.carica("test_hotel.txt")
        risultati.append(testEqual(hotel1, hotel2))
        print("✓ Caricamento e confronto riusciti")
    except Exception as e:
        print(f"✗ Errore caricamento: {e}")
        risultati.append(False)
    
    return risultati

def esegui_tutti_test():
    """Esegue tutti i test approfonditi"""
    print("AVVIO TEST APPROFONDITI SISTEMA HOTEL")
    print("=" * 50)
    
    tutti_risultati = []
    
    # Esegui ogni gruppo di test
    test_groups = [
        test_data_avanzati,
        test_prenotazioni_avanzate, 
        test_stanze_avanzate,
        test_hotel_avanzato,
        test_calcoli_prezzi,
        test_salvataggio_caricamento
    ]
    
    for test_func in test_groups:
        risultati = test_func()
        tutti_risultati.extend(risultati)
    
    # Resoconto finale
    print("\n" + "=" * 50)
    print("RESOCONTO FINALE TEST APPROFONDITI")
    print("=" * 50)
    
    test_passati = sum(tutti_risultati)
    test_totali = len(tutti_risultati)
    
    print(f"Test passati: {test_passati}/{test_totali}")
    
    if test_passati == test_totali:
        print("🎉 TUTTI I TEST APPROFONDITI SUPERATI! 🎉")
        print("Il sistema è robusto e gestisce correttamente:")
        print("- Validazione dati di input")
        print("- Casi limite e valori estremi") 
        print("- Calcoli complessi dei prezzi")
        print("- Gestione delle sovrapposizioni")
        print("- Salvataggio e caricamento dati")
    else:
        test_falliti = test_totali - test_passati
        print(f"❌ {test_falliti} test non superati")
        print("Rivedere l'implementazione delle funzionalità interessate")
    
    return tutti_risultati

if __name__ == "__main__":
    esegui_tutti_test()