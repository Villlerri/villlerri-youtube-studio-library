# Event 1 · Switchback Sprint: freeze log

Frozen 2026-10-15 19:48 UTC, before the official seed exists.

- Course spec: trials/switchback-sprint.json, sha256 3e6dc8085fa77cf5993a3f8491d56c319617b94a1ecf40d377faa92de5a26d24
- Roster: league/roster.json, sha256 1cf5a194f21121149edf3c26c70f48d040fc68aeeef393cad1db1092c3234248
- Scene for the simulator: sha256 0547a2a183d17b6478cfd2223021b24cab6bf219ef4ac568078cd87a81971c94
- Simulator: sim/league.c, sha256 ef6206da32aab17e472e734ef903ee48e214728316e1783da50f15cce9ec4521; Box2D 3.1.1, archive sha256 fb6ef914b50f4312d7d921a600eabc12318bb3c55a0b8c0b90608fa4488ef2e4
- Code commit: db559d82fbee1f229b1787ab700d8fc824ecfd5e
- Test runs: seeds 1-1000, log/event-1/test-runs-1-1000.csv, sha256 dfb4135316879b817b85f425ea7794cd41b202b52b53759a08aa5f723cf4c60e

Test-run summary: GLIDE 29%, BOUNCE 15.2%, COMET 11.4%, HEX 9.7%, PIP 8.9%, WOBBLE 7.6%, ECHO 5.4%, BRICK 3.7%, ANVIL 3%, SPIN 2.6%, GRIT 1.9%, TWIN 1.6%. Winning margin median 1.275 s, under 1 s in 44.3% of runs.

## Official seed rule

- Source: drand mainnet (chain hash 8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce, period 30 s).
- Round: 6555429, due 2026-10-15 19:51:30 UTC.
- Seed: the first 8 hex digits of that round's randomness, read as an unsigned integer.
- One official run with that seed. It is rendered as it falls. No other run replaces it.

## After the official run

- 2026-10-15 19:51:49 UTC: official run with seed 612826258 on the frozen simulator above. Result hash 5aaf2fa57acde9da, saved as result-612826258.json. A repeat run gave the same hash.
- 19:52 UTC: the leader-change counter in sim/league.c was changed. It now starts 1 s after the gate opens, so shapes settling in the start pile do not count as lead changes. Physics is untouched. New sim/league.c sha256 0c176b091f901b5bee09049c13158f204fc2dbc80600412e4083d521057b1ecf.
- Check: seeds 1-1000 re-run with the changed simulator, test-runs-1-1000-recount.csv, sha256 984df8d335edde3fbb1ddb8e3776fdda61c1cc1b912b3bc47a9d411c792b7fcd. Hash, steps and every finish time match the frozen test runs for all 1000 seeds. Only the leader-change column differs: 2 or more changes in 52.6% of runs before, 51.3% after.
- The official run counts 2 lead changes under both counters: WOBBLE, then COMET, then HEX.
