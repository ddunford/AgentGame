# Guide — Monetization craft (the money-facing product)

> Read before designing any store, offer, currency, or payout. The core idea: **in a creator economy the way the game makes money is not a bolt-on tacked onto a finished game — it is the product, a two-sided market where creators earn, visitors spend, and the platform takes a transparent cut. It is done when spend respects the no-pay-to-win rule, entitlement is server-authoritative, the store is honest, creators are paid correctly and on time, and every money endpoint's compliance surface is named and owned by someone.**

The *economy* — faucets, sinks, the numbers — and the **no-pay-to-win rule** are `agents/game-designer`'s and `guides/game-design.md`'s, and the rule is **settled in the decisions log**. **This guide does not restate or relitigate that rule; it aligns to it.** The transaction rails, the ledger, and the payout infrastructure are `guides/backend-services.md`'s — this guide owns the *product* on top: the storefront, the pricing, the offer, the payout policy. Every purchase and payout endpoint goes to `agents/security-reviewer`. The **hard law** — PCI, tax/VAT, consumer protection, minors' spending, loot-box/gambling regulation — belongs to a **legal/compliance** role; this guide names the compliance surface and hands the hard law across. **Money and public surface are owner-reserved** (`<studio-root>/AGENTS.md` decision rights) — this role recommends; the owner decides.

## The two failures this prevents
1. **Pay-to-win creep.** Monetizing power on a competition surface — selling, directly or by grind-skip, the strength that decides contested play. It violates a settled rule, and in a social world built on fairness it is a trust breach the game does not recover from. (The *rule* is `game-design.md`'s; this guide's job is to enforce it at the store boundary.)
2. **A compliance or trust breach at the point of money.** Charging minors without consent, a dark-pattern store, opaque randomised-offer odds, or a creator payout that fails tax/KYC. Each is a legal exposure and a trust failure — and a persistent creator economy runs on trust that spend is fair and payout is correct.

## PRINCIPLES
- **No pay-to-win in mixed-competition zones — settled; align, don't relitigate.** `guides/game-design.md` and the decisions log own the rule. The store enforces it at the boundary: in contested play, spend buys **cosmetics, access, convenience, and creator tools — never power.** Where the line is ambiguous, it goes to `game-designer` + `creative-review`, not resolved unilaterally at the store.
- **The creator economy is the product.** A two-sided market: creators earn, visitors spend, the platform takes a transparent cut. **Payout trust is existential** — a creator who doubts they'll be paid correctly and on time leaves, and the supply side is the pitch ("every door leads somewhere else").
- **Entitlement is server-authoritative.** A purchase grants an entitlement the server records in the ledger and re-derives; the client never asserts "I own this" or "I paid" (cross-ref `agents/security-reviewer`, `guides/backend-services.md §3`). Grant on verified payment, not on the client's claim of payment.
- **Honest storefront — no dark patterns.** Clear real-money pricing, real cost shown (not obscured behind currency-conversion confusion), transparent odds on any randomised offer, easy refunds, and special care with minors. The store's job is to offer value, not to extract by manipulation.
- **The subscription model is settled — build to it.** The decisions log owns the model; this guide builds the product around recurring value, not one-time extraction. (Defer to the log for the model's shape.)
- **Money and public surface are owner-reserved.** Pricing, store launch, real-money flows, and payout policy are recommended here and **decided by the owner** (with legal). Escalate with a recommendation; never set a price or launch a store as an agent.
- **Every money endpoint carries a compliance surface — name it, hand the hard law across.** PCI, tax/VAT nexus, consumer protection and refunds, minors' spending, loot-box/gambling regulation. This role owns the product decision and flags the compliance need; legal/compliance owns the law.

## 1 — The model
- **Settled shape (defer to the decisions log).** A **subscription** plus a **creator economy**. This guide summarises the shape only — the canonical model and the no-pay-to-win rule live in the vault; read them there, do not re-derive them here.
- **What is sold:** subscription (recurring access/value), cosmetics, **access** (to zones/experiences), **convenience**, and **creator tools**. What creators sell to each other and to visitors, within the platform's rules.
- **What is never sold:** contested power in mixed-competition zones. This is the one hard boundary the store's catalog respects unconditionally.
- **The three parties.** Visitor spend, creator earn, platform cut — every offer is designed knowing which parties it touches and how value flows between them (the ledger records all three legs — `guides/backend-services.md §3`).

## 2 — Storefront & offer design
- **Catalog & presentation.** What's on sale, how it's grouped, how it's discovered — in-world (a shop you walk to) and out-of-world (a menu). Presentation is `agents/ui-ux-designer`'s surface; the *offer* is this role's.
- **The honest-store bar.** Real cost shown clearly; no countdown-pressure manufactured against value; no confusing currency layers designed to obscure spend; no default-opt-in upsells. Measured against the dark-pattern taxonomy (§Sources), the store must pass.
- **Discoverability without manipulation.** Players find what they'd want; the store does not exploit sunk-cost, FOMO, or confusion to drive spend they'll regret. A regretted purchase is a refund and a trust loss, not a win.
- **Respect the per-district rules.** The store honours the world's safety and fairness structure — cosmetic-only offers in competition zones, and offers appropriate to the district's audience (all-ages vs mature — `guides/moderation.md`).

## 3 — Payments
- **Processors & flow.** Payment goes through a processor [verify — web pass: current processors and their platform-policy constraints, esp. console/mobile store cuts]; the flow is: client initiates → processor authorises → **server verifies the payment and grants the entitlement in the ledger** → client reflects it. The grant is server-side and idempotent (`guides/backend-services.md §3`).
- **Premium vs soft currency.** A premium (bought) currency and a soft (earned) currency have different rules; premium currency carries **regulatory weight** (stored-value, refundability, and in some regions gambling-adjacency for randomised spend) [verify — web pass]. Prefer transparency; avoid currency layering designed to obscure real cost.
- **Refunds & chargebacks.** An easy, honest refund path (a legal requirement in many regions [verify — web pass]) and a chargeback-handling policy that doesn't let a chargeback-then-keep-the-item dupe the economy (join with `backend-services` ledger + `security-reviewer`).

## 4 — Creator payouts
The supply side of the two-sided market — and the part where trust is won or lost.
- **Revenue share.** A transparent split between creator and platform, published and stable. Creators build businesses on it; changing it arbitrarily breaks the trust the pitch depends on.
- **Thresholds & schedule.** Minimum payout thresholds and a predictable payout schedule; a creator must be able to know when and how much they'll be paid.
- **KYC & tax on payouts.** Paying real money *out* triggers know-your-customer and tax-form obligations on the payee (W-9/W-8/local equivalents) [verify — web pass] — this is legal/compliance's law, but the product must collect what's needed and gate payout on it.
- **Payout fraud is a real surface.** Self-dealing (buying your own content with stolen/laundered funds to extract a payout), wash-purchasing, and collusion — hand to `agents/security-reviewer` and `backend-engineer`; the ledger and reconciliation (`backend-services.md §3`) are how it's caught.

## 5 — The compliance surface (name it; don't own the hard law)
Every money endpoint sits on regulation. This role's duty is to **name each obligation and route it to legal/compliance**, not to interpret the law.
- **PCI-DSS** — card-data handling; typically discharged by never touching raw card data (processor-hosted fields) [verify — web pass].
- **Tax** — VAT/GST/sales-tax collection and nexus by region on the *spend* side; income/withholding on the *payout* side [verify — web pass].
- **Consumer protection** — refund rights, distance-selling rules, subscription auto-renewal disclosure and easy-cancel requirements [verify — web pass].
- **Minors' spending** — parental-consent and spending-limit requirements for under-age players (COPPA-class and regional) — joins `guides/moderation.md`'s age surface [verify — web pass].
- **Loot-box / randomised-offer regulation** — odds-disclosure mandates and, in some regions, gambling classification of paid randomised offers [verify — web pass]. The safest product answer is often to avoid paid randomised offers entirely; that is an owner-reserved call.

## 6 — Fairness & alignment (the lens over everything above)
- **Enforce no-pay-to-win at the store boundary.** The catalog is the last gate: an offer that would sell contested power is blocked here regardless of revenue. Ambiguous cases → `game-designer` + `creative-review`.
- **Cosmetic/access/convenience only in competition zones.** Spend may change how you look, where you can go, and how fast you grind *outside* contested play — never how you win inside it.
- **Alignment is a trust asset.** In a social world, a store visibly fair to non-payers is a retention and reputation asset; a store that quietly advantages spenders is a slow trust leak. Treat fairness as product value, not a constraint.

## QUALITY BAR
A monetization surface is ready to recommend when all of these hold — verified, never self-signed, with owner-reserved calls escalated:
- **Aligned.** No offer sells contested power; competition-zone spend is cosmetic/access/convenience only; ambiguous cases were resolved by `game-designer` + `creative-review`, not at the store.
- **Server-authoritative.** Entitlement is granted server-side on verified payment and re-derived; no client claim of purchase or ownership is trusted (`security-reviewer`, `backend-services` ledger).
- **Honest.** Real cost shown clearly; no dark patterns; transparent odds on any randomised offer; easy refunds; minors specially handled.
- **Creator-fair.** Revenue share published and stable; payout thresholds and schedule predictable; KYC/tax gating on payout; payout-fraud surface handed to security + backend.
- **Compliance-named.** PCI, tax (both sides), consumer protection, minors, and loot-box surfaces each named and handed to legal/compliance — none guessed.
- **Owner-reserved respected.** Pricing, store launch, and payout policy are recommendations with escalation, not agent decisions.
- **Model-consistent.** Built to the settled subscription + creator-economy model (deferred to the decisions log), not a re-invention of it.

## COMMON FAILURE MODES
- **Pay-to-win creep.** An offer that sells or grind-skips contested power. → block at the store boundary; the rule is settled — align to it.
- **Client-asserted purchase.** Trusting a client's claim of payment/ownership to grant an item. → server verifies payment and grants in the ledger; re-derive entitlement.
- **Dark patterns.** Manufactured urgency, obscured cost, currency layering, default-opt-in upsells, sunk-cost/FOMO exploitation. → the honest-store bar; measured against the dark-pattern taxonomy.
- **Opaque randomised odds.** A paid randomised offer with undisclosed odds — a regulatory and trust failure. → disclose odds, or (safer) avoid paid randomised offers; escalate the call.
- **Creator payout distrust.** Unstable revenue share, unpredictable payouts, or a broken KYC/tax path. → publish and hold the share; predictable schedule; gate payout on KYC/tax.
- **Payout fraud unguarded.** Self-dealing / wash-purchasing extracting real money. → hand to `security-reviewer` + `backend-engineer`; ledger reconciliation catches it.
- **Compliance guessed.** Interpreting tax/PCI/minors/loot-box law in-house. → name each obligation; hand the hard law to legal/compliance.
- **Restating the economy rule.** Re-deriving or relitigating no-pay-to-win or the subscription model here instead of deferring. → defer to `game-design.md` / the decisions log; this guide aligns.
- **Agent-set pricing.** Setting a price or launching the store without owner sign-off. → money + public surface is owner-reserved; recommend and escalate.

## CHECKLIST
**Design (before building):**
- [ ] Model and no-pay-to-win rule read from the decisions log / `game-design.md` — not restated; the store's catalog boundary set to enforce them.
- [ ] Offer set defined (subscription / cosmetics / access / convenience / creator tools); the never-sold boundary (contested power) explicit.
- [ ] Storefront designed to the honest-store bar with `ui-ux-designer`; dark-pattern taxonomy checked.
- [ ] Payment flow specified with server-authoritative, idempotent entitlement grant (`backend-services §3`); premium/soft currency rules and refund/chargeback policy set.
- [ ] Creator-payout policy: revenue share, thresholds, schedule, KYC/tax gating; payout-fraud surface identified.
- [ ] Every compliance obligation (PCI, tax both sides, consumer protection, minors, loot-box) named and routed to legal.
- [ ] Owner-reserved calls (pricing, launch, payout policy) framed for escalation.

**Build:**
- [ ] Entitlement granted server-side on verified payment; no client claim trusted.
- [ ] Store honest in the built UI; odds disclosed on any randomised offer; refund path working.
- [ ] Payout gated on KYC/tax; fraud checks in place with `security-reviewer` + `backend-engineer`.

**Before recommending done:**
- [ ] Quality bar met.
- [ ] Every purchase and payout endpoint handed to `agents/security-reviewer`.
- [ ] No-pay-to-win boundary confirmed with `game-designer` + `creative-review` on any ambiguous offer.
- [ ] Compliance surface handed off to legal; owner-reserved calls escalated with a recommendation, not decided.

## Sources
Craft grounded in the standard live-game monetization, market-design, and consumer-protection literature; specifics to re-confirm on the web pass are tagged `[verify — web pass]`:
- **Two-sided market / platform economics** — the creator-marketplace model; take-rate and payout-trust dynamics `[verify — web pass]`.
- **Dark-pattern taxonomy** — the deceptive-design categories (Brignull / regulator guidance) the honest-store bar is measured against `[verify — web pass]`.
- **Loot-box & randomised-offer regulation** — odds-disclosure mandates and per-region gambling classification `[verify — web pass]`.
- **Payments & compliance** — PCI-DSS scope, tax/VAT nexus, consumer refund rights, KYC/tax on payouts, COPPA-class minors' spending rules `[verify — web pass]`.
- **UGC-platform creator economies** — Roblox / Fortnite-Creative / UEFN payout and revenue-share models as reference points `[verify — web pass]`. The no-pay-to-win rule and the subscription model are owned by `guides/game-design.md` and the decisions log; the transaction rails and ledger by `guides/backend-services.md`; the hard law by legal/compliance.
