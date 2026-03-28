# The Quality Threshold: Why Capability Doesn't Scale Linearly

*On emergent abilities, the limits of parallelism, and the minimum viable model.*

---

## The Intuition That Fails

When a model is too small for a task, the instinct is to compensate: use more models, run more passes, add more structure. If one 3B model can't reliably produce a tool call, perhaps three of them — voting, checking each other, retrying — can approximate the reliability of a single capable model.

This intuition is wrong. It fails not for engineering reasons, but for reasons intrinsic to how language models develop capability. Understanding why requires looking at what "capability" actually means at these scales.

---

## Emergent Abilities and the Threshold Effect

Large language models do not scale smoothly. Certain abilities are absent at small scale and appear abruptly as scale increases — not as gradual improvements, but as phase transitions.

Wei et al. (2022) documented this across a range of tasks: few-shot arithmetic, logical reasoning, multi-step inference, instruction following. At small scales, performance is near chance. At a threshold — different for each capability, typically in the range of 10–100 billion parameters — performance jumps discontinuously. The models are not gradually getting better at these tasks; they are not doing them at all, and then they are.

The relevant threshold for outheis is **structured tool dispatch**: producing a valid JSON tool call with correct argument names and types, derived from a natural-language query. This is not pattern matching against training examples. It requires:

1. Understanding the query semantically
2. Identifying which tool satisfies the intent
3. Extracting the correct arguments from context
4. Producing syntactically valid structured output

Models below the threshold fail on step 1 or 3. They produce plausible-looking output — often structurally valid JSON — but with wrong tool names, hallucinated arguments, or complete non sequiturs. The failures are not graceful degradations; they are category errors.

---

## Why Parallelism Does Not Help

If capability is absent below the threshold, adding more below-threshold models does not produce it. This is not a resource argument. It is an argument about the nature of what is missing.

Consider what it would mean for three 3B models to "vote" on a tool call. Each produces its best guess. Voting requires comparing outputs and finding a majority — but if none of the outputs is correct, majority vote returns the most common error, not a correct result. Worse: the errors from similar small models are correlated. They fail in the same ways because they have the same limitations. Ensemble methods gain from *diverse* failures, not from *identical* failures.

More passes don't help either. A model that cannot derive the correct argument from the query on the first pass will not derive it on the third. The pass is not where the capability lives; the capability would need to live in the weights, and the weights don't have it.

The engineering parallel: you cannot implement a feature in software by running buggy code faster. The bug must be fixed. For language models, below the threshold, there is no equivalent of "fixing the bug" without retraining. The model is what it is.

---

## The Structural Argument

There is a deeper reason why the threshold cannot be bypassed. Transformer models process a query in a single forward pass through all layers. Each layer refines the representation of the query, building increasingly abstract features. The final layer produces the output distribution.

The capability to follow a complex instruction depends on having enough layers, enough heads, and enough parameters to represent the necessary intermediate abstractions. A small model does not have a degraded version of this ability; it has a different architecture that reaches a lower ceiling. You can run it more times, but the ceiling does not move.

Larger models also have more capacity to represent what is not said — inference from context, disambiguation, recognition of unstated intent. This is exactly what tool dispatch requires: "check my agenda" must be resolved to an `agenda_query` call, not a `file_read` or `memory_lookup`. The resolution requires contextual inference that a small model cannot reliably perform.

---

## The Practical Threshold for outheis

Empirically, the 7B boundary holds reliably for instruction-following in outheis's context. Below it:

- Tool call syntax is correct; tool selection is wrong
- Arguments are plausible-sounding but don't correspond to actual parameters
- Multi-step reasoning (which tool, then which arguments) collapses

At 7B with instruction tuning, the threshold is crossed for routing-class tasks (relay). At 12–14B, it holds for tool-use agents (zeno, cato) if verified. Below 7B, no amount of prompt engineering, retrying, or structural scaffolding produces reliable results — because the capability the scaffold assumes is not there.

This means the relevant question when selecting a model is not "how small can I go?" but "is this model past the threshold for the task?" It is a binary, not a gradient. Testing confirms this: `test_ollama_tool_use.py` produces ✓ or ✗, not a score. A ✗ model cannot be provisionally used with more care.

---

## What This Means for outheis Design

**One capable agent beats many weak ones.** outheis is built around a small number of specialized agents, each with a focused tool set and a model that has crossed the relevant capability threshold. This is not a concession to practical limitations; it is a structural property of how these systems work.

**The boundary is a quality threshold, not a resource threshold.** The decision to require a minimum model size is not about running costs or latency. It is about whether the capability required by the task exists in the model at all. A model that fails the tool-use test is not a slower or cheaper version of one that passes; it is a different category of tool.

**Verification is mandatory before deployment.** Because capability is threshold-based and not inferrable from parameter count alone (different architectures, different training regimes, different fine-tuning), empirical testing is required. The parameter count is a heuristic for where to start looking; the test result is the ground truth.

**Disable rather than degrade.** When no model past the threshold is available for a given agent role, the correct response is to disable that agent's scheduled tasks, not to run them with a below-threshold model. A nightly pattern inference run that produces hallucinated memories is worse than no run: it injects false data into the knowledge base. A failed run leaves the system unchanged. A degraded run corrupts it.

---

## Further Reading

- Wei, J. et al. "Emergent Abilities of Large Language Models." *Transactions on Machine Learning Research*, 2022. — The systematic documentation of threshold effects across capability dimensions.
- Kaplan, J. et al. "Scaling Laws for Neural Language Models." *arXiv*, 2020. — Power-law relationships in loss; the baseline from which emergence departures are measured.
- Schaeffer, R. et al. "Are Emergent Abilities of Large Language Models a Mirage?" *NeurIPS*, 2023. — The challenge: some apparent emergence may be an artifact of metric choice. Worth reading alongside Wei et al. for an accurate picture.
- Srivastava, A. et al. "Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models." *Transactions on Machine Learning Research*, 2023. — The BIG-Bench benchmark; large-scale empirical evidence for capability emergence across 200+ tasks.
