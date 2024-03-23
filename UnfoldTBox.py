from py4j.java_gateway import JavaGateway
gateway = JavaGateway()
elFactory = gateway.getELFactory()
formatter = gateway.getSimpleDLFormatter()

allowed_concept_types = ["ConceptName", "ExistentialRoleRestriction", "ConceptConjunction"]

def unfold_tbox(concept, tbox, max_depth, depth_count=0):

    complex_concept = elFactory.getConceptName(concept)
    depth_count += 1
    if depth_count >= max_depth:
        return complex_concept

    for axiom in tbox:
        if axiom.getClass().getSimpleName() == "GeneralConceptInclusion":
            if concept == formatter.format(
                    axiom.lhs()) and axiom.rhs().getClass().getSimpleName() in allowed_concept_types:
                rhs = unfold(axiom.rhs(), tbox, max_depth, depth_count)
                complex_concept = elFactory.getConjunction(complex_concept, rhs)
        elif axiom.getClass().getSimpleName() == "EquivalenceAxiom":
            if concept == formatter.format(axiom.getConcepts()[0]) and axiom.getConcepts()[
                1].getClass().getSimpleName() in allowed_concept_types:
                rhs = unfold(axiom.getConcepts()[1], tbox, max_depth, depth_count)
                complex_concept = elFactory.getConjunction(complex_concept, rhs)
            if concept == formatter.format(axiom.getConcepts()[1]) and axiom.getConcepts()[
                0].getClass().getSimpleName() in allowed_concept_types:
                lhs = unfold(axiom.getConcepts()[1], tbox, max_depth, depth_count)
                complex_concept = elFactory.getConjunction(complex_concept, lhs)

    return complex_concept


def unfold(concept, tbox, max_depth, depth_count):

    conceptType = concept.getClass().getSimpleName()

    if conceptType == "ConceptName":
        return concept
    else:
        if conceptType == "ConceptConjunction":
            conjuncts = concept.getConjuncts()
            conjunct1 = unfold(conjuncts[0], tbox, max_depth, depth_count)
            conjunct2 = unfold(conjuncts[1], tbox, max_depth, depth_count)
            return elFactory.getConjunction(conjunct1, conjunct2)
        if conceptType == "ExistentialRoleRestriction":
            role = concept.role()
            filler = unfold_tbox(formatter.format(concept.filler()), tbox, max_depth, depth_count)
            return elFactory.getExistentialRoleRestriction(role, filler)