""" framesets.py

Description:
    This program is an extension to the python scripting language.  
    It provides a frame and frameset mechanism which can be used to 
    dynamically organize and perform operations on values and procedures.

Frame Structure:
    Both frames and framesets are dictionaries containing a set of slots,
    slots containing a set of facets, and various facets consisting of
    methods, values, references, and demons. Framesets also contain a
    set of frames.

    The dictionary key for slots is "<frame name>,slots".
    The dictionary key for a slot is "<slot name>,facets".
    The dictionary key for a method is "<slot name>,method".
    The dictionary key for a value is "<slot name>,value".
    The dictionary key for a reference is "<slot name>,ref".
    The dictionary key for a demon is "<slot name>,<demon name>".
    The dictionary key for a set of frames is "<frame name>,set".

    A references is a frame name which is used to access either
    a method or value in the same slot of a different frame.

    A demon is code which is automatically triggered by an action
    on either a method, value, or reference. Demons include
    ifcreatem, ifcreater, ifcreatev, ifexecm, ifexistm, ifexistr,
    ifexistv, ifgetm, ifgetr, ifgetv, ifputm, ifputr, ifputv,
    ifref (called when chaining), ifremovem, ifremover, ifremovev.

Functions:
    fcomparef  - compare slots of two frames
    fcompares  - compare two slots
    fcopyf     - make a copy of a frame
    fcopys     - make a copy of a slot in another frame
    fcreated   - create a demon facet
    fcreatef   - create a frame
    fcreatefs  - create a frameset
    fcreatem   - create a method facet
    fcreater   - create a reference facet
    fcreates   - create a slot
    fcreatev   - create a value facet
    fexecd     - directly execution a demon
    fexecm     - execute a method
    fexistd    - determine if a demon facet exists
    fexistf    - determine if a frame exists
    fexistm    - determine if a method facet exists
    fexistr    - determine if a reference facet exists
    fexistrx   - (same as fexistr without a demon call)
    fexists    - determine if a slot exists
    fexistv    - determine if a value facet exists
    ffilterf   - filter a frame based on another frame
    fgetd      - get the value of a demon facet
    fgetm      - get the value of a method facet
    fgetr      - get the value of a reference facet
    fgetv      - get the value of a value facet
    flistf     - get a list of existing frames
    flistr     - get a list of references in a frame
    flists     - get a list of slots for a frame
    flistt     - get a list of facet types for a slot
    floadf     - load a frame into memory
    floadfs    - load a frameset into memory
    fmergef    - merge slots of a frame into another frame
    fpathr     - get a list of frames in a reference chain
    fputd      - put a value into a demon facet
    fputm      - put a value into a method facet
    fputr      - put a value into a reference facet
    fputv      - put a value into a value facet
    fremoved   - destroy a demon facet
    fremovef   - destroy a frame
    fremovefs  - destroy a frameset
    fremovem   - destroy a method facet
    fremover   - destroy a reference facet
    fremoves   - destroy a slot
    fremovev   - destroy a value facet
    fscreated  - create a demon facet in a frameset
    fscreatem  - create a method facet in a frameset
    fscreater  - create a reference facet in a frameset
    fscreates  - create a slot in a frameset
    fscreatev  - create a value facet in a frameset
    fsexcludef - exclude a frame from a frameset
    fsgetr     - get a value from a reference facet in a frameset
    fsincludef - include a frame in a frameset
    fslistf    - get a list of frames in a frameset
    fsmemberf  - get list of framesets in which a frame is a member
    fsputr     - put a value in a reference facet in a frameset
    fsremoved  - remove a demon facet from a frameset
    fsremovem  - remove a method facet from a frameset
    fsremover  - remove a reference facet from a frameset
    fsremoves  - remove a slot from a frameset
    fsremovev  - remove a value facet from a frameset
    fstoref    - store a frame on disk
    fstorefs   - store a frameset on disk
    fupdatef   - synchronize a frame based on another frame

History:
    Written September 2, 1998 (wrote frames.tcl)
    changed: September 28, 1998 (added floadf and fstoref to frames)
    changed: November 25, 1998 (wrote framesets.tcl)
    changed: February 10, 1999 (added fupdatef to frames,
        added fsgetr, fsputr and fsmemberf to framesets)
    changed: April 16, 1999 (merged frames and framesets)
    changed: November 8, 1999 (added args to fputv,fputm,fputd)
    changed: August 13, 2001 (converted to Python)
    changed: December 19, 2015 (used Python sets instead of code converted 
        from Tcl)

Copyright (c) 2015 Cris A. Fugate

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""

__author__ = "Cris A. Fugate"
__version__ = "2.0"
__copyright__ "Copyright (c) 2015, Cris A. Fugate"
__license__ = "MIT"

import os
from sets import Set


def ffind(sname):
    """ Find all frames having a given value facet

    Parameters:
    sname - name of a slot
    
    calls flistf, fexistv
    returns a list of frames
    """

    listx = []
    for i in flistf():
        if fexistv(i, sname):
            listx.append(i)
    return listx


def ffindeq(sname, args):
    """ Find all frames having a given value for a given value facet

    Parameters:
    sname - name of a slot
    args - value to search for

    calls flistf, fexistv, fgetv
    returns list of frames
    """

    listx = []
    for i in flistf():
        if fexistv(i, sname):
            if fgetv(i, sname) == args:
                listx.append(i)
    return listx


def ffindne(sname, args):
    """ Find all frames not having a given value for a given value facet

    Parameters:
    sname - name of a slot
    args - value to search for

    calls flistf, fexistv, fgetv
    returns a list of frames
    """

    listx = []
    for i in flistf():
        if fexistv(i, sname):
            if fgetv(i, sname) != args:
                listx.append(i)
    return listx


# initialize fframes
fframes = Set()


def fexistf(fname):
    """ Determine if a frame exists.

    Parameters:
    fname - frame name

    returns True if frame exists, False otherwise
    """

    return fname in fframes


def fcreatef(fname):
    """ Create a frame and place it in fframes.

    Parameters:
    fname - frame name

    calls fexistf
    returns True if frame was created, False otherwise
    """

    if (not fexistf(fname)):
        fframes.add(fname)
        globals()[fname] = {fname + ',slots': Set()}
        return True
    else:
        return False


def fremovef(fname):
    """ Remove a frame from fframes and delete it.

    Parameters:
    fname - frame name

    calls fexistf
    returns True if frame was removed, False otherwise
    """

    if (fexistf(fname)):
        del globals()[fname]
        fframes.remove(fname)
        return True
    else:
        return False


def flistf():
    """ Return list of frames

    returns list of frames in fframes
    """

    return fframes


def fcopy(fname1, fname2):
    """ Create a new frame based on another frame

    Parameters:
    fname1 - name of first frame
    fname2 - name of second frame

    calls fexistf, fremovef
    returns True if fname1 was copied, False otherwise
    """

    if (fexistf(fname1)):
        fremovef(fname2)
        fframes.add(fname2)
        globals()[fname2] = globals()[fname1].copy()
        return True
    else:
        return False


def fcomparef(fname1, fname2):
    """ Determine if two frames are equivalent

    Parameters:
    fname1 - first frame name
    fname2 - second frame name

    calls fexistf
    returns True if the two frames are equivalent, False otherwise
    """

    if (fexistf(fname1) and fexistf(fname2)):
        x = globals()[fname1][fname1 + ',slots']
        y = globals()[fname2][fname2 + ',slots']
        if x == y:
            return True
        else:
            return False
    else:
        return False


def fmergef(fname1, fname2):
    """ Merge slots of one frame into another

    Parameters:
    fname1 - name of first frame
    fname2 - name of second frame

    calls fexistf
    returns True if the merge was possible, False otherwise
    """

    if (fexistf(fname1) and fexistf(fname2)):
        y = globals()[fname2][fname2 + ',slots']
        for i in globals()[fname1].keys():
            if i != fname1 + ',set' and i != fname1 + ',slots':
                sname = i.split(',')[0]
                if sname not in y:
                    globals()[fname2][i] = globals()[fname1][i]
                    globals()[fname2][fname2 + ',slots'].add(sname)
        return True
    else:
        return False


def floadf(fname):
    """ Load a frame into memory from a file.

    Parameters:
    fname - name of a frame

    calls fexistf
    returns True if successful, False otherwise
    """

    if (os.exists(fname) and not fexistf(fname)):
        fframes[fname] = {}
        fh = open(fname, "r")
        for fhbuf in fh:
            aname = fhbuf.split()[0]
            avalue = fhbuf.split()[1:]
            globals()[fname][aname] = avalue
        fh.close()
        return True
    else:
        return False


def fstoref(fname):
    """ Store a frame on disk

    Parameters:
    fname - name of a frame

    calls fexistf
    returns True if successful, False otherwise
    """

    if (fexistf(fname)):
        fh = open(fname, "w")
        for i in globals()[fname].keys():
            avalue = globals()[fname][i]
            fh.writeline(i + " " + avalue)
        fh.close()
        return True
    else:
        return False


def fupdatef(fname1, fname2):
    """ Update structure of a frame from another frame

    Parameters:
    fname1 - name of first frame
    fname2 - name of second frame

    calls fexistf
    returns True if update was possible, False otherwise
    """

    if (fexistf(fname1) and fexistf(fname2)):
        slist = globals()[fname1][fname1 + ',slots']
        globals()[fname2][fname2 + ',slots'] = slist
        for i in globals()[fname2].keys():
            if i != fname2 + ',set' and i != fname2 + ',slots':
                if i not in globals()[fname1].keys():
                    del globals()[fname2][i]

        for i in globals()[fname1].keys():
            if i != fname1 + ',set' and i != fname1 + ',slots':
                if i not in globals()[fname2].keys():
                    globals()[fname2][i] = globals()[fname1][i]
        return True
    else:
        return False


def ffilterf(fname1, fname2):
    """ Filter slots of a frame based on another frame

    Parameters:
    fname1 - name of first frame
    fname2 - name of second frame

    calls fexistf
    returns True if filter was possible, False otherwise
    """

    if (fexistf(fname1) and fexistf(fname2)):
        for i in globals()[fname2].keys():
            if i != fname2 + ',set' and i != fname2 + ',slots':
                if i in globals()[fname1].keys():
                    del globals()[fname2][i]
        return True
    else:
        return False


def fexists(fname, sname):
    """ Determine if a slot exists

    Parameters:
    fname - name of frame
    sname - name of slot

    calls fexistf
    returns True if slot exists, False otherwise
    """

    if (fexistf(fname)):
        return sname in globals()[fname][fname + ',slots']
    else:
        return False


def fcreates(fname, sname):
    """ Create a slot

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexistf
    returns True if successful, False otherwise
    """

    if (fexistf(fname)):
        if sname not in globals()[fname].keys():
            globals()[fname][fname + ',slots'].add(sname)
            globals()[fname][sname + ',facets'] = Set()
            return True
        else:
            return False
    else:
        return False


def fremoves(fname, sname):
    """ Remove a slot

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists
    returns True if slot was removed, False otherwise
    """

    if (fexists(fname, sname)):
        for i in globals()[fname].keys():
            sname2 = i.split(',')[0]
            if sname == sname2:
                del globals()[fname][i]
        globals()[fname][fname + ',slots'].remove(sname)
        return True
    else:
        return False


def flists(fname):
    """ List slots of a frame

    Parameters:
    fname - name of a frame

    calls fexistf
    returns a set of slots or an empty set
    """

    if (fexistf(fname)):
        x = globals()[fframes][fname + ',slots']
        return x
    else:
        return Set()


def fcopys(fname1, sname, fname2):
    """ Copy a slot into another frame

    Parameters:
    fname1 - name of frame from which to copy
    fname2 - name of frame to copy to
    sname - name of slot to copy

    calls fexists, fexistf
    returns True if successful, False otherwise
    """

    if fexists(fname, sname) and fexistf(fname2):
        globals()[fname2][fname2 + ',slots'].add(sname)
        for i in globals()[fname1].keys():
            sname2 = i.split(',')[0]
            if sname == sname2:
                globals()[fname2][i] = globals()[fname1][i]
        return True
    else:
        return False


def fcompares(fname1, sname, fname2):
    """ Compare a slot in two frames

    Parameters:
    fname1 - name of first frame
    fname2 - name of second frame
    sname - name of slot to compare

    calls fexists
    returns True if slots are equivalent, False otherwise
    """

    cmp = True
    if fexists(fname1, sname) and fexists(fname2, sname):
        x = globals()[fname1][sname + ',facets']
        y = globals()[fname2][sname + ',facets']
        if x == y:
            for i in globals()[fname1].keys():
                sname2 = i.split(',')[0]
                if sname == sname2:
                    x = globals()[fname1][i]
                    y = globals()[fname2][i]
                    if x != y:
                        cmp = False
            return cmp
        else:
            return False
    else:
        return False


def flistt(fname, sname):
    """ List of facet types in a slot

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists
    returns a set of facet types or an empty set
    """

    if fexists(fname, sname):
        return globals()[fname][sname + ',facets']
    else:
        return Set()


def fexistrx(fname, sname):
    """ Determine if a reference exists (internal)

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists
    returns True if a slot has a reference, False otherwise
    """

    if fexists(fname, sname):
        return 'ref' in globals()[fname][sname + ',facets']
    else:
        return False


def fexistr(fname, sname):
    """ Determine if a reference exists and execute associated demon

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexistrx
    returns True if reference exists, False otherwise
    """

    if fexistrx(fname, sname):
        if 'ifexistr' in globals()[fname][sname + ',facets']:
            exec globals()[fname][sname + ',ifexistr']
        return True
    else:
        return False


def fcreater(fname, sname):
    """ Create a reference facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists
    returns True if successful, False otherwise
    """

    if (fexists(fname, sname)):
        if 'ref' not in globals()[fname][sname + ',facets']:
            x = 'method' not in globals()[fname][sname + ',facets']
            y = 'value' not in globals()[fname][sname + ',facets']
            if not (x or y):
                globals()[fname][sname + ',facets'].add('ref')
                globals()[fname][sname + ',ref'] = ""
                if 'ifcreater' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifcreater']
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def fremover(fname, sname):
    """ Remove a reference facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexistrx
    returns True if successful, False otherwise
    """

    if fexistrx(fname, sname):
        if 'ifremover' in globals()[fname][sname + ',facets']:
            exec globals()[fname][sname + ',ifremover']
        del globals()[fname][sname + ',ref']
        globals()[fname][sname + ',facets'].remove('ref')
        return True
    else:
        return False


def fgetr(fname, sname):
    """ Get a value from a reference facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexistrx
    returns the value of a reference or an empty string
    """

    if fexistrx(fname, sname):
        if 'ifgetr' in globals()[fname][sname + ',facets']:
            exec globals()[fname][sname + ',ifgetr']
        return globals()[fname][sname + ',ref']
    else:
        return ""


def fputr(fname1, sname, fname2):
    """ Put a value in a reference facet

    Parameters:
    fname1 - name of frame containing the reference
    sname - name of slot containing the reference
    fname2 - name of frame to be referenced

    calls fexistrx
    returns True if successful, False otherwise
    """

    if fexistrx(fname1, sname):
        globals()[fname1][sname + ',ref'] = fname2
        if 'ifputr' in globals()[fname1][sname + ',facets']:
            exec globals()[fname1][sname + ',ifputr']
        return True
    else:
        return False


def flistr(fname):
    """ List of references in a frame

    Parameters:
    fname - name of a frame

    calls fexistf
    returns list of references or an empty list
    """

    flist = []
    if fexistf(fname):
        for i in globals()[fname].keys():
            if 'ref' in globals()[fname][i]:
                flist.append(i)
    return flist


def fpathr(fname, sname, plist=[]):
    """ Get a chain of references

    Parameters:
    fname - name of a frame
    sname - name of a slot
    plist - reference chain

    calls fexists, fpathr
    returns a list of references or an empty list
    """

    if fexists(fname, sname):
        if fname not in plist:
            plist.append(fname)
            if 'ref' in globals()[fname][sname + ',facets']:
                fname2 = globals()[fname][sname + ',ref']
                fpathr(fname2, sname, plist)
            else:
                return plist
        else:
            return plist
    else:
        return plist


def fexistm(fname, sname):
    """ Determine if a method facet exists

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fexistrx
    returns True if method is found, False otherwise
    """

    found = False
    if fexists(fname, sname):
        if fexistrx(fname, sname):
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifref']
            found = fexistm(fname2, sname)
        if 'method' in globals()[fname][sname + ',facets']:
            if 'ifexistm' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifexistm']
            found = 1
    return found


def fcreatem(fname, sname):
    """ Create a method facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fcreatem
    returns True if method created, False otherwise
    """

    created = False
    if fexists(fname, sname):
        if 'method' in globals()[fname][sname + ',facets'] or \
           'value' in globals()[fname][sname + ',facets']:
            created = False
        else:
            if 'ref' in globals()[fname][sname + ',facets']:
                fname2 = globals()[fname][sname + ',ref']
                if 'ifref' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifref']
                created = fcreatem(fname2, sname)
            else:
                globals()[fname][sname + ',method'] = ""
                globals()[fname][sname + ',facets'].add('method')
                if 'ifcreatem' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifcreatem']
                created = 1
    return created


def fremovem(fname, sname):
    """ Remove a method facet

    Parameters:
    fname - name of a frame
    sname -name of a slot

    calls fexists, fremovem
    returns True if method removed, False otherwise
    """

    removed = False
    if fexists(fname, sname):
        if 'ref' in globals()[fname][sname + ',facets']:
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ref']
            removed = fremovem(fname2, sname)
        else:
            if 'method' in globals()[fname][sname + ',facets']:
                if 'ifremovem' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifremovem']
                del globals()[fname][sname + ',method']
                globals()[fname][sname + ',facets'].remove('method')
                removed = 1
    return removed


def fexecm(fname, sname):
    """ Execute a method

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fexecm
    returns True if a method executed, False otherwise
    """

    executed = False
    if (fexists(fname, sname)):
        if 'ref' in globals()[fname][sname + ',facets']:
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',ifref']:
                exec globals()[fname][sname + ',ifref']
            executed = fexecm(fname2, sname)
        else:
            if 'method' in globals()[fname][sname + ',facets']:
                if 'ifexecm' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifexecm']
                exec globals()[fname][sname + ',method']
                executed = 1
    return executed


def fgetm(fname, sname):
    """ Get a value from a method facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fgetm
    returns the method found, empty string otherwise
    """

    pname = ""
    if fexists(fname, sname):
        if 'ref' in globals()[fname][sname + ',facets']:
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifref']
            pname = fgetm(fname2, sname)
        else:
            if 'method' in globals()[fname][sname + ',facets']:
                if 'ifgetm' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifgetm']
                    pname = globals()[fname][sname + ',method']
    return pname


def fputm(fname, sname, *args):
    """ Put a value in a method facet

    Parameters:
    fname - name of a frame
    sname - name of a slot
    args - code to put in a method facet

    calls fexists, fputm
    returns True if method placed, False otherwise
    """

    put = False
    if fexists(fname, sname):
        if 'ref' in globals()[fname][sname + ',facets']:
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifref']
            put = fputm(fname2, sname, args)
        else:
            if 'method' in globals()[fname][sname + ',facets']:
                if 'ifputm' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifputm']
                globals()[fname][sname + ',method'] = args
                put = True
    return put


def fexistv(fname, sname):
    """ Determine if a value facet exists

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fexistrx, fexistv
    returns True if value found, False otherwise
    """

    found = False
    if fexists(fname, sname):
        if fexistrx(fname, sname):
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifref']
            found = fexistv(fname2, sname)
        if 'value' in globals()[fname][sname + ',facets']:
            if 'ifexistv' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifexistv']
            found = True
    return found


def fcreatev(fname, sname):
    """ Create a value facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fcreatev
    returns True if value facet was created, False otherwise
    """

    created = False
    if fexists(fname, sname):
        if 'method' in globals()[fname][sname + ',facets'] or \
           'value' in globals()[fname][sname + ',facets']:
            pass
        else:
            if 'ref' in globals()[fname][sname + ',facets']:
                fname2 = globals()[fname][sname + ',ref']
                if 'ifref' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifref']
                created = fcreatev(fname2, sname)
            else:
                globals()[fname][sname + ',value'] = ""
                globals()[fname][sname + ',facets'].add('value')
                if 'ifcreatev' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifcreatev']
                created = 1
    return created


def fremovev(fname, sname):
    """ Remove a value facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fremovev
    returns True if value facet was removed, False otherwise
    """

    removed = False
    if fexists(fname, sname):
        if 'ref' in globals()[fname][sname + ',facets']:
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifref']
            removed = fremovev(fname2, sname)
        else:
            if 'value' in globals()[fname][sname + ',facets']:
                if 'ifremovev' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifremovev']
                del globals()[fname][sname + ',value']
                globals()[fname][sname + ',facets'].remove('value')
                removed = True
    return removed


def fgetv(fname, sname):
    """ Get a value from a value facet

    Parameters:
    fname - name of a frame
    sname - name of a slot

    calls fexists, fgetv
    returns the value from a value facet or None
    """

    pname = None
    if fexists(fname, sname):
        if 'ref' in globals()[fname][sname + ',facets']:
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifref']
            pname = fgetv(fname2, sname)
        else:
            if 'value' in globals()[fname][sname + ',facets']:
                if 'ifgetv' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifgetv']
                pname = globals()[fname][sname + ',value']
    return pname


def fputv(fname, sname, *args):
    """ Put a value in a value facet

    Parameters:
    fname - name of a frame
    sname - name of a slot
    args - data to put in value facet

    calls fexists, fputv
    returns True if data put in value facet, False otherwise
    """

    put = False
    if fexists(fname, sname):
        if 'ref' in globals()[fname][sname + ',facets']:
            fname2 = globals()[fname][sname + ',ref']
            if 'ifref' in globals()[fname][sname + ',facets']:
                exec globals()[fname][sname + ',ifref']
            put = fputv(fname2, sname, args)
        else:
            if 'value' in globals()[fname][sname + ',facets']:
                if 'ifputv' in globals()[fname][sname + ',facets']:
                    exec globals()[fname][sname + ',ifputv']
                globals()[fname][sname + ',value'] = args
                put = True
    return put


def fexistd(fname, sname, dname):
    """ Determine if a demon facet exists

    Parameters:
    fname - name of a frame
    sname - name of a slot
    dname - name of a demon

    calls fexists
    returns True if demon exists, False otherwise
    """

    if fexists(fname, sname):
        if dname in globals()[fname][sname + ',facets']:
            return True
        else:
            return False
    else:
        return False


def fcreated(fname, sname, dname):
    """ Create a demon facet

    Parameters:
    fname - name of a frame
    sname - name of a slot
    dname - name of a demon

    calls fexists
    """

    if fexists(fname, sname):
        if dname not in globals()[fname][sname + ',facets']:
            globals()[fname][sname + ',' + dname] = ""
            globals()[fname][sname + ',facets'].add(dname)
            return True
        else:
            return False
    else:
        return False


def fremoved(fname, sname, dname):
    """ Remove a demon facet

    Parameters:
    fname - name of a frame
    sname - name of a slot
    dname - name of a demon

    calls fexistd
    returns True if demon was removed, False otherwise
    """

    if fexistd(fname, sname, dname):
        del globals()[fname][sname + ',' + dname]
        globals()[fname][sname + ',facets'].remove(dname)
        return True
    else:
        return False


def fgetd(fname, sname, dname):
    """ Get a value from a demon facet

    Parameters:
    fname - name of a frame
    sname - name of a slot
    dname - name of a demon

    calls fexistd
    returns demon data or an empty string
    """

    if fexistd(fname, sname, dname):
        return globals()[fname][sname + ',' + dname]
    else:
        return ""

    
def fputd(fname, sname, dname, *args):
    """ Put a value in a demon facet

    Parameters:
    fname - name of a frame
    sname - name of a slot
    dname - name of a demon
    args - code to put in a demon facet

    calls fexistd
    returns True if successful, False otherwise
    """

    if fexistd(fname, sname, dname):
        globals()[fname][sname + ',' + dname] = args
        return True
    else:
        return False

    
def fexecd(fname, sname, dname):
    """ Directly execute a demon

    Parameters:
    fname - name of a frame
    sname - name of a slot
    dname - name of a demon

    calls fexistd
    returns True is demon was executed, False otherwise
    """

    if fexistd(fname, sname, dname):
        exec globals()[fname][sname + ',' + dname]
        return True
    else:
        return False


def fcreatefs(name):
    """ Create a frameset

    Parameters:
    name - name of a frameset

    calls fexistf
    """

    if not fexistf(name):
        fframes.add(name)
        globals()[name] = {name + ',set': Set()}
        globals()[name][name + ',slots'] = Set()
        return True
    else:
        return False


def fremovefs(name):
    """ Remove a frameset

    Parameters:
    name - name of a frame

    calls fremovef
    returns True if frameset was removed, False otherwise
    """

    return fremovef(name):


def fslistf(name):
    """ Return a list of frames in a frameset

    Parameters:
    name - name of a frameset

    calls fexistf
    returns a list of frames or an empty list
    """

    if 'set' in globals()[name]
        return globals()[name][name + ',set']
    else:
        return []


def floadfs(name):
    """ Load a frameset into memory

    Parameters:
    name - name of a frameset

    calls floadf, fslistf
    returns True if successful, False otherwise 
    """

    if floadf(name):
        s = fslistf(name)
        for i in s:
            floadf(i)
        return True
    else:
        return False


def fstorefs(name):
    """ Store a frameset on disk

    Parameters:
    name - name of a frameset

    calls fstoref, fslistf
    returns True if successful, False otherwise
    """

    if fstoref(name):
        s = fslistf(name)
        for i in s:
            fstoref(i)
        return True
    else:
        return False


def fsincludef(name, fname):
    """ Include a frame in a frameset

    Parameters:
    name - name of a frameset
    fname - name of a frame

    calls fexistf
    returns True if successful, False otherwise
    """

    if fexistf(name) and fexistf(fname):
        globals()[name][name + ',set'].add(fname)
        return True
    else:
        return False


def fsexcludef(name, fname):
    """ Exclude a frame from a frameset

    Parameters:
    name - name of a frameset
    fname - name of a frame

    calls fexistf
    returns True if successful, False otherwise
    """

    if fexistf(name):
        if fname in globals()[name][name + ',set']:
            globals()[name][name + ',set'].remove(fname)
            return True 
        else:
            return False
    else:
        return False


def fscreates(name, sname):
    """ Create a slot in a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fcreates, fslistf
    returns True if successful, False otherwise
    """

    if fcreates(name, sname):
        s = fslistf(name)
        for i in s:
            fcreates(i, sname)
        return True
    else:
        return False


def fsremoves(name, sname):
    """ Remove a slot from a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fremoves, fslistf
    returns True if successful, False otherwise
    """

    if fremoves(name, sname):
        s = fslistf(name)
        for i in s:
            fremoves(i, sname)
        return True
    else:
        return False


def fscreated(name, sname, dname):
    """ Create a demon facet in a frameset

    Parameters:
    calls fcreated, fslistf
    """
    
    if fcreated(name, sname, dname):
        s = fslistf(name)
        for i in s:
            fcreated(i, sname, dname)
        return True
    else:
        return False


def fsremoved(name, sname, dname):
    """ Remove a demon facet from a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot
    dname - name of a demon

    calls fremoved, fslistf
    returns True if successful, False otherwise
    """

    if fremoved(name, sname, dname):
        s = fslistf(name)
        for i in s:
            fremoved(i, sname, dname)
        return True
    else:
        return False


def fscreatem(name, sname):
    """ Create a method facet in a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fcreatem, fslistf
    returns True if successful, False otherwise
    """
    
    if fcreatem(name, sname):
        s = fslistf(name)
        for i in s:
            fcreatem(name, sname)
        return True
    else: 
        return False


def fsremovem(name, sname):
    """ Remove a method facet from a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fremovem, fslistf
    returns True if successful, False otherwise
    """

    if fremovem(name, sname):
        s = fslistf(name)
        for i in s:
            fremovem(i, sname)
        return True
    else:
        return False


def fscreater(name, sname):
    """ Create a reference facet in a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fcreater, fslistf
    returns True if successful, False otherwise
    """
    
    if fcreater(name, sname):
        s = fslistf(name)
        for i in s:
            fcreater(name, sname)
        return True
    else:
        return False


def fsremover(name, sname):
    """ Remove a reference facet from a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fremover, fslistf
    returns True if successful, False otherwise
    """

    if fremover(name, sname):
        s = fslistf(name)
        for i in s:
            fremover(i, sname)
        return True
    else:
        return False


def fscreatev(name, sname):
    """ Create a value facet in a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fcreatev, fslistf
    returns True is successful, False otherwise
    """

    if fcreatev(name, sname):
        s = fslistf(name)
        for i in s:
            fcreatev(i, sname)
        return True
    else:
        return False


def fsremovev(name, sname):
    """ Remove a value facet from a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fremovev, fslistf
    returns True if successful, False otherwise
    """

    if fremovev(name, sname):
        s = fslistf(name)
        for i in s:
            fremovev(i, sname)
        return True
    else:
        return False


def fsputr(name, sname, fname):
    """ Put a value in reference facet in a frameset 

    Parameters:
    name - name of a frameset
    sname - name of a slot
    fname - name of a frame

    calls fexistr, fputr, fslistf
    returns True if successful, False otherwise
    """

    if fexistr(name, sname):
        fputr(name, sname, fname)
        s = fslistf(name)
        for i in s:
            fputr(i, sname, fname)
        return True
    else:
        return False


def fsgetr(name, sname):
    """ Get a value from a reference facet in a frameset

    Parameters:
    name - name of a frameset
    sname - name of a slot

    calls fexistr, fgetr
    returns a reference or an empty string
    """

    if fexistr(name, sname):
        r = fgetr(name, sname)
        return r
    else: 
        return ""


def fsmemberf(fname):
    """ Get list of framesets in which a frame is a member

    Parameters:
    fname - name of a frame

    calls fexistf
    returns a list of framesets or an empty list
    """

    mlist = []
    if fexistf(fname):
        for i in flistf():
            for j in globals()[i].keys():
                ename = j.split(',')[1]
                if ename == 'set':
                    if fname in globals()[i][i + ',set']:
                        mlist.append(i)
        return mlist
    else:
        return []
