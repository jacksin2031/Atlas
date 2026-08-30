# Atlas input control script

`atlas_input_control.py` is a CLI client for the provider-independent Atlas
Input Service. It is dry-run by default:

```powershell
python scripts/atlas_input_control.py --actions '[{"action":"move","x":400,"y":300},{"action":"click"},{"action":"type","text":"Hello Atlas"},{"action":"hotkey","keys":["ctrl","s"]}]'
```

To send real Windows input, pass both `--execute` and `--confirm` only after
reviewing the script:

```powershell
python scripts/atlas_input_control.py --script actions.json --execute --confirm
```

Supported actions are `move`, `click`, `double_click`, `drag`, `scroll`,
`press`, `hotkey`, `type`, `key_down`, `key_up`, `wait`, and `release_all`.
No shell commands or arbitrary Python are accepted. All held input is released
when the script exits.

Run a Studio workflow through Workflow Runtime and Input Runtime in test mode:

```powershell
python scripts/run_input_workflow.py sample-workflow-input.json
```

Real Windows acceptance requires explicit confirmation:

```powershell
python scripts/run_input_workflow.py sample-workflow-input.json --execute --confirm
```
