# Brief A diagrams

These diagrams describe the selected Brief-A analysis: explaining the change in
validated booking test lines between H1 2025 and H1 2026.

## 1. Brief-A analysis in one view

```mermaid
flowchart LR
    RAW["Raw booking exports"] --> PROFILE["01 Profile"]
    PROFILE --> LOAD["02 Load and validate"]
    LOAD --> ACCEPTED["Accepted booking records"]
    LOAD --> REJECTS[("Rejected bookings with reasons")]
    ACCEPTED --> CLEAN["03 Clean and reconcile"]
    CLEAN --> BOOKING[("Clean booking table")]
    CLEAN --> PEOPLE[("Analytical person map")]
    BOOKING --> TREE["05 Growth tree"]
    PEOPLE --> TREE
    TREE --> ANSWER["06 Brief-A answer"]
    ANSWER --> BOARD[("Board number workbook")]
    ANSWER --> CHART[("City growth chart")]
    PROFILE -.-> LOGS[("Approach, decisions and challenges logs")]
    LOAD -.-> LOGS
    CLEAN -.-> LOGS
    TREE -.-> LOGS
```

## 2. What is counted for Brief A

```mermaid
flowchart TB
    SOURCE["Booking source rows"] --> VALID{"Pass the booking rules?"}
    VALID -->|No| REJECT["Keep in rejects file"]
    VALID -->|Yes| RECORD["Retain booking record"]
    RECORD --> TESTS["Count n_tests"]
    RECORD --> VISIT["Count one booking record as a visit proxy"]
    RECORD --> PERSON["Link patient_id to person_id"]
    TESTS --> TOTAL["Validated booking test lines"]
    VISIT --> VISITS["Visit proxy count"]
    PERSON --> PEOPLE["Distinct analytical people"]
    TOTAL --> TREE["Test lines = people x visits/person x test lines/visit"]
    VISITS --> TREE
    PEOPLE --> TREE
```

The result is a booking-line measure. It is not a claim that every line was
attended, collected or performed.

## 3. Cleaning and identity decisions

```mermaid
flowchart TD
    INPUT["Accepted booking records"] --> ID["Use the documented booking identity"]
    ID --> STATUS{"Superseded reschedule record?"}
    STATUS -->|Yes| REMOVED["Remove from the comparable population and record the count"]
    STATUS -->|No| RETAIN["Keep the booking record"]
    RETAIN --> PERSONKEY["Map patient details to person_id"]
    PERSONKEY --> PERSONRULE["Normalised phone + name + date of birth"]
    PERSONRULE --> PEOPLE["Analytical people denominator"]
    RETAIN --> COLLECTION["Check collections with a left join"]
    COLLECTION --> MATCHED["Matched collection"]
    COLLECTION --> MISSING["left_only: keep and flag, do not call it cancellation"]
    RETAIN --> FINAL["Clean booking table for Brief A"]
    PEOPLE --> FINAL
```

The person key is suitable for aggregate growth analysis. It is not a verified
clinical identity and should not be used for result routing.

## 4. Brief-A growth tree

```mermaid
flowchart TB
    P["People"] --> VPP["Visits per person"]
    VPP --> V["Visits"]
    V --> TPV["Test lines per visit"]
    TPV --> T["Validated booking test lines"]
    P --> T

    T0["H1 2025: 433,611"] --> T1["H1 2026: 455,383"]
    P0["94,275 people"] --> P1["97,827 people"]
    VPP0["2.0027 visits/person"] --> VPP1["1.9833 visits/person"]
    TPV0["2.2966 test lines/visit"] --> TPV1["2.3471 test lines/visit"]
```

The measured changes are:

- Total test lines: **+5.02%**
- People: **+3.77%**
- Visits per person: **-0.97%**
- Test lines per visit: **+2.20%**

The three factor changes multiply back to the total change. Their logarithmic
changes also add up to the total logarithmic change.

## 5. H1 comparison and reconciliation

```mermaid
flowchart LR
    subgraph H1_2025["H1 2025"]
        A1["Raw nonblank test lines: 435,880"]
        A2["Validation exclusions: 2,269"]
        A3["Superseded lines removed: 0"]
        A4["Retained lines: 433,611"]
        A1 --> A2 --> A3 --> A4
    end
    subgraph H1_2026["H1 2026"]
        B1["Raw nonblank test lines: 461,080"]
        B2["Validation exclusions: 2,156"]
        B3["Superseded lines removed: 3,541"]
        B4["Retained lines: 455,383"]
        B1 --> B2 --> B3 --> B4
    end
    A4 --> COMPARE["Compare like-for-like retained booking test lines"]
    B4 --> COMPARE
    COMPARE --> RESULT["+5.02% growth"]
```

The periods use the complete local calendar half-years:
`[2025-01-01, 2025-07-01)` and `[2026-01-01, 2026-07-01)`.

## 6. City contribution to the Brief-A result

```mermaid
flowchart LR
    TOTAL["+21,772 net test-line increase"] --> AHM["Ahmedabad: +8,043"]
    TOTAL --> BLR["Bengaluru: +7,535"]
    TOTAL --> HYD["Hyderabad: +5,303"]
    TOTAL --> PUN["Pune: +4,916"]
    TOTAL --> CHE["Chennai: +740"]
    TOTAL --> JAI["Jaipur: -4,765"]
```

The city view describes where the change appeared. It does not prove why the
change happened. The source city fields remain unchanged; the documented
`Bangalore` to `Bengaluru` mapping is used only for the comparable city view.

## 7. Evidence and audit trail

```mermaid
flowchart TD
    RAW["Raw files remain unchanged"] --> PROFILE["Profile outputs"]
    PROFILE --> RULES["Documented validation and identity rules"]
    RULES --> CLEAN["Clean tables and rejects"]
    CLEAN --> METRICS["Hypo A metric summary CSV"]
    METRICS --> TREECHECK["Product and log-growth checks"]
    TREECHECK --> HEADLINE["Brief-A headline: +5.0%"]
    PROFILE -.-> DECISIONS["Decisions log"]
    RULES -.-> DECISIONS
    CLEAN -.-> DECISIONS
    METRICS -.-> DECISIONS
    TREECHECK -.-> CHALLENGES["Challenges log"]
```

The main evidence files are:

- `data/hypo_A/brief_a_iitgn_metric_summary.csv`
- `data/hypo_A/brief_a_iitgn_component_changes.csv`
- `data/hypo_A/brief_a_iitgn_city_contributions.csv`
- `data/hypo_A/brief_a_iitgn_reconciliation.csv`
- `docs/brief-a-iitgn-aligned-results.md`
