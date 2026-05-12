# Numer albumu: s27634
# Data: 2026-05-12
# Opis - Generator losowych sekwencji DNA w formacie FASTA.
#        Program generuje sekwencje, zapisuje do pliku, oblicza statystyki.
#        wybrane funkcjonlaności: wyszukiwanie motywow, sekwencja komplementarna,
#        szukanie ORF, walidator pliku FASTA.

import random


def generate_sequence(length: int) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choices(nucleotides, k=length))


def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.

    Klucze: 'A', 'C', 'G', 'T' (wartości float, %),
            'GC' (wartość float, %).
    """
    length = len(sequence)
    stats = {
        'A': sequence.count('A') / length * 100,
        'C': sequence.count('C') / length * 100,
        'G': sequence.count('G') / length * 100,
        'T': sequence.count('T') / length * 100,
    }
    stats['GC'] = stats['G'] + stats['C']
    return stats


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name.lower() + sequence[pos:]


def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"
    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]
    return header + '\n' + '\n'.join(lines) + '\n'


def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu [min_val, max_val].
    W przypadku błędu powtarza pytanie zamiast rzucać wyjątek."""
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


def validate_seq_id(prompt: str) -> str:
    """Pobiera od użytkownika ID sekwencji bez białych znaków.
    W przypadku błędu powtarza pytanie."""
    while True:
        seq_id = input(prompt)
        if seq_id and len(seq_id.split()) == 1:
            return seq_id
        else:
            print("Błąd: ID nie może zawierać białych znaków ani być puste.")


# --- Funkcjonalności dodatkowe ---

def find_motif(sequence: str, motif: str) -> list:
    """Wyszukuje motyw w sekwencji. Zwraca listę pozycji (indeksowanie od 1)."""
    positions = []
    motif = motif.upper()
    for i in range(len(sequence) - len(motif) + 1):
        if sequence[i:i + len(motif)] == motif:
            positions.append(i + 1)
    return positions


def complement(sequence: str) -> str:
    """Zwraca nić komplementarną do podanej sekwencji DNA.
    Reguły: A<->T, C<->G."""
    pairs = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(pairs[n] for n in sequence)


def reverse_complement(sequence: str) -> str:
    """Zwraca nić odwrotnie komplementarną.
    Czyli: najpierw komplementarna, potem odwrócona."""
    return complement(sequence)[::-1]


def find_orfs(sequence: str, min_length: int = 1) -> list:
    """Wyszukuje wszystkie ORF-y (ATG -> STOP) o minimalnej długości.
    Kodon STOP to TAA, TAG lub TGA.
    min_length to minimalna liczba kodonów (wliczając START i STOP).
    Zwraca listę słowników z kluczami: start, end, length (wszystko w nt, indeks od 1)."""
    stop_codons = {'TAA', 'TAG', 'TGA'}
    orfs = []

    for frame in range(3):
        i = frame
        while i < len(sequence) - 2:
            codon = sequence[i:i + 3]
            if codon == 'ATG':
                start = i
                for j in range(i + 3, len(sequence) - 2, 3):
                    stop_codon = sequence[j:j + 3]
                    if stop_codon in stop_codons:
                        end = j + 3
                        orf_length = end - start
                        if orf_length >= min_length * 3:
                            orfs.append({
                                'start': start + 1,
                                'end': end,
                                'length': orf_length
                            })
                        i = end
                        break
                else:
                    i += 3
            else:
                i += 3

    return orfs


def validate_fasta_file(filepath: str) -> list:
    """Wczytuje plik FASTA i sprawdza poprawność formatu.
    Zwraca listę błędów (pustą jeśli plik jest poprawny)."""
    errors = []
    # Dozwolone znaki w sekwencji DNA (duże i małe — bo wstawiamy imię małymi)
    allowed_chars = set('ACGTacgtRYSWKMBDHVNryswkmbdhvn')

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        errors.append(f"Błąd: plik '{filepath}' nie istnieje.")
        return errors

    if not lines:
        errors.append("Błąd: plik jest pusty.")
        return errors

    # Sprawdzamy czy pierwszy rekord zaczyna się od '>'
    if not lines[0].startswith('>'):
        errors.append("Linia 1: brak nagłówka (linia powinna zaczynać się od '>').")

    in_sequence = False
    for i, line in enumerate(lines, start=1):
        line = line.rstrip('\n')

        if line.startswith('>'):
            # Nagłówek — sprawdzamy czy nie jest sam '>'
            if len(line.strip()) == 1:
                errors.append(f"Linia {i}: nagłówek nie zawiera ID.")
            in_sequence = True
        elif in_sequence:
            # Linia sekwencji — sprawdzamy dozwolone znaki
            invalid = [c for c in line if c not in allowed_chars]
            if invalid:
                errors.append(f"Linia {i}: niedozwolone znaki: {set(invalid)}")
            # Sprawdzamy szerokość linii (max 80, ostatnia może być krótsza)
            if len(line) > 80:
                errors.append(f"Linia {i}: za szeroka ({len(line)} znaków, max 80).")
        else:
            errors.append(f"Linia {i}: zawartość przed pierwszym nagłówkiem.")

    return errors


def main():
    """Główna funkcja programu."""
    # 1. Pobieramy dane od użytkownika
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = validate_seq_id("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    # 2. Generujemy sekwencję i od razu liczymy statystyki
    #    (PRZED wstawieniem imienia — imię nie może wpływać na statystyki)
    sequence = generate_sequence(length)
    stats = calculate_stats(sequence)

    # 3. Wstawiamy imię do sekwencji (tylko do wyświetlenia w pliku)
    sequence_with_name = insert_name(sequence, name)

    # 4. Formatujemy rekord FASTA i zapisujemy do pliku
    fasta_record = format_fasta(seq_id, description, sequence_with_name)
    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(fasta_record)
    print(f"Sekwencja zapisana do pliku: {filename}")

    # 5. Wypisujemy statystyki (na podstawie czystej sekwencji bez imienia)
    print(f"Statystyki sekwencji (n={length}):")
    print(f"  A: {stats['A']:.2f}%")
    print(f"  C: {stats['C']:.2f}%")
    print(f"  G: {stats['G']:.2f}%")
    print(f"  T: {stats['T']:.2f}%")
    print(f"  GC-content: {stats['GC']:.2f}%")

    # 6. Wyszukiwanie motywów
    motif = input("\nPodaj motyw do wyszukania (Enter aby pominąć): ").strip()
    if motif:
        positions = find_motif(sequence, motif)
        if positions:
            print(f"Motyw '{motif}' znaleziony na pozycjach: {positions}")
        else:
            print(f"Motyw '{motif}' nie został znaleziony.")

    # 7. Sekwencja komplementarna i odwrotnie komplementarna
    comp = complement(sequence)
    rev_comp = reverse_complement(sequence)
    print(f"\nNić komplementarna:           {comp[:40]}{'...' if length > 40 else ''}")
    print(f"Nić odwrotnie komplementarna: {rev_comp[:40]}{'...' if length > 40 else ''}")

    with open(filename, 'a') as f:
        f.write(format_fasta(f"{seq_id}_comp", "nic komplementarna", comp))
        f.write(format_fasta(f"{seq_id}_revcomp", "nic odwrotnie komplementarna", rev_comp))
    print(f"Nici komplementarne dopisane do pliku: {filename}")

    # 8. Szukanie ORF-ów
    min_orf = validate_positive_int("\nPodaj minimalną długość ORF (w kodonach, min. 1): ", 1, 100_000)
    orfs = find_orfs(sequence, min_orf)
    if orfs:
        print(f"\nZnalezione ORF-y (min. {min_orf} kodon/y):")
        for orf in orfs:
            print(f"  start={orf['start']}, end={orf['end']}, długość={orf['length']} nt")
    else:
        print(f"\nNie znaleziono ORF-ów o minimalnej długości {min_orf} kodon/y.")

    # 9. Walidator pliku FASTA
    validate_path = input("\nPodaj ścieżkę do pliku FASTA do walidacji (Enter aby pominąć): ").strip()
    if validate_path:
        errors = validate_fasta_file(validate_path)
        if not errors:
            print("Plik jest poprawny formatowo.")
        else:
            print(f"Znalezione błędy ({len(errors)}):")
            for error in errors:
                print(f"  {error}")


if __name__ == "__main__":
    main()