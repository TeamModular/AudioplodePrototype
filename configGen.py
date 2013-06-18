import ConfigParser as c
config = c.RawConfigParser()
config.add_section("Sound")
config.set("Sound","sfLocation","/usr/share/sounds/sf2/FluidR3_GM.sf2")
with open("config.cfg",'wb') as configfile:
    config.write(configfile)
