import os, sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.document import Document


if __name__ == '__main__':
    c = {
        "a": 1,
        "b": 2,
        "c": {
            "d": 1,
            "e": []
        }
    }
    
    doc = Document()
    doc.update(c)
    print(doc)
    for _k, _v in doc.items():
        print(_k, _v)