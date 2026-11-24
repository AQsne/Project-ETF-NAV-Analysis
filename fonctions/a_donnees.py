"""Téléchargement et nettoyage des données des ETF."""

import pandas as pd
import yfinance as yf


ETF_INFO = {
    "SPY": ("Actions américaines", "Actions"),
    "SPEM": ("Actions émergentes", "Actions"),
    "SPIB": ("Obligations investment grade", "Obligations"),
    "SPHY": ("Obligations high yield", "Obligations"),
}
TICKERS = tuple(ETF_INFO)
DATE_DEBUT = "2012-06-19"
DATE_FIN = "2026-10-15"
URL_NAV = (
    "https://www.ssga.com/library-content/products/fund-data/"
    "etfs/us/navhist-us-en-{}.xlsx"
)


def charger_nav(tickers=TICKERS):
    """Télécharge et nettoie les historiques de NAV State Street."""
    historiques = {}
    for ticker in tickers:
        ticker_minuscule = ticker.lower()
        nav = pd.read_excel(
            URL_NAV.format(ticker_minuscule),
            header=3,
            usecols="A:D",
        ).dropna(how="all").dropna(axis=1, how="all")
        if not {"Date", "NAV"}.issubset(nav.columns):
            raise ValueError(f"Colonnes Date et NAV absentes pour {ticker}.")

        nav["Date"] = pd.to_datetime(
            nav["Date"],
            format="%d-%b-%Y",
            errors="coerce",
        )
        nav["NAV"] = pd.to_numeric(nav["NAV"], errors="coerce")
        nav = (
            nav.dropna(subset=["Date", "NAV"])
            .loc[lambda frame: frame["NAV"] > 0]
            .drop_duplicates(subset=["Date"])
            .sort_values("Date")
            .reset_index(drop=True)
        )
        if nav.empty:
            raise ValueError(f"Aucune observation NAV valide pour {ticker}.")
        historiques[ticker_minuscule] = nav
    return historiques


def charger_prix(tickers=TICKERS, start=DATE_DEBUT, end=DATE_FIN):
    """Télécharge les cours de clôture et volumes depuis Yahoo Finance."""
    historiques = {}
    for ticker in tickers:
        prix = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=False,
            progress=False,
        )
        if prix.empty:
            raise ValueError(f"Aucune donnée de marché téléchargée pour {ticker}.")
        if isinstance(prix.columns, pd.MultiIndex):
            prix.columns = prix.columns.get_level_values(0)
        if not {"Close", "Volume"}.issubset(prix.columns):
            raise ValueError(f"Colonnes Close et Volume absentes pour {ticker}.")

        prix.index = pd.to_datetime(prix.index, errors="coerce")
        prix = prix.loc[prix.index.notna()].copy()
        prix.index.name = "Date"
        prix["Close"] = pd.to_numeric(prix["Close"], errors="coerce")
        prix["Volume"] = pd.to_numeric(prix["Volume"], errors="coerce")
        prix = (
            prix.dropna(subset=["Close"])
            .loc[lambda frame: frame["Close"] >= 0]
            .sort_index()
            .reset_index()
        )
        if prix.empty:
            raise ValueError(f"Aucun cours de clôture valide pour {ticker}.")
        historiques[ticker] = prix[["Date", "Close", "Volume"]]
    return historiques


def charger_vix(start, end):
    """Télécharge et nettoie les clôtures quotidiennes du VIX."""
    vix = yf.download(
        "^VIX",
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
    )
    if vix.empty:
        raise ValueError("Aucune donnée VIX téléchargée.")
    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)
    if "Close" not in vix.columns:
        raise ValueError("Colonne Close absente des données VIX.")

    vix = vix.reset_index().rename(columns={"Close": "VIX"})
    vix["Date"] = pd.to_datetime(vix["Date"], errors="coerce")
    vix["VIX"] = pd.to_numeric(vix["VIX"], errors="coerce")
    vix = (
        vix[["Date", "VIX"]]
        .dropna()
        .drop_duplicates(subset=["Date"])
        .sort_values("Date")
        .reset_index(drop=True)
    )
    if vix.empty:
        raise ValueError("Aucune observation VIX valide.")
    return vix

