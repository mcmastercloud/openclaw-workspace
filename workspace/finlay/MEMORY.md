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

## Promoted From Short-Term Memory (2026-07-19)

<!-- openclaw-memory-promotion:memory:memory/2026-07-13-bonus-update.md:4:6 -->
- Actual Bonus Received: **Gross Bonus:** £114,600 (not the £50k assumed in earlier scenarios); **Pension Sacrifice Decision:** £50,000; **Remaining Gross Bonus:** £64,600 (subject to tax) [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-bonus-update.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-bonus-update.md:9:11 -->
- Pension Implications: £50k sacrifice fully covers the **£46,851 "No Loss"** target — all expiring carry-forward (£35,051 from 2023/24) is now protected.; Gross pension contribution for 2026-27 now totals: £40,800 (regular salary) + £50,000 (bonus sacrifice) = **£90,800**; Remaining carry-forward headroom after this year will be recalculated. [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-bonus-update.md:9-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:2:2 -->
- title: Pension Taper Analysis (Partnership Year 1) — Updated July 2026 [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:2-2]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:5:5 -->
- Analysis for Stephen based on actual 2026/27 income. [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:8:11 -->
- Actual Income (July 2026 Update): | Item | Amount | |---|---| | Base Salary | £200,000 | | Actual Bonus (received) | £114,600 | [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:8-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:12:14 -->
- Actual Income (July 2026 Update): | **Gross Total** | **£314,600** | | Bonus Pension Sacrifice | -£50,000 | | **Adjusted Income** | **£264,600** | [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:12-14]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:17:17 -->
- Taper Risk Re-assessment: With Adjusted Income of **£264,600**, Stephen is £4,600 above the £260,000 taper threshold. This means the £60,000 annual allowance is reduced by £2,300 (£1 for every £2 over £260k) to **£57,700**. [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:19:19 -->
- Taper Risk Re-assessment: However, carry-forward brings in unused allowances from prior years, so the real constraint is whether total contributions exceed the available carry-forward + current allowance. [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:19-19]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:22:25 -->
- 2026-27 Contribution Summary: | Item | Amount | |---|---| | Regular salary sacrifice (20.4%) | £40,800 | | Bonus sacrifice | £50,000 | [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:22-25]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:26:26 -->
- 2026-27 Contribution Summary: | **Total 2026-27 Contributions** | **£90,800** | [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:26-26]

## Promoted From Short-Term Memory (2026-07-20)

<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:28:28 -->
- 2026-27 Contribution Summary: Since this exceeds the tapered allowance of ~£57,700, carry-forward is required. The £35,051 from 2023/24 fully covers the gap. [score=0.857 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:28-28]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:31:31 -->
- Carry Forward Summary (Revised April 2026): <table header-row="true" header-column="false"> [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:31-31]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:33:36 -->
- Carry Forward Summary (Revised April 2026): <td>Tax Year</td> <td>Annual Allowance</td> <td>Total Contributions</td> <td>Unused (Carry Forward)</td> [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:33-36]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:39:42 -->
- Carry Forward Summary (Revised April 2026): <td>2023-24</td> <td>£60,000.00</td> <td>£24,790.08</td> <td>£35,209.92</td> [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:39-42]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:45:48 -->
- Carry Forward Summary (Revised April 2026): <td>2024-25</td> <td>£60,000.00</td> <td>£42,482.02</td> <td>£17,517.98</td> [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:45-48]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13-taper-recalc.md:51:54 -->
- Carry Forward Summary (Revised April 2026): <td>2025-26</td> <td>£55,732.76</td> <td>£38,158.40</td> <td>£17,574.36</td> [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-13-taper-recalc.md:51-54]
