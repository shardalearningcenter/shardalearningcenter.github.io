---
layout: course
title: "35. Evaluation: Beyond Vibes"
permalink: /courses/llm-mastery/35-eval-harness-thinking/
course_track: "LLM Mastery"
description: "A benchmark score is a summary statistic of your blind spots, not a measurement of quality — and it's only trustworthy if you've ruled out contamination."
level: Advanced
toc:
  - id: "the-claim"
    label: "The claim"
  - id: "mental-model-four-layers-that-each-lie-differently"
    label: "Mental model: four layers that each lie differently"
  - id: "worked-example-exact-match-scoring-and-why-it-s-fragile"
    label: "Worked example: exact-match scoring, and why it's fragile"
  - id: "the-contamination-check-you-should-always-run"
    label: "The contamination check you should always run"
  - id: "failure-mode-prompt-format-sensitivity"
    label: "Failure mode: prompt format sensitivity"
  - id: "exercise"
    label: "Exercise"
---

> **Level:** Advanced · **Article 35/50** · Karpathy-style LLM course

## The claim
{: #the-claim }

A single scalar benchmark number — "72.3% on MMLU" — is not a measurement of model quality in any general sense. It's a measurement of performance on the *specific distribution of questions in that specific benchmark*, filtered through the *specific prompt format and scoring rule* the harness used, computed on a model that may or may not have seen those exact questions during training. Every one of those specifics is a place the number can quietly diverge from "how good is this model, actually" — and the failure modes compound, because they're each invisible from the number alone. Treating a leaderboard score as ground truth, instead of as one lossy signal among several that each fail in different, mostly uncorrelated ways, is the single most common evaluation mistake in the field.

## Mental model: four layers that each lie differently
{: #mental-model-four-layers-that-each-lie-differently }

Think of model evaluation as four progressively more expensive, less gameable layers, each of which lies to you in a different way if used alone. Training/validation loss lies by being too abstract — a lower loss doesn't tell you the model got *better at anything a user cares about*, just that it predicts held-out tokens from the same distribution slightly better. Standardized harnesses (MMLU, GSM8K, HumanEval) lie via contamination and format-sensitivity, discussed below. Blind human pairwise preference lies by rewarding style, confidence, and length over correctness — humans reliably prefer longer, more confidently-worded wrong answers over short correct ones in blind A/B tests, a well-documented bias in RLHF-adjacent research. Product metrics (did the user's task actually succeed) lie by being slow, expensive, and noisy, and by only covering the specific use cases your product happens to exercise. No single layer is sufficient; the useful signal is agreement (or informative disagreement) across all four.

## Worked example: exact-match scoring, and why it's fragile
{: #worked-example-exact-match-scoring-and-why-it-s-fragile }

Here's a minimal exact-match harness for a GSM8K-style math benchmark, and the exact place it breaks:

```python
import re

def extract_final_answer(model_output):
    # naive: assume the answer follows "The answer is"
    match = re.search(r"[Tt]he answer is\s*\$?(-?[\d,]+\.?\d*)", model_output)
    if not match:
        return None
    return match.group(1).replace(",", "")

def score(model_output, gold_answer):
    predicted = extract_final_answer(model_output)
    if predicted is None:
        return 0
    return int(float(predicted) == float(gold_answer))

case_a = "Let's compute step by step. 3 apples plus 5 apples is 8. The answer is 8."
case_b = "So the final count comes out to 8 apples in total."
case_c = "The answer is $8.00"

for out in [case_a, case_b, case_c]:
    print(out[:30], "->", score(out, "8"))
```

`case_a` scores correctly. `case_b` — semantically identical, arguably clearer prose — scores `0`, not because the model got the math wrong, but because it phrased the answer in a way the regex doesn't recognize. `case_c` should probably score `1` and does, but only because the parsing happened to handle the `$` and `.00`; a slightly different formatting choice by the model breaks it. This is the entire problem with exact-match harnesses in miniature: the harness isn't measuring "did the model solve the problem," it's measuring "did the model solve the problem *and* phrase the answer in one of the specific formats the parser anticipated." Every real benchmark harness carries some version of this fragility, and score differences of a few points between models are frequently within the noise floor this fragility introduces.

## The contamination check you should always run
{: #the-contamination-check-you-should-always-run }

Before trusting any benchmark score for a model you trained (or a training corpus you built), run an n-gram overlap check between the benchmark's test questions and your training corpus:

```python
def ngrams(text, n=13):
    words = text.lower().split()
    return {tuple(words[i:i+n]) for i in range(len(words) - n + 1)}

def contamination_rate(test_questions, train_corpus_ngrams, n=13):
    contaminated = 0
    for q in test_questions:
        q_grams = ngrams(q, n)
        if q_grams and q_grams & train_corpus_ngrams:
            contaminated += 1
    return contaminated / len(test_questions)
```

A long n-gram (13 words is a common choice in contamination studies) that matches exactly between a test question and the training corpus is a strong signal the exact text was present during pretraining — natural language rarely reproduces a specific 13-word sequence by coincidence. Running this check is inexpensive relative to training and is the single highest-leverage thing you can do to know whether a benchmark score is measuring capability or memorization. Its absence — reporting a benchmark score with no contamination analysis — should be treated as a real gap in the claim, not a formality, precisely because the failure it would catch is invisible from the score itself.

## Failure mode: prompt format sensitivity
{: #failure-mode-prompt-format-sensitivity }

The same model, evaluated on the same benchmark questions, can show swings of several points to double digits depending on details that feel like they shouldn't matter: the exact wording of the instruction, whether answer choices are labeled "A/B/C/D" or "1/2/3/4," the number and choice of few-shot examples included before the question, whether a trailing newline is present. This is a documented, reproducible phenomenon (see "State of What Art" and related prompt-sensitivity studies across MMLU-style benchmarks) — it is not a hypothetical edge case. The direct consequence: comparing two models' benchmark scores from two different papers or leaderboards, evaluated with two different harness implementations and prompt formats, is frequently comparing noise, not capability, even when both numbers are individually "correct" for the harness that produced them. The only reliable comparison is running both models through the *identical* harness, prompt format, and scoring code — which is exactly why standardized eval frameworks (lm-evaluation-harness and similar) matter as infrastructure, not just convenience.

## Exercise
{: #exercise }

Using the `score` function above, write two more model-output variants for the same "8 apples" question that a human grader would clearly mark correct but that your regex-based `extract_final_answer` would score as `0`. Then modify `extract_final_answer` to correctly handle at least one of your new cases without breaking the three original ones. Finally, state in one sentence why no regex-based fix can ever fully close this gap, and what evaluation approach (hint: think about what layer 3 in the mental model above does differently) would.

---

[← 34. Mixed Precision Training](/courses/llm-mastery/34-mixed-precision/)  
[36. Supervised Fine-Tuning (SFT) →](/courses/llm-mastery/36-finetuning-sft/)

[Course hub](/courses/llm-mastery/) · [All courses](/courses/)
