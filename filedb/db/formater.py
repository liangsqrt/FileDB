class Formater(object):
    @staticmethod
    def format(format_dict, data_dict):
        for _k, _ in list(data_dict.items()):
            _f_v = format_dict.get(_k)
            if _f_v == 1:
                continue
            elif _f_v:
                target = Formater.format(format_dict.get(_k), data_dict.get(_k))
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
        "a":{"b":1, "c":0},
        "b": {
            "e":1,
            "f":1
        }
    }
    print(Formater.format(format_a, a))
    

            