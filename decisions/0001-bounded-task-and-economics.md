# ADR 0001: Begin with bounded localization and economics

Date: 2026-10-06. Status: accepted.

## Context

End-to-end code repair combines retrieval, planning, editing, tools and validation.
Starting with LoRA would assume training is useful before measuring the capability
and economic gap. ToolGap studies a separate runtime mechanism.

## Decision

Use Efficient Agentic Inference as the project name and Small Specialist as Track 1.
Begin with ranked file localization, a frozen evaluation contract and total cost
per successful localization. Build dataset and untuned baselines before training.
Keep the harness independent of ToolGap and competition orchestration frameworks.

Compare prompt/retrieval engineering against adaptation. Include training
amortization, failures and all fallback costs. Treat null measurements explicitly.
Accept a finding that training is unnecessary or economically unfavorable.

## Consequences

Localization quality does not prove patch resolution success. Gold patch files
are an observable reference, not proof that every alternative solution must touch
those same files. Downstream repair and systems results require later experiments.
Initial work produces contracts and software checks, not model efficacy evidence.
