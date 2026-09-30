# Studio lessons — injected every session

Hard-won, and cheap to forget. The doctrine in `AGENTS.md` is the law; these are the field notes behind it.

- **The builder is the worst judge of their own work.** Every "it looks good" this project shipped from one flattering angle fell apart from another. QA and review are fresh, separate passes. (doctrine 1, 4)
- **A tool returning success proves the tool ran, not that the work is right.** `placed=60` says the tool ran; bounds say `-128` while buildings float. Verify the *result*, from the *saved* state, from every view.
- **The owner's eyes outrank the query.** When the owner sees a defect a check missed, the check is broken — audit what it measures; don't re-assert the green.
- **Don't build unproven work in the main map.** Spike it in isolation, get it reviewed, then integrate — or discard. (doctrine 3)
- **Solid massing, not flat cards. Walk it, don't fly it.** (doctrine 5)
- **Never `taskkill //IM UnrealEditor.exe`** — it can take the owner's editor with it. One captured PID, or shut a `-server` run from inside.
- **Assets: measure before use** (bounds lie), place from the project content root (not a vendor path), record provenance.
- **Verify engine behaviour against source** before asserting or building on it. A doc/forum/marketplace claim is not proof.
- **Complete or descope; `[x]` means verified.** No placeholders, no silent scope cuts, no hopeful ticks.
