Here are multiple-choice questions based on the provided lecture transcript, complete with answer keys and explanations.

---

### **Question 1: History of AI in Medicine (MYCIN)**
In the 1970s, Stanford developed the MYCIN system, which was one of the earliest clinical applications of artificial intelligence. What was the primary goal of this system?
* **A)** To predict the length of stay for psychiatric inpatients.
* **B)** To identify bacteria causing infections and recommend appropriate therapy.
* **C)** To automatically extract chief complaints from free-text clinical notes.
* **D)** To diagnose chronic kidney disease stages using creatinine levels.

**Correct Answer:** **B) To identify bacteria causing infections and recommend appropriate therapy.**
* **Explanation:** According to the lecture, the goal of the MYCIN system "was to try to identify bacteria that might cause infection, and then to try to guide what would be the appropriate therapy for that bacteria."

---

### **Question 2: Translation Challenges of Early AI Systems**
According to the lecture, what was one of the primary reasons why highly effective 1980s AI systems, such as Internist-1 (Quick Medical Reference), failed to translate into actual clinical care?
* **A)** They had a success rate of less than 30% when evaluated by experts.
* **B)** They required expensive GPU hardware that was unavailable at the time.
* **C)** There was a significant mismatch between the input they expected and existing clinical workflows.
* **D)** The medical community completely banned the use of computer-assisted diagnosis.

**Correct Answer:** **C) There was a significant mismatch between the input they expected and existing clinical workflows.**
* **Explanation:** Sontag explains that these early systems were designed to solve narrow problems and "there was a big gap between the input they expected and the current clinical workflows." Clinicians had to manually type structured symptoms into a mainframe computer, which took too much time.

---

### **Question 3: Policy and EMR Adoption**
What major policy initiative in the United States catalyzed the dramatic increase in hospital adoption of Electronic Medical Records (EMRs) from under 10% in 2008 to over 80% by 2015?
* **A)** The Precision Medicine Initiative (All of Us)
* **B)** An economic stimulus package allocating approximately $30 billion for EMR purchases
* **C)** The nationwide rollout of the ICD-10 coding system
* **D)** The creation of the Fast Healthcare Interoperability Resources (FHIR) standard

**Correct Answer:** **B) An economic stimulus package allocating approximately $30 billion for EMR purchases**
* **Explanation:** The transcript notes that as part of an economic stimulus package initiated by President Obama, "there was something like $30 billion allocated to hospitals purchasing electronic medical records," which caused adoption to increase dramatically.

---

### **Question 4: Medical Data Standards**
Which of the following statements accurately describes a medical data standard mentioned in the lecture?
* **A)** **LOINC** is a standardized system used to encode pharmacy national drug codes.
* **B)** **OMOP** is an ontology with millions of medical concepts used to map free text.
* **C)** **FHIR** is a common data model used primarily for insurance claims databases.
* **D)** **ICD-10** is a highly detailed system used to code diagnoses.

**Correct Answer:** **D) ICD-10 is a highly detailed system used to code diagnoses.**
* **Explanation:** The transcript states that diagnoses are coded in a standardized system called ICD-9 or ICD-10. Sontag notes that ICD-10 is highly detailed, even including codes for specific events like being "bitten by a turtle." (LOINC is for lab tests, FHIR is an API standard, and OMOP is a common data model).

---

### **Question 5: Redesigning the Emergency Department Workflow**
In the machine learning system deployed by Sontag's group at Beth Israel Deaconess Medical Center to improve "chief complaints," how was the clinical workflow redesigned?
* **A)** The triage nurse types the chief complaint first, and the system automatically orders lab tests.
* **B)** The chief complaint is assigned last, using a machine learning algorithm to predict and prioritize standardized options based on vitals and a short clinical note.
* **C)** The system uses speech recognition to record the entire patient-doctor conversation and bypasses the nurse entirely.
* **D)** The system completely eliminated the chief complaint field and replaced it with a deep learning EKG analyzer.

**Correct Answer:** **B) The chief complaint is assigned last, using a machine learning algorithm to predict and prioritize standardized options based on vitals and a short clinical note.**
* **Explanation:** Sontag explains that they changed the workflow so that the chief complaint is the *last* thing assigned. First, the nurse takes vitals and writes a short note. The machine learning algorithm uses this data to predict and display the five most likely standardized chief complaints, which the nurse can easily select.

---

### **Question 6: Unique Challenges of Healthcare ML (Censoring)**
In the context of healthcare machine learning, what does "censoring" refer to?
* **A)** The removal of patient identifiers (like names and Social Security numbers) to protect privacy.
* **B)** Having data for patients only within small windows of time, such as not knowing when a patient died because they were still alive at the end of the study period.
* **C