"""Calculs des primes/décotes et analyses des régimes de marché."""

import numpy as np
import pandas as pd

from .a_donnees import ETF_INFO, TICKERS


def construire_donnees(nav, prix):
    """Fusionne NAV et cours sur les dates communes et calcule les écarts."""
    tableaux = []
    for ticker in TICKERS:
        if ticker.lower() not in nav or ticker not in prix:
            raise ValueError(f"Données NAV ou marché manquantes pour {ticker}.")

        nav_etf = nav[ticker.lower()][["Date", "NAV"]].copy()
        nav_etf["Date"] = pd.to_datetime(nav_etf["Date"])
        if ticker == "SPEM":
            nav_etf.loc[
                nav_etf["Date"] < pd.Timestamp("2017-10-16"),
                "NAV",
            ] /= 2

        prix_etf = prix[ticker][["Date", "Close", "Volume"]].copy()
        prix_etf["Date"] = pd.to_datetime(prix_etf["Date"])
        jointure = pd.merge(nav_etf, prix_etf, on="Date", how="inner")
        jointure = jointure.sort_values("Date").reset_index(drop=True)
        if jointure.empty:
            raise ValueError(f"Aucune date commune entre NAV et prix pour {ticker}.")

        jointure["ETF"] = ticker
        jointure["Type"], jointure["Classe"] = ETF_INFO[ticker]
        jointure["Prime_decote_pct"] = (
            (jointure["Close"] - jointure["NAV"]) / jointure["NAV"] * 100
        )
        jointure["Abs_prime_decote_pct"] = jointure["Prime_decote_pct"].abs()
        jointure["Prime_decote_moyenne_30j"] = (
            jointure["Prime_decote_pct"].rolling(30, min_periods=5).mean()
        )
        tableaux.append(jointure)

    return (
        pd.concat(tableaux, ignore_index=True)
        .sort_values(["ETF", "Date"])
        .reset_index(drop=True)
    )


def statistiques_ecarts(donnees, seuils=(0.25, 0.5, 1.0)):
    """Résume les écarts moyens et la fréquence de dépassement des seuils."""
    statistiques = (
        donnees.groupby(["ETF", "Classe", "Type"])
        .agg(
            Nombre_observations=("Date", "size"),
            Prime_decote_moyenne_pct=("Prime_decote_pct", "mean"),
            Prime_decote_mediane_pct=("Prime_decote_pct", "median"),
            Ecart_absolu_moyen_pct=("Abs_prime_decote_pct", "mean"),
            Ecart_absolu_max_pct=("Abs_prime_decote_pct", "max"),
        )
        .reset_index()
    )
    for seuil in seuils:
        frequence = donnees.groupby("ETF")["Abs_prime_decote_pct"].apply(
            lambda ecarts: ecarts.gt(seuil).mean() * 100
        )
        statistiques[f"Jours_au_dessus_{seuil:g}pct"] = statistiques["ETF"].map(
            frequence
        )
    return statistiques


def ajouter_regimes(donnees, vix, seuil_bas=15, seuil_haut=30):
    """Ajoute les régimes VIX et les quartiles de volume propres à chaque ETF."""
    resultat = donnees.merge(vix, on="Date", how="left")
    resultat["Regime_volatilite"] = np.select(
        [
            resultat["VIX"] < seuil_bas,
            resultat["VIX"] >= seuil_haut,
        ],
        ["Faible", "Forte"],
        default="Intermédiaire",
    )

    groupes = []
    for _, groupe in resultat.groupby("ETF", sort=False):
        groupe = groupe.copy()
        quantile_bas, quantile_haut = groupe["Volume"].quantile([0.25, 0.75])
        groupe["Regime_liquidite"] = np.select(
            [
                groupe["Volume"] <= quantile_bas,
                groupe["Volume"] >= quantile_haut,
            ],
            ["Faible", "Forte"],
            default="Intermédiaire",
        )
        groupes.append(groupe)
    return (
        pd.concat(groupes, ignore_index=True)
        .sort_values(["ETF", "Date"])
        .reset_index(drop=True)
    )


def comparer_regimes(donnees, colonne_regime):
    """Compare les primes et écarts absolus entre régimes faible et fort."""
    if colonne_regime not in {"Regime_volatilite", "Regime_liquidite"}:
        raise ValueError(f"Régime inconnu : {colonne_regime}")
    observations = donnees[donnees[colonne_regime].isin(["Faible", "Forte"])]
    return (
        observations.groupby(["ETF", "Type", colonne_regime])
        .agg(
            Nb_jours=("Date", "size"),
            Prime_moyenne_pct=("Prime_decote_pct", "mean"),
            Ecart_absolu_moyen_pct=("Abs_prime_decote_pct", "mean"),
        )
        .reset_index()
    )


def analyser_correction(donnees, seuil_ecart=0.25):
    """Calcule l'évolution des écarts importants à la séance suivante."""
    triees = donnees.sort_values(["ETF", "Date"]).copy()
    ecart_lendemain = triees.groupby("ETF")["Abs_prime_decote_pct"].shift(-1)
    triees["Variation_abs_1j"] = (
        ecart_lendemain - triees["Abs_prime_decote_pct"]
    )
    triees["Correction_lendemain"] = (
        triees["Variation_abs_1j"].lt(0).where(ecart_lendemain.notna())
    )
    importantes = triees.loc[
        triees["Abs_prime_decote_pct"].ge(seuil_ecart)
        & ecart_lendemain.notna()
    ].copy()
    importantes["Ecart_abs_1j"] = (
        importantes["Abs_prime_decote_pct"] + importantes["Variation_abs_1j"]
    )
    resume = (
        importantes.groupby(["ETF", "Classe", "Type"])
        .agg(
            Nb_dates=("Correction_lendemain", "count"),
            Taux_correction_pct=("Correction_lendemain", lambda valeurs: valeurs.mean() * 100),
            Variation_abs_moyenne_1j=("Variation_abs_1j", "mean"),
        )
        .reset_index()
    )
    return importantes, resume

