def interpret(local_var, context_vars):
    '''
    Finds the variable named 'local_var' and returns its value
    '''
    return context_vars['local_vars'][local_var]