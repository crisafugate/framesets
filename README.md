framesets 2.0

Introduction:

Framesets is an extension which provides a data construction based on the 
artificial intelligence concept of frames, created by Marvin Minsky. 

A frame has a number of slots, and each slot can contain a number of facets.
A facet is either a value, a method, a reference to another frame, and
a number of demons. Demons get automatically triggered depending on how
the slot is manipulated. The slots, the facetswhat the slots contain, and what
the facets contain are all user defined.

A frameset is a special type of frame which holds a set of frames. Moreover,
what is done to the frameset is done to each of its member frames.

Frame Commands:

fcomparef <frame> <frame> - compare slots of two frames
fcompares - compare two slots
fcopyf - make a copy of a frame
fcopys - make a copy of a slot in another frame
fcreated - create a demon facet
fcreatef <frame> - create a frame
fcreatefs <frameset> - create a frameset
fcreatem <frame> <slot> - create a method facet
fcreater <frame> <slot> - create a reference facet
fcreates <frame> <slot> - create a slot
fcreatev <frame> <slot> - create a value facet
fexecd <frame> <slot> <demon> - directly execute a demon
fexecm <frame> <slot> - execute a method
fexistd <frame> <slot> <demon> - determine if a demon facet exists
fexistf <frame> - determine if a frame exists
fexistm <frame> <slot> - determine if a method facet exists
fexistr <frame> <slot> - determine if a reference facet exists
fexistrx <frame> <slot> - (same as fexistr without a demon call)
fexists <frame> <slot> - determine if a slot exists
fexistv <frame> <slot> - determine if a value facet exists
ffilterf - filter a frame based on another frame
ffind <slot> - find all frames having a given value facet
ffindeq <slot> <value> - find all frames having a given value for a given value facet
ffindne <slot> <value> - find all frames not having a given value for a given value facet
fgetd <frame> <slot> <demon> - get the value of a demon facet
fgetm <frame> <slot> - get the value of a method facet
fgetr <frame> <slot> - get the value of a reference facet
fgetv <frame> <slot> - get the value of a value facet
flistf - get a list of existing frames
flistr <frame> - get a list of references in a frame
flists <frame> - get a list of slots for a frame
flistt <frame> <slot> - get a list of facet types for a slot
floadf <frame> - load a frame into memory
floadfs <frameset> - load a frameset into memory
fmergef - merge slots of a frame into another frame
fpathr - get a list of frames in a reference chain
fputd <frame> <slot> <demon> - put a value into a demon facet
fputm <frame> <slot> - put a value into a method facet
fputr <frame> <slot> - put a value into a reference facet
fputv <frame> <slot> - put a value into a value facet
fremoved <frame> <slot> <demon> - destroy a demon facet
fremovef <frame> - destroy a frame
fremovefs <frameset> - destroy a frameset
fremovem <frame> <slot> - destroy of method facet
fremover <frame> <slot> - destroy a reference facet
fremoves <frame> <slot> - destroy a slot
fremovev <frame> <slot> - destroy a value facet
fscreated <frameset> <slot> <demon> - create a demon facet in a frameset
fscreatem <frameset> <slot> - create a method facet in a frameset
fscreater <frameset> <slot> - create a reference facet in a frameset
fscreates <frameset> <slot> - create a slot in a frameset
fscreatev <frameset> <slot> - create a value facet in a frameset
fsexcludef <frameset> <frame> - exclude a frame from a frameset
fsgetr <frameset> <slot> - get a value from a reference facet in a frameset
fsincludef <frameset> <frame> - include a frame in a frameset
fslistf <frameset> - get list of frames in a a frameset
fsmemberf <frame> - get list of framesets in which a frame is a member
fsputr <frameset> <slot> - put a value in a reference facet in a frameset
fsremoved <frameset> <slot> <demon> - remove a demon facet from a frameset
fsremovem <frameset> <slot> - remove a method facet from a frameset
fsremover <frameset> <slot> - remove a reference facet from a frameset
fsremoves <frameset> <slot> - remove a slot from a frameset
fsremovev <frameset> <slot> - remove a value facet from a frameset
fstoref <frame> - store a frame on disk
fstorefs <frameset> - store a frameset on disk
fupdatef - synchronize a frame based on another frame

Demon Types:

Only frames and slots have user defined names. Methods, values, and 
references have builtin names which the user normally does not see.
Demons also have builtin type names, but the user determines which demon
types are associated with a given slot. Those type names are as follows:

ifcreatem - if fcreatem is executed
ifcreater - if fcreater is executed
ifcreatev - if fcreatev is executed
ifexecm - if fexecm is executed
ifexistm - if fexistm is executed
ifexistr - if fexistr is executed
ifexistv - if fexistv is executed
ifgetm - if fgetm is executed
ifgetr - if fgetr is executed
ifgetv - if fgetv is executed
ifputm - if fputm is executed
ifputr - if fputr is executed
ifputv - if fputv is executed
ifref - if command is executed on a reference
ifremovem - if fremovem is executed
ifremover - if fremover is executed
ifremovev - if fremovev is executed

Set Commands:

fcompress <list> - order and remove duplicates from a list
fdifference <list> <list> - return difference of two lists
fdisjunction <list> <list> - return disjunction of two lists
fequivalence <list> <list> - determine if two lists are equivalent
fintersection <list> <list> - return intersection of two lists
fmember <list> <value> - determine if a value is a member of a list
fremove <list> <value> - remove a value from a list
fsubset <list> <list> - determine if a list is a subset of another list
funion <list> <list> - return union of two lists
