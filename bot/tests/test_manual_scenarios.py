"""Interaktywne testy manualne dla bota Discord

UWAGA: Te testy wymagają działającego bota na serwerze Discord.
Nie są to testy automatyczne - służą jako przewodnik do testowania manualnego.
"""
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import Database


class ManualTestScenarios:
    """Scenariusze testowe do manualnego testowania bota"""

    @staticmethod
    async def scenario_1_basic_detection():
        """
        SCENARIUSZ 1: Podstawowe wykrywanie n-word
        
        Kroki:
        1. Uruchom bota na serwerze testowym
        2. Napisz wiadomość zawierającą n-word
        3. Sprawdź czy bot zareagował
        
        Oczekiwany rezultat:
        - Bot odpowiada reakcją (np. "CAUGHT 📸")
        - Licznik użytkownika zwiększa się o 1
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 1: Podstawowe wykrywanie n-word")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Uruchom bota: cd bot && python bot.py")
        print("2. Na Discordzie napisz wiadomość z n-word")
        print("3. Sprawdź czy bot odpowiedział")
        print("\n✅ Sprawdź:")
        print("   - Bot wysłał reakcję")
        print("   - /count @ty pokazuje zwiększony licznik")
        
    @staticmethod
    async def scenario_2_count_verification():
        """
        SCENARIUSZ 2: Weryfikacja licznika
        
        Kroki:
        1. Napisz 5 wiadomości z n-word
        2. Użyj komendy /count @twój-nick
        3. Sprawdź czy licznik pokazuje 5
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 2: Weryfikacja licznika")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Napisz 5 wiadomości z n-word")
        print("2. Wpisz: /count @twój-nick")
        print("\n✅ Sprawdź:")
        print("   - Licznik pokazuje dokładnie 5")
        print("   - Embed jest poprawnie sformatowany")

    @staticmethod
    async def scenario_3_voting_system():
        """
        SCENARIUSZ 3: System głosowania
        
        Kroki:
        1. Użytkownik A: /vote @użytkownikB
        2. Użytkownik C: /vote @użytkownikB (threshold=2)
        3. Użytkownik B pisze n-word
        4. Sprawdź czy bot NIE reaguje
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 3: System głosowania")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Użytkownik A: /vote @użytkownikB")
        print("2. Użytkownik C: /vote @użytkownikB")
        print("3. Użytkownik B pisze n-word")
        print("\n✅ Sprawdź:")
        print("   - Po 2 głosach użytkownik B jest zweryfikowany")
        print("   - Bot nie reaguje na wiadomości użytkownika B")
        print("   - Licznik nadal się zwiększa")

    @staticmethod
    async def scenario_4_rankings():
        """
        SCENARIUSZ 4: System rankingów
        
        Kroki:
        1. 3 użytkowników pisze różną ilość n-word
        2. Użyj /top guild user
        3. Sprawdź czy ranking jest poprawny
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 4: System rankingów")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Użytkownik A: pisze 10x n-word")
        print("2. Użytkownik B: pisze 5x n-word")
        print("3. Użytkownik C: pisze 15x n-word")
        print("4. Wpisz: /top guild user")
        print("\n✅ Sprawdź:")
        print("   - Kolejność: C (15) > A (10) > B (5)")
        print("   - Wszystkie liczniki są poprawne")
        print("   - Paginacja działa dla >10 użytkowników")

    @staticmethod
    async def scenario_5_whitelist():
        """
        SCENARIUSZ 5: Whitelist
        
        Kroki:
        1. Sprawdź whitelist.txt
        2. Napisz wiadomość ze słowem z whitelisty
        3. Sprawdź czy licznik się NIE zwiększył
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 5: Whitelist")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Sprawdź zawartość: cat bot/whitelist.txt")
        print("2. Napisz wiadomość ze słowem z whitelisty")
        print("3. Sprawdź licznik: /count @ty")
        print("\n✅ Sprawdź:")
        print("   - Licznik się NIE zwiększył")
        print("   - Bot NIE zareagował")

    @staticmethod
    async def scenario_6_database_check():
        """
        SCENARIUSZ 6: Sprawdzenie bazy danych
        
        Kroki:
        1. Wykonaj kilka akcji (dodaj n-word)
        2. Sprawdź bot_database.json
        3. Zweryfikuj strukturę danych
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 6: Sprawdzenie bazy danych")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Napisz kilka wiadomości z n-word")
        print("2. Sprawdź bazę: cat bot/bot_database.json | python -m json.tool")
        print("\n✅ Sprawdź:")
        print("   - Struktura JSON jest poprawna")
        print("   - guild_id i member_id są zapisane")
        print("   - nword_count jest aktualny")
        
        # Pokazujemy przykładową strukturę
        print("\n📄 Przykładowa struktura:")
        db = await Database._async_load_database()
        print(f"   Liczba serwerów: {len(db.get('guilds', []))}")
        
        if db.get('guilds'):
            guild = db['guilds'][0]
            print(f"   Pierwszy serwer: {guild.get('guild_name')}")
            print(f"   Liczba członków: {len(guild.get('members', []))}")

    @staticmethod
    async def scenario_7_stress_test():
        """
        SCENARIUSZ 7: Test obciążeniowy
        
        Kroki:
        1. Napisz wiele wiadomości szybko
        2. Sprawdź czy bot nie ma opóźnień
        3. Sprawdź czy wszystkie są zliczone
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 7: Test obciążeniowy")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Napisz 20 wiadomości z n-word w ciągu 10 sekund")
        print("2. Sprawdź licznik: /count @ty")
        print("\n✅ Sprawdź:")
        print("   - Wszystkie 20 wiadomości zostało zliczonych")
        print("   - Bot nie crashuje się")
        print("   - Nie ma zgubienia danych")
        print("\n⚠️  UWAGA:")
        print("   - Bot może nie reagować na spam (>50 n-word)")
        print("   - To jest funkcja anti-rate-limit")

    @staticmethod
    async def scenario_8_multi_server():
        """
        SCENARIUSZ 8: Test wieloserwerowy
        
        Kroki:
        1. Dodaj bota na 2 serwery
        2. Na każdym serwerze napisz n-word
        3. Sprawdź statystyki globalne
        """
        print("\n" + "="*60)
        print("SCENARIUSZ 8: Test wieloserwerowy")
        print("="*60)
        print("\n📋 Instrukcje:")
        print("1. Dodaj bota na Serwer A i Serwer B")
        print("2. Serwer A: napisz 10x n-word")
        print("3. Serwer B: napisz 5x n-word")
        print("4. Wpisz: /statistics")
        print("\n✅ Sprawdź:")
        print("   - Globalna liczba: co najmniej 15")
        print("   - /top global server pokazuje oba serwery")
        print("   - Dane z różnych serwerów nie mieszają się")


async def run_all_scenarios():
    """Uruchom wszystkie scenariusze testowe"""
    print("\n" + "🧪"*30)
    print("INTERAKTYWNY PRZEWODNIK TESTOWANIA BOTA")
    print("🧪"*30)
    
    scenarios = [
        ManualTestScenarios.scenario_1_basic_detection,
        ManualTestScenarios.scenario_2_count_verification,
        ManualTestScenarios.scenario_3_voting_system,
        ManualTestScenarios.scenario_4_rankings,
        ManualTestScenarios.scenario_5_whitelist,
        ManualTestScenarios.scenario_6_database_check,
        ManualTestScenarios.scenario_7_stress_test,
        ManualTestScenarios.scenario_8_multi_server,
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        await scenario()
        
        if i < len(scenarios):
            input("\n⏸️  Naciśnij Enter aby przejść do następnego scenariusza...")


async def run_single_scenario(scenario_num: int):
    """Uruchom pojedynczy scenariusz"""
    scenarios = {
        1: ManualTestScenarios.scenario_1_basic_detection,
        2: ManualTestScenarios.scenario_2_count_verification,
        3: ManualTestScenarios.scenario_3_voting_system,
        4: ManualTestScenarios.scenario_4_rankings,
        5: ManualTestScenarios.scenario_5_whitelist,
        6: ManualTestScenarios.scenario_6_database_check,
        7: ManualTestScenarios.scenario_7_stress_test,
        8: ManualTestScenarios.scenario_8_multi_server,
    }
    
    if scenario_num in scenarios:
        await scenarios[scenario_num]()
    else:
        print(f"❌ Scenariusz {scenario_num} nie istnieje!")
        print(f"Dostępne scenariusze: 1-{len(scenarios)}")


if __name__ == "__main__":
    print("\n🎯 MANUAL TESTING GUIDE")
    print("=" * 60)
    print("\nWybierz tryb:")
    print("  1. Wszystkie scenariusze")
    print("  2-9. Pojedynczy scenariusz (nr)")
    print("  0. Wyjście")
    
    try:
        choice = input("\nWybór: ").strip()
        
        if choice == "0":
            print("👋 Do zobaczenia!")
            sys.exit(0)
        elif choice == "1":
            asyncio.run(run_all_scenarios())
        elif choice.isdigit() and 2 <= int(choice) <= 9:
            asyncio.run(run_single_scenario(int(choice)))
        else:
            print("❌ Nieprawidłowy wybór!")
    except KeyboardInterrupt:
        print("\n\n👋 Przerwano testowanie!")
    except Exception as e:
        print(f"\n❌ Błąd: {e}")

