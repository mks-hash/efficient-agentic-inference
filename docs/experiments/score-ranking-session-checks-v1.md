# Score-ranking session checks — supplementary contract v1

Prepared 2026-10-07; before any validation generation. Paid execution NOT_AUTHORIZED.
[ADR 0010](../../decisions/0010-score-session-preflight.md). This supplements
[score-ranking-validation-v2](score-ranking-validation-v2.md); no changes to its
recipes, population, primary analysis or evaluator.

## Fixed twenty-four technical requests

Each of S-paths, S-scores, G-scores, G-paths runs the same five-request synthetic
packet in order: two candidates, empty candidates, twenty candidates, quote/non-ASCII
paths, then an exact repeat of the first payload. Only the technical instance ID
changes; IDs do not enter messages. Use the already declared system prompts,
native rendering, greedy settings, output limits and strict parsers.

Each arm separately runs the frozen bounded packet for exposed dev-v1 issue
marshmallow-code__marshmallow-1810, without labels or quality evaluation. This
checks a real-sized request and native capacity, not an additional quality sample.
There are 20 synthetic plus four old-issue requests. No retries or substitution.

Verify physical gold-free isolation, full nonzero GPU offload, exact weight/source/
binary/template identities, eager grammar, native token counters and EOS without
context truncation. Path grammars admit known candidate strings; duplicate paths
still fail the strict parser. Score grammars require N integer enum entries 0..100
and saved canonical binding/schema hashes; mapped paths must match the declared
rule. A malformed schema/binding, overflow, limit stop, runtime/provenance or
repeatability failure blocks validation. Path duplicates and semantically wrong
valid outputs remain recorded; they do not trigger prompt changes or repair.

For each arm compare the first/fifth synthetic requests' rendered prompt, native
input/output IDs, raw text, ranked paths, disposition and failure reason. Report
these four same-backend greedy pairs independently, without selecting a stable
subset. Within each model the two recipes must have identical user-message
bytes; their system prompts and full native input IDs must differ as preregistered.
Do not demand full-prompt token equality between different recipes.

## Freeze, resources and collection

All technical gates precede the joint four-config execution freeze and first
validation generation. Infer only from canonical bounded packets in the isolated
namespace; transport neither gold/evaluator, upstream data, Git history nor full
repositories. Freeze hashes for the exact two prompts, twelve-member minimal
inference archive, technical/validation packets, launcher and these supplements.
The existing 29-file research freeze remains unchanged.

Use fresh backends per run, one slot, four threads and one resident model.
Synthetic arm budget 600s, old-issue budget 300s, per task 120s; research arm
budgets remain 1,800s for 30 fixed tasks. Provider three-hour DELETE backstop,
150-minute controller limit and cleanup reserve take precedence; unavailable
slots remain recorded failures. Capture passive one-second NVIDIA memory,
utilization and power observations consistently; sampling may miss peaks and
does not establish active GPU-seconds. Stop telemetry before archiving.

Archive technical completion and each research arm under a unique immutable
milestone name. Preserve a final or failure archive, every raw trace and timing;
collect/checksum locally before deleting the new VM/disk. Open local gold only
after all four arms have been collected. Technical work, failures, downloads,
shared setup/transfer/cleanup remain in session accounting; actual costs and
missing components remain unknown until attributable provider evidence exists.

The plan requests one new L4 session, USD 5 maximum and at most three hours,
with early deletion after verified collection. This is on-demand usage, not a
three-hour reservation. Prior paid authorizations cover their completed runs.
No new allocation, tuning, training or research publication is authorized here.
