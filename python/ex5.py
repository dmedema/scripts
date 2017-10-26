my_name = 'Denise Medema'
my_age = 39 # not a lie
my_height = 74 # inches
my_weight = 150 # lbs
my_eyes = 'Green'
my_teeth = 'White'
my_hair = 'Blonde'

print "Let's talk about %s." % my_name
print "She's %d inches tall." % my_height
print "She's %d centimeters tall." % (my_height * 2.54)
print "She's %d pounds heavy." % my_weight
print "She's %d kilos heavy." % (my_weight * 0.453592)
print "Actually that's not too heavy."
print "She's got %s eyes and %s hair." % (my_eyes, my_hair)
print "Her teeth are usually %s depending on the coffee." % my_teeth

# this line is tricky, try to get it exactly right
print "If I add %d, %d, and %d I get %d." % (
    my_age, my_height, my_weight, my_age + my_height + my_weight)
