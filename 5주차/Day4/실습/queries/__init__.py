from .q01 import QUESTION as Q01
from .q02 import QUESTION as Q02
from .q03 import QUESTION as Q03
from .q04 import QUESTION as Q04
from .q05 import QUESTION as Q05
from .q06 import QUESTION as Q06
from .q07 import QUESTION as Q07
from .q08 import QUESTION as Q08
from .q09 import QUESTION as Q09
from .q10 import QUESTION as Q10
from .q11 import QUESTION as Q11


QUESTIONS = {number: question for number, question in enumerate(
    (Q01, Q02, Q03, Q04, Q05, Q06, Q07, Q08, Q09, Q10, Q11), start=1
)}
