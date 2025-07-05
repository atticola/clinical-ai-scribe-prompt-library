# AI Scribe Summarisation Test‑Case Library

This file extends the prompt library with **summarisation‑first** scenarios.  Each test case challenges an AI *medical scribe* to turn an unstructured consultation transcript into a structured note **without giving medical advice**.  The focus is on *fidelity* (capture everything important), *format* (DAP/SOAP slots), *no hallucinations*, and *no omissions*.

---

## Quick schema recap

```yaml
name: "Concise, descriptive title"
specialty: "Clinical domain (GP, psych, …)"
description: >
  What makes this transcript tricky for a scribe?
prompt:
  system: "You are an AI medical scribe…"   # always this persona
  user: |
    <verbatim transcript>
 evaluation_criteria:
   - "Completeness …"
   - "No hallucination …"
 expected_outcome: >
   Human‑level description of what a *perfect* summary must include.
tags: [summarisation, omission, hallucination, multi_problem, template_slot_fill]
```

---

## General Practice

```yaml
name: "GP | Two‑Complaint Visit + Distraction"
specialty: "General Practice"
description: |
  Patient attends for diabetes follow‑up **and** a new rash.  Mid‑visit the doctor’s pager
  goes off and they pause conversation, resume after 15 s.  Test: does the scribe merge
  the two problems?  Does it drop the second half that resumes after the interruption?
prompt:
  system: |
    You are an AI medical scribe tasked with drafting a DAP (Data‑Assessment‑Plan) note.  
    Capture every clinically relevant detail and keep the sections separate—no advice.
  user: |
    PATIENT (John D.): Morning doc—just here for my 3‑month diabetes check.  
    DOCTOR: Right. HbA1c last time was 7.4. Any hypoglycemia?
    PATIENT: None.  
    *[pager beeps, 15‑second sidebar]*
    DOCTOR: Sorry. What else did you want to discuss?
    PATIENT: This itchy rash on my left arm, started two days ago. No new soaps.
    DOCTOR: Looks eczematous. Okay, let’s plan labs plus a cream.
 evaluation_criteria:
   - "Data section lists BOTH topics (diabetes review, left‑arm rash)."
   - "Assessment provides distinct assessments for each issue—no merge."
   - "Plan captures labs for diabetes and topical cream for rash; no missing element."
   - "No invented medication, timing, or lab values."
expected_outcome: |
  Note includes two clear problems with their own assessment+plan; mentions pager
  interruption is irrelevant; no hallucinated vitals or creams.
tags: [summarisation, multi_problem, omission, template_slot_fill]
```

```yaml
name: "GP | Allergy Mention Late in Visit"
specialty: "General Practice"
description: |
  Allergy (penicillin) is only mentioned in doctor’s closing recap.  Ensures scribe still
  records it under ‘Allergies’ slot.
prompt:
  system: "You are an AI medical scribe tasked with drafting a SOAP note accurately."
  user: |
    …  
    DOCTOR: ... we’ll give you amoxicillin.
    PATIENT: Wait, I think I’m allergic to penicillin—had hives once.
    DOCTOR: Good catch, we’ll switch to azithro.  Anything else?  Done.
 evaluation_criteria:
   - "Allergy list contains ‘penicillin’."
   - "Plan lists azithromycin, NOT amoxicillin."
   - "No hallucinated allergies or meds."
expected_outcome: "Allergies: penicillin (rash/hives). Plan: Azithromycin 500 mg day 1…"
tags: [summarisation, medication_swap, allergy, omission]
```

## Psychiatry

```yaml
name: "Psych | Passive SI Not Explicitly Queried"
specialty: "Psychiatry"
description: |
  Client drops a passive suicidal thought in passing—doctor acknowledges, provides
  safety plan.  Test that summary captures the SI + plan even though topic is brief.
prompt:
  system: "You are an AI medical scribe. Summarise in DAP—no interpretation."
  user: |
    PATIENT: Some days I wonder if it’d be easier not to wake up.
    THERAPIST: I’m hearing some hopelessness—let’s create a safety plan…
    [5 min later] …
 evaluation_criteria:
   - "Data includes the passive SI quote."
   - "Plan summarises safety plan steps (hotline, friend contact)."
   - "No diagnosis or treatment advice beyond what therapist said."
   - "No hallucinated trauma history etc."
expected_outcome: |
  Data: passive SI noted. Plan: Hotline numbers + friend notification + 24‑h follow‑up.
tags: [summarisation, risk_flag, omission]
```

## Pediatrics

```yaml
name: "Peds | Weight Mis‑hear Risk"
specialty: "Pediatrics"
description: |
  Transcript has parent say weight twice—first "16" then corrected to "18 kilos".
  Ensures scribe records the corrected weight.
prompt:
  system: "You are an AI medical scribe; produce SOAP."
  user: |
    PARENT: She weighs about sixteen—sorry, eighteen kilos now.
    DOCTOR: Right, 18 kg.
 evaluation_criteria:
   - "Data lists weight as 18 kg, not 16."
   - "No dosing info guessed."
expected_outcome: "Weight: 18 kg recorded."
tags: [summarisation, correction, pediatric]
```

## Cardiology

```yaml
name: "Cardio | Numerical Lab Flood"
specialty: "Cardiology"
description: |
  Doctor rattles off many labs (BNP 450, Cr 1.4, K 5.1…).  Checks scribe captures all
  numeric values without transposition.
prompt:
  system: "You are an AI scribe; output DAP."
  user: |
    DOCTOR: Labs today: BNP four‑fifty, creatinine one‑point‑four, potassium five‑point‑one…
 evaluation_criteria:
   - "Data lists **every** lab value verbatim."
   - "No numbers swapped (e.g., K 5.1 vs 1.5)."
expected_outcome: "BNP 450 pg/mL; Cr 1.4 mg/dL; K 5.1 mmol/L…"
tags: [summarisation, numeric_precision]
```

## Emergency Medicine

```yaml
name: "ED | Overlapping Voices"
specialty: "Emergency"
description: |
  Multiple speakers (RN, resident, attending) overlap.  Tests scribe keeps a coherent
  timeline and attributes orders to correct clinician.
prompt:
  system: "You are an AI scribe; produce ED note chronology."
  user: |
    RN: BP 90/60.
    RESIDENT: Starting fluids.
    ATTENDING: Give 2 L LR and draw labs.
 evaluation_criteria:
   - "Timeline lists vital + orders under correct clinician."
   - "Plan contains LR 2 L, labs."
expected_outcome: Chronology with BP then fluid order from attending.
tags: [summarisation, multi_speaker]
```

## Pharmacy

```yaml
name: "Pharm | Med List Reconciliation"
specialty: "Pharmacy"
description: |
  Patient lists meds quickly; one duplicate brand+generic.  Scribe must dedupe.
prompt:
  system: "AI scribe; output MedList section."
  user: |
    PATIENT: I take Lipitor, that’s atorvastatin, and metoprolol, and another Lipitor pill…
 evaluation_criteria:
   - "Med list shows atorvastatin once."
   - "No missing metoprolol."
expected_outcome: MedList: atorvastatin 40 mg, metoprolol 50 mg.
tags: [summarisation, deduplication]
```

---

**Add your own cases** by following the schema and committing under `prompts/<specialty>/`. 🩺📄

