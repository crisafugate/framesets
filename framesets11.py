######################################################################
#
# program name: framesets.py 1.1
#   programmer: Cris A. Fugate
# date written: September 2, 1998 (wrote frames.tcl)
#      changed: September 28, 1998 (added floadf and fstoref to frames)
#      changed: November 25, 1998 (wrote framesets.tcl)
#      changed: February 10, 1999 (added fupdatef to frames,
#               added fsgetr, fsputr and fsmemberf to framesets)
#      changed: April 16, 1999 (merged frames and framesets)
#      changed: November 8, 1999 (added args to fputv,fputm,fputd)
#      changed: August 13, 2001 (converted to Python)
#
#  description: This program is an extension to the python scripting
#               language.  It provides a frame and frameset
#               mechanism which can be used to dynamically organize
#               and perform operations on values and procedures.
#
# Copyright (c) 1999 Cris A. Fugate
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
######################################################################
#
#                              Variables
#
# aname                        array name
# args                         list of arguments
# avalue                       array value
# cmp                          comparison flag
# created                      create flag
# elema                        element of a list
# dname                        demon type
# elcnt                        count of list elements
# executed                     execute flag
# fframes                      list of frames
# {<fname>: {..}}                frame entry in fframes
#    {set: []}                 frames in a frameset
#    {<sname>: {..}}             facets in a slot
#       {<dtype>: ""}          demon facet
#       {ifcreatem: ""}        ifcreatem demon
#       {ifcreater: ""}        ifcreater demon
#       {ifcreatev: ""}        ifcreatev demon
#       {ifexecm: ""}          ifexecm demon
#       {ifexistm: ""}         ifexistm demon
#       {ifexistr: ""}         ifexistr demon
#       {ifexistv: ""}         ifexistv demon
#       {ifgetm: ""}           ifgetm demon
#       {ifgetr: ""}           ifgetr demon
#       {ifgetv: ""}           ifgetv demon
#       {ifputm: ""}           ifputm demon
#       {ifputr: ""}           ifputr demon
#       {ifputv: ""}           ifputv demon
#       {ifref: ""}            ifref demon
#       {ifremovem: ""}        ifremovem demon
#       {ifremover: ""}        ifremover demon
#       {ifremovev: ""}        ifremovev demon
#       {method: ""}           method facet
#       {ref: ""}              reference facet
#       {value: ..}            value facet
# fh                           file handle
# fhbuf                        file handle buffer
# flist                        list of references in a frame
# fname                        frame name
# fname1                       frame name
# fname2                       frame name
# found                        exist flag
# ftype                        facet type
# i                            loop variable
# j                            loop variable
# lista                        first list to be processed
# listb                        second list to be processed
# listx                        first temporary list
# listy                        second temporary list
# mlist                        list of framesets of which a frame
#                              is a member
# name                         frameset name
# plist                        list of frames in a reference chain
# pname                        procedure name
# put                          put flag
# r                            reference
# removed                      remove flag
# s                            list of frames in the frameset
# sname                        slot name
# sname2                       slot name
# x                            variable used in place of expression
# y                            variable used in place of expression
#
######################################################################
#
#                              Procedures
#
# fcomparef                    compare slots of two frames
# fcompares                    compare two slots
# fcopyf                       make a copy of a frame
# fcopys                       make a copy of a slot in another frame
# fcreated                     create a demon facet
# fcreatef                     create a frame
# fcreatefs                    create a frameset
# fcreatem                     create a method facet
# fcreater                     create a reference facet
# fcreates                     create a slot
# fcreatev                     create a value facet
# fexecd                       directly execution a demon
# fexecm                       execute a method
# fexistd                      determine if a demon facet exists
# fexistf                      determine if a frame exists
# fexistm                      determine if a method facet exists
# fexistr                      determine if a reference facet exists
# fexistrx                     (same as fexistr without a demon call)
# fexists                      determine if a slot exists
# fexistv                      determine if a value facet exists
# ffilterf                     filter a frame based on another frame
# fgetd                        get the value of a demon facet
# fgetm                        get the value of a method facet
# fgetr                        get the value of a reference facet
# fgetv                        get the value of a value facet
# flistf                       get a list of existing frames
# flistr                       get a list of references in a frame
# flists                       get a list of slots for a frame
# flistt                       get a list of facet types for a slot
# floadf                       load a frame into memory
# floadfs                      load a frameset into memory
# fmergef                      merge slots of a frame into another frame
# fpathr                       get a list of frames in a reference chain
# fputd                        put a value into a demon facet
# fputm                        put a value into a method facet
# fputr                        put a value into a reference facet
# fputv                        put a value into a value facet
# fremoved                     destroy a demon facet
# fremovef                     destroy a frame
# fremovefs                    destroy a frameset
# fremovem                     destroy a method facet
# fremover                     destroy a reference facet
# fremoves                     destroy a slot
# fremovev                     destroy a value facet
# fscreated                    create a demon facet in a frameset
# fscreatem                    create a method facet in a frameset
# fscreater                    create a reference facet in a frameset
# fscreates                    create a slot in a frameset
# fscreatev                    create a value facet in a frameset
# fsexcludef                   exclude a frame from a frameset
# fsgetr                       get a value from a reference facet
#                              in a frameset
# fsincludef                   include a frame in a frameset
# fslistf                      get a list of frames in a frameset
# fsmemberf                    get list of framesets in which
#                              a frame is a member
# fsputr                       put a value in a reference facet
#                              in a frameset
# fsremoved                    remove a demon facet from a frameset
# fsremovem                    remove a method facet from a frameset
# fsremover                    remove a reference facet from a frameset
# fsremoves                    remove a slot from a frameset
# fsremovev                    remove a value facet from a frameset
# fstoref                      store a frame on disk
# fstorefs                     store a frameset on disk
# fupdatef                     synchronize a frame based on another frame
# lcompress                    order and remove duplicates from a list
# lequivalence                 determine if two lists are equivalent
#

import os

def lcompress (lista):
   """ compress - order and remove duplicates from a list
   """
   listx = lista[:]
   listx.sort()
   listy = [listx[0]]
   elema = listy[0]
   for i in listx:
      if (elema != i):
         listy.append(i)
      elema = i
   return listy

def lequivalence (lista, listb):
   """ equivalence - determine if two lists are equivalent
       calls lcompress
   """
   listx = lista[:]
   listy = listb[:]
   listx = lcompress(listx)
   listy = lcompress(listy)
   if (listx == listy):
      return 1
   else:
      return 0

# initialize fframes
fframes = {}

def fexistf (fname):
   """ fexistf - determine if a frame exists
   """
   global fframes
   return fframes.has_key(fname)
   
def fcreatef (fname):
   """ fcreatef - create a frame
       requires that fname does not exist
       modifies fframes
       calls fexistf
   """
   global fframes
   if (not fexistf(fname)):
      fframes[fname] = {}
      return 1
   else:
      return 0

def fremovef (fname):
   """ fremovef - remove a frame
       requires that fname exists
       modifies fframes
       calls fexistf
   """
   global fframes
   if (fexistf(fname)):
      del fframes[fname]
      return 1
   else:
      return 0

def flistf ():
   """ flistf - return list of frames
   """
   global fframes
   return fframes.keys()

def fcopy (fname1, fname2):
   """ fcopyf - create a new frame based on another frame
       requires that fname1 exists
       modifies fframes
       calls fexistf, fremovef
   """
   global fframes
   if (fexistf(fname1)):
      fremovef(fname2)
      fframes[fname2]=fframes[fname1].deepcopy()
      return 1
   else:
      return 0

def fcomparef (fname1, fname2):
   """ fcomparef - determine if two frames are equivalent
       calls fexistf, lequivalence
   """
   global fframes
   if (fexistf(fname1) and fexistf(fname2)):
      x = fframes[fname1].keys()
      if ("set" in x):
         x.remove("set")
      y = fframes[fname2].keys()
      if ("set" in y):
         y.remove("set")
      return lequivalence(x, y)
   else: 
      return 0

def fmergef (fname1, fname2):
   """ fmergef - merge slots of one frame into another
       requires that fname1 and fname2 exist
       modifies fframes
       calls fexistf
   """
   global fframes
   if (fexistf(fname1) and fexistf(fname2)):
      lista = fframes[fname2].keys()
      for i in fframes[fname1].keys():
         if (i != "set"):
            if (i not in lista):
               x =  fframes[fname2]
               del fframes[fname2]
               x[i] = {}
               fframes[fname2] = x
      return 1
   else:
      return 0

def floadf (fname):
   """ floadf - load a frame into memory
       requires that fname exists on disk. but not in memory
       modifies fframes
       calls fexistf
   """
   global fframes
   if (os.exists(fname) and not fexistf(fname)):
      fframes[fname] = {}
      fh = open(fname, "r")
      while (1):
         fhbuf = fh.readline()
         if (fhbuf == ""):
            break
         aname = fhbuf.split()[0]
         avalue = fhbuf.split()[1:]
         fframes[fname][aname] = avalue
      fh.close()
      return 1
   else:
      return 0

def fstoref (fname):
   """ fstoref - store a frame on disk
       requires that fname exists
       calls fexistf
   """
   global fframes
   if (fexistf(fname)):
      fh = open(fname, "w")
      for i in fframes[fname].keys():
         avalue = fframes[fname][i]
         fh.writeline(i, avalue)
      fh.close()
      return 1
   else:
      return 0

def fupdatef (fname1, fname2):
   """ fupdatef - update structure of a frame from another frame
       requires that both frames exist
       modifies fframes
       calls fexistf
   """
   global fframes
   if (fexistf(fname1) and fexistf(fname2)):
      for i in fframes[fname2].keys():
         if (i != "set"):
            if (i not in fframes[fname1].keys()):
               del fframes[fname2][i]
      for i in fframes[fname1].keys():
         if (i != "set"):
            if (i not in fframes[fname2].keys()):
               fframes[fname2][i] = {}
      return 1
   else:
      return 0

def ffilterf (fname1, fname2):
   """ ffilterf - filter slots of a frame based on another frame
       requires that both frames exist
       modifies fframes
       calls fexistf
   """
   global fframes
   if (fexistf(fname1) and fexistf(fname2)):
      for i in fframes[fname2].keys():
         if (i != "set"):
            if (i not in fframes[fname1].keys()):
               del fframes[fname2][i]
      return 1
   else:
      return 0

def fexists (fname, sname):
   """ fexists - determine if a slot exists
       requires that fname exists
       calls fexistf
   """
   global fframes
   if (fexistf(fname)):
      return fframes[fname].has_key(sname)
   else:
      return 0

def fcreates (fname, sname):
   """ fcreates - create a slot
       requires that fname exists
       modifies fframes
       calls fexistf
   """
   global fframes
   if (fexistf(fname)):
      if (not fframes[fname].has_key(sname)):
         fframes[fname][sname] = {}
         return 1
      else:
         return 0
   else:
      return 0

def fremoves (fname, sname):
   """ fremoves - remove a slot
       requires that fname and sname exists
       modifies fframes
       calls fexists
   """
   global fframes
   if (fexists(fname, sname)):
      del fframes[fname][sname]
      return 1
   else:
      return 0

def flists (fname):
   """ flists - list slots of a frame
       requires that fname exists
       calls fexistf
   """
   global fframes
   if (fexistf(fname)):
      x = fframes[fname].keys()
      x.remove("set")
      return x
   else:
      return []

def fcopys (fname1, sname, fname2):
   """ fcopys - copy a slot into another frame
       requires that both frames exist
       modifies fframes
       calls fexists, fexistf
   """
   global fframes
   if (fexists(fname, sname) and fexistf(fname2)):
      if (not fexists(fname2, sname)):
         fframes[fname2][sname] = {}
      fframes[fname2][sname] = fframes[fname1][sname].deepcopy()
      return 1
   else:
      return 0

def fcompares (fname1, sname, fname2):
   """ fcompares - compare a slot in two frames
       requires that sname exists in both frames
       calls fexists
   """
   global fframes
   cmp = 1
   if (fexists(fname1, sname) and fexists(fname2, sname)):
      x = fframes[fname1][sname].keys()
      y = fframes[fname2][sname].keys()
      if (lequivalence(x, y)):
         for i in fframes[fname1][sname].keys():
            x = fframes[fname1][sname][i]
            y = fframes[fname2][sname][i]
            if (x != y):
               cmp = 0
         return cmp
      else:
         return 0
   else:
      return 0

def flistt (fname, sname):
   """ flistt - list of facet types in a slot
       requires that the facet exists
       calls fexists
   """
   global fframes
   if (fexists(fname, sname)):
      return fframes[fname][sname]
   else:
      return []

def fexistrx (fname, sname):
   """ fexistrx - determine if a reference exists (internal)
       requires that the slot exists
       calls fexists
   """
   global fframes
   if (fexists(fname, sname)):
      return fframes[fname][sname].has_key("ref")
   else:
      return 0

def fexistr (fname, sname):
   """ fexistr - determine if a reference exists
       requires that the slot exists
       calls fexistrx
   """
   global fframes
   if (fexistrx(fname,sname)):
      if (fframes[fname][sname].has_key("ifexistr")):
         exec fframes[fname][sname]["ifexistr"]
      return 1
   else:
      return 0

def fcreater (fname, sname):
   """ fcreater - create a reference facet
       requires that the slot exists
       modifies fframes
       calls fexists
   """
   global fframes
   if (fexists(fname, sname)):
      if ("ref" not in fframes[fname][sname].keys()):
         x = fframes[fname][sname].has_key("method")
         y = fframes[fname][sname].has_key("value")
         if (not (x or y)):
            fframes[fname][sname]["ref"] = ""
            if (fframes[fname][sname].has_key("ifcreater")):
               exec fframes[fname][sname]["ifcreater"]
            return 1
         else:
            return 0
      else:
         return 0
   else:
      return 0

def fremover(fname, sname):
   """ fremover - remove a reference facet
       requires that the reference facet exists
       modifies fframes
       calls fexistrx
   """
   global fframes
   if (fexistrx(fname, sname)):
      if (fframes[fname][sname].has_key("ifremover")):
         exec fframes[fname][sname]["ifremover"]
      del fframes[fname][sname]["ref"]
      return 1
   else:
      return 0

def fgetr (fname, sname):
   """ fgetr - get a value from a reference facet
       requires that the reference facet exists
       calls fexistrx
   """
   global fframes
   if (fexistrx(fname, sname)):
      if (fframes[fname][sname].has_key("ifgetr")):
         exec fframes[fname][sname]["ifgetr"]
      return fframes[fname][sname]["ref"]
   else:
      return ""

def fputr (fname1, sname, fname2):
   """ fputr - put a value in a reference facet
       requires that the reference facet exists
       modifies fframes
       calls fexistrx
   """
   global fframes
   if (fexistrx(fname1, sname)):
      fframes[fname1][sname]["ref"] = fname2
      if (fframes[fname1][sname].has_key("ifputr")):
         exec fframes[fname1][sname]["ifputr"]
      return 1
   else:
      return 0

def flistr (fname):
   """ flistr - list of references in a frame
       requires that the frame exists
       calls fexistf
   """
   global fframes
   flist = []
   if (fexistf(fname)):
      for i in fframes[fname].keys():
         if (fframes[fname][i].has_key("ref")):
            flist.append(i)
   return flist

def fpathr (fname, sname, plist=[]):
   """ fpathr - return chain of references
       requires that the slot exists
       calls fexists, fpathr
   """
   global fframes
   if (fexists(fname, sname)):
      if (fname not in plist):
         plist.append(fname)
         if (fframes[fname][sname].has_key("ref")):
            fname2 = fframes[fname][sname]["ref"]
            fpathr(fname2, sname, plist)
         else:
            return plist
      else:
         return plist
   else:
      return plist

def fexistm (fname, sname):
   """ fexistm - determine if a method facet exists
       requires that the slot exists
       calls fexists, fexistrx
   """
   global fframes
   found = 0
   if (fexists(fname, sname)):
      if (fexistrx(fname, sname)):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         found = fexistm(fname2, sname)
      if (fframes[fname][sname].has_key("method")):
         if (fframes[fname][sname].has_key("ifexistm")):
            exec fframes[fname][sname]["ifexistm"]
         found = 1
   return found

def fcreatem (fname, sname):
   """ fcreatem - create a method facet
       requires that the slot exists
       modifies fframes
       calls fexists, fcreatem
   """
   global fframes
   created = 0
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("method") or
          fframes[fname][sname].has_key("value")):
         created = 0
      else:
         if (fframes[fname][sname].has_key("ref")):
            fname2 = fframes[fname][sname]["ref"]
            if (fframes[fname][sname].has_key("ifref")):
               exec fframes[fname][sname]["ifref"]
            created = fcreatem(fname2, sname)
         else:
            fframes[fname][sname]["method"] = ""
            if (fframes[fname][sname].has_key("ifcreatem")):
               exec fframes[fname][sname]["ifcreatem"]
            created = 1
   return created

def fremovem (fname, sname):
   """ fremovem - remove a method facet
       requires that the slot exists
       modifies fframes
       calls fexists, fremovem
   """
   global fframes
   removed = 0
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("ref")):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         removed = fremovem(fname2, sname)
      else:
         if (fframes[fname][sname].has_key("method")):
            if (fframes[fname][sname].has_key("ifremovem")):
               exec fframes[fname][sname]["ifremovem"]
            del fframes[fname][sname]["method"]
            removed = 1
   return removed
   
def fexecm (fname, sname):
   """ fexecm - execute a method
       requires that the slot exists
       calls fexists, fexecm
   """
   global fframes
   executed = 0
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("ref")):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         executed = fexecm(fname2, sname)
      else:
         if (fframes[fname][sname].has_key("method")):
            if (fframes[fname][sname].has_key("ifexecm")):
               exec fframes[fname][sname]["ifexecm"]
            exec fframes[fname][sname]["method"]
            executed = 1
   return executed

def fgetm (fname, sname):
   """ fgetm - get a value from a method facet
       requires that the slot exists
       calls fexists, fgetm
   """
   global fframes
   pname = ""
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("ref")):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         pname = fgetm(fname2, sname)
      else:
         if (fframes[fname][sname].has_key("method")):
            if (fframes[fname][sname].has_key("ifgetm")):
               exec fframes[fname][sname]["ifgetm"]
            pname = fframes[fname][sname]["method"]
   return pname

def fputm (fname, sname, *args):
   """ fputm - put a value in a method facet
       requires that the slot exists
       modifies fframes
       calls fexists, fputm
   """
   global fframes
   put = 0
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("ref")):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         put = fputm(fname2, sname, args)
      else:
         if (fframes[fname][sname].has_key("method")):
            if (fframes[fname][sname].has_key("ifputm")):
               exec fframes[fname][sname]["ifputm"]
            fframes[fname][sname]["method"] = args
            put = 1
   return put

def fexistv(fname, sname):
   """ fexistv - determine if a value facet exists
       requires that the slot exists
       calls fexists, fexistrx, fexistv 
   """
   global fframes
   found = 0
   if (fexists(fname, sname)):
      if (fexistrx(fname, sname)):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         found = fexistv(fname2, sname)
      if (fframes[fname][sname].has_key("value")):
         if (fframes[fname][sname].has_key("ifexistv")):
            exec fframes[fname][sname]["ifexistv"]
         found = 1
   return found

def fcreatev(fname, sname):
   """ fcreatev - create a value facet
       requires that the slot exists
       modifies fframes
       calls fexists, fcreatev
   """
   global fframes
   created = 0
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("method") or
         fframes[fname][sname].has_key("value")):
         created = 0
      else:
         if (fframes[fname][sname].has_key("ref")):
            fname2 = fframes[fname][sname]["ref"]
            if (fframes[fname][sname].has_key("ifref")):
               exec fframes[fname][sname]["ifref"]
            created = fcreatev(fname2, sname)
         else:
            fframes[fname][sname]["value"] = ""
            if (fframes[fname][sname].has_key("ifcreatev")):
               exec fframes[fname][sname]["ifcreatev"]
            created = 1
   return created   

def fremovev(fname, sname):
   """ fremovev - remove a value facet
       requires that the slot and value facet exists
       modifies fframes
       calls fexists, fremovev
   """
   global fframes
   removed = 0
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("ref")):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         removed = fremovev(fname2, sname)
      else:
         if (fframes[fname][sname].has_key("value")):
            if (fframes[fname][sname].has_key("ifremovev")):
               exec fframes[fname][sname]["ifremovev"]
            del fframes[fname][sname]["value"]
            removed = 1
   return removed

def fgetv (fname, sname):
   """ fgetv - get a value from a value facet
       requires that the slot exists
       calls fexists, fgetv
   """
   global fframes
   pname = ""
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("ref")):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         pname = fgetv(fname2, sname)
      else:
         if (fframes[fname][sname].has_key("value")):
            if (fframes[fname][sname].has_key("ifgetv")):
               exec fframes[fname][sname]["ifgetv"]
            pname = fframes[fname][sname]["value"]
   return pname

def fputv (fname, sname, *args):
   """ fputv - put a value in a value facet
       requires that the slot exists
       modifies fframes
       calls fexists, fputv
   """
   global fframes
   put = 0
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key("ref")):
         fname2 = fframes[fname][sname]["ref"]
         if (fframes[fname][sname].has_key("ifref")):
            exec fframes[fname][sname]["ifref"]
         put = fputv(fname2, sname, args)
      else:
         if (fframes[fname][sname].has_key("value")):
            if (fframes[fname][sname].has_key("ifputv")):
               exec fframes[fname][sname]["ifputv"]
            fframes[fname][sname]["value"] = args
            put = 1
   return put

def fexistd (fname, sname, dname):
   """ fexistd - determine if a demon facet exists
       requires that the slot exists
       calls fexists
   """
   global fframes
   if (fexists(fname, sname)):
      if (fframes[fname][sname].has_key(dname)):
         return 1
      else:
         return 0
   else:
      return 0
      
def fcreated (fname, sname, dname):
   """ fcreated - create a demon facet
       requires that the slot exists
       modifies fframes
       calls fexists
   """
   global fframes
   if (fexists(fname, sname)):
      if (dname not in fframes[fname][sname].keys()):
         fframes[fname][sname][dname] = ""
         return 1
      else:
         return 0
   else:
      return 0

def fremoved (fname, sname, dname):
   """ fremoved - remove a demon facet
       requires that the demon facet exists
       modifies fframes
       calls fexistd
   """
   global fframes
   if (fexistd(fname, sname, dname)):
      del fframes[fname][sname][dname]
      return 1
   else:
      return 0

def fgetd (fname, sname, dname):
   """ fgetd - get a value from a demon facet
       requires that the demon facet exists
       calls fexistd
   """
   global fframes
   if (fexistd(fname, sname, dname)):
      return fframes[fname][sname][dname]
   else: 
      return ""

def fputd (fname, sname, dname, *args):
   """ fputd - put a value in a demon facet
       requires that the demon facet exists
       modifies fframes
       calls fexistd
   """
   global fframes
   if (fexistd(fname, sname, dname)):
      fframes[fname][sname][dname] = args
      return 1
   else:
      return 0

def fexecd (fname, sname, dname):
   """ fexecd - directly execute a demon
       requires that the demon facet exists
       calls fexistd
   """
   global fframes
   if (fexistd(fname, sname, dname)):
      exec fframes[fname][sname][dname]
      return 1
   else:
      return 0

def fcreatefs (name):
   """ fcreatefs - create a frameset
       requires that the frameset does not exist
       modifies fframes
       calls fexistf
   """
   global fframes
   if (not fexistf(name)):
      fframes[name] = {}
      fframes[name]["set"] = []
      return 1
   else:
      return 0

def fremovefs (name):
   """ fremovefs - remove a frameset
       requires that the frameset exists
       modifies fframes
       calls fremovef
   """
   if (fremovef(name)):
      return 1
   else:
      return 0

def fslistf (name):
   """ return a list of frames in a frameset
       requires that the frameset exists
       calls fexistf
   """
   global fframes
   if (fexistf(name) and fframes[name].has_key("set")):
      return fframes[name]["set"]
   else:
      return []
          
def floadfs (name):
   """ floadfs - load a frameset into memory
       requires that the frameset exists on disk
       modifies fframes
       calls floadf, fslistf
   """
   if (floadf(name)):
      s = fslistf(name)
      for i in s:
         floadf(i)
      return 1
   else:
      return 0

def fstorefs (name):
   """ fstorefs - store a frameset on disk
       requires that the frameset exists
       calls fstoref, fslistf
   """
   if (fstoref(name)):
      s = fslistf(name)
      for i in s:
         fstoref(i)
      return 1
   else:
      return 0

def fsincludef (name, fname):
   """ fsincludef - include a frame in a frameset
       requires that the frame and frameset exist
       modifies fframes
       calls fexistf
   """
   global fframes
   if (fexistf(name) and fexistf(fname)):
      fframes[name]["set"].append(fname)
      return 1
   else:
      return 0

def fsexcludef (name, fname):
   """ fsexcludef - exclude a frame from a frameset
       requires that the frameset exists
       modifies fframes
       calls fexistf
   """
   global fframes
   if (fexistf(name)):
      if (fname in fframes[name]["set"]):
         fframes[name]["set"].remove(fname)
         return 1
      else:
         return 0
   else:
      return 0

def fscreates (name, sname):
   """ fscreates - create a slot in a frameset
       requires that the frameset exists
       modifies fframes
       calls fcreates, fslistf
   """
   if (fcreates(name, sname)):
      s = fslistf(name)
      for i in s:
         fcreates(i, sname)
      return 1
   else:
      return 0

def fsremoves (name, sname):
   """ fsremoves - remove a slot from a frameset
       requires that the frameset exists
       modifies fframes
       calls fremoves, fslistf
   """
   if (fremoves(name, sname)):
      s = fslistf(name)
      for i in s:
         fremoves(i, sname)
      return 1
   else:
      return 0

def fscreated (name, sname, dname):
   """ fscreated - create a demon facet in a frameset
       requires that the frameset exists
       modifies fframes
       calls fcreated, fslistf
   """
   if (fcreated(name, sname, dname)):
      s = fslistf(name)
      for i in s:
         fcreated(i, sname, dname)
      return 1
   else:
      return 0

def fsremoved (name, sname, dname):
   """ fsremoved - remove a demon facet from a frameset
       requires that the frameset exists
       modifies fframes
       calls fremoved, fslistf
   """
   if (fremoved(name, sname, dname)):
      s = fslistf(name)
      for i in s:
         fremoved(i, sname, dname)
      return 1
   else:
      return 0

def fscreatem (name, sname):
   """ fscreatem - create a method facet in a frameset
       requires that the frameset exists
       modifies fframes
       calls fcreatem, fslistf
   """
   if (fcreatem(name, sname)):
      s = fslistf(name)
      for i in s:
         fcreatem(name, sname)
      return 1
   else: 
      return 0

def fsremovem (name, sname):
   """ fsremovem - remove a method facet from a frameset
       requires that the frameset exists
       modifies fframes
       calls fremovem, fslistf
   """
   if (fremovem(name, sname)):
      s = fslistf(name)
      for i in s:
         fremovem(i, sname)
      return 1
   else:
      return 0

def fscreater (name, sname):
   """ fscreater - create a reference facet in a frameset
       requires that the frameset exists
       modifies fframes
       calls fcreater, fslistf
   """
   if (fcreater(name, sname)):
      s = fslistf(name)
      for i in s:
         fcreater(name, sname)
      return 1
   else:
      return 0

def fsremover (name, sname):
   """ fsremover - remove a reference facet from a frameset
       requires that the frameset exists
       modifies fframes
       calls fremover, fslistf
   """
   if (fremover(name, sname)):
      s = fslistf(name)
      for i in s:
         fremover(i, sname)
      return 1
   else:
      return 0

def fscreatev (name, sname):
   """ fscreatev - create a value facet in a frameset
       requires that the frameset exists
       modifies fframes
       calls fcreatev, fslistf
   """
   if (fcreatev(name, sname)):
      s = fslistf(name)
      for i in s:
         fcreatev(i, sname)
      return 1
   else:
      return 0

def fsremovev (name, sname):
   """ fsremovev - remove a value facet from a frameset
       requires that the frameset exists
       modifies fframes
       calls fremovev, fslistf
   """
   if (fremovev(name, sname)):
      s = fslistf(name)
      for i in s:
         fremovev(i, sname)
      return 1
   else:
      return 0

def fsputr (name, sname, fname):
   """ fsputr - put a value in reference facet in a frameset 
       requires that the reference exists
       modifies fframes
       calls fexistr, fputr, fslistf
   """
   if (fexistr(name, sname)):
      fputr(name, sname, fname)
      s = fslistf(name)
      for i in s:
         fputr(i, sname, fname)
      return 1
   else:
      return 0

def fsgetr (name, sname):
   """ fsgetr - get a value from a reference facet in a frameset
       requires that the reference exists
       calls fexistr, fgetr
   """
   if (fexistr(name, sname)):
      r = fgetr(name, sname)
      return r
   else: 
      return ""

def fsmemberf (name):
   """ fsmemberf - get list of framesets in which a frame is a member
       requires that the frame exists
       calls fexistf
   """
   mlist = []
   if (fexistf(name)):
      for i in flistf():
         if (fframes[i].has_key("set")):
            if (name in fframes[i]["set"]):
               mlist.append(i)
      return mlist
   else:
      return []
