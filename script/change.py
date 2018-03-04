from script import config
 
# import config



def change_name(args):
	config.set_name(args)
	print(config.get_name())

# change_name('is fukc')