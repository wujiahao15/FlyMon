from enum import Enum
from termios import PARMRK
from flymonlib.location import Location
from flymonlib.resource import Resource, ResourceType
from flymonlib.operation import *
from flymonlib.param import *
from flymonlib.flow_key import FlowKey

class AttributeType(Enum):
    """
    A enum class for flow attributes
    """
    Frequency = 1
    SingleKeyDistinct  = 2
    MultiKeyDistinct  = 2
    Existence = 3
    Max = 4 

def parse_param(param_str):
    """
    param string to param object.
    """
    param = None
    if param_str == 'pkt_size':
        param = Param(ParamType.PacketSize)
    elif param_str == 'timestamp':
        param = Param(ParamType.Timestamp)
    elif param_str == 'queue_size':
        param = Param(ParamType.QueueLen)
    elif 'hdr' in param_str:
        # Don't check the validity here.
        # Check it in Resource Manager when allocating resources.
        param = Param(ParamType.CompressedKey)
    else: # Must be a const.
        try:
            param = Param(ParamType.Const, int(param_str))
        except Exception as e:
            print(f"{e} when set a const param for the frequency attribute.")
            print(f"WARN: Set the param to Const 1.")
            param = Param(ParamType.Const, 1)
    return param


class FlowAttribute():
    """
    This is an abstrace class!
    Do not use it.
    TODO: use a standard ABC defination.
    """
    def __init__(self, param_str):
        """
        Exception:
         - No exception.
        """
        self._param1 = parse_param(param_str)

    def analyze(self, datas):
        """ Parse attribute data.
        """
        return 0 # To be implemented by concreate attribute class.
    
    @property
    def type(self):
        return None

    @property
    def memory_num(self):
        return None
    
    @property
    def param1(self):
        return self._param1

    @property
    def operation(self):
        return None

    @property
    def resource_list(self):
        resource_list = []
        if self._param1.type == ParamType.CompressedKey:
            resource_list.append(Resource(ResourceType.CompressedKey, self._param1))
        elif self._param1.type != ParamType.Const:
            resource_list.append(Resource(ResourceType.StdParam, self._param1))
        return resource_list

    def __str__(self):
        return "Unknown"
    

class Frequency(FlowAttribute):
    def __init__(self, param_str):
        """
        Implement the built-in algorithm: Count-Min Sketch.
        Exception:
         - No exception.
        """
        super(Frequency, self).__init__(param_str)
        self._param2 = Param(ParamType.Const, 65535)

    def analyze(self, datas):
        """ Parse attribute data.
            datas: is an list of data list.
        """
        return min(datas)

    @property
    def type(self):
        return AttributeType.Frequency

    @property
    def param2(self):
        return self._param2

    @property
    def memory_num(self):
        return 3

    @property
    def param_mapping(self):
        return { 
            # key : param
            # val : code
        }

    @property
    def operation(self):
        return OperationType.CondADD

    def __str__(self):
        return f"frequency({self.param1})"

class SleKeyDistinct(FlowAttribute):
    def __init__(self, param_str):
        """
        Implement the built-in algorithm: HyperLogLog
        Exception:
         - No exception.
        """
        super(Frequency, self).__init__(param_str)
        self._param2 = Param(ParamType.Const, 0) # No need

    @property
    def type(self):
        return AttributeType.SingleKeyDistinct

    @property
    def param2(self):
        return self._param2

    @property
    def memory_num(self):
        return 1

    @property
    def param_mapping(self):
        return { 
            # key : param
            # val : code
        }

    @property
    def operation(self):
        return OperationType.Max

    def __str__(self):
        return f"sk_distinct({self.param1})"

class MulKeyDistinct(FlowAttribute):
    def __init__(self, param_str):
        """
        Implement the built-in algorithm: BeauCoup.
        Exception:
         - No exception.
        """
        super(Frequency, self).__init__(param_str)
        self._param2 = Param(ParamType.Const, 0)

    @property
    def type(self):
        return AttributeType.MultiKeyDistinct

    @property
    def param2(self):
        return self._param2

    @property
    def memory_num(self):
        return 1

    @property
    def param_mapping(self):
        return { 
            # key : param
            # val : code
        }

    @property
    def operation(self):
        return OperationType.Max

    def __str__(self):
        return f"sk_distinct({self.param1})"


class Existence(FlowAttribute):
    def __init__(self, param_str):
        """
        Implement the built-in algorithm: BloomFilter.
        Exception:
         - No exception.
        """
        super(Frequency, self).__init__(param_str)
        self._param2 = Param(ParamType.Const, 0)

    @property
    def type(self):
        return AttributeType.MultiKeyDistinct

    @property
    def param2(self):
        return self._param2

    @property
    def memory_num(self):
        return 1

    @property
    def param_mapping(self):
        return { 
            # key : param
            # val : code
        }

    @property
    def operation(self):
        return OperationType.Max

    def __str__(self):
        return f"sk_distinct({self.param1})"


class Max(FlowAttribute):
    def __init__(self, param_str):
        """
        Implement the built-in algorithm: SuMax.
        Exception:
         - No exception.
        """
        super(Frequency, self).__init__(param_str)
        self._param2 = Param(ParamType.Const, 0)

    @property
    def type(self):
        return AttributeType.MultiKeyDistinct

    @property
    def param2(self):
        return self._param2

    @property
    def memory_num(self):
        return 1

    @property
    def param_mapping(self):
        return { 
            # key : param
            # val : code
        }

    @property
    def operation(self):
        return OperationType.Max

    def __str__(self):
        return f"sk_distinct({self.param1})"