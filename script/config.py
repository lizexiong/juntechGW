class global_var:
    name = []
 
def set_name(name):
    global_var.name.append(name)
def get_name():
    return global_var.name
