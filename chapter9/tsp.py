from typing import Dict, List, Iterable, Tuple
from itertools import permutations


vt_distances: Dict[str,Dict[str,int]] = {
    "Rutland":{
        'Burlington':67,
        'White River Junction':46,
        'Bennington':55,
        'Brattleboro':75
    },
    "Burlington":{
        'Rutland':67,
        'White River Junction':91,
        'Bennington':122,
        'Brattleboro':153
    },
    "White River Junction":{
        'Rutland':46,
        'Burlington':91,
        'Bennigton':98,
        'Brattleboro':65
    },
    "Bennington":{
        'Rutland':55,
        'Burlington':122,
        'White River Junction':98,
        'Brattleboro':40
    },
    "Brattleboro":{
        'Rutland':75,
        'Burlington':153,
        'White River Junction':65,
        'Bennington':40

    }
}