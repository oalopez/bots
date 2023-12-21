def interpret(global_var, context_vars):
    '''
    Finds the variable named 'global_var' and returns its value
    '''
    return context_vars['global_vars'][global_var]