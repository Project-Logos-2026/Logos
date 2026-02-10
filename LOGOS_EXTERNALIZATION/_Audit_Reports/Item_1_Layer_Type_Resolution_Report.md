# Item 1 Layer Type Resolution Report

## Summary of the issue
The template registry used EXPLANATORY for both terminal explanations and compositional discourse, creating a layer-4 identity collision between terminal explanation output and multi-statement discourse assembly.

## Rationale for adding DISCOURSE
A distinct DISCOURSE template type separates compositional discourse assembly from terminal human-facing explanation, preserving EXPLANATORY as terminal-only while enabling non-terminal composition in a schema-compliant and auditable way.

## Template_Type_Registry.json excerpts

### Before
```json
    "EXPLANATORY": {
      "Category": "Human_Facing",
      "Runtime_Priority": 4,
      "Composable": false,
      "Sequence_Class": "Terminal",
      "Definition": "A human-oriented explanatory template that does not participate in logical composition.",
      "Runtime_Semantics": [
        "Never used in logical inference",
        "Appended last if present",
        "Optional in compiled output"
      ],
      "Constraints": [
        "Must not affect runtime decision logic"
      ]
    }
```

### After
```json
    "EXPLANATORY": {
      "Category": "Human_Facing",
      "Runtime_Priority": 4,
      "Composable": false,
      "Sequence_Class": "Terminal",
      "Definition": "A human-oriented explanatory template that does not participate in logical composition.",
      "Runtime_Semantics": [
        "Never used in logical inference",
        "Appended last if present",
        "Optional in compiled output"
      ],
      "Constraints": [
        "Must not affect runtime decision logic"
      ]
    },
    "DISCOURSE": {
      "Category": "Human_Facing",
      "Runtime_Priority": 5,
      "Composable": true,
      "Sequence_Class": "NonTerminal",
      "Definition": "A multi-statement compositional template for discourse assembly.",
      "Runtime_Semantics": [
        "Supports multi-statement composition",
        "May wrap or aggregate multiple statements",
        "Not used in logical inference"
      ],
      "Constraints": [
        "Must not alter logical truth",
        "Must not affect runtime decision logic"
      ]
    }
```

## EXPLANATORY unchanged confirmation
The EXPLANATORY template entry was not modified.

## Status
Item 1 is CLOSED.
