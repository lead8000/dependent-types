from copy import deepcopy
from .dict import AttributeDict


class Contraints:
    """
    List of constraints coupling sets of `dependent attributes` with 
    their respective values.
    """
    def __init__(self, __contraints = None):
        if isinstance(__contraints, list):
            self.__contraints__ = deepcopy(__contraints)
        elif isinstance(__contraints, AttributeDict):
            self.__contraints__ = [__contraints]
        elif not __contraints:
            self.__contraints__ = []

    def __contains__(self, attr, value):
        for dict in self:
            if dict[attr].__contains__(value):
                return True
        return False

    def __getitem__(self, index):
        return self.__contraints__[index]

    def __or__(self, other):
        if isinstance(other, Contraints):
            union = Contraints(deepcopy(self.__contraints__) \
                            +  deepcopy(other.__contraints__))
            union_copy = deepcopy(union)

            for i in range(len(union_copy)):
                for j in range(i + 1, len(union_copy)):
                    if i == j: continue
                    
                    differ = 0
                    attr = None
                    for attr1, value1 in union_copy[i].__attribute_dict__.items():
                        for attr2, value2 in union_copy[j].__attribute_dict__.items():
                            if attr1 == attr2 and value1 != value2:
                                attr = attr1
                                differ += 1
                    
                    if differ == 1:
                        print(f'\n\n{union.__contraints__} -- {union_copy[i]}\n\n')

                        added = False                        
                        try:
                            union.__contraints__.remove(union_copy[i])
                            union.__contraints__.remove(union_copy[j])
                        except ValueError:
                            added = True

                        print(f'\n\nPINGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n{union.__contraints__}\n\n')

                        if not added:
                            dict12 = deepcopy(union_copy[i])
                            dict12[attr] = value1 | value2
                            union.__contraints__.append(AttributeDict(dict12.__attribute_dict__))

            return union

    def __and__(self, other):
        if isinstance(other, Contraints):
            list_ = []
            for dict1 in self:
                for dict2 in other:
                    list_.append(deepcopy(dict1) & deepcopy(dict2))
            return Contraints(list_)

    def __iter__(self):
        for dict in self.__contraints__:
            yield dict

    def __repr__(self) -> str:
        _str = ''
        first = True
        for contr in self.__contraints__:
            if first:
                first = False
            else:
                _str += f', '
            _str += f'{contr}'
        return f'Contraints[ {_str} ]'
    
    def __len__(self):
        return len(self.__contraints__)
