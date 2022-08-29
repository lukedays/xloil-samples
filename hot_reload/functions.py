import xloil as xlo
from debug_func import debug_func
import debugpy


@xlo.func
# @debug_func # Doesn't work together with xlo.func. The function doesn't get registered
def BreakpointTest():
    debugpy.debug_this_thread()
    return 3
