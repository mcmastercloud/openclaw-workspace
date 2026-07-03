# MEMORY.md - Finlay's Long-Term Memory

## Strict Execution Guardrails (Mandatory)
- **STRICT HALT ON PIPELINE & ENV FAILURES:** If any script, process, dependency installation, or permission setup fails or throws an error:
  - **STOP IMMEDIATELY.** Do not attempt automatic workarounds, do not clobber/recreate virtual environments, and do not chain consecutive fallback commands.
  - Present the exact error log to Stephen.
  - Propose clear, precise solutions.
  - **Wait for explicit human confirmation** before executing any further action.
- **NO TOKEN-BURN LOOPS:** Do not run rapid-fire, repetitive shell commands (`exec`) to solve environment limits. If a standard CLI path is blocked by system permissions or mount restrictions, halt and report it.

## Personal Context
- **Human:** Stephen, Partner at Deloitte.
- **Partner:** Samuel, self-employed Dog Groomer.
- **Income:** Stephen earns £200k salary + £50k bonus (£250k total).
- **Pension:** Currently contributing 20.4% total (8% employee, 12.4% employer) on £200k base salary.

- **Net Worth Sync (2026-04-19):** Created the `net-worth-sync` skill to automate the updates of the global Net Worth register. 
    - **Mortgage Logic:** Implemented dynamic tracking of the Progressive Building Society mortgage. Balance is calculated from a 31 Dec 2025 anchor (-£203,269.35) by applying subsequent payments found in the Starling feed. Current balance: -£196,822.05 (39.4% LTV).
    - **Investment Tracking:** Automated share price retrieval for GBG.L and ALL.L. Portfolio value now updates in real-time.
    - **Cash Assets:** Synchronised all account balances, including internalised Spaces. Starling Personal now correctly reflects the £10,257.21 aggregate.
- **Space Ledgers:** Established and populated dedicated Notion ledgers for all personal Starling Spaces (Household, Entertainment, etc.) to ensure absolute spend organisation.
- **Environment Maintenance:** Corrected a typographical error in `.env` (`STARLING_BUISINESS_ACCOUNT_TOKEN` -> `STARLING_BUSINESS_ACCOUNT_TOKEN`).
- **Pension (2026-04-13):** Monthly contributions increased to £3,400 (£40,800/yr) following salary increase.
- **Tapered Allowance:** Adjusted Income estimated at £274,800. Tapered allowance for 2026-27 is £52,600.
- **Headroom:** ~£11,800 remaining allowance for the current tax year.
- **Carry Forward (2026-04-20):** Performed a forensic audit of P60s (1843-1845) and Standard Life Statement (1846). Calculated total carry forward available of **£96,894**. Specifically identified **£35,051** as the balance expiring on 5th April 2027.
- **Pension Strategy (2026-04-20):** Formulated a "No Loss" execution strategy requiring a gross contribution of **£46,851** before year-end to protect all expiring balances.
- **Health Data Sync:** Experienced recurring stale data in Withings sync (last noticed June 2026). Pipeline health check on health data sync is a standing requirement to ensure morning-brief automation (lobster flow) succeeds.

## Tasks & Goals
- Monitor pension taper risk given high income.
- Triage HMRC communications.
- Manage Finance ecosystem in Notion.
- **Paperless Access:** Restricted access granted via `tag:Finlay`. Follow `SOP_PAPERLESS.md`.

## Notion Financial Ecosystem
### Categories (Master List)
- **Car**: `3466a781-d358-8002-ac40-fcd60236c3e3`
- **Transport**: `3466a781-d358-8007-a67a-ccbf6baed887`
- **Credit Card**: `3466a781-d358-8060-ae98-fcaad396ccdf`
- **Uncategorised**: `3466a781-d358-8094-8188-dffaa257cb60`
- **Transfer**: `3466a781-d358-80a0-8b23-f2febecada3e`
- **Housing**: `3466a781-d358-80a8-8954-c8cd647f3001`
- **Subsistence**: `3466a781-d358-80ac-8da3-ee09472cd902`
- **Entertainment**: `3466a781-d358-80d8-8f78-f584aa5ef99b`
- **Bills**: `3466a781-d358-80dc-a550-fa2cd41c63d7`
- **Fitness**: `3466a781-d358-80eb-b371-fc009a569a9c`

### Vendor Mapping Rules (Learned)
- **Amex / American Express**: Credit Card
- **JD Sports Gyms / Nayax **jd Sports Gyms**: Fitness
- **German Doner Kebab / GDK**: Subsistence
- **G4s Facilities Managem**: Subsistence (VMS Elements)
- **Snax / Loaf / Welcome Break / Emerald Airlines**: Subsistence
- **Black Gold**: Uncategorised

## Notion Access Constraint
- **Scope/Red Line:** Restrict all operations strictly to the Finance dashboard (`https://www.notion.so/Finance-33f6a781d35880f1ab39d1d3ca6098cf?v=3a12f0a118e841838fba86b94553cfa3&source=copy_link`) and its child pages. Do not traverse outside this organizational subtree. Ignore all other Notion pages.
2026-06-07: Added explicit note to TOOLS.md to read /home/node/.openclaw/workspace/finlay/skills/firefly-iii/SKILL.md instead of trying to run 'firefly-iii' as a single system tool. The skill is a bash/curl framework, not a CLI alias.

## Promoted From Short-Term Memory (2026-06-10)

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:3:5 -->
- Daily Memory - 2026-06-04: **Signal Migration:** The Signal channel migration to the OpenClaw Docker environment is complete; decommissioning the old server is pending.; **Morning-brief Issue:** The morning-brief lobster flow failed on June 4th, 2026, due to stale Withings data (last sync: June 2nd, 2026).; **Stephen's Schedule:** On June 2nd, 2026, Stephen visited Cheltenham and had productive meetings followed by dinner with Robin Southwold and Nicholas Ter Porsche. [score=0.835 recalls=0 avg=0.620 source=memory/2026-06-04.md:3-5]

## Promoted From Short-Term Memory (2026-06-13)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07-firefly-error-correction.md:6:6 -->
- Context: A major execution loop fault occurred when navigating tools. I attempted to execute `firefly-iii` as if it were a direct system binary or discrete tool call. [score=0.858 recalls=0 avg=0.620 source=memory/2026-06-07-firefly-error-correction.md:6-6]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07-firefly-error-correction.md:11:11 -->
- Correction: It provides explicit bash and `curl` commands. I must `read` or `cat` that file to learn how to interact with the Firefly III API when Firefly requests are made. There is no native `firefly-iii` tool. [score=0.858 recalls=0 avg=0.620 source=memory/2026-06-07-firefly-error-correction.md:11-11]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07-firefly-error-correction.md:9:9 -->
- Correction: The Firefly III functionality is represented entirely via a documentation **Skill**. It is located at `~/.openclaw/workspace/finlay/skills/firefly-iii/SKILL.md`. [score=0.844 recalls=0 avg=0.620 source=memory/2026-06-07-firefly-error-correction.md:9-9]

## Promoted From Short-Term Memory (2026-06-14)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07-firefly-error-correction.md:3:3 -->
- Setup Correction: Firefly III Skill: Date: 2026-06-07 [score=0.901 recalls=0 avg=0.620 source=memory/2026-06-07-firefly-error-correction.md:3-3]
