"""Visualisations des résultats de l'analyse."""

import matplotlib.pyplot as plt


def tracer_primes_decotes(donnees):
    """Trace les primes/décotes quotidiennes avec la présentation d'origine."""
    plt.style.use("ggplot")
    fig, axes = plt.subplots(2, 2, figsize=(15, 9))
    for axe, (ticker, groupe) in zip(
        axes.flat,
        donnees.groupby("ETF", sort=False),
    ):
        groupe = groupe.sort_values("Date")
        axe.plot(
            groupe["Date"],
            groupe["Prime_decote_pct"],
            linewidth=0.8,
        )
        axe.axhline(0, color="black", linewidth=0.8)
        axe.set_title(f"Prime/décote de {ticker}")
        axe.set_xlabel("Date")
        axe.set_ylabel("Écart (%)")
        axe.grid(True)
    fig.suptitle("Évolution de la prime/décote par ETF", fontsize=16)
    fig.tight_layout()
    return fig


def tracer_comparaison_regimes(donnees):
    """Compare les écarts absolus moyens selon volatilité et liquidité."""
    regimes = (
        (
            "Regime_volatilite",
            "Volatilité",
            "Écart absolu moyen selon la volatilité",
        ),
        (
            "Regime_liquidite",
            "Liquidité",
            "Écart absolu moyen selon la liquidité",
        ),
    )
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for axe, (colonne, legende, titre) in zip(axes, regimes):
        comparaison = (
            donnees[donnees[colonne].isin(["Faible", "Forte"])]
            .groupby(["ETF", colonne])["Abs_prime_decote_pct"]
            .mean()
            .unstack()
            .reindex(columns=["Faible", "Forte"])
        )
        comparaison.plot(kind="bar", ax=axe, color=["blue", "red"])
        axe.set_title(titre)
        axe.set_xlabel("ETF")
        axe.set_ylabel("Écart absolu moyen (%)")
        axe.legend(title=legende)
        axe.grid(axis="y")
    fig.tight_layout()
    return fig


def tracer_corrections(donnees_ecarts_importants):
    """Compare chaque écart important à celui observé le lendemain."""
    groupes = list(donnees_ecarts_importants.groupby("ETF", sort=False))
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    for axe, (ticker, groupe) in zip(axes.flat, groupes):
        axe.scatter(
            groupe["Abs_prime_decote_pct"],
            groupe["Ecart_abs_1j"],
            alpha=0.35,
            s=12,
        )
        valeur_max = max(
            groupe["Abs_prime_decote_pct"].max(),
            groupe["Ecart_abs_1j"].max(),
        )
        axe.plot([0, valeur_max], [0, valeur_max], "k--")
        axe.set_title(f"Correction des écarts : {ticker}")
        axe.set_xlabel("Écart absolu aujourd'hui (%)")
        axe.set_ylabel("Écart absolu le lendemain (%)")
        axe.grid(True)
    fig.suptitle("Évolution des écarts importants entre deux séances", fontsize=15)
    fig.tight_layout()
    return fig

