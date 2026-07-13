# judge-card

Turn LLM judge diagnostics into a portable disclosure card that reviewers can inspect and archive.

`judge-card` is for evaluation owners, auditors, and release reviewers who need a small, stable record of the judge model, diagnostic summary, known bias signals, recommended use, generation time, and synthetic-data disclosure. It validates the card shape and renders the same evidence as JSON, Markdown, or HTML.

## Inspectable Output

`judge-card generate` reads a `judge-bench`-shaped JSON report and writes:

- `.json`: the structured Judge Card.
- `.md`: a review-ready Markdown disclosure.
- `.html`: a standalone HTML document containing the Markdown evidence.

Every generated card includes a 64-character `prompt_hash` field computed from the sorted input `results` payload, plus the probe summary and known-bias rows. `validate` emits JSON with `ok` and explicit schema errors.

## Runtime Boundary

Generation and validation operate only on local JSON files. The package has no runtime dependencies, network requests, model calls, telemetry, or hosted storage.

## Install

```bash
python -m pip install judge-card==0.1.2
```

For development from a clone:

```bash
python -m pip install -e .
```

## Quickstart

From a repository checkout:

```bash
judge-card generate --from examples/judge_bench_output.json --out judge-card.json
judge-card generate --from examples/judge_bench_output.json --out judge-card.md
judge-card validate judge-card.json
```

The schema is available at [`spec/judge-card-schema-v1.json`](spec/judge-card-schema-v1.json), with synthetic examples under [`examples/`](examples/).

## Release Status

Registry status verified July 13, 2026: version `0.1.2` is published on PyPI and tagged `v0.1.2` in the public repository. The project is alpha software. No model endorsement, certification, or adoption claim is made.

## Limits

A Judge Card discloses the supplied diagnostic evidence; it does not independently test a model, verify a provider, certify a judge, or establish benchmark quality.

## Next Action

Generate JSON and Markdown cards from the matching `judge-bench` report, review the model id, prompt hash, bias rows, and recommended use, then attach the JSON card to the corresponding eval-run manifest.
