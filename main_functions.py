# Modules for master functions.

def showModules(moduleName):
    '''
    Function to print names of modules

    Parameter:
        modules (str): name of module
    '''
    print("List of available functions:")
    for i, func in enumerate(moduleName.function_list):
        print("   {}: {}".format(i+1, func.__name__))