# Submitter: romeo1(Montague, Romeo)
# Partner  : jcapulet(Capulet, Juliet)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (raises AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (raise AssertionError) this classes raises AssertionError and prints its
      failure, along with a list of all annotations tried followed by the check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation():
    # set name to True for checking to occur
    checking_on  = True
  
    # self._checking_on must also be true for checking to occur
    def __init__(self,f):
        self._f = f
        self.checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
          # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        def check_sequence(type_given):
            assert isinstance(value, type_given), "AssertionError: '{}' failed annotation check(wrong type): value = {}\
                \n  was type {} ...should be type {}\n{}".format(param, value, type(value), type_given, check_history)
            if len(annot) == 1:
                for i,j in enumerate(value):
                    temp_history_1 = check_history + "{}[{}] check: {}\n".format(str(type_given)[8:-2], i, annot[0])
                    self.check(param, annot[0], j, temp_history_1)
            else:
                assert len(annot) == len(value), "AssertionError: '{}' failed annotation check(wrong number of elements): value = {}\
                    \n  annotation had {} elements{}\n{}".format(param, value, len(annot), annot, check_history)
                n = 0
                for i,j in zip(annot, value):
                    temp_history_2 = check_history + "{}[{}] check: {}\n".format(str(type_given)[8:-2], n, annot[n])
                    self.check(param, i, j, temp_history_2)
                    n += 1
                    
        def check_dict():
            assert isinstance(value, dict), "AssertionError: '{}' failed annotation check(wrong type): value = {}\
                \n  was type {} ...should be type dict\n{}".format(param, value, type_as_str(value), check_history)
            if len(annot) != 1:
                assert False, "AssertionError: {} annotation inconsistency: dict should have 1 item but had {}\
                    \n  annotation = {}\n{}".format(param, len(annot), annot, check_history)
            else:
                for a1,a2 in annot.items():
                    pass
                for v1,v2 in value.items():
                    temp_history_3 = check_history + "dict key check: {}\n".format(a1)
                    self.check(param, a1, v1, temp_history_3)
                    temp_history_4 = check_history + "dict value check: {}\n".format(a2)
                    self.check(param, a2, v2, temp_history_4)
                    
        def check_set(type_given):
            assert isinstance(value, type_given), "AssertionError: '{}' failed annotation check(wrong type): value = {}\
                \n  was type {} ...should be type {}\n{}".format(param, value, type_as_str(value), str(type_given), check_history)
            if len(annot) != 1:
                assert False, "AssertionError: {} annotation inconsistency: {} should have 1 item but had {}\
                \n  annotation = {}\n{}".format(param, str(type_given), len(annot), annot, check_history)
            else:
                for a, v in zip(annot, value):
                    temp_history_5 = check_history + "{} value check: {}\n".format(str(type_given), v)
                    self.check(param, a, v, check_history)
        
        def check_predicate():
            len_annot = len(annot.__code__.co_varnames)
            assert len_annot == 1, "AssertionError: {} annotation inconsistency: predicate should have 1 item but had {}\
                \n  annotation = {}\n{}".format(param, len_annot, annot, check_history)
            try:
                true = annot(value)
            except:
                assert False, "AssertionError: {} annotation predicate raised exception\
                \n predicate = {}\n{}".format(param, annot, check_history)
            else:
                assert true, "AssertionError: {} failed annotation check: value = {}\
                \n predicate = {}\n{}".format(param, value, annot, check_history)
                    
        # Decode annotation and check it              
        if annot == None:
            pass
        elif type(annot) is type:
            assert isinstance(value,annot), "AssertionError: '{}' failed annotation check(wrong type): value = '{}'\
                \n  was type {} ...should be type {}\n{}".format(param, value, type_as_str(value), str(annot)[8:-2], check_history)
        elif isinstance(annot, list):     
            check_sequence(list)
        elif isinstance(annot, tuple):     
            check_sequence(tuple)
        elif isinstance(annot, dict):
            check_dict()
        elif isinstance(annot, set):
            check_set(set)
        elif isinstance(annot, frozenset):
            check_set(frozenset)
        elif inspect.isfunction(annot):
            check_predicate()
        else:
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except AttributeError:
                assert False, "AssertionError: {} annotation undecipherable: {}\n{}".format(param, annot, check_history)
            except:
                assert False, "AssertionError: {} failed annotation check(wrong type): value = {}\
                    \n  was type {} ...should be type {}\n{}".format(param, value, type_as_str(value), str(annot)[8:-2], check_history)
                
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, in the order parameters occur in the function's header)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if param.name not in bound_f_signature.arguments:
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if not (self.checking_on and Check_Annotation.checking_on):
            return self._f(*args, **kargs)
        try:
            # Check the annotation for every parameter (if there is one)
            arguments = param_arg_bindings()
            annotations = self._f.__annotations__
            for param in arguments:
                if param in annotations:
                    self.check(param, annotations[param], arguments[param])
                    
            # Compute/remember the value of the decorated function
            answer = self._f(*args,**kargs)
            
            # If 'return' is in the annotation, check it
            if 'return' in annotations:
                arguments['_return'] = answer
                self.check('return', annotations['return'], answer)
            
            # Return the decorated answer
            return answer
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
                #print(l.rstrip())
            #print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    '''
    @Check_Annotation
    def f(x:[[int]]): pass
    
    f([[1,2],[3,4],[5,'a']])
    
    @Check_Annotation
    def f(x : {str : int}): pass
    f({'a':1,'b':2})
    
    def f(x:int)->str: pass 
    f = Check_Annotation(f)
    f(3)
    f('a')
    '''
    import driver
    driver.driver()
