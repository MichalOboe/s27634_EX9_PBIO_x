# Numer albumu: s27634
# Data: 2026-05-12
# Opis - Generator losowych sekwencji DNA w formacie FASTA.
#        Program generuje sekwencje, zapisuje do pliku, oblicza statystyki.
#        wybrane funkcjonlaności: wyszukiwanie motywow, sekwencja komplementarna,
#        szukanie ORF, walidator pliku FASTA.

import random


def generate_sequence(length: int) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""
    # random.choices losuje 'length' znaków z listy nukleotydów (z powtórzeniami)
    # ''.join() skleja listę znaków w jeden string
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choices(nucleotides, k=length))


def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.

    Klucze: 'A', 'C', 'G', 'T' (wartości float, %),
            'GC' (wartość float, %).
    """
    length = len(sequence)
    # Liczymy wystąpienia każdego nukleotydu i przeliczamy na procenty
    stats = {
        'A': sequence.count('A') / length * 100,
        'C': sequence.count('C') / length * 100,
        'G': sequence.count('G') / length * 100,
        'T': sequence.count('T') / length * 100,
    }
    # GC-content to suma procentów G i C
    stats['GC'] = stats['G'] + stats['C']
    return stats


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    pass


def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    pass


def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu [min_val, max_val].
    W przypadku błędu powtarza pytanie zamiast rzucać wyjątek."""
    while True:
        raw = input(prompt)
        try:
            # Próbujemy zamienić wpisany tekst na liczbę całkowitą
            value = int(raw)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            # Użytkownik wpisał coś co nie jest liczbą całkowitą (np. "abc")
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


def validate_seq_id(prompt: str) -> str:
    """Pobiera od użytkownika ID sekwencji bez białych znaków.
    W przypadku błędu powtarza pytanie."""
    while True:
        seq_id = input(prompt)
        # split() dzieli po białych znakach — jeśli wynik ma >1 element lub jest pusty,
        # to ID zawiera spacje lub jest puste
        if seq_id and len(seq_id.split()) == 1:
            return seq_id
        else:
            print("Błąd: ID nie może zawierać białych znaków ani być puste.")


# --- Funkcjonalności dodatkowe ---

def find_motif(sequence: str, motif: str) -> list:
    """Wyszukuje motyw w sekwencji. Zwraca listę pozycji (indeksowanie od 1)."""
    pass


def complement(sequence: str) -> str:
    """Zwraca nić komplementarną do podanej sekwencji DNA."""
    pass


def reverse_complement(sequence: str) -> str:
    """Zwraca nić odwrotnie komplementarną."""
    pass


def find_orfs(sequence: str, min_length: int = 1) -> list:
    """Wyszukuje wszystkie ORF-y (ATG -> STOP) o minimalnej długości.
    Zwraca listę słowników z kluczami: start, end, length."""
    pass


def validate_fasta_file(filepath: str) -> list:
    """Wczytuje plik FASTA i sprawdza poprawność formatu.
    Zwraca listę błędów (pustą jeśli plik jest poprawny)."""
    pass


def main():
    """Główna funkcja programu."""
    pass


if __name__ == "__main__":
    main()