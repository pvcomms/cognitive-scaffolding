# Security

## What this handles

The ledger holds what a person writes about their own loops: beliefs, body states, what they
intend to do and whether they did it. That's sensitive. It lives in the browser's
`localStorage` under `cognitive-scaffolding.v1`, and in any JSON file the person exports.

## What leaves the machine

Nothing, unless the person does it. The page makes no network requests, loads no third-party
script or font, and has no analytics. DOI links go to doi.org when clicked. The sparring
brief is copied to the clipboard, never sent anywhere. Where the person pastes it is their
choice, and whatever they paste goes to that service.

`check_sources.py` sends citation DOIs to api.crossref.org when run by hand. It sends no
ledger data.

## Rendering

The toolbox is escaped at build time. Everything typed into a run goes through `esc()` before
it reaches `innerHTML`. Imported ledger files are shape-checked and normalised, and their
fields are escaped the same way.

## Reporting

This is a personal tool. Tell Param directly: pvcomms (at) pm dot me.
