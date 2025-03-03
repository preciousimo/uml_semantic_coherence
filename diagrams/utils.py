import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def validate_use_case_diagram(use_case_diagram):
    """
    Validate semantic features of a Use Case Diagram.
    """
    errors = defaultdict(list)
    doc = nlp(use_case_diagram.description)

    # 1. Actor Semantics
    actors = [ent.text for ent in doc.ents if ent.label_ == "PERSON" or ent.label_ == "ORG"]
    for actor in actors:
        if not actor.istitle():  # Check for proper naming (nouns)
            errors['Actor Naming'].append(f"Actor '{actor}' should be a noun and start with a capital letter.")

    # 2. Use Case Semantics
    use_cases = [token.text for token in doc if token.pos_ == "VERB"]
    for use_case in use_cases:
        if not use_case.islower():  # Check for verb phrases
            errors['Use Case Naming'].append(f"Use Case '{use_case}' should be a verb or verb phrase.")

    # 3. Relationship Semantics
    relationships = [token.text for token in doc if token.dep_ in ("prep", "conj")]
    for rel in relationships:
        if rel not in ["include", "extend", "generalization"]:
            errors['Relationship Semantics'].append(f"Invalid relationship '{rel}'. Use 'include', 'extend', or 'generalization'.")

    return errors

def validate_class_diagram(class_diagram):
    """
    Validate semantic features of a Class Diagram.
    """
    errors = defaultdict(list)
    doc = nlp(class_diagram.description)

    # 1. Class Semantics
    classes = [ent.text for ent in doc.ents if ent.label_ == "ORG" or ent.label_ == "PRODUCT"]
    for cls in classes:
        if not cls.istitle():  # Check for proper naming (nouns)
            errors['Class Naming'].append(f"Class '{cls}' should be a noun and start with a capital letter.")

    # 2. Attribute Semantics
    attributes = [token.text for token in doc if token.pos_ == "NOUN" and token.dep_ == "attr"]
    for attr in attributes:
        if not attr.islower():  # Check for camelCase or snake_case
            errors['Attribute Naming'].append(f"Attribute '{attr}' should be in camelCase or snake_case.")

    # 3. Relationship Semantics
    relationships = [token.text for token in doc if token.dep_ in ("prep", "conj")]
    for rel in relationships:
        if rel not in ["association", "aggregation", "composition", "generalization", "dependency"]:
            errors['Relationship Semantics'].append(f"Invalid relationship '{rel}'. Use 'association', 'aggregation', 'composition', 'generalization', or 'dependency'.")

    return errors

def validate_semantic_coherence(use_case_diagram, class_diagram):
    """
    Validate semantic coherence between Use Case and Class Diagrams.
    """
    use_case_errors = validate_use_case_diagram(use_case_diagram)
    class_diagram_errors = validate_class_diagram(class_diagram)

    # Cross-diagram consistency checks
    cross_errors = defaultdict(list)
    use_case_actors = [ent.text for ent in nlp(use_case_diagram.description).ents if ent.label_ in ("PERSON", "ORG")]
    class_diagram_classes = [ent.text for ent in nlp(class_diagram.description).ents if ent.label_ in ("ORG", "PRODUCT")]

    for actor in use_case_actors:
        if actor not in class_diagram_classes:
            cross_errors['Cross-Diagram Consistency'].append(f"Actor '{actor}' in Use Case Diagram has no corresponding class in Class Diagram.")

    return {
        'use_case_errors': dict(use_case_errors),
        'class_diagram_errors': dict(class_diagram_errors),
        'cross_errors': dict(cross_errors),
    }