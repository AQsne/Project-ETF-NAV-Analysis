# ETF NAV vs. Market Price

Empirical analysis of the deviations between the net asset value (NAV) and the market price of four U.S. ETFs.

## Research question

An ETF and the underlying portfolio it tracks provide similar exposure, but their prices can temporarily diverge. This project measures these premiums and discounts, then studies their relationship with volatility, trading volume, and the correction observed during the following session.

## Main results

The results below come from the merged NAV and closing-price histories, with **3,601 common dates per ETF**, from **June 19, 2012 to October 14, 2026**.

### 1. NAV / market-price deviations

| ETF | Mean premium/discount | Median | Mean absolute deviation | Maximum absolute deviation | Days > 0.25% | Days > 0.5% | Days > 1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SPY | 0.0020% | 0.0036% | 0.0242% | 0.9004% | 0.3055% | 0.0555% | 0.0000% |
| SPEM | 0.0759% | 0.1046% | 0.4514% | 4.3401% | 63.6768% | 35.0736% | 8.0533% |
| SPIB | 0.0913% | 0.0570% | 0.1315% | 6.1028% | 15.3291% | 3.8600% | 0.3055% |
| SPHY | 0.1632% | 0.1483% | 0.3336% | 4.4806% | 45.4041% | 19.7445% | 6.1927% |

**Interpretation:**

- **SPY** is the ETF closest to its NAV: its mean absolute deviation is **0.0242%**, exceeding 0.25% on only **0.3055%** of days.
- **SPEM** has the highest mean absolute deviation (**0.4514%**) and exceeds 0.25% on **63.6768%** of days.
- **SPHY** also shows frequent deviations (**0.3336%** on average; **45.4041%** of days above 0.25%).
- **SPIB** lies between the equity ETFs and the high-yield ETF (**0.1315%** on average).
- Mean premiums/discounts are positive for all four ETFs: the market price is, on average, slightly above the NAV.

### 2. Volatility effect

The VIX defines the following regimes: low volatility when **VIX < 15** and high volatility when **VIX ≥ 30**. The comparison uses only these two regimes.

| Category | Regime | Number of days | Mean premium/discount | Mean absolute deviation |
| --- | --- | ---: | ---: | ---: |
| U.S. equities | Low | 1,446 | 0.0023% | 0.0202% |
| U.S. equities | High | 158 | −0.0186% | 0.0671% |
| Emerging-market equities | Low | 1,446 | 0.1876% | 0.3752% |
| Emerging-market equities | High | 158 | −0.3442% | 0.8283% |
| Investment-grade bonds | Low | 1,446 | 0.1214% | 0.1314% |
| Investment-grade bonds | High | 158 | −0.1393% | 0.3412% |
| High-yield bonds | Low | 1,446 | 0.1880% | 0.3323% |
| High-yield bonds | High | 158 | 0.0759% | 0.5096% |

**Result:** the mean absolute deviation increases in all four categories when volatility moves from a low to a high regime. The effect is especially pronounced for emerging-market equities (**0.3752% → 0.8283%**).

### 3. Trading-volume effect

Liquidity regimes are defined separately for each ETF using volume quartiles. Volume is an imperfect proxy for liquidity.

| Category | Volume regime | Number of days | Mean premium/discount | Mean absolute deviation |
| --- | --- | ---: | ---: | ---: |
| U.S. equities | Low | 901 | 0.0067% | 0.0199% |
| U.S. equities | High | 901 | −0.0029% | 0.0332% |
| Emerging-market equities | Low | 901 | 0.0668% | 0.4164% |
| Emerging-market equities | High | 901 | 0.0563% | 0.5442% |
| Investment-grade bonds | Low | 901 | 0.2398% | 0.2503% |
| Investment-grade bonds | High | 901 | 0.0304% | 0.0618% |
| High-yield bonds | Low | 903 | 0.1574% | 0.4625% |
| High-yield bonds | High | 901 | 0.1088% | 0.1722% |

**Result:** the volume effect is heterogeneous. Deviation increases with volume for U.S. and emerging-market equities, while it decreases for bonds: **0.2503% → 0.0618%** for SPIB and **0.4625% → 0.1722%** for SPHY.

### 4. Correction during the following session

The selected observations are those with an absolute deviation greater than or equal to **0.25%**. A correction is a decrease in the absolute deviation on the following day.

| ETF | Dates analyzed | Correction rate | Mean one-day change in deviation |
| --- | ---: | ---: | ---: |
| SPY | 11 | 100.0000% | −0.3203 percentage points |
| SPEM | 2,292 | 68.6736% | −0.1663 percentage points |
| SPHY | 1,635 | 67.2783% | −0.1050 percentage points |
| SPIB | 552 | 65.2174% | −0.0526 percentage points |

**Result:** large deviations decrease during the following session in most cases. The **SPY** result should be interpreted cautiously because it is based on only **11 observations**.

### Empirical conclusion

Deviations between NAV and market price remain small for SPY, but become larger for ETFs exposed to emerging markets and high-yield bonds. They generally widen when volatility is high and often begin to narrow during the following session. These results describe statistical regularities in the sample; they do not establish a causal relationship.

## Sources and limitations

- NAV: [State Street Global Advisors — ETF fund data](https://www.ssga.com/us/en/intermediary/etfs/resources/fund-data)
- Prices and volumes: [Yahoo Finance](https://finance.yahoo.com/)
- Volatility: VIX index downloaded through Yahoo Finance

The NAV and closing price may correspond to different timestamps or valuation conventions. Volume is an imperfect proxy for liquidity, and the analysis describes associations without establishing causality.
