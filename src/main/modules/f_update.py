

def function(saas, *args):
    """Updates all channels referenced by its name in *args"""
    for channel_name in args:
        saas.channels[channel_name].update()
