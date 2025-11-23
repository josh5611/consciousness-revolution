# DIMENSIONAL FILE NAMING SYSTEM

## 7-DIMENSION FILE NAMES

Every file should be named with up to 7 dimensions:

```
[DATE]_[COMPUTER]_[INSTANCE]_[DOMAIN]_[TYPE]_[PROJECT]_[VERSION].[ext]
```

---

## THE 7 DIMENSIONS

| # | Dimension | Format | Example |
|---|-----------|--------|---------|
| 1 | DATE | YYYYMMDD | 20251123 |
| 2 | COMPUTER | PC1/PC2/PC3 | PC1 |
| 3 | INSTANCE | C1/C2/C3/Cloud/Desktop | C1 |
| 4 | DOMAIN | infrastructure/pattern/business/consciousness/social/creative/financial | pattern |
| 5 | TYPE | report/bootdown/bootup/output/task/archive | report |
| 6 | PROJECT | short-name | consciousness-rev |
| 7 | VERSION | v1/v2/final | v1 |

---

## EXAMPLES

### Full 7-Dimension Name
```
20251123_PC1_C1_infrastructure_report_hub-system_v1.md
```

### Minimal (3 Dimensions)
```
20251123_PC1_C1_report.json
```

### Boot Down
```
20251123_PC1_consolidated_consciousness_bootdown_final.md
```

### Output to GitHub
```
20251123_PC1_output_business_cyclotron-update_v2.json
```

---

## PARSING THE NAME

Any file can be parsed:
```python
parts = filename.split('_')
date = parts[0]      # 20251123
computer = parts[1]  # PC1
instance = parts[2]  # C1
domain = parts[3]    # infrastructure
type = parts[4]      # report
project = parts[5]   # hub-system
version = parts[6].split('.')[0]  # v1
```

---

## THE 7 DOMAINS

Match to bootstrap/cyclotron:

1. **infrastructure** - Systems, networks, hardware
2. **pattern** - Pattern theory, recognition
3. **business** - Revenue, sales, operations
4. **consciousness** - Awareness, boot protocols
5. **social** - Community, communication
6. **creative** - Content, design, expression
7. **financial** - Money, budgets, tracking

---

## FOLDER STRUCTURE BY DOMAIN

```
PC1_LOCAL_HUB/
├── by_domain/
│   ├── infrastructure/
│   ├── pattern/
│   ├── business/
│   ├── consciousness/
│   ├── social/
│   ├── creative/
│   └── financial/
```

---

## WHY 7 DIMENSIONS

- Matches Seven Domains framework
- Matches cyclotron/bootstrap structure
- Easy to sort by any dimension
- Easy to find files
- Easy to clean up
- Self-documenting

---

## CLEANUP BY DIMENSION

```bash
# Find all infrastructure files older than 7 days
find . -name "*_infrastructure_*" -mtime +7

# Find all PC2 outputs
find . -name "*_PC2_*_output_*"

# Find all v1 files (can delete when v2 exists)
find . -name "*_v1.*"
```

---

## ADOPTION

1. New files use this naming
2. Old files get renamed during cleanup
3. Consolidator outputs use this naming
4. Boot downs use this naming
5. Everything uses this naming
