def tableauMethod(c):
    idx = 0
    idx_list = [idx]
    ABox_dict = {"x0": [c]}
    aBox_add(c, idx, idx_list, ABox_dict)
    return ABox_dict


def aBox_add(concept, idx, idx_list, ABox_dict):
    if concept.getClass().getSimpleName() == "ConceptConjunction":
        conjuncts = concept.getConjuncts()
        key_idx = "x" + str(idx)
        if conjuncts[0] not in ABox_dict[key_idx] or conjuncts[1] not in ABox_dict[key_idx]:
            ABox_dict[key_idx] = ABox_dict.get(key_idx, []) + [conjuncts[0]]
            aBox_add(conjuncts[0], idx, idx_list, ABox_dict)
            ABox_dict[key_idx] = ABox_dict.get(key_idx, []) + [conjuncts[1]]
            aBox_add(conjuncts[1], idx, idx_list, ABox_dict)


    elif concept.getClass().getSimpleName() == "ExistentialRoleRestriction":
        check = True
        for key, value_list in ABox_dict.items():
            for value in value_list:
                if (concept.role() == value) and (concept.filler() == ABox_dict[key[1]]):
                    check = False
        if check:
            max_index = max(idx_list)
            role_idx = f"x{str(idx)}", f"x{str(max(idx_list) + 1)}"
            filler_idx = "x" + str(max_index+1)
            ABox_dict[role_idx] = ABox_dict.get(role_idx, []) + [concept.role()]
            ABox_dict[filler_idx] = ABox_dict.get(filler_idx, []) + [concept.filler()]
            idx_list.append(max_index+1)
            aBox_add(concept.filler(), max_index+1, idx_list, ABox_dict)