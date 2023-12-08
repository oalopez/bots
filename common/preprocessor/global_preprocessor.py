def pre_process(global_var):
    '''
    Finds the variable named 'global_var' and returns its value
    '''
    return globals()[global_var]