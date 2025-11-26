# Presidio anonymizer

## Description

The Presidio anonymizer is a Python based module for anonymizing detected PII text
entities with desired values.

![Anonymizer Design](../docs/assets/anonymizer-design.png)

### Deploy Presidio anonymizer to Azure

Use the following button to deploy presidio anonymizer to your Azure subscription.
 
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmicrosoft%2Fpresidio%2Fmain%2Fpresidio-anonymizer%2Fdeploytoazure.json)

The Presidio-Anonymizer package contains both Anonymizers and Deanonymizers.

**Anonymizers** are used to replace a PII entity text with some other value.
**Deanonymizers** are used to revert the anonymization operation (ex: decrypting encrypted text).

---

### Anonymizer

Presidio anonymizer comes by default with the following anonymizers:

**Replace**  
  Replaces the PII with desired value.  
  Parameters:  
  - new_value: replaces existing text with the given value.  
    If no value is supplied, the default will be <entity_type>.

**Redact**  
  Removes the PII completely from text.

**Hash**  
  Hashes the PII using sha256 or sha512.  
  Parameters:
  - hash_type: sha256 or sha512 (default sha256)

**Mask**  
  Replaces the PII with repeated characters.  
  Parameters:
  - chars_to_mask
  - masking_char
  - from_end

**Encrypt**  
  Encrypts the text and replaces it with the encrypted value.

**Custom**  
  Applies a user lambda function.

**AHDS Surrogate**  
  Uses Azure Health Data Services to generate realistic surrogates.

Encryption uses AES (Rijndael). Keys must be 128, 192, or 256 bits.

---

### Handling overlaps between entities

Presidio handles overlaps in several ways:

**No overlap** → replace normally  
**Full overlap** → keep higher score  
**One contains another** → keep the larger span  
**Partial intersection** → anonymize both and concatenate  

Examples included in original file.

---

### Deanonymizer

Supports:

**Decrypt** (AES)

---

## Installation

### Install using pip
pip install presidio-anonymizer

---

## Getting started

Example:
python
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

engine = AnonymizerEngine()

result = engine.anonymize(
    text="My name is Bond, James Bond",
    analyzer_results=[
        RecognizerResult(entity_type="PERSON", start=11, end=15, score=0.8),
        RecognizerResult(entity_type="PERSON", start=17, end=27, score=0.8),
    ],
    operators={"PERSON": OperatorConfig("replace", {"new_value": "BIP"})},
)

print(result)

Decrypt example also included in original.

---

## As Docker service
docker-compose up -d

---

## HTTP API

See official API docs.

---

# 📘 Lab: Debugging & Strategy Pattern Explanation

For this part of the lab, I used the VS Code debugger to see how Presidio chooses the correct operator.  
I set a breakpoint on this line inside **operators_factory.py**:
operator = operators_by_type.get(operator_name)

This stopped the program right before the operator was selected, so I could inspect everything.

---

## 📸 Call Stack Screenshot

I saved the screenshot as **call-stack.png** in the root folder of the repository.

When the debugger paused, the call stack showed this flow:
main
→ run_anonymizer
→ anonymize
→ _operate
→ _operate_on_text
→ create_operator_class

---

## 🔍 How many if/elif branches?

The factory literally uses **only one main check**:

If it's an anonymizer  
If it's a deanonymizer  

There is **no long chain of if/elif statements**.

---

## 🧱 What Python data structure is used?

The factory uses a **dictionary** to map operator names to operator classes:
python
{
  "replace": Replace,
  "mask": Mask,
  "redact": Redact,
  "initial": Initial
}

The operator is selected by:
operators_by_type.get(operator_name)

---

## 🎯 How this shows the Strategy Pattern

This is the Strategy pattern because:

Each operator (replace, mask, hash, initial, etc.) has the same interface (operate()).
The engine doesn’t care which operator it uses.
The behavior is chosen **at runtime** based on the operator name.
New operators can be added without changing the engine.

This makes the operators **swappable behaviors**, which is the whole idea of Strategy.

---
