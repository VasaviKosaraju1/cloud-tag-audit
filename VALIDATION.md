# Validation

Local verification on Python 3.9.6 using synthetic inputs.

## Tests

```text
test_blank (test_audit.Tests) ... ok
test_case_sensitive_keys (test_audit.Tests) ... ok
test_compliant (test_audit.Tests) ... ok
test_duplicate_id (test_audit.Tests) ... ok
test_empty_inventory_not_full_compliance (test_audit.Tests) ... ok
test_invalid_value (test_audit.Tests) ... ok
test_missing_required (test_audit.Tests) ... ok
test_nonstring_tag (test_audit.Tests) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK
```

## Example

```sh
python3 audit.py sample.json
```

Exit status: 1. A nonzero policy result is expected for the failing example and is not a test failure.

```text
{
  "resources": 2,
  "compliant": 1,
  "compliance_ratio": 0.5,
  "findings": [
    {
      "resource": "demo-storage-02",
      "issues": [
        {
          "tag": "owner",
          "reason": "missing_or_blank"
        },
        {
          "tag": "cost_center",
          "reason": "missing_or_blank"
        },
        {
          "tag": "environment",
          "reason": "invalid_value"
        }
      ]
    }
  ]
}
```

These results demonstrate the included fixtures. They do not establish production readiness or performance on real customer data.
