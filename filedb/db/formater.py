class Formater(object):
    format = {}
    def __init__(self, format_dict: dict):
        assert isinstance(format_dict, dict), "format_dict must be dict like"
        self.format = format_dict
    
    def generate_result(self, input_data):
        result  = {}
        if 1 not in self.format.values():
            for _k,_v in self.format.items():
                if _v == 0:
                    continue
                result[_k] = input_data.get(_k)
        else:
            pass
    
    @staticmethod
    def generate_dict_path(format_dict):
        for _k, _v in format_dict.items():
            if(format_dict[_k]):
                pass


def formater(format_dict, data_dict):
    for _k, _ in list(data_dict.items()):
        _f_v = format_dict.get(_k)
        if _f_v == 1:
            continue
        elif _f_v:
            target = formater(format_dict.get(_k), data_dict.get(_k))
            data_dict[_k] = target
        else:
            del data_dict[_k]
            
    return data_dict



if __name__ == '__main__':
    a = {
        "a": {
            "b": 1,
            "c": 2,
            "d": {
                "e": 1,
                "f": 2
            }
        },
        "b": {
            "e":"d",
            "f":2
        }
    }
    
    format_a = {
        "a":1,
        "b": {
            "e":1
        }
    }
    print(formater(format_a, a))
    

            