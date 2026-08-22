---
id: ATLAS-PLUGINSPEC-CATALOG-MIG
title: Plugin Migration Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Migration Catalog

## 1. Purpose

Documents migration types, rules, and common migration patterns.

## 2. Migration Types

| Type              | Scope         | Atomic | Rollbackable |
|-------------------|---------------|--------|--------------|
| Manifest          | Schema format | Yes    | Yes          |
| Configuration     | Config values | Yes    | Yes          |
| Storage           | Data schema   | Tx     | Yes          |
| Permission        | Permission decl| Partial| Yes         |

## 3. Common Migration Patterns

### Pattern 1: Field Rename
```
from: "author_name" -> to: "author.name"
```

### Pattern 2: Field Add with Default
```
add: "homepage" default: ""
```

### Pattern 3: Field Remove
```
remove: "deprecated_flag"
```

### Pattern 4: Schema Upgrade
```
from: "v1" -> to: "v2"
validate: "https://atlas.dev/schemas/plugin/v2"
```

### Pattern 5: Storage Table Migration
```
create: "users_v2"
migrate: "users" -> "users_v2"
drop: "users" (after validation)
```

## 4. Cross-References

- RFC-0228 Plugin Migration
