import pyprojroot
from decimal import Context

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
ROUNDING_LIM = 2
PREC_LIM = 8
decimal_context = Context(prec=PREC_LIM)
INIT_WORLD_LEN = ("10", "6", "3/4")
INIT_WORLD_LEN_M = "3.8862"
INIT_PX_LEN = "234"


