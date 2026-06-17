import pandas as pd
import numpy as np
from pathlib import Path



# =============================================================================
# DANE WEJŚCIOWE
# =============================================================================

plik_do_zapisu = 'analityka_biegowa_master.csv'
folder_zapisu = 'Projekt_02_bieganie'
folder_zapisu_df_dane = Path('Projekt_02_bieganie') / 'treningi_pojedyncze'

# Plik od sortowania
sciezka_pliku_csv = Path.home()/ 'Dokumenty' / 'NAUKA' / 'PROJEKT_ANALIZA_DANYCH' / folder_zapisu / plik_do_zapisu



# =============================================================================
# ZMIENNE WEJŚCIOWE
# =============================================================================

sprint_predkosc = '2:59'
rytm_predkosc = '4:30'
baza_predkosc = '8:00'



# =============================================================================
# Strefy Tętna wg "Uphill Athlete" - GÓRNE ZAKRESY
# =============================================================================

prog_tlenowy = 138
prog_beztlenowy = 165



# =============================================================================
# FUNKCJE
# =============================================================================

def z_predkosc_na_tempo_srednie(df: pd.DataFrame):
    """
    Przelicza prędkość [m/s] na średnie tempo w formacie "0:00" [min/km].
    Przyjmuje całą tabelę DF i sam wchodzi do kolumny ['prędkość'].
    """ 
    if isinstance(df['prędkość'], pd.Series):
        predkosc = df['prędkość'].mean()
    if pd.isna(predkosc) or predkosc <= 0.1:
        return "0:00"
    minuty = int(1000 / predkosc // 60)
    sekundy = int(1000 / predkosc % 60)
    return f"{minuty}:{str(sekundy).zfill(2)}"


def z_predkosc_na_tempo_max(df: pd.DataFrame):
    """
    Przelicza prędkość [m/s] na średnie tempo w formacie "0:00" [min/km].
    Przyjmuje całą tabelę DF i sam wchodzi do kolumny ['prędkość'].
    """ 
    if isinstance(df['prędkość'], pd.Series):
        predkosc = df['prędkość'].max()
    if pd.isna(predkosc) or predkosc <= 0.1:
        return "0:00"
    minuty = int(1000 / predkosc // 60)
    sekundy = int(1000 / predkosc % 60)
    return f"{minuty}:{str(sekundy).zfill(2)}"


def z_tempo_na_predkosc(tempo: str):
    """
    Przelicza tempo biegu [min/km] na prędkość [m/s].
    Przyjmuje wartość tekstową np. "5:40".
    """
    min_tekst, sec_tekst = tempo.split(':')
    wszystkie_sekundy = int(min_tekst) * 60 + int(sec_tekst)    
    return round(1000 / wszystkie_sekundy, 2)


def oblicz_predkosc_srednia(df: pd.DataFrame):
    """
    Oblicza średnią prędkość w kolumnie 'prędkość'.
    Przyjmuje całą tabelę DF i sam wchodzi do kolumny ['prędkość'].
    """
    if isinstance(df['prędkość'], pd.Series):
        predkosc_srednia = df['prędkość'].mean()
    else:
        predkosc_srednia = df['prędkość']
    if pd.isna(predkosc_srednia) or predkosc_srednia <= 0.1:
        return 0
    return round(predkosc_srednia, 2)


def oblicz_predkosc_max(df: pd.DataFrame):
    """
    Oblicza prędkość maksymalną w kolumnie 'prędkość'.
    Przyjmuje całą tabelę DF i sam wchodzi do kolumny ['prędkość'].
    """
    if isinstance(df['prędkość'], pd.Series):
        predkosc_max = df['prędkość'].max()
    else:
        predkosc_max = df['prędkość']
    if pd.isna(predkosc_max) or predkosc_max <= 0.1:
        return 0
    return round(predkosc_max, 2)


def oblicz_dystans(df: pd.DataFrame):
    """
    Oblicza dystans odcinka w kolumnie 'dystans'.
    Przyjmuje całą tabelę DF i sam wchodzi do kolumny ['dystans'].
    """
    if df['dystans'].empty or pd.isna(df['dystans'].max()):
        return 0.0
    wynik = (df['dystans'].max() - df['dystans'].min()) / 1000
    return round(float(wynik), 3)


def oblicz_czas_trwania(df: pd.DataFrame):
    """
    Oblicza czas trwanie odcinka ciągłego w tabeli na podstawie kolumny ['stoper'].
    Przyjmuje całą tabelę DF.
    """
    return str(df['stoper'].max() - df['stoper'].min()).split()[-1]


def oblicz_czas_trwania_interwalu(df: pd.DataFrame):
    """
    Oblicza czas trwania dla interwałów czy tzw. wysp. 
    Liczy ilość wierszy wystęujących w DF i zamienia na czas.
    """
    sekundy = len(df['stoper'])
    return int(sekundy)


def zamien_na_czas(sekundy: int):
    """
    Konwertuje sekundy na format HH:MM:SS. 
    Obsługuje braki danych (NaN, None) oraz wartości nieliczbowe, 
    zwracając w takich przypadkach "00:00:00".
    """
    if pd.isna(sekundy) or sekundy is None or sekundy <= 0:
        return "00:00:00"
    try:
        sekundy_int = int(round(float(sekundy)))
        return str(pd.to_timedelta(sekundy_int, unit='s')).split()[-1]
    except (ValueError, TypeError):
        return "00:00:00"
    

def oblicz_tetno_srednie(df: pd.DataFrame):
    """
    Oblicza średnie tętno odcinka w tabeli na podstawie kolumny ['tętno'].
    Przyjmuje samo DF bez nazwy kolumny.
    """
    if isinstance(df['tętno'], pd.Series):
        srednia = df['tętno'].mean()
    else:
        srednia = df['tętno']
    if pd.isna(srednia):
        return 0
    return int(srednia)


def oblicz_tetno_max(df: pd.DataFrame):
    """
    Oblicza maksymalne tętno w tabeli na podstawie kolumny ['tętno'].
    Przyjmuje samo DF bez nazwy kolumny.
    """
    t_max = df['tętno'].max()
    prog_tetno_max = int(t_max) if pd.notna(t_max) else 0
    return prog_tetno_max


def oblicz_tetno_std(df: pd.DataFrame):
    """
    Oblicza odchylenie standardowe tętna w tabeli na podstawie kolumny ['tętno'].
    Przyjmuje samo DF bez nazwy kolumny.
    """
    if df['tętno'].empty:
        return 0.0
    wynik = df['tętno'].std()
    if pd.isna(wynik):
        return 0.0    
    return round(float(wynik), 2)


def oblicz_tetno_poczatkowe(df: pd.DataFrame):
    """
    Oblicza tętno początkowe aktywności w tabeli na podstawie kolumny ['tętno'].
    Potrzebne do obliczenia Delta tętna.
    Przyjmuje samo DF bez nazwy kolumny.
    """
    if df['tętno'].empty:
        return 0
    tetno_poczatkowe = df['tętno'].head(15).max()
    if pd.isna(tetno_poczatkowe):
        return 0        
    return int(tetno_poczatkowe)


def oblicz_tetno_koncowe(df: pd.DataFrame):
    """
    Oblicza tętno końcowe po 5 minutach aktywności na podstawie kolumny ['tętno'].
    Potrzebne do obliczenia Delta tętna.
    Przyjmuje samo DF bez nazwy kolumny.
    """
    if df['tętno'].empty:
        return 0    
    if len(df['tętno']) >= 300:
        tetno_koncowe = df['tętno'].iloc[285:300].min()
    else:
        tetno_koncowe = df['tętno'].tail(15).min()     
    if pd.isna(tetno_koncowe):
        return 0
    return int(tetno_koncowe)


def oblicz_delta_tetna(df: pd.DataFrame):
    if df['tętno'].empty:
        return 0
    tetno_poczatkowe = df['tętno'].head(15).max()
    tetno_koncowe = df['tętno'].min()
    delta = tetno_koncowe - tetno_poczatkowe
    if pd.isna(delta):
        return 0
    return int(delta)


def uplyw_czasu_w_strefie(df: pd.DataFrame, strefa: str):
    """
    Oblicza ile czasu spędziłeś w poszczególnych aktywnościach w kolumnie ['marszobieg'].
    Przyjmuje kolumnę bez nazwy oraz string z nazwą aktywności która nas interesuje.
    """
    maska = df['marszobieg'] == strefa
    return str(pd.to_timedelta(maska.sum(), unit='s')).split()[-1]


def oblicz_kadencje_srednia(df: pd.DataFrame):
    """
    Oblicza kadencję z biegu na odcinku, który zawiera DF.
    Przyjmuje tylko tabelę DF bez nazw kolumn ['prędkość'] i ['kadencja']
    """
    if df is None or df.empty:
        return 0
    df_kadencja = df[(df['marszobieg'] == 'bieg') & (df['kadencja'] >= 150)]
    if df_kadencja.empty:
        return 0
    srednia = df_kadencja['kadencja'].mean()
    if pd.isna(srednia):
        return 0
    return int(srednia)


def pobierz_temperature():
    """
    Pyta cię o temperaturę powietrza podczas biegu.
    Przyjmuje int.
    """
    global dzien_biegu
    while True:
        temperatura = input(f'Wpisz jaka była temperatura powietrza podczas biegu dnia {dzien_biegu}: ')
        print('\n')
        try:
            return int(temperatura)
        except ValueError:
            print('Zły format temperatury, spróbuj jeszcze raz (użyj samej liczby): ')
            
            
def oblicz_przewyzszenia(df: pd.DataFrame):
    """
    Oblicza przewyższenia na trasie na podstawie kolumny ['wysokość'].
    Przyjmuje samą tabelę DF bez nazwy kolumny.
    Oddaje krotkę z dwoma int, gdzie jedna to suma pod górę a dróga w dół.
    """
    if df['wysokość'].empty:
        return 0, 0
    roznice = df['wysokość'].diff()
    ascent = roznice[roznice > 0].sum()
    descent = roznice[roznice < 0].abs().sum()
    return int(round(ascent, 0)), int(round(descent, 0))


def analizuj_odpoczynek(grupa):
    sekundy = len(grupa)
    aktywnosc = grupa['marszobieg'].iloc[0]
    return pd.Series({
        'prędkość': oblicz_predkosc_srednia(grupa),
        'sekundy': sekundy,
        'delta': oblicz_delta_tetna(grupa),
        'aktywność': aktywnosc
        })
            
        
def oblicz_dystans_dla_serii(seria):
    if seria.empty:
        return 0.0, 0.0
    
    id_wysp = seria.index
    df_wyspy = df_dane[df_dane['wyspy_aktywności'].isin(id_wysp)]
    
    dystans = df_wyspy.groupby('wyspy_aktywności').apply(oblicz_dystans)
    
    suma = round(float(dystans.sum()), 3)
    srednia = round(float(dystans.mean()), 3)
    
    return suma, srednia


def zapis_pliku_csv(df_do_zapisu, folder_do_zapisu ,nazwa_pliku_csv):
    sciezka_pliku_do_zapisu = Path.home()/ 'Dokumenty' / 'NAUKA' / 'PROJEKT_ANALIZA_DANYCH' / folder_do_zapisu / nazwa_pliku_csv
    if sciezka_pliku_do_zapisu.exists():
        print(f'Dane zostały dopisane do pliku "{nazwa_pliku_csv}".\n')
        return df_do_zapisu.to_csv(sciezka_pliku_do_zapisu, index=False, header=False, mode='a')
    else:
        print(f'Dane zostały zapisane do pliku "{nazwa_pliku_csv}".\n')
        return df_do_zapisu.to_csv(sciezka_pliku_do_zapisu, index=False)
            

def zapis_pliku_csv_pytaj(df_do_zapisu, folder_do_zapisu ,nazwa_pliku_csv):
    while True:
        czy_zapisac = input(f'Czy zapisać do pliku "{nazwa_pliku_csv}" (t/n): ')
        czy_zapisac_czysty = czy_zapisac.strip().lower()
        if czy_zapisac_czysty == 't':
            sciezka_pliku_do_zapisu = Path.home()/ 'Dokumenty' / 'NAUKA' / 'PROJEKT_ANALIZA_DANYCH' / folder_do_zapisu / nazwa_pliku_csv
            if sciezka_pliku_do_zapisu.exists():
                print(f'Dane zostały dopisane do pliku "{nazwa_pliku_csv}".\n')
                return df_do_zapisu.to_csv(sciezka_pliku_do_zapisu, index=False, header=False, mode='a')
            else:
                print(f'Dane zostały zapisane do pliku "{nazwa_pliku_csv}".\n')
                return df_do_zapisu.to_csv(sciezka_pliku_do_zapisu, index=False)
        elif czy_zapisac_czysty == 'n':
            print('Zapis anulowany.\n')
            return
        else:
            print('Spróbuj jeszcze raz, pamiętaj aby wybrać t lub n')


def analizuj_trend_tetna(kolumna_hr):
    """
    Oblicza kierunek i wielkość dryfu tętna z wykorzystaniem regresji liniowej.
    Zoptymalizowano pod kątem usuwania pustych odczytów (NaN).
    """
    # Zabezpieczenie: usunięcie ewentualnych braków danych z pulsometru
    kolumna_hr = kolumna_hr.dropna()
    
    if kolumna_hr.empty or len(kolumna_hr) < 2:
        return "Brak danych", 0.0, 0.0

    x = np.arange(len(kolumna_hr))
    y = kolumna_hr.values

    # a - nachylenie (wzrost hr/sekundę), b - przecięcie z osią (startowe HR)
    a, b = np.polyfit(x, y, 1)

    hr_start_trend = b
    hr_end_trend = a * len(kolumna_hr) + b
    roznica_trend = round(hr_end_trend - hr_start_trend, 1)

    kierunek = "Rosnący" if a > 0 else "Spadający"
    
    return kierunek, roznica_trend, a


def oblicz_cardiac_drift(df):
    """
    Oblicza Cardiac Drift (Aerobic Decoupling) na podstawie stosunku prędkości do tętna.
    Zabezpieczono przed dzieleniem przez zero i błędami pustych ramek.
    """
    # Zabezpieczenie fizjologiczne: drift liczymy tylko z danych, gdzie faktycznie biegniemy
    df = df.dropna(subset=['prędkość', 'tętno'])
    
    if df.empty or len(df) < 60:
        return 0.0

    polowa = len(df) // 2
    h1 = df.iloc[:polowa]
    h2 = df.iloc[polowa:]

    mean_hr1 = h1['tętno'].mean()
    mean_hr2 = h2['tętno'].mean()

    # Blokada dzielenia przez zero
    if mean_hr1 == 0 or mean_hr2 == 0:
        return 0.0

    efekt_1 = h1['prędkość'].mean() / mean_hr1
    efekt_2 = h2['prędkość'].mean() / mean_hr2

    if efekt_1 == 0:
        return 0.0

    # Wzór Joe Friela na sprzężenie tlenowe
    drift = ((efekt_1 - efekt_2) / efekt_1) * 100
    return round(drift, 2)


def oblicz_ef(df_bieg):
    """
    Oblicza Efficiency Factor (EF) = średnia prędkość / średnie tętno.
    """
    df_bieg = df_bieg.dropna(subset=['prędkość', 'tętno'])
    
    if df_bieg.empty:
        return 0.0
    
    srednia_predkosc = df_bieg['prędkość'].mean()
    srednie_hr = df_bieg['tętno'].mean()
    
    if srednie_hr == 0:
        return 0.0
        
    return round(srednia_predkosc / srednie_hr, 4)


def oblicz_skorygowany_decoupling(df):
    """
    Oblicza dryf sercowy skorygowany o nachylenie terenu (GAP).
    Korekta: każde 1% nachylenia to ok. 3.5% dodatkowego wysiłku.
    """
    df = df.dropna(subset=['dystans', 'wysokość', 'prędkość', 'tętno']).copy()
    
    if df.empty or len(df) < 60:
        return 0.0

    # .fillna(0) zapobiega błędom na pierwszej iteracji (diff zrzuca NaN)
    dist_diff = df['dystans'].diff().fillna(0) * 1000  # metry
    alt_diff = df['wysokość'].diff().fillna(0)         # metry
    
    # Zabezpieczenie przed mikroskokami GPS i dzieleniem przez zero
    # Grade jest liczone tylko, jeśli przebiegliśmy co najmniej 1 metr w danej sekundzie/interwale
    grade = np.where(dist_diff > 1.0, alt_diff / dist_diff, 0)
    
    # Zabezpieczenie fizjologiczne: bieganie stromo w dół również kosztuje energię
    # Algorytm min/max obcina nierealne piki z GPS (grade powyżej 30%)
    grade = np.clip(grade, -0.15, 0.30)
    
    gap_speed = df['prędkość'] * (1 + grade * 3.5)

    polowa = len(df) // 2
    h1, h2 = df.iloc[:polowa], df.iloc[polowa:]

    mean_hr1 = h1['tętno'].mean()
    mean_hr2 = h2['tętno'].mean()

    if mean_hr1 == 0 or mean_hr2 == 0: 
        return 0.0

    ef1 = gap_speed.iloc[:polowa].mean() / mean_hr1
    ef2 = gap_speed.iloc[polowa:].mean() / mean_hr2

    if ef1 == 0: 
        return 0.0
    
    drift_skorygowany = ((ef1 - ef2) / ef1) * 100
    return round(drift_skorygowany, 2)


def oblicz_fatigue_score(dryft, delta_hr, ef):
    """
    Autorski FST (Fatigue Score) Gema, zoptymalizowany pod profil Zawodnika:
    - Dryft < 5% to norma (Max 40 pkt obciążenia)
    - Delta HR z MAF po 5 min na poziomie 25+ bpm to wynik idealny (Max 30 pkt)
    - Skala EF odniesiona do "Złotego Okresu" 0.0210 (Max 30 pkt)
    Zwraca wynik 0-100 (wyższy = większe wyeksploatowanie silnika na treningu).
    """
    # 1. Komponent Dryftu
    drift_comp = max(0, dryft * 4)
    drift_comp = min(40, drift_comp)

    # 2. Komponent Regeneracji 
    # Dla Autoregulacji (MAF) spadek 25 bpm to 0 zmęczenia.
    recovery_comp = max(0, (25 - delta_hr) * 2)
    recovery_comp = min(30, recovery_comp)

    # 3. Komponent Wydajności (EF)
    # Różnica względem życiówki 0.0210
    ef_comp = max(0, (0.0210 - ef) * 5000)
    ef_comp = min(30, ef_comp)

    # Sumowanie wyniku do skali 0-100
    fatigue_score = drift_comp + recovery_comp + ef_comp
    return int(min(100, max(0, fatigue_score)))


def oblicz_aef_terenowe(df_bieg):
    """
    Oblicza Skorygowany Wskaźnik Wydajności (aEF) z uwzględnieniem przewyższeń (GAP).
    Każde 1% nachylenia pod górę dodaje ok. 3.5% do "wirtualnej" prędkości.
    Zabezpieczone przed mikroskokami GPS.
    """
    df_bieg = df_bieg.dropna(subset=['dystans', 'wysokość', 'prędkość', 'tętno']).copy()
    
    if df_bieg.empty or len(df_bieg) < 10:
        return 0.0

    dist_diff = df_bieg['dystans'].diff().fillna(0) * 1000
    alt_diff = df_bieg['wysokość'].diff().fillna(0)
    
    grade = np.where(dist_diff > 1.0, alt_diff / dist_diff, 0)
    grade = np.clip(grade, -0.15, 0.30)
    
    # Skorygowana prędkość (GAP)
    gap_speed = df_bieg['prędkość'] * (1 + grade * 3.5)
    
    srednia_predkosc_gap = gap_speed.mean()
    srednie_hr = df_bieg['tętno'].mean()
    
    if srednie_hr == 0:
        return 0.0
        
    return round(srednia_predkosc_gap / srednie_hr, 4)


def oblicz_ultra_index(ef_globalny, dystans_km): 
    """
    Ultra-Index (UI) rozwiązujący problem 1km vs 20km.
    Wzór Zawodnika: Dystans * Wydajność. Mnożnik 1000 dla czytelności całkowitoliczbowej.
    """
    if ef_globalny == 0 or dystans_km == 0:
        return 0
    return int(round(ef_globalny * dystans_km * 1000, 0))


def predkosc_na_tempo_wykres(v):
    minuty = int(1000 / v // 60)
    sekundy = int(1000 / v % 60)
    return f'{minuty}:{sekundy:02d}'
    


# ZAPISANIE PLIKU DO DATAFRAME

folder_wejsciowy = Path.home() / 'Pobrane'

wzorzec_nazwy = '*.csv'
lista_plikow = list(folder_wejsciowy.glob(wzorzec_nazwy))


if not lista_plikow:
    print('Nie znaleziono plików pasujących do wzorca')
    
else:
    wyniki_do_skonsolidowania = []
    for sciezka_pliku in lista_plikow:
        
        # print(sciezka_pliku.name)

        df_dane_brudne = pd.read_csv(
            filepath_or_buffer=sciezka_pliku,
            sep=',',
            header=0,
            usecols=[
                'Time', 
                'Distance', 
                'HeartRate', 
                'Speed', 
                'RunCadence', 
                'Altitude',
                'Latitude',
                'Longitude'
                ]
            ).reset_index(
                drop=False
                ).rename(
                    columns={
                        'index': 'sekundy',
                        'HeartRate': 'tętno',
                        'RunCadence': 'kadencja',
                        'Speed': 'prędkość',
                        'Distance': 'dystans',
                        'Altitude': 'wysokość',
                        'Latitude': 'szerokość_goegraficzna',
                        'Longitude': 'długość_geograficzna'
                        }
                    )
                    
        df_dane_brudne['dystans'] = df_dane_brudne['dystans'].fillna(0).round(2)
        df_dane_brudne['wysokość'] = df_dane_brudne['wysokość'].fillna(0).rolling(window=100).mean().bfill().round(2)
        df_dane_brudne['prędkość'] = df_dane_brudne['prędkość'].shift(-7).ffill().fillna(0).round(2)
        df_dane_brudne['tętno'] = df_dane_brudne['tętno'].fillna(0).astype('Int32')
        df_dane_brudne['kadencja'] = df_dane_brudne['kadencja'].shift(-7).ffill().fillna(0)


        # USUWAM SZUM W KADENCJI ZWIĄZANY Z NAGŁYM POJAWIANIEM SIĘ ZER W KADENCJI PODCZAS BIEGU
        
        maska_szumu = (df_dane_brudne['kadencja'] == 0) & (df_dane_brudne['prędkość'] >= 0.2)
        df_dane_brudne['kadencja'] = np.where(maska_szumu, np.nan, df_dane_brudne['kadencja'])
        df_dane_brudne['kadencja'] = df_dane_brudne['kadencja'].interpolate(method='linear')           
        df_dane_brudne['kadencja'] = df_dane_brudne['kadencja'].round(0).astype('Int32') * 2
        
                    
        
# =============================================================================
# Czyszczenie danych i przypisywanie ich do nowych kolumn
# =============================================================================
            
        df_dane = df_dane_brudne.assign(
            data = pd.to_datetime(df_dane_brudne['Time'].astype(str).str.slice(0, 10)),
            stoper = pd.to_timedelta(df_dane_brudne['sekundy'], unit='s'),
            )[['data', 
               'stoper', 
               'szerokość_goegraficzna',
               'długość_geograficzna',
               'dystans', 
               'wysokość', 
               'prędkość',
               'kadencja',
               'tętno', 
               ]].copy()
        
               
        
# =============================================================================
# Ustalenie granic dla kolumny STREFY_TĘTNA
# =============================================================================

        warunek_stref = [
            (df_dane['tętno'] >= prog_beztlenowy),
            (df_dane['tętno'] > prog_tlenowy),
            (df_dane['tętno'] <= prog_tlenowy)
            ]
        
        etykiety_stref = [
            'beztlen',
            'czarna_dziura',
            'tlen'
            ]

        df_dane['strefy_tętna'] = np.select(warunek_stref, etykiety_stref, default='błąd')



# =============================================================================
# Ustalanie granic dla kolumny MARSZOBIEGI
# =============================================================================
        
        warunek_marszobieg = [
            ((df_dane['prędkość'] >= z_tempo_na_predkosc(baza_predkosc)) & (df_dane['kadencja'] >= 150)).fillna(False).astype(bool),
            ((df_dane['prędkość'] < z_tempo_na_predkosc(baza_predkosc)) & (df_dane['tętno'] < (prog_tlenowy * 0.8)) & (df_dane['kadencja'] >= 150)).fillna(False).astype(bool),
            (df_dane['prędkość'] >= 0.2).fillna(False).astype(bool),
            (df_dane['prędkość'] < 0.2).fillna(False).astype(bool)
            ]
        etykiety_marszobieg = ['bieg', 'regeneracja', 'marsz', 'postój']
        
        df_dane['marszobieg_surowy'] = np.select(warunek_marszobieg, etykiety_marszobieg, default='błąd')
        
        # Minimalny filtr 2-sekundowy, żeby usunąć pojedyncze błędy np. GPS-u
        grupy_stanow = (df_dane['marszobieg_surowy'] != df_dane['marszobieg_surowy'].shift()).cumsum()
        dlugosci_stanow = df_dane['marszobieg_surowy'].groupby(grupy_stanow).transform('size')
        df_dane['marszobieg'] = df_dane['marszobieg_surowy'].mask(dlugosci_stanow < 2).ffill().bfill()
        df_dane.drop(columns=['marszobieg_surowy'], inplace=True, errors='ignore')
        
        
        
# =============================================================================
# Ustalanie granic dla kolumny AKTYWNOŚCI
# =============================================================================
        
        czy_ruch_biegowy = df_dane['marszobieg'].isin(['bieg', 'regeneracja'])
        
        warunek_aktywnosc = [
            (czy_ruch_biegowy) & (df_dane['prędkość'] >= z_tempo_na_predkosc(sprint_predkosc)),
            (czy_ruch_biegowy) & (df_dane['prędkość'] >= z_tempo_na_predkosc(rytm_predkosc)),
            (df_dane['marszobieg'].isin(['postój', 'marsz', 'regeneracja'])),
            (df_dane['marszobieg'] == 'bieg') & (df_dane['strefy_tętna'] == 'beztlen'),
            (df_dane['marszobieg'] == 'bieg')
            ]
        
        etykiety_aktywnosc = ['sprint', 'rytm', 'odpoczynek', 'próg', 'baza']
                           
        df_dane['aktywność_temp'] = np.select(warunek_aktywnosc, etykiety_aktywnosc, default='błąd')
        
        hierarchia_mocy = {'sprint': 3, 'rytm': 2, 'próg': 1, 'baza': 1, 'odpoczynek': 0}
        df_dane['id_wyspy'] = (df_dane['marszobieg'] != df_dane['marszobieg'].shift()).cumsum()
        df_dane['moc_wyspy'] = df_dane['aktywność_temp'].map(hierarchia_mocy)
        maksymalna_moc = df_dane.groupby('id_wyspy')['moc_wyspy'].transform('max')
        
        warunki_ostateczne = [
            (czy_ruch_biegowy) & (maksymalna_moc >= 3), 
            (czy_ruch_biegowy) & (maksymalna_moc == 2), 
            (df_dane['aktywność_temp'] == 'próg'),
            (df_dane['aktywność_temp'] == 'baza'),
            (df_dane['marszobieg'].isin(['postój', 'marsz', 'regeneracja']))
            ]
        
        etykiety_ostateczne = ['sprint', 'rytm', 'próg', 'baza', 'odpoczynek']
        df_dane['aktywność'] = np.select(warunki_ostateczne, etykiety_ostateczne, default='błąd')
        
        df_dane.drop(columns=['aktywność_temp', 'id_wyspy', 'moc_wyspy'], inplace=True, errors='ignore')                                        



# =============================================================================
# DZIELĘ AKTYWNOŚĆ ODPOCZYNEK NA DWA ODPOCZYNKI, BAZOWY I MOCY
# =============================================================================
                
        indeksy_biegu = df_dane[df_dane['marszobieg'] == 'bieg'].index
        
        if not indeksy_biegu.empty:
            start_treningu = indeksy_biegu[0]
            koniec_treningu = indeksy_biegu[-1]
        
            df_dane.loc[:start_treningu - 1, 'aktywność'] = 'rozgrzewka'
            df_dane.loc[koniec_treningu + 1:, 'aktywność'] = 'schłodzenie'
        
            maska_trening = (df_dane.index >= start_treningu) & (df_dane.index <= koniec_treningu)
            
            aktywnosc_do_pamieci = df_dane['aktywność'].copy()
            
            grupy_temp = (aktywnosc_do_pamieci != aktywnosc_do_pamieci.shift()).cumsum()
            rozmiary_wysp = aktywnosc_do_pamieci.groupby(grupy_temp).transform('size')
            
            aktywnosc_oczyszczona = aktywnosc_do_pamieci.mask((rozmiary_wysp < 5) & (aktywnosc_do_pamieci == 'baza'))
            df_dane['poprzedni_wysiłek'] = aktywnosc_oczyszczona.where(aktywnosc_oczyszczona != 'odpoczynek').ffill().shift()
        
            warunki_odpoczynku = [
                (maska_trening) & (df_dane['aktywność'] == 'odpoczynek') & (df_dane['poprzedni_wysiłek'].isin(['rytm', 'sprint', 'próg'])),
                (maska_trening) & (df_dane['aktywność'] == 'odpoczynek')
            ]
        
            etykiety_odpoczynku = [
                'odpoczynek_moc',
                'odpoczynek_baza'
            ]
        
            df_dane['aktywność'] = np.select(
                warunki_odpoczynku, 
                etykiety_odpoczynku, 
                default=df_dane['aktywność']
            )
        
            df_dane.drop(columns=['poprzedni_wysiłek'], inplace=True)     
 

               
# =============================================================================
# Podział aktywności na SERIE - wyspy_aktywności
# =============================================================================

        df_dane['wyspy_aktywności'] = (df_dane['aktywność'].ne(df_dane['aktywność'].shift(1))).cumsum()
        wyspy_aktywnosci = df_dane.groupby(['aktywność', 'wyspy_aktywności']).size()
        
        df_dane['wyspy_marszobieg'] = (df_dane['marszobieg'] != df_dane['marszobieg'].shift(1)).cumsum()



# =============================================================================
# Podział CAŁEGO TRENINGU NA ETAPY OSOBNE DF
# =============================================================================

        df_rozgrzewka = df_dane[df_dane['aktywność'] == 'rozgrzewka']
        df_schlodzenie = df_dane[df_dane['aktywność'] == 'schłodzenie']
        df_trening_biegowy = df_dane.loc[start_treningu:koniec_treningu]
        
        df_baza = df_dane[(df_dane['aktywność'] == 'baza')]
        df_odpoczynek_baza = df_trening_biegowy[(df_trening_biegowy['aktywność'] == 'odpoczynek_baza')]
        df_odpoczynek_moc = df_trening_biegowy[(df_trening_biegowy['aktywność'] == 'odpoczynek_moc')]
        df_prog = df_dane[df_dane['aktywność'] == 'próg']
        df_rytmy = df_dane[df_dane['aktywność'] == 'rytm']
        df_sprint = df_dane[df_dane['aktywność'] == 'sprint']

        df_czarna_dziura = df_trening_biegowy[(df_trening_biegowy['strefy_tętna'] == 'czarna_dziura')]
        df_tlen = df_trening_biegowy[(df_trening_biegowy['strefy_tętna'] == 'tlen')]

        wyspy_marszobieg = df_trening_biegowy.groupby(['marszobieg', 'wyspy_marszobieg']).size()
        id_najdluzszy_bieg = wyspy_marszobieg['bieg'].idxmax()
        df_najdluzszy_bieg = df_dane[(df_dane['marszobieg'] == 'bieg') & (df_dane['wyspy_marszobieg'] == id_najdluzszy_bieg)]
        
        
        
# =============================================================================
# DATA i TEMPERATURA biegu do nowego pliku .csv
# =============================================================================
        
        data_biegu = df_dane.at[0, 'data']
        dzien_biegu = data_biegu.date()
        
        temperatura = pobierz_temperature()
        # temperatura = np.nan
        print(f'\ndata treningu --> {dzien_biegu}')
        print(f'temperatura powietrza --> {temperatura} st C\n')
               
        
        
# =============================================================================
# ROZGRZEWKA        
# =============================================================================
        
        rozgrzewka_dystans = oblicz_dystans(df_rozgrzewka)
        print(f'rozgrzewka: dystans --> {rozgrzewka_dystans} km')
        rozgrzewka_predkosc_srednia = oblicz_predkosc_srednia(df_rozgrzewka)
        rozgrzewka_tempo_srednie = z_predkosc_na_tempo_srednie(df_rozgrzewka)
        print(f'rozgrzewka: tempo średnie --> {rozgrzewka_tempo_srednie} min/km')
        rozgrzewka_tetno_srednie = oblicz_tetno_srednie(df_rozgrzewka)
        print(f'rozgrzewka: tętno średnie --> {rozgrzewka_tetno_srednie} bpm\n')

                
        
# =============================================================================
# CZĘŚĆ TRENING BIEGOWY
# =============================================================================
            
        trening_biegowy_dystans = oblicz_dystans(df_trening_biegowy)
        print(f'trening: dystans --> {trening_biegowy_dystans} km')
        trening_biegowy_czas = oblicz_czas_trwania(df_trening_biegowy)
        print(f'trening: czas --> {trening_biegowy_czas} hms')
        
        trening_biegowy_postoj_czas = uplyw_czasu_w_strefie(df_trening_biegowy, 'postój')
        print(f'trening: czas postoju --> {trening_biegowy_postoj_czas} hms')
        trening_biegowy_marsz_czas = uplyw_czasu_w_strefie(df_trening_biegowy, 'marsz')
        print(f'trening: czas marszu --> {trening_biegowy_marsz_czas} hms')
        trening_biegowy_bieg_czas = uplyw_czasu_w_strefie(df_trening_biegowy, 'bieg')
        print(f'trening: czas wszystkich biegów --> {trening_biegowy_bieg_czas} hms')
        
        trening_czarna_dziura_czas = zamien_na_czas(oblicz_czas_trwania_interwalu(df_czarna_dziura))
        print(f'trening: czas bycia w czarnej dziurze --> {trening_czarna_dziura_czas} hms')
        trening_tlen_czas = zamien_na_czas(oblicz_czas_trwania_interwalu(df_tlen))
        print(f'trening: czas bycia w tlenie --> {trening_tlen_czas} hms')

        trening_biegowy_podgore, trening_biegowy_zgorki = oblicz_przewyzszenia(df_trening_biegowy)
        print(f'trening: podgóre --> {trening_biegowy_podgore} m')
        print(f'trening: zgórki --> {trening_biegowy_zgorki} m')
        
        trening_biegowy_prędkość_średnia = oblicz_predkosc_srednia(df_trening_biegowy)
        trening_biegowy_srednie_tempo = z_predkosc_na_tempo_srednie(df_trening_biegowy)
        print(f'trening: tempo średnie --> {trening_biegowy_srednie_tempo} min/km')
        
        trening_biegowy_tetno_srednie = oblicz_tetno_srednie(df_trening_biegowy)
        print(f'trening: tętno średnie --> {trening_biegowy_tetno_srednie} bpm')
        trening_biegowy_tetno_odchylenie = oblicz_tetno_std(df_trening_biegowy)
        print(f'trening: tętno odchylenie standardowe --> {trening_biegowy_tetno_odchylenie} bpm')
        trening_biegowy_tetno_max = int(df_trening_biegowy['tętno'].max())
        print(f'trening: tętno maksymalne --> {trening_biegowy_tetno_max} bpm\n')

        
        
# =============================================================================
# CZĘŚĆ NAJDŁUŻSZY BIEG
# =============================================================================

        najdluzszy_bieg_dystans = oblicz_dystans(df_najdluzszy_bieg)
        print(f'najdłuższy bieg: dystans --> {najdluzszy_bieg_dystans} km')
        
        najdluzszy_bieg_predkosc_srednia = oblicz_predkosc_srednia(df_najdluzszy_bieg)
        najdluzszy_bieg_tempo_srednie = z_predkosc_na_tempo_srednie(df_najdluzszy_bieg)
        print(f'najdłuższy bieg: tempo średnie --> {najdluzszy_bieg_tempo_srednie} min/km')
        
        najdluzszy_bieg_tetno_srednie = oblicz_tetno_srednie(df_najdluzszy_bieg)
        print(f'najdłuższy bieg: tętno średnie --> {najdluzszy_bieg_tetno_srednie} bpm')
        najdluzszy_bieg_tetno_max = oblicz_tetno_max(df_najdluzszy_bieg)
        print(f'najdłuższy bieg: tętno maksymalne --> {najdluzszy_bieg_tetno_max} bpm')
        
        najdluzszy_bieg_kadencja = oblicz_kadencje_srednia(df_najdluzszy_bieg)
        print(f'najdłuższy bieg: kadencja --> {najdluzszy_bieg_kadencja} krok/min')
        
        najdluzszy_bieg_czarna_dziura_czas = zamien_na_czas((df_najdluzszy_bieg['strefy_tętna'] == 'czarna_dziura').sum())
        print(f'najdłuższy bieg: czas w czarnej dziurze --> {najdluzszy_bieg_czarna_dziura_czas} hms\n')

        
        
# =============================================================================
# CZĘŚĆ BAZA
# =============================================================================

        seria_baza = wyspy_aktywnosci.get('baza', pd.Series([], dtype=float))        
        
        liczba_interwałow_bazowych = (seria_baza > 10).sum()
        print(f'baza: liczba interwałów --> {liczba_interwałow_bazowych}')
        baza_laczny_dystans, baza_sredni_dystans = oblicz_dystans_dla_serii(seria_baza)
        print(f'baza: łączny dystans bazy --> {baza_laczny_dystans} km')
        print(f'baza: średni dystans na interwał --> {baza_sredni_dystans} km')
        baza_czas = zamien_na_czas(oblicz_czas_trwania_interwalu(df_baza))
        print(f'baza: łączny czas trwania --> {baza_czas} hms')
        baza_czarna_dziura_czas = zamien_na_czas((df_baza['strefy_tętna'] == 'czarna_dziura').sum())
        print(f'baza: czas w czarnej dziurze --> {baza_czarna_dziura_czas} hms')
        baza_predkosc_srednia = oblicz_predkosc_srednia(df_baza)
        baza_tempo_średnie = z_predkosc_na_tempo_srednie(df_baza)
        print(f'baza: tempo średnie --> {baza_tempo_średnie} min/km')
        baza_tetno_srednie = oblicz_tetno_srednie(df_baza)
        print(f'baza: tętno średnie --> {baza_tetno_srednie} bpm')
        baza_tetno_max = oblicz_tetno_max(df_baza)
        print(f'baza: tętno maksymalne --> {baza_tetno_max} bpm')
        baza_kadencja = oblicz_kadencje_srednia(df_baza)
        print(f'baza: kadencja --> {baza_kadencja} krok/min\n')

        

# =============================================================================
# CZĘŚĆ ODPOCZYNEK PO BAZIE
# =============================================================================
        
        seria_odpoczynek_baza = wyspy_aktywnosci.get('odpoczynek_baza', pd.Series([], dtype=float))
        liczba_odpoczynek_baza = (seria_odpoczynek_baza > 10).sum()
        print(f'odpoczynek_baza: liczba interwałów marszu --> {liczba_odpoczynek_baza} marszów')
        
        odpoczynek_baza_raport = df_odpoczynek_baza.groupby('wyspy_aktywności').apply(analizuj_odpoczynek)
        odpoczynek_baza_raport['numeracja'] = (odpoczynek_baza_raport.groupby('aktywność').cumcount() + 1).astype(str).str.zfill(2)
        odpoczynek_baza_raport.index = odpoczynek_baza_raport['aktywność'] + '_' + odpoczynek_baza_raport['numeracja']
        odpoczynek_baza_raport = odpoczynek_baza_raport.drop(columns=['aktywność', 'numeracja'])
        
        odpoczynek_baza_czas_sredni_interwalu = zamien_na_czas(odpoczynek_baza_raport.get('sekundy', pd.Series([0])).mean())
        print(f'odpoczynek_baza: średni czas każdego odpoczynku --> {odpoczynek_baza_czas_sredni_interwalu} hms')
        odpoczynek_baza_czarna_dziura_czas = zamien_na_czas((df_odpoczynek_baza['strefy_tętna'] == 'czarna_dziura').sum())
        print(f'odpoczynek_baza: czas w czarnej dziurze --> {odpoczynek_baza_czarna_dziura_czas} hms')
        odpoczynek_baza_predkosc_srednia_interwalu = round(odpoczynek_baza_raport['prędkość'].mean(), 2)
        odpoczynek_baza_tempo_srednie_interwalu = z_predkosc_na_tempo_srednie(odpoczynek_baza_raport)
        print(f'odpoczynek_baza: średnie tempo każdego odpoczynku --> {odpoczynek_baza_tempo_srednie_interwalu} min/km')
        odpoczynek_baza_tetno_max = df_odpoczynek_baza['tętno'].max()
        print(f'odpoczynek_baza: tętno maksymalne --> {odpoczynek_baza_tetno_max} bpm')
        odpoczynek_baza_delta_tetna_srednia = int(odpoczynek_baza_raport.get('delta', pd.Series([0])).mean())
        print(f'odpoczynek_baza: średnia delta tętna dla odpoczynku --> {odpoczynek_baza_delta_tetna_srednia} bpm\n')
            


# =============================================================================
# CZĘŚĆ PRÓG
# =============================================================================

        seria_progow = wyspy_aktywnosci.get('próg', pd.Series([], dtype=float))
        
        liczba_interwalow_progu = (seria_progow > 5).sum()
        print(f'próg: liczba interwałów --> {liczba_interwalow_progu}')
        prog_laczny_dystans, prog_sredni_dystans = oblicz_dystans_dla_serii(seria_progow)
        print(f'próg: łączny dystans biegu progowego --> {prog_laczny_dystans} km')
        print(f'próg: średni dystans na interwał --> {prog_sredni_dystans} km')
        prog_czas = zamien_na_czas(oblicz_czas_trwania_interwalu(df_prog))
        print(f'próg: łączny czas trwania --> {prog_czas} hms')
        prog_predkosc_srednia = oblicz_predkosc_srednia(df_prog)
        prog_tempo_srednie = z_predkosc_na_tempo_srednie(df_prog)
        print(f'próg: tempo średnie --> {prog_tempo_srednie} min/km')
        prog_tetno_srednie = oblicz_tetno_srednie(df_prog)
        print(f'próg: tętno średnie --> {prog_tetno_srednie} bpm')
        prog_tetno_max = oblicz_tetno_max(df_prog)
        print(f'próg: tętno maksymalne --> {prog_tetno_max} bpm')
        prog_kadencja = oblicz_kadencje_srednia(df_prog)
        print(f'próg: kadencja --> {prog_kadencja} krok/min\n')



# =============================================================================
# CZĘŚĆ RYTMY
# =============================================================================

        seria_rytmow = wyspy_aktywnosci.get('rytm', pd.Series([], dtype=float))
        liczba_interwalow_rytmow = (seria_rytmow > 5).sum()
        print(f'rytm: liczba interwałów --> {liczba_interwalow_rytmow}')
        rytm_czas = zamien_na_czas(oblicz_czas_trwania_interwalu(df_rytmy))
        print(f'rytm: łączny czas trwania --> {rytm_czas} hms')
        rytm_predkosc_srednia = oblicz_predkosc_srednia(df_rytmy)
        rytm_tempo_srednie = z_predkosc_na_tempo_srednie(df_rytmy)
        print(f'rytm: tempo średnie --> {rytm_tempo_srednie} min/km')
        rytm_predkosc_max = oblicz_predkosc_max(df_rytmy)
        rytm_tempo_max = z_predkosc_na_tempo_max(df_rytmy)
        print(f'rytm: tempo maksymalne --> {rytm_tempo_max} min/km')
        rytm_kadencja = oblicz_kadencje_srednia(df_rytmy)
        print(f'rytm: kadencja --> {rytm_kadencja} krok/min\n')
        


# =============================================================================
# CZĘŚĆ SPRINTY
# =============================================================================

        seria_sprintow = wyspy_aktywnosci.get('sprint', pd.Series([], dtype=float))
        liczba_interwalow_sprintow = (seria_sprintow > 5).sum()
        print(f'sprint: liczba interwałów --> {liczba_interwalow_sprintow}')
        sprint_czas = zamien_na_czas(oblicz_czas_trwania_interwalu(df_sprint))
        print(f'sprint: łączny czas trwania --> {sprint_czas} hms')
        sprint_predkosc_srednia = oblicz_predkosc_srednia(df_sprint)
        sprint_tempo_srednie = z_predkosc_na_tempo_srednie(df_sprint)
        print(f'sprint: tempo średnie --> {sprint_tempo_srednie} min/km')
        sprint_predkosc_max = oblicz_predkosc_max(df_sprint)
        sprint_tempo_max = z_predkosc_na_tempo_max(df_sprint)
        print(f'sprint: tempo maksymalne --> {sprint_tempo_max} min/km')
        sprint_kadencja = oblicz_kadencje_srednia(df_sprint)
        print(f'sprint: kadencja --> {sprint_kadencja} krok/min\n')
        


# =============================================================================
# CZĘŚĆ ODPOCZYNEK PO MOCY
# =============================================================================
        
        seria_odpoczynek_moc = wyspy_aktywnosci.get('odpoczynek_moc', pd.Series([], dtype=float))
        liczba_odpoczynek_moc = (seria_odpoczynek_moc> 10).sum()
        print(f'odpoczynek_moc: liczba odpoczynków po mocy --> {liczba_odpoczynek_moc}')
        
        odpoczynek_moc_raport = df_odpoczynek_moc.groupby('wyspy_aktywności').apply(analizuj_odpoczynek)
        odpoczynek_moc_raport['numeracja'] = (odpoczynek_moc_raport.groupby('aktywność').cumcount() + 1).astype(str).str.zfill(2)
        odpoczynek_moc_raport.index = odpoczynek_moc_raport['aktywność'] + '_' + odpoczynek_moc_raport['numeracja']
        odpoczynek_moc_raport = odpoczynek_moc_raport.drop(columns=['aktywność', 'numeracja'])
        
        odpoczynek_moc_czas_sredni_interwalu = zamien_na_czas(odpoczynek_moc_raport.get('sekundy', pd.Series([0])).mean())
        print(f'odpoczynek_moc: średni czas każdego odpoczynku --> {odpoczynek_moc_czas_sredni_interwalu} hms')
        odpoczynek_moc_czarna_dziura_czas = zamien_na_czas((df_odpoczynek_moc['strefy_tętna'] == 'czarna_dziura').sum())
        print(f'odpoczynek_moc: czas w czarnej dziurze --> {odpoczynek_moc_czarna_dziura_czas} hms')
        odpoczynek_moc_predkosc_srednia_interwalu = round(odpoczynek_moc_raport['prędkość'].mean(), 2)
        odpoczynek_moc_tempo_srednie_interwalu = z_predkosc_na_tempo_srednie(odpoczynek_moc_raport)
        print(f'odpoczynek_moc: średnie tempo każdego odpoczynku --> {odpoczynek_moc_tempo_srednie_interwalu} min/km')
        odpoczynek_moc_tetno_max = df_odpoczynek_moc['tętno'].max()
        print(f'odpoczynek_moc: tętno maksymalne --> {odpoczynek_moc_tetno_max} bpm')
        odpoczynek_moc_delta_tetna_srednia = int(odpoczynek_moc_raport.get('delta', pd.Series([0])).mean())
        print(f'odpoczynek_moc: średnia delta tętna dla odpoczynku --> {odpoczynek_moc_delta_tetna_srednia} bpm\n')

        
        
# =============================================================================
# SCHŁODZENIE
# =============================================================================
        
        schlodzenie_dystans = oblicz_dystans(df_schlodzenie)
        schlodzenie_czas = oblicz_czas_trwania(df_schlodzenie)
        print(f'schłodzenie: czas --> {schlodzenie_czas} hms')
        schlodzenie_predkosc_srednia = oblicz_predkosc_srednia(df_schlodzenie)
        schlodzenie_tempo_srednie = z_predkosc_na_tempo_srednie(df_schlodzenie)
        print(f'schłodzenie: tempo średnie --> {schlodzenie_tempo_srednie} min/km')
        schlodzenie_tetno_srednie = oblicz_tetno_srednie(df_schlodzenie)
        print(f'schłodzenie: tętno średnie --> {schlodzenie_tetno_srednie} bpm')
        schlodzenie_tetno_poczatkowe = oblicz_tetno_poczatkowe(df_schlodzenie)
        print(f'schłodzenie: tętno początkowe --> {schlodzenie_tetno_poczatkowe} bpm')
        schlodzenie_tetno_koncowe = oblicz_tetno_koncowe(df_schlodzenie)
        print(f'schłodzenie: tętno końcowe --> {schlodzenie_tetno_koncowe} bpm')
        schlodzenie_delta_tetna = schlodzenie_tetno_koncowe - schlodzenie_tetno_poczatkowe
        print(f'schłodzenie: delta tętna do max 5 min --> {schlodzenie_delta_tetna} bpm\n')



# =============================================================================
# WYDAJNOŚĆ
# =============================================================================
        
        if oblicz_czas_trwania_interwalu(df_najdluzszy_bieg) >= 1200 or oblicz_dystans(df_najdluzszy_bieg) >= 4.0:
            trend_kierunek, trend_roznica, nachylenie = analizuj_trend_tetna(df_najdluzszy_bieg['tętno'])
            dryft_standard = oblicz_cardiac_drift(df_najdluzszy_bieg)
            dryft_terenowy = oblicz_skorygowany_decoupling(df_najdluzszy_bieg)
            wskaznik_wydajnosci_ef = oblicz_ef(df_najdluzszy_bieg)
            wynik_zmeczenia_fst = oblicz_fatigue_score(dryft_standard, schlodzenie_delta_tetna, wskaznik_wydajnosci_ef)  
        else:
            print('>>> UWAGA!\n Czas trwania najdłuższego biegu był krótszy niż 20 minut lub\n dystans był krótszy niż 4 km,\n dlatego skrypt nie policzył tych danych <<<\n')
            trend_roznica = np.nan
            dryft_standard = np.nan
            dryft_terenowy = np.nan
            wskaznik_wydajnosci_ef = np.nan
            wynik_zmeczenia_fst = np.nan
        
        print(f'wydajność: różnica trendu tętna --> {trend_roznica}')
        print(f'wydajność: dryf standardowy --> {dryft_standard} %')
        print(f'wydajność: dryf terenowy --> {dryft_terenowy} %')
        print(f'wydajność: wskaźnik wydajności EF (najdłuższy bieg) --> {wskaznik_wydajnosci_ef}')
        print(f'wydajność: wynik zmęczenia FST (najdłuższy bieg) --> {wynik_zmeczenia_fst}\n')


        dryft_standard_global = oblicz_cardiac_drift(df_najdluzszy_bieg)
        wskaznik_wydajnosci_ef_globalny = oblicz_ef(df_trening_biegowy)
        wskaznik_aef_terenowy_globalny = oblicz_aef_terenowe(df_trening_biegowy)
        wynik_zmeczenia_fst_globalny = oblicz_fatigue_score(dryft_standard_global, schlodzenie_delta_tetna, wskaznik_wydajnosci_ef_globalny)
        
        print(f'wydajność: wskaźnik wydajności EF (cały trening z marszami) --> {wskaznik_wydajnosci_ef_globalny}')
        print(f'wydajność: skorygowany EF terenowy (aEF) --> {wskaznik_aef_terenowy_globalny}')
        print(f'wydajność: wynik zmęczenia FST (cały trening) --> {wynik_zmeczenia_fst_globalny}\n')

    
        
# =============================================================================
# Tabela GOTOWA
# =============================================================================
        
        dane_treningu = {
            ('OGOLNE', 'data'): dzien_biegu,
            ('OGOLNE', 'temperatura_[st.C])'): temperatura,
            
            # ROZGRZEWKA
            ('ROZGRZEWKA', 'dystans_km'): rozgrzewka_dystans,
            ('ROZGRZEWKA', 'predkosc_srednia_m/s'): rozgrzewka_predkosc_srednia,
            ('ROZGRZEWKA', 'tetno_srednie_bpm'): rozgrzewka_tetno_srednie,
            
            # TRENING WŁAŚCIWY
            ('TRENING', 'dystans_km'): trening_biegowy_dystans,
            ('TRENING', 'czas_hms'): trening_biegowy_czas,
            ('TRENING', 'czas_postoju_hms'): trening_biegowy_postoj_czas,
            ('TRENING', 'czas_marszu_hms'): trening_biegowy_marsz_czas,
            ('TRENING', 'czas_biegow_hms'): trening_biegowy_bieg_czas,
            ('TRENING', 'czas_w_czarnej_dziurze_hms'): trening_czarna_dziura_czas,
            ('TRENING', 'czas_w tlenie'): trening_tlen_czas,
            ('TRENING', 'podgore_m'): trening_biegowy_podgore,
            ('TRENING', 'zgorki_m'): trening_biegowy_zgorki,
            ('TRENING', 'predkosc_srednia_m/s'): trening_biegowy_prędkość_średnia,
            ('TRENING', 'tetno_srednie_bpm'): trening_biegowy_tetno_srednie,
            ('TRENING', 'tetno_odchylenie_bpm'): trening_biegowy_tetno_odchylenie,
            ('TRENING', 'tetno_max_bpm'): trening_biegowy_tetno_max,
            
            # NAJDŁUŻSZY BIEG
            ('NAJDLUZSZY_BIEG', 'dystans_km'): najdluzszy_bieg_dystans,
            ('NAJDLUZSZY_BIEG', 'predkosc_m/s'): najdluzszy_bieg_predkosc_srednia,
            ('NAJDLUZSZY_BIEG', 'tetno_srednie_bpm'): najdluzszy_bieg_tetno_srednie, 
            ('NAJDLUZSZY_BIEG', 'tetno_max_bpm'): najdluzszy_bieg_tetno_max, 
            ('NAJDLUZSZY_BIEG', 'kadencja_krok/min'): najdluzszy_bieg_kadencja,
            ('NAJDLUZSZY_BIEG', 'czas_w_czarnej_dziurze_hms'): najdluzszy_bieg_czarna_dziura_czas,
            
            # BAZA
            ('BAZA', 'liczba_interwalow'): liczba_interwałow_bazowych, 
            ('BAZA', 'czas_hms'): baza_czas, 
            ('BAZA', 'czas_w_czarnej_dziurze_hms'): baza_czarna_dziura_czas,
            ('BAZA', 'predkosc_srednia_m/s'): baza_predkosc_srednia,
            ('BAZA', 'tetno_srednie_bpm'): baza_tetno_srednie,
            ('BAZA', 'tetno_max_bpm'): baza_tetno_max,
            ('BAZA', 'kadencja_krok/min'): baza_kadencja,

            # ODPOCZYNEK
            ('ODPOCZYNEK_BAZA', 'liczba_odpoczynek_baza'): liczba_odpoczynek_baza,
            ('ODPOCZYNEK_BAZA', 'czas_sredni_hms'): odpoczynek_baza_czas_sredni_interwalu,
            ('ODPOCZYNEK_BAZA', 'czas_w_czarnej_dziurze_hms'): odpoczynek_baza_czarna_dziura_czas,
            ('ODPOCZYNEK_BAZA', 'predkosc_srednia_m/s'): odpoczynek_baza_predkosc_srednia_interwalu,
            ('ODPOCZYNEK_BAZA', 'delta_tetna_srednia_bpm'): odpoczynek_baza_delta_tetna_srednia,

            # PRÓG
            ('PROG', 'liczba_interwalow'): liczba_interwalow_progu,
            ('PROG', 'czas_hms'): prog_czas, 
            ('PROG', 'predkosc_srednia_m/s'): prog_predkosc_srednia ,
            ('PROG', 'tetno_srednie_bpm'): prog_tetno_srednie, 
            ('PROG', 'tetno_max_bpm'): prog_tetno_max,
            ('PROG', 'kadencja_krok/min'): prog_kadencja,
            
            # RYTM
            ('RYTM', 'liczba_interwalow'): liczba_interwalow_rytmow,
            ('RYTM', 'czas_hms'): rytm_czas, 
            ('RYTM', 'predkosc_srednia_m/s'): rytm_predkosc_srednia, 
            ('RYTM', 'predkosc_max_m/s'): rytm_predkosc_max,
            ('RYTM', 'kadencja_krok/min'): rytm_kadencja, 
            
            # SPRINT
            ('SPRINT', 'liczba_interwalow'): liczba_interwalow_sprintow,
            ('SPRINT', 'czas_hms'): sprint_czas,
            ('SPRINT', 'predkosc_srednia_m/s'): sprint_predkosc_srednia,
            ('SPRINT', 'predkosc_max_m/s'):sprint_predkosc_max,
            ('SPRINT', 'kadencja_krok/min'): sprint_kadencja,
            
            # ODPOCZYNEK
            ('ODPOCZYNEK_MOC', 'liczba_odpoczynek_moc'): liczba_odpoczynek_moc,
            ('ODPOCZYNEK_MOC', 'czas_sredni_hms'): odpoczynek_moc_czas_sredni_interwalu,
            ('ODPOCZYNEK_MOC', 'czas_w_czarnej_dziurze_hms'): odpoczynek_moc_czarna_dziura_czas,
            ('ODPOCZYNEK_MOC', 'predkosc_srednia_m/s'): odpoczynek_moc_predkosc_srednia_interwalu,
            ('ODPOCZYNEK_MOC', 'delta_tetna_srednia_bpm'): odpoczynek_moc_delta_tetna_srednia,

            # SCHŁODZENIE
            ('SCHLODZENIE', 'czas_hms'): schlodzenie_czas,
            ('SCHLODZENIE', 'predkosc_srednia_m/s'): schlodzenie_predkosc_srednia,
            ('SCHLODZENIE', 'tetno_srednie_bpm'): schlodzenie_tetno_srednie,
            ('SCHLODZENIE', 'tetno_poczatkowe_bpm'): schlodzenie_tetno_poczatkowe,
            ('SCHLODZENIE', 'tetno_koncowe_bpm'): schlodzenie_tetno_koncowe,
            ('SCHLODZENIE', 'delta_tetna_bpm'): schlodzenie_delta_tetna,
            
            # WYDAJNOŚĆ
            ('WYDAJNOSC', 'roznica_trendu_tetna'): trend_roznica,
            ('WYDAJNOSC', 'dryf_standardowy_%'): dryft_standard,
            ('WYDAJNOSC', 'dryf_terenowy_%'): dryft_terenowy,
            ('WYDAJNOSC', 'wskaznik_wydajnosci_ef'): wskaznik_wydajnosci_ef,
            ('WYDAJNOSC', 'wynik_zmeczenia_fst'): wynik_zmeczenia_fst,
            
            ('WYDAJNOSC', 'wskaznik_wydajnosci_ef_globalny'): wskaznik_wydajnosci_ef_globalny,
            ('WYDAJNOSC', 'wskaznik_aef_terenowy_globalny'): wskaznik_aef_terenowy_globalny,
            # ('WYDAJNOSC', 'ultra_index'): ultra_index,
            ('WYDAJNOSC', 'wynik_zmeczenia_fst_globalny'): wynik_zmeczenia_fst_globalny
            }        
        
        wyniki_do_skonsolidowania.append(dane_treningu)

        
        
# =============================================================================
# ZAPIS OD CSV
# =============================================================================

        # zapis_pliku_csv_pytaj(df_dane, folder_zapisu_df_dane, f'trening_biegowy_{dzien_biegu}.csv')
        # zapis_pliku_csv(df_dane, folder_zapisu_df_dane, f'trening_biegowy_{dzien_biegu}.csv')


    if wyniki_do_skonsolidowania:
        df_zbiorcza = pd.DataFrame(wyniki_do_skonsolidowania)
        df_zbiorcza.columns = pd.MultiIndex.from_tuples(df_zbiorcza.columns)
        
        # zapis_pliku_csv_pytaj(df_zbiorcza, folder_zapisu, plik_do_zapisu)
        # zapis_pliku_csv(df_zbiorcza, folder_zapisu, plik_do_zapisu)



# =============================================================================
# SORTOWANIE I ZAPISYWANIE
# =============================================================================

        print(f'Rozpoczynam sortowanie pliku {plik_do_zapisu}.')
        df_sortowanie = pd.read_csv(sciezka_pliku_csv, header=[0, 1])
        df_sortowanie = df_sortowanie.sort_values(by=('OGOLNE', 'data'), ascending=False)
        df_sortowanie.to_csv(sciezka_pliku_csv, index=False)
        print('Sortowanie zakończone sukcesem.')
    else:
        print('Brak danych do zapisania.')