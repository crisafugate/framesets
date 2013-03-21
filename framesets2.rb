######################################################################
#
# program name: framesets.rb 2.0
# programmer: Cris A. Fugate
# date written: March 12, 2013 (converted from Tcl)
# description: This program is an extension which provides a frame
# and frameset mechanism which can be used to dynamically organize
# and perform operations on values and procedures.
#
######################################################################
# 
# Variables
#
# args - list of arguments
# cmp - comparison flag
# created - create flag
# dname - demon type
# doc - JSON document
# executed - execute flag
# fbuf - file buffer
# ffile - output file
# fframes - list of frames
# file - file object
# flist - list of references in a frame
# fname - frame name
# fname1 - frame name
# fname2 - frame name
# found - exist flag
# ftype - facet type
# i - loop variable
# line - line from file
# listx - temporary list
# mlist - list of framesets of which a frame is a member
# name - frameset name
# plist - list of frames in a reference chain
# put - put flag
# r - reference
# removed - remove flag
# s - list of frames in the frameset
# sarray - slot array
# slots - frame slot element
# sname - slot name
# x - variable used in place of expression
# y - variable used in place of expression
# <fname>[<ename>] - used in operations involving many elements
# <fname>[<fname>,set] - frames in a frameset
# <fname>[<fname>,slots] - slots in a frame
# <fname>[<sname>,<ftype>] - demon facet
# <fname>[<sname>,facets] - facets in a slot
# <fname>[<sname>,ifcreatem] - ifcreatem demon
# <fname>[<sname>,ifcreater] - ifcreater demon
# <fname>[<sname>,ifcreatev] - ifcreatev demon
# <fname>[<sname>,ifexecm] - ifexecm demon
# <fname>[<sname>,ifexistm] - ifexistm demon
# <fname>[<sname>,ifexistr] - ifexistr demon
# <fname>[<sname>,ifexistv] - ifexistv demon
# <fname>[<sname>,ifgetm] - ifgetm demon
# <fname>[<sname>,ifgetr] - ifgetr demon
# <fname>[<sname>,ifgetv] - ifgetv demon
# <fname>[<sname>,ifputm] - ifputm demon
# <fname>[<sname>,ifputr] - ifputr demon
# <fname>[<sname>,ifputv] - ifputv demon
# <fname>[<sname>,ifref] - ifref demon
# <fname>[<sname>,ifremovem] - ifremovem deamon
# <fname>[<sname>,ifremover] - ifremover demon
# <fname>[<sname>,ifremovev] - ifremovev demon
# <fname>[<sname>,method] - method facet
# <fname>[<sname>,ref] - reference facet
# <fname>[<sname>,value] - value facet
#
######################################################################
#
# Procedures
#
# fcomparef - compare slots of two frames
# fcompares - compare two slots
# fcopyf - make a copy of a frame
# fcopys - make a copy of a slot in another frame
# fcreated - create a demon facet
# fcreatef - create a frame
# fcreatefs - create a frameset
# fcreatem - create a method facet
# fcreater - create a referemce facet
# fcreatev - create a value facet
# fcreates - create a slot
# fcreatev - create a value facet
# fexecd - directly execute a demon
# fexecm - execute a method
# fexistf - determine if a demon facet exists
# fexistm - determine if a method facet exists
# fexistr - determine if a reference exists
# fexistrx - (same as fexistr without a demon call)
# fexists - determine if a slot exists
# fexistv - determine if a value facet exists
# ffilterf - filter a frame based on another frame
# ffind - find all frames having a given value facet
# ffindeq - find all frames having a given value for a given value facet
# ffindne - file all frames not having a given value for a given value facet
# fgetd - get the value of a demon facet
# fgetm - get the value of a method facet
# fgetr - get the value of a reference facet
# fgetv - get the value of a value facet
# flistf - get a list of existing frames
# flistr - get a list of references in a frame
# flists - get a list of slots for a frame
# flistt - get a list of facet types for a slot
# floadf - load a frame into memory
# floadfs - load a frameset into memory
# fmergef - merge slots of a frame into another frame
# fpathr - get a list of frames in a reference chain
# fputd - put a value into a demon facet
# fputm - put a value into a method facet
# fputr - put a value into a reference facet
# fputv - put a value into a value facet
# fremoved - destroy a demon facet
# fremovef - destroy a frame
# fremovefs - destroy a frameset
# fremovem - destroy a method facet
# fremover - destroy a reference facet
# fremoves - destroy a slot
# fremovev - destroy a value facet
# fscreated - create a demon facet in a frameset
# fscreatem - create a method facet in a frameset
# fscreater - create a reference facet in a frameset
# fscreates - create a slot in a frameset
# fscreatev - create a value facet in a frameset
# fsexcludef - exclude a frame from a frameset
# fsgetr - get a value from a reference facet in a frameset
# fsincludef - include a frame in a frameset
# fslistf - get a list of frames in a frameset
# fsmemberf - get a list of framesets in which a frame is a member
# fsputr - put a value in a reference facet in a frameset
# fsremoved - remove a demon facet from a frameset
# fsremovem - remove a method facet from a frameset
# fsremover - remove a reference facet from a frameset
# fsremoves - remove a slot from a frameset
# fsremovev - remove a value facet from a frameset
# fstoref - store a frame on disk
# fstorefs - store a frameset on disk
# fupdatef - synchronize a frame based on another frame
#

require "set"
require "json"

# initialize frames
fframes = Set.new

# 
# ffind - find all frames having a given value facet
#
def ffind(sname)
  listx = []
  flistf().each do |i|
    if fexistv i, sname
      listx.push i
    end
  end
  return listx
end

#
# ffindeq - find all frames having a given value for a given value facet
# 
def ffindeq(sname, args)
  listx = []
  flistf().each do |i|
    if fexistv i, sname
      if (fgetv i sname) == args
        listx.push i
      end
    end
  end
  return listx
end

#
# ffindne - find all frames not having a given value for a given value facet
#
def ffindne(sname, args)
  listx = []
  flistf().each do |i|
    if fexistv i, sname
      if (fgetv i sname) != args
        listx.push i
      end
    end
  end
  return listx
end

#
# fexistf - determine if a frame exists
#
def fexistf(fname)
  return $fframes.include? fname
end

#
# fcreatef - create a frame
# requires that fname{} does not exist
# modifies fframes, fname{fname,slots}
#
def fcreatef(fname)
  if not $fframes.include? fname
    $fframes.add fname
    eval "$#{fname} = {'#{fname},slots' => Set.new}"
    return true
  else
    return false
  end
end

#
# fremovef - remove a frame
# requires that fname{} exists
# modifies fframes,fname{}
#
def fremovef(fname)
if $fframes.include? fname
    eval "$#{fname} = nil"
    $fframes.delete fname
    return true
  else
    return false
  end
end

#
# flistf - return list of frames
#
def flistf
  return $fframes.to_a
end

# 
# fcopyf - create a new frame based on another frame
# requires that fname1{} exists
# modifies fframes,fname2
#
def fcopy(fname1, fname2)
  if fexists fname1
    fremovef fname2
    $fframes.add fname2
    eval "$#{fname2} = {}"
    eval "$#{fname2} = $#{fname2}.merge $#{fname1}"
    return true
  else 
    return falise
  end
end

#
# fcomparef - determine if two frames are equivalent
# requires that fname1{} and fname2{} exist
#
def fcomparef(fname1, fname2)
  if fexistf fname1 and fexistf fname2
    x = eval "$#{fname1}['#{fname1},slots']"
    y = eval "$#{fname2}['#{fname2},slots']"
    if x == y
      return true
    else
      return false
    end
  else
    return false
  end
end

#
# fmergef - merge slots of one frame into another frame
# requires that fname1{} and fname2{} exist
# modifies fname2{}
#
def fmergef (fname1, fname2)
  if fexistf fname1 and fexistf fname2
    y = eval "$#{fname2}['#{fname2},slots']"
    (eval "$#{fname1}.keys").each do |i|
      if i != "#{fname1},set" && i != "#{fname1},slots"
        sname = i.scan(/^\w+/)
        if y.include? sname
          eval "$#{fname2}[i] = $#{fname1}[i]"
          eval "$#{fname2}['#{fname2},slots'].add sname"
        end
      end
    end
    return true
  else
    return false
  end
end

#
# floadf - load a frame into memory
# requires that fname[] exists on disk, but not in memory
#
def floadf(fname)
  if File.exist? fname && not fexistf fname
    $fframes.add fname
    fbuf = ""
    File.open(fname, "r") do |file|
      while line = file.gets
        fbuf << line
      end
    end
    doc = JSON.parse(fbuf)
    slots = "#{fname},slots"
    sarray = doc[slots]
    doc[slots] = Set.new(sarray)
    doc[slots].each do |slot|
      sarray = doc["#{slot},facets"]
      doc["#{slot},facets"] = Set.new(sarray)
    end
    eval "${fname} = doc"
    return true
  else
    return false
  end
end
    
#
# fstoref - store a frame on disk
# requires that fname[] exists
#
def fstoref(fname)
  if fexistf fname
    doc = eval "$fname"
    slots = "#{fname},slots"
    sarray = doc[slots].to_a
    doc[slots] = sarray
    doc[slots].each do |slot|
      sarray = doc["#{slot},facets"].to_a
      doc["#{slot},facets"] = sarray
    end
    fbuf = JSON.generate(doc)
    ffile = File.open(fname, "w")
    ffile.puts fbuf
    ffile.close
    return true
  else
    return false
  end
end
   
#
# fupdatef - update structure of a frame from another frame
# requires that both frames exist
# modifies frame2[]
#
def fupdatef(fname1 fname2)
  if fexistf fname1 && fexistf fname2
    eval "$#{fname2}['#{fname2},slots'] = ${fname1}['#{fname1},slots']"
    (eval "$#{frame2}").each do |i|
      if not i.equal? "#{fname2},set" && not i.equal? "#{fname2},slots"
        if not (eval "$#{fname1}").key?(i)
          eval "$#{fname2}".delete(i)
        end
      end
    end
    (eval "$#{fname1}").each do |i|
      if not i.equal? "#{fname1},set" && not i.equal? "#{fname1},slots"
        if not (eval "$#{fname2}").key?(i)
          eval "$#{fname2}[i] = $#{fname1}[i]"
        end
      end
    end
    return true
  else
    return false
  end
end

#
# ffilterf - filter slots of a frame based on another frame
# requires that both frames exist
# modifies frame2[]
#
def ffilterf(fname1 fname2)
  if fexistf fname1 && fexistf fname2
    (eval "$#{fname2}").each do |i|
      if not i.equal? "#{fname2},set" && not i.equal? "#{fname2},slots"
        if not (eval "$#{fname1}").key?(i)
          eval "$#{fname2}".delete(i)
        end
      end
    end
    return true
  else
    return false
  end
end

#
# fexists - determine if a slot exists
# requires that fname[] exists
#
def fexists(fname sname)
  if fexistf fname
    if (eval "$#{fname}['#{fname},slots'].include?(sname)")
      return true
    else
      return false
    end
  else
    return false
  end
end
    
#
# fcreates - create a slot
# requires that fname[] exists
# modifies fname[fname,slot], fname[sname,facets]
#
def fcreates(fname sname)
  if fexistf fname
    if not eval "$#{fname}['#{fname},slots'].member? sname"
      eval "${fname}['#{fname},slots'].add sname"
      eval "${fname}['#{sname},facets'] = Set.new"
      return true
    else 
      return false
    end
  else
    return false
  end
end

#
# fremoves - remove a slot
# requires that fname[sname,facets] exists
# modifies fname[fname,slots], fname[sname,*]
#
def fremoves(fname, sname)
  if fexists fname, sname
    eval "$#{fname}.delete_if {|key,val| sname.eql? key.scan(/^\w+/)}"
    eval "$#{fname}['#{fname},slots'].delete sname"
    return true
  else
    return false
  end
end

#
# flists - list slots of a frame
# requires that fname[] exists
#
def flists(fname)
  if fexistf fname
    return eval "$#{fname}['#{fname},slots'].to_a"
  else
    return []
  end
end

#
# fcopys - copy a slot into another frame
# requires that fname1[] and fname2[] exist
# modifies fname2[sname,*]
#
def fcopys(fname1, sname, fname2)
  if (fexists fname1, sname) and (fexists fname2, sname)
    # if slot does not exist in fname2 then add it
    if not eval "$#{fname2}['#{fname2},slots'].include? sname"
      eval "$#{fname2}['#{fname2},slots'].add sname"
    end
    (eval "$#{fname1}").each do |i|
      if sname.eql?(i.scan(/^\w+/)) then eval "$#{fname2}[i] = ${fname1}[i]" end
    end
    return true
  else
    return false
  end
end
 
#
# fcompares - compare a slot in two frames
# requires that fname1[sname,facets] and fname2[sname,facets] exist
#
def fcompares(fname1, sname, fname2)
  cmp = true
  if (fexists fname1, sname) and (fexists fname2, sname)
    x = eval "$#{fname1}['#{sname},facets']"
    y = eval "$#{fname2}['#{sname},facets']"
    if x == y
      (eval "$#{fname1}").each do |i|
        if sname.eql? i.scan(/^\w+/)
          x = eval "$#{fname1}[i]"
          y = eval "$#{fname2}[i]"
          if x != y
            cmp = false
          end
        end
      end
      return cmp
    else 
      return false
    end
  else
    reuturn false
  end
end

#
# flistt - list of facet types in a slot
# requires that fname[sname,facets] exists
#
def flistt(fname,sname)
  if fexists fname, sname
    return eval "$#{fname}['#{sname},facets'].to_a"
  else
    return []
  end
end

#
# fexistrx - determine if a reference facet exists (internal)
# requires that fname[sname,facets] exists
#
def fexistrx(fname, sname)
  if fexists fname, sname
    if eval "$#{fname}['#{sname},facets'].include? 'ref'"
      return true
    else
      return false
    end
  else
    return false
  end
end

#
# fexistr - determine if a reference facet exists
# requires that fname[sname,facets] exists
# calls ifexistr demon
#
def fexistr(fname,sname)
  if fexistrx fname, sname
    if eval "$#{fname}['#{sname},facets'].include? 'ifexistr'" 
      eval "eval $#{fname}['#{sname},ifexistr']"
    end
    return true
  else
    return false
  end
end

#
# fcreater - create a reference facet
# requires that fname[sname,facets] exists
# modifies fname[sname,facets], fname[sname,ref]
# calls ifcreater demon
#
def fcreater(fname, sname)
  if fexists fname, sname
    if eval "$#{fname}['#{sname},facets'].include? 'ref'"
      x = eval "$#{fname}['#{sname},facets'].include? 'method'"
      y = eval "$#{fname}['#{sname},facets'].include? 'value'"
      if not (x || y)
        eval "$#{fname}['#{sname},facets'].add 'ref'"
        eval "$#{fname}['#{sname},ref'] = ''"
        if eval "$#{fname}['#{sname},facets'].include? 'ifcreater'"
          eval "eval $#{fname}['#{sname},ifcreater']"
        end
        return true
      else
        return false
      end
    else
      return false
    end
  else
    return false
  end
end

#
# fremover - remove a reference facet
# requires that fname[sname,ref] exists
# modifies fname[sname,facets], fname[sname,ref]
# calls ifremover demon
#
def fremover(fname, sname)
  if fexistrx fname, sname
    if eval "$#{fname}['#{sname},facets'].include? 'ifremover'"
      eval "eval $#{fname}['#{sname},ifremover']"
    end
    eval "${fname}.delete('#{sname},ref')"
    eval "${fname}['#{sname},facets'].delete('ref')"
    return true
  else
    return false
  end
end

#
# fgetr - get a value from a reference facet
# requires that fname[sname,ref] exists
# calls ifgetr demon
#
def fgetr(fname, sname)
  if fexistrx fname, sname
    if eval "$#{fname}['#{sname},facets'].include? 'ifgetr'"
      eval "eval $#{fname}['#{sname},ifgetr']"
    end
    return eval "$#{fname}['#{sname},ref']"
  else
    return ""
  end
end

#
# fputr - put a value in a reference facet
# requires that fname[sname,ref] exists
# modifies fname[sname,ref]
# calls ifputr demon
#
def fputr(fname1, sname, fname2)
  if fexistrx fname1, sname
    eval "$#{fname1}['#{sname},ref'] = fname2"
    if eval "$#{fname1}['#{sname},facets'].include? 'ifputr'"
      eval "eval $#{fname1}['#{sname},ifputr']"
    end
    return true
  else
    return false
  end
end

#
# flistr - list of references in a frame
# requires that fname[] exists
# 
def flistr fname
  flist = []
  if fexistr fname
    eval "$#{fname}.each" do |i|
      sname,ftype = i.split ","
      if ftype.eq "ref"
        flist.push sname
      end      
    end
  end
  return flist
end

#
# fpathr - return chain of references
# requires that fname[sname,facets] exists
#
def fpathr(fname,sname,plist=[])
  if fexists fname, sname
    if not plist.include? fname
      plist.push fname
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        fpathr fname2,sname,plist
      else
        return plist
      end
    else
      return plist
    end
  else
    return plist
  end
end

#
# fexistm - determine if a method facet exists
# requires that fname[sname,facets] exists
# calls ifref and ifexistm demons
#
def fexistm(fname, sname)
  found = false
  if fexists fname, sname
    if fexistrx fname, sname
      fname2 = eval "$#{fname}['#{sname},ref']"
      if eval "$#{fname}['#{sname},ref'].include? 'ifref'"
        eval "eval $#{fname}['#{sname},ifref']"
      end
      found = fexistm(fname2, sname)
    end
    if eval "$#{fname}['#{sname},facets'].include? 'method'"
      if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
        eval "eval $#{fname}['#{sname},ifexistm']"
      end
      found = true
    end
  end
  return found
end

#
# fcreatem - create a method facet
# requires that fname[sname,facets] exists
# modifies fname[sname,facets], fname[sname,method] where fname is
#          the original or referenced frame
# calls ifref and ifcreatem demons
#
def fcreatem(fname, sname)
  created = false
  if fexists fname, sname
    if (eval "$#{fname}['#{sname},facets'].include? 'method'" ||
      eval "$#{fname}['#{sname},facets'].include? 'value'")
      created = false
    else
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
          eval "eval $#{fname}['#{sname},ifref']"
        end
        created = fcreatem(fname2, sname)
      else
        eval "$#{fname}['#{sname},method'] = ''"
        eval "$#{fname}['#{sname},facets'].add 'method'"
        if eval "$#{fname}['#{sname},facets'].include? 'ifcreatem'"
          eval "eval $#{fname}['#{sname},ifcreatem']"
        end
        created = true
      end
    end
  end
  return created
end

#
# fremovem - remove a method facet
# requires that fname[sname,facets] exists
# modifies fname[sname,facets], fname[sname,method] where fname is
#          the original or referenced frame
# calls ifref and ifremovem demons
#
def fremovem(fname, sname)
  removed = false
  if fexists fname, sname
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
          eval "eval $#{fname}['#{sname},ifref']"
        end
        removed = fremovem(fname2, sname)
      else
          if eval "$#{fname}['#{sname},facets'].include? 'method'"
            if eval "$#{fname}['#{sname},facets'].include? 'ifremovem'"
              eval "eval $#{fname}['#{sname},ifremovem']"
            end
            eval "$#{fname}.delete('#{sname},method')"
            eval "$#{fname}['#{sname},facets'].delete 'method'"
            removed = true
          end
      end
  end
  return removed
end

#
# fexecm - execute a method
# requires that fname[sname,facets] exists
# calls ifref and ifexecm demons
#
def fexecm(fname,sname)
  executed = false
  if fexists fname, sname
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
          eval "eval $#{fname}['#{sname},ifref'"
        end
        executed = fexecm(fname2,sname)
      else
        if eval "$#{fname}['#{sname},facets'].include? 'method'"
          if eval "$#{fname}['#{sname},facets'].include? 'ifexecm'"
            eval "eval $#{fname}['#{sname},ifexecm']"
          end
          eval "eval $#{fname}['#{sname},method']"
          executed = true
        end
      end
  end
  return executed
end

#
# fgetm - get a value from a method facet
# requires that fname[sname,facets] exists
# calls ifref and ifgetm demons
#
def fgetm(fname,sname)
  pname = ""
  if fexists fname, sname
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
          eval "eval $#{fname}['#{sname},ifref']"
        end
        pname = fgetm(fname2,sname)
      else
        if eval "$#{fname}['#{sname},facets'].include? 'method'"
          if eval "$#{fname}['#{sname},facets'].include? 'ifgetm'"
            eval "eval $#{fname}['#{sname},ifgetm']"
          end
          fname = eval "$#{fname}['#{sname},method']"
        end
      end
  end
  return pname
end

#
# fputm - put a value in a method facet
# requires that fname[sname,facets] exists
# modifies fname[sname,method] where fname is the original or
#          referenced frame
# calls ifref and ifputm demons
#
def fputm(fname, sname, args)
  put = false
  if fexists fname, sname
    if eval "$#{fname}['#{sname},facets'].include? 'ref'"
      fname2 = eval "$#{fname}['#{sname},ref']"
      if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
        eval "eval $#{fname}['#{sname},ifref']"
      end
      put = fputm(fname2,sname,args)
    else
      if eval "$#{fname}['#{sname},facets'].include? 'method'"
        if eval "$#{fname}['#{sname},ref'].include? 'ifputm'"
          eval "eval $#{fname}['#{sname},ifputm']"
        end
        eval "$#{fname}['#{sname},method'] = args"
        put = true
      end
    end
  end
  return put
end

#
# fexistv - determine if a value facet exists
# requires that fname[sname,facets] exists
# calls ifref and ifexistv demons
#
def fexistv(fname, sname)
  found = false
  if fexists fname, sname
    if fexistrx fname, sname
      fname2 = eval "$#{fname}['#{sname},ref']"
      if eval "$#{fname}['#{sname},ref'].include? 'ifref'"
        eval "eval $#{fname}['#{sname},ifref']"
      end
      found = fexistv(fname2, sname)
    end
    if eval "$#{fname}['#{sname},facets'].include? 'value'"
      if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
        eval "eval $#{fname}['#{sname},ifexistv']"
      end
      found = true
    end
  end
  return found
end

#
# fcreatev - create a value facet
# requires that fname[sname,facets] exists
# modifies fname[sname,facets], fname[sname,value] where fname is
#          the original or referenced frame
# calls ifref and ifcreatev demons
#
def fcreatev(fname, sname)
  created = false
  if fexists fname, sname
    if (eval "$#{fname}['#{sname},facets'].include? 'method'" ||
      eval "$#{fname}['#{sname},facets'].include? 'value'")
      created = false
    else
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
          eval "eval $#{fname}['#{sname},ifref']"
        end
        created = fcreatev(fname2, sname)
      else
        eval "$#{fname}['#{sname},value'] = ''"
        eval "$#{fname}['#{sname},facets'].add 'value'"
        if eval "$#{fname}['#{sname},facets'].include? 'ifcreatev'"
          eval "eval $#{fname}['#{sname},ifcreatev']"
        end
        created = true
      end
    end
  end
  return created
end
      
#
# fremovev - remove a value facet
# requires that fname[sname,facets] exists
# modifies fname[sname,facets], fname[sname,method] where fname is
#          the original or referenced frame
# calls ifref and ifremovev demons
#
def fremovev(fname, sname)
  removed = false
  if fexists fname, sname
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
          eval "eval $#{fname}['#{sname},ifref']"
        end
        removed = fremovev(fname2, sname)
      else
          if eval "$#{fname}['#{sname},facets'].include? 'value'"
            if eval "$#{fname}['#{sname},facets'].include? 'ifremovev'"
              eval "eval $#{fname}['#{sname},ifremovev']"
            end
            eval "$#{fname}.delete('#{sname},value')"
            eval "$#{fname}['#{sname},facets'].delete 'value'"
            removed = true
          end
      end
  end
  return removed
end
    
#
# fgetv - get a value from a value facet
# requires that fname[sname,facets] exists
# calls ifref and ifgetv demons
#
def fgetv(fname,sname)
  pname = ""
  if fexists fname, sname
      if eval "$#{fname}['#{sname},facets'].include? 'ref'"
        fname2 = eval "$#{fname}['#{sname},ref']"
        if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
          eval "eval $#{fname}['#{sname},ifref']"
        end
        pname = fgetv(fname2,sname)
      else
        if eval "$#{fname}['#{sname},facets'].include? 'value'"
          if eval "$#{fname}['#{sname},facets'].include? 'ifgetv'"
            eval "eval $#{fname}['#{sname},ifgetv']"
          end
          fname = eval "$#{fname}['#{sname},value']"
        end
      end
  end
  return pname
end

#
# fputv - put a value in a value facet
# requires that fname[sname,facets] exists
# modifies fname[sname,value] where fname is the original or
#          referenced frame
# calls ifref and ifputv demons
#
def fputv(fname, sname, args)
  put = false
  if fexists fname, sname
    if eval "$#{fname}['#{sname},facets'].include? 'ref'"
      fname2 = eval "$#{fname}['#{sname},ref']"
      if eval "$#{fname}['#{sname},facets'].include? 'ifref'"
        eval "eval $#{fname}['#{sname},ifref']"
      end
      put = fputv(fname2,sname,args)
    else
      if eval "$#{fname}['#{sname},facets'].include? 'value'"
        eval "$#{fname}['#{sname},value'] = args"
        if eval "$#{fname}['#{sname},ref'].include? 'ifputv'"
          eval "eval $#{fname}['#{sname},ifputv']"
        end
        put = true
      end
    end
  end
  return put
end

#
# fexistd - determines if a demon facet exists
# requires that fname[sname,facets] exists
#
def fexistd(fname, sname, dname)
  if fexists fname, sname
    if eval "$#{fname}['#{sname},facets'].include? dname"
      return true
    else
      return false
    end
  else
    return false
  end
end

#
# fcreated - create a demon facet
# requires that fname[sname,facets] exists
# modifies fname[sname,facets], fname[sname,dname]
#
def fcreated(fname, sname, dname)
  if fexists fname, sname
    if not eval "$#{fname}['#{sname},facets'].include? dname"
      eval "$#{fname}['#{sname},{dname}'] = ''"
      eval "$#{fname}['#{sname},facets'].add dname"
      return true
    else
      return false
    end
  else
    return false
  end
end

#
# fremoved - remove a demon facet
# requires that fname[sname,dname] exists
# modifies fname[sname,facets], fname[sname,dname]
#
def fremoved(fname, sname, dname)
  if fexistd fname, sname, dname
    eval "$#{fname}.delete('#{sname},#{dname}')"
    eval "$#{fname}['#{sname},facets'].delete dname"
    return true
  else
    return false
  end
end

#
# fgetd - get a value from a demon facet
# requires that fname[sname,dname] exists
#
def fgetd(fname, sname, dname)
  if fexistd fname, sname, dname
    return eval "$#{fname}['#{sname},#{dname}']"
  else
    return ""
  end
end

#
# fputd - put a value in a demon facet
# requires that fname[sname,dname] exists
# modifies fname[sname,dname]
#
def fputd(fname, sname, dname, args)
  if fexistd fname, sname, dname
    eval "$#{fname}['#{sname},#{dname}'] = args"
    return true
  else
    return false
  end
end

#
# fexecd - directly execute a demon
# requires that fname[sname,dname] exists
# 
def fexecd(fname, sname, dname)
  if fexistd fname, sname, dname
    eval "eval $#{fname}['#{sname},#{dname}']"
    return true
  else
    return false
  end
end

#
# fcreatefs - create a frameset
# requires that name[] does not exist
# modifies fframes, name[name,set), name[name,slots]
#
def fcreatefs(name)
  if not fexistf name
    $fframes.add name
    eval "$#{name} = {'#{name},set'=>#{Set.new}}"
    eval "$#{name}['#{name},slots'] = Set.new"
    return true
  else
    return false
  end
end

#
# fremovefs - remove a frameset
# requires that name[] exists
# modifies fframes, name[]
#
def fremovefs(name)
  if fremovef name
    return true
  else
    return false
  end
end

#
# fslistf - return a list of frames in a frameset
# requires that name[] exists
#
def fslistf(name)
  if fexistf name
    return eval "$#{name}['#{name},set'].to_a"
  else
    return []
  end
end

#
# floadfs - load a frameset into memory
# requires that name[] exist on disk, but not in memory
#
def floadfs(name)
  if floadf name
    s = fslistf name
    s.each do |i|
      floadf i
    end
    return true
  else
    return false
  end
end

#
# fstorefs - store a frameset on disk
# requires that name[] exists
#
def fstorefs(name)
  if fstoref name
    s = fslistf name
    s.each do |i|
      fstoref i
    end
    return true
  else
    return false
  end
end

#
# fsincludef - include a frame in a frameset
# requires that name[] and fname[] exist
# modifies name[name,set]
#
def fsincludef(name, fname)
  if fexistf name && fexistf fname
    eval "$#{name}['#{name},set'].add fname"
    return true
  else
    return false
  end
end

#
# fsexcludef - exclude a frame from a frameset
# requires that name[] exists
# modifies name[name,set]
#
def fsexcludef(name, fname)
  if fexistf name
    if eval "$#{name}['#{name},set'].include? fname"
      eval "$#{name}['#{name},set'].delete fname"
      return true
    else
      return false
    end
  else
    return false
  end
end

#
# fscreates - create a slot in a frameset
# requires that name[] exists
# modifies name[name,slots], name[sname,facets], associated frames
#
def fscreates(name, sname)
  if fcreates name, sname
    s = fslistf name
    s.each do |i|
      fcreates i, sname
    end
    return true
  else
    return false
  end
end

#
# fsremoves - remove a slot from a frameset
# requires that name[sname,facets] exists
# modifies name[name,slots], name[sname,*], associated frames
#
def fsremoves(name, sname)
  if fremoves name, sname
    s = fslistf name
    s.each do |i|
      fremoves i, sname
    end
    return true
  else
    return false
  end
end

#
# fscreated - create a demon facet in a frameset
# requires that name[sname,facets] exists
# modifies name[name,facets], name[sname,dname], associated frames
#
def fscreated(name, sname, dname)
  if fcreated name, sname, dname
    s = fslistf name
    s.each do |i|
      fcreated i, sname
    end
    return true
  else
    return false
  end
end

#
# fsremoved - remove a demon facet from a frameset
# requires that name[sname,dname] exists
# modifies name[name,slots], name[sname,dname], associated frames
#
def fsremoved(name, sname, dname)
  if fremoved name, sname, dname
    s = fslistf name
    s.each do |i|
      fremoved i, sname
    end
    return true
  else
    return false
  end
end

#
# fscreatem - create a method facet in a frameset
# requires that name[sname,facets] exists
# modifies name[name,facets], name[sname,method], associated frames
#
def fscreatem(name, sname)
  if fremoved name, sname
    s = fslistf name
    s.each do |i|
      fcreatem i, sname
    end
    return true
  else
    return false
  end
end

#
# fsremovem - remove a method facet from a frameset
# requires that name[sname,facets] exists
# modifies name[name,facets], name[sname,method], associated frames
#
def fsremovem(name, sname)
  if fremoved name, sname
    s = fslistf name
    s.each do |i|
      fremovem i, sname
    end
    return true
  else
    return false
  end
end

#
# fscreater - create a reference facet in a frameset
# requires that name[sname,facets] exists
# modifies name[name,facets], name[sname,ref], associated frames
#
def fscreater(name, sname)
  if fremoved name, sname
    s = fslistf name
    s.each do |i|
      fcreater i, sname
    end
    return true
  else
    return false
  end
end

#
# fsremover - remove a reference facet from a frameset
# requires that name[sname,facets] exists
# modifies name[name,facets], name[sname,ref], associated frames
#
def fsremover(name, sname)
  if fremover name, sname
    s = fslistf name
    s.each do |i|
      fremover i, sname
    end
    return true
  else
    return false
  end
end

#
# fscreatev - create a value facet in a frameset
# requires that name[sname,facets] exists
# modifies name[name,facets], name[sname,value], associated frames
#
def fscreatev(name, sname)
  if fcreatev name, sname
    s = fslistf name
    s.each do |i|
      fcreatev i, sname
    end
    return true
  else
    return false
  end
end

#
# fsremovev - remove a value facet from a frameset
# requires that name[sname,facets] exists
# modifies name[name,facets], name[sname,value], associated frames
#
def fsremovev(name, sname)
  if fremovev name, sname, dname
    s = fslistf name
    s.each do |i|
      fremovev i, sname
    end
    return true
  else
    return false
  end
end

#
# fsputr - put a value in reference facet in a frameset
# requires that name[sname,facets] exists
# modifies name[name,ref]
#
def fsputr(name, sname, fname)
  if fexistr name sname
    fputr name, sname, fname
    s = fslistf name
    s.each do |i|
      fputr i, sname, fname
    end
    return true
  else
    return false
  end
end

#
# fsgetr - get a value from a reference facet in a frameset
# requires that name[sname,ref] exists
# modifies nothing
#
def fsgetr(name, sname)
  if fexistr name sname
    r = fgetr name sname
    return r
  else
    return ""
  end
end

#
# fsmemberf - get list of framesets in which a frame is a member
# requires that the frame exists
# modifies nothing
#
def fsmemberf(name)
  mlist = []
  if fexistf name
    fslitf().each do |i|
      if eval "$#{i}.include? '#{i},set'"
        if fslistf(i).include? name
          mlist.push i
        end
      end
    end
    return mlist
  else
    return []
  end
end
