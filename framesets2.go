package framesets

import (
    "fmt"
    "strings"
    "sort"
    "bufio"
    "os"
)

type Frame map[string][]string
var fframes map[string]Frame
var fmethods map[string]func(string)

// initialize fframes and fmethods
func init() {
    fframes = make(map[string]Frame)
    fmethods = make(map[string]func(string))
}

/* value wrappers
 * For simplicity making Frame a map of string arrays.
 * Just need simple wrappers to simulate single strings.
*/
func getval(vector []string) string {
    return vector[0]
}
func putval(vector []string, value string) {
    vector[0] = value
}


// set operations

// fcompress - order and remove duplicates from a list
func fcompress(lista []string) {
    sort.String(lista)
    listy := []string{}
    listy = append(listy, lista[0])
    elema := lista[0]
    for _, i := range lista {
        if elema != i {
            listy = append(listy, i)
        }
        elema = i
    }
    lista = listy  
}

// fmember - determine if an element is a member of a list
func fmember(lista []string, elema string) bool {
    for _, i := range lista {
        if elema == i {
            return true
        }
    }
    return false
}

// fremove - remove all occurances of an element from a list
func fremove(lista []string, elema string) {
    listy := []string{}
    for _, i := lista {
        if elema != i {
            listy = append(listy, i)
        }
    }
    lista = listy
}

// funion - return union of two lists
func funion(lista, listb []string) []string {
    listx := append(lista, listb...)
    fcompress(listx)
    return listx
}

// fintersection - return intersection of two lists
func fintersection(lista, listb []string) []string {
    listx := []string{}
    fcompress(lista)
    fcompress(listb)
    for _, i := range lista {
        if fmember(listb, i) > 0 {
            listx = append(listx, i)
        }
    }
    return listx
}

// fdifference - return difference of two lists
func fdifference(lista, listb []string) []string {
    listx := []string{}
    fcompress(lista)
    fcompress(listb)
    for _, i := range lista {
        if fmember(listb, i)  == 0{
            listx = append(listx, i)
        }
    }
    return listx
}

// fdisjunction - return disjunction of two lists
func fdisjunction(lista, listb []string) []string {
    listx := []string{}
    fcompress(lista)
    fcompress(listb)
    for _, i := range lista {
        if fmember(lista, i) == 0 {
            listx = append(listx, i)
        }
    }
    sort.String(listx)
    return listx
}

// fequivalence - determine if two lists are equivalent
func fequivalence(lista, listb []string) bool {
    fcompress(lista)
    fcompress(listb)
    if string.Compare(lista, listb) == 0 {
        return true
    } else {
        return false
    }    
}

// fsubset - determine if a list is a subset of another list
func fsubset(lista, listb []string) bool {
    found := 0
    fcompress(lista)
    fcompress(listb)
    for _, i := range lista {
        if fmember(listb, i) {
            found++
        }
    }
    if found == 0 {
        return false
    } else {
        return true
    }
}

// ffind - find all frames having a given value facet
func ffind(sname string) []string {
    listx := []string{}
    for _, i := range flistf() {
        if fexistv(i, sname) {
            listx = append(listx, i)
        }
    }
    return listx
}

// ffindeq - find all frames having a given value for a given value facet
func ffindeq(sname string, args ...string) []string {
    listx := []string{}
    for _, i := range flistf() {
        if fexistv(i, sname) {
	        if fgetv(i, sname) == args {
                listx = append(listx, i)
            }   
        }
    }
    return listx
}

// ffindne - find all frames not having a given value for a given value facet
func ffindne(sname string, args ...string) []string {
    listx := []string{}
    for _, i := range flistf() {
        if fexistv(i, sname) {
	        if fgetv(i, sname) != args {
	            listx = append(listx, i)
	        }
	    }
    }
    return listx
}

// frames functions

// fexistf - determine if a frame exists
func fexistf(fname string) bool {
    return fmember(fframes, fname)
}

// fcreatef - create a frame
func fcreatef(fname string) bool {
    if !fexistf(fname) {
        fframes[fname] = Frame{fname+",slots": {}} 
        return true
    } else {
       return false
    }
}

// fremovef - remove a frame
func fremovef(fname string) bool {
    if fexistf(fname) {
        delete(fframes, fname)
    	return true
    } else {
        return false
    }
}

// flistf - return list of frames
func flistf() []string {
    frames := []string{}
    for _, k := range fframes {
        frames = append(frames, k)
    }
    return frames
}

// fcopyf - create a new frame based on another frame
func fcopyf(fname1, fname2 string) bool {
    if fexistf(fname1) {
        fremovef(fname2)
    	fcreatef(fname2)
    	for _, i := range fframes[fname1] {
    	    if strings.HasSuffix(i, "slots") {
    	        copy(fframes[fname2][fname2+",slots"], fframes[fname1][fname1+",slots"])
            } else {
                copy(fframes[fname2][i], fframes[fname1][i])
    	    }
    	}
    	return true
    } else {
        return false
    }
}
    
// fcomparef - determine if two frames are equivalent
func fcomparef(fname1, fname2 []string) bool {
    if fexistf(fname1) && fexistf(fname2) {
        x := fframes[fname1][fname1+",slots"]
    	y := fframes[fname2][fname2+",slots"]
    	if fequivalence(x, y) {
    	    return true
    	} else {
    	    return false
    	}
    } else {
        return false
    }
}

// fmergef - merge slots of one frame into another frame
func fmergef(fname1, fname2 []string) bool {
    if fexistf(fname1) && fexistf(fname2) {
        y := fframes[fname2][fname2+",slots"]
    	for _, i := range fframes[fname1] {
    	    if i != fname1+",set" && i != fname1+",slots" {
    	        sname := strings.Split(i, ",")[0]
                if !fmember(y, sname) {
                    copy(fframes[fname2][i], fframes[fname1][i])
                    slots := append(fframes[fname2][fname2+",slots"], sname)
                    copy(fframes[fname2][fname2+",slots"], slots)
        		}
            }
        }
        return true
    } else {
        return false
    }
}

// floadf - load a frame into memory
func floadf(fname string) bool {
    if _, err := os.Stat(path); os.IsExist(err) {
        if !fexistf(fname) {
            fcreatef(fname)
            fh, err := os.Open(fname)
            defer fh.Close()
            reader := bufio.NewReader(fh)
            for {
                line, _, err := reader.ReadLine()
                if err != nil {break}
                aname := strings.Split(line, " ")[0]
                avalue := strings.TrimPrefix(line, aname+" ")                
                fframes[fname][aname] = strings.Split(avalue, ",")
            }
            return true
        }
        return false
    }
    return false
}

// fstoref - store a frame on disk
func fstoref(fname string) bool {
    if fexistf(fname) {
        fh, err := os.Create(fname)
        defer fh.Close()
        writer := bufio.NewWriter(fh)
        for _, i := range fframes[fname] {
            writer.WriteString(i+" "+strings.Join(fframes[fname][i], ",")+"\n") 
        }
        fh.Flush()
        return true
    }
    return false
}

// fupdatef - update structure of a frame from another frame
func fupdatef(fname1, fname2 []string) bool {
    if fexistf(fname1) && fexistf(fname2) {
        copy(fframes[fname2][fname2+",slots"], fframes[fname1][fname1+",slots"])
        for _, i := range fframes[fname2] {
            if !strings.HasSuffix(i, "set") && !strings.HasSuffix(i, "slots") {
                if _, err := fframes[fname1][i]; err != nil {
                    delete(fframes[fname2], i)
                }
            }
        }
        for _, i := range fframes[fname1] {
            if !strings.HasSuffix(i, "set") && !strings.HasSuffix(i, "slots") { 
                if _, err := fframes[fname2][i]; err != nil {
                    copy(fframes[fname2][i], fframes[fname1][i])
                }
            }
        }
        return true
    } else {   
        return false
    }
}

// ffilterf - filter slots of a frame based on another frame
func ffilterf(fname1, fname2 []string) bool {
    if fexistf(fname1) && fexistf(fname2) {
        for _, i := range fframes[fname2] {
            if !strings.HasSuffix(i, "set") && !strings.HasSuffix(i, "slots") {
                if _, err := fframes[fname1][i]; err != nil {
                    delete(fframes[fname2][i])
                }
            }
        }
        return true
    } else {
        return false
    }
}

// fmethods functions

// fcreatex - create a method in fmethods
func fcreatex(mname string) bool {
    if _, err := fmethods[mname]; err != nil {
        fmethods[mname] = func(string){}
        return true
    } else {
        return false
    }
}

// fremovex - remove a method from fmethods
func fremovex(mname string) bool {
    if _, err := fmethods[mname]; err == nil {
        delete(fmethods, mname)
        return true
    } else {
        return false
    }
    
}

// fexistx - determine if a method exists in fmethods
func fexistx(mname string) bool {
    if _, err := fmethods[mname]; err == nil {
        return true
    } else {
        return false
    }
}

// flistx - return list of methods in fmethods
func flistx() []string {
    methods := []string{}
    for _, k := range fmethods {
        fmethods = append(fmethods, k)
    }
    return fmethods
}

// fgetx - get a method from fmethods
func fgetx(mname string) (func(string), err) {
    if _, err := fmethods[mname]; err == nil {
        return fmethods[mname]
    } else {
        return func(string){}, err
    }
}

// fputx - put a method in fmethods
func fputx(mname string, method func(string)) bool {
    if _, err := fmethods[mname]; err == nil {
        fmethods[mname] = method
        return true
    } else {
        return false
    }
}

// slot functions

// fexists - determine if a slot exists
func fexists(fname, sname string) bool {
    if fexistf(fname) {
        if fmember(fframes[fname][fname+",slots"], sname) {
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}

// fcreates - create a slot
func fcreates(fname, sname string) bool {
    if fexistf(fname) {
        if !fmember(fframes[fname][fname+",slots"], sname) {
            slots = append(fframes[fname][fname+",slots"], sname)
            copy(fframes[fname][fname+",slots"], slots)
            fframes[fname][sname+",facets"] = []string{}
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}

// fremoves - remove a slot
func fremoves(fname, sname string) bool {
    if fexists(fname, sname) {
        for _, i := range fframes[fname] {
            sname2 := strings.Split(i, ",")[0]
            if sname == sname2 {
                delete(fframes[fname], i)
            }
        }
        fremove(&fframes[fname][fname+",slots"], sname)
        return true
    } else {
        return false
    }
}

// flists - list slots of a frame
func flists(fname string) []string {
    if fexistf(fname) {
        return fframes[fname][fname+",slots"]
    } else {
        return []string{}
    }
}

// fcopys - copy a slot into another frame
func fcopys(fname1, sname, fname2 string) bool {
    if fexists(fname1, sname) && fexistf(fname2) {
        if fmember(fframes[fname2][fname2+",slots"], sname) {
            slots = append(fframes[fname2][fname2+",slots"], sname)
            copy(fframes[fname2][fname2+",slots"], slots)
        }
        for _, i := range fframes[fname1] {
            sname2 := strings.Split(i, ",")[0]
            if sname == sname2 {
                copy(fframes[fname2][i], fframes[fname1][i])
            }
        }
        return true
    } else {
        return false
    }
}

// fcompares - compare a slot in two frames
func fcompares(fname1, sname, fname2 string) bool {
    cmp := true
    if fexists(fname1, sname) && fexists(fname2, sname) {
        x := fframes[fname1][sname+",facets"]
        y := fframes[fname2][sname+",facets"]
        if fequivalence(x, y) {
            for _, i := range fframes[fname1] {
                sname2 := strings.Split(i, ",")[0]
                if sname == sname2 {
                    x = fframes[fname1][i]
                    y = fframes[fname2][i]
                    if x != y {
                        cmp = false
                    }
                }
            }
            return cmp
        } else {
            return false
        }
    } else {
        return false
    }
}

// flistt - list of facet types in a slot
func flistt(fname, sname string) []string {
    if fexists(fname, sname) {
        return fframes[fname][sname+",facets"]
    } else {
        return []string{}
    }
}

// fexistrx - determine if a reference facet exists (internal)
func fexistrx(fname, sname string) bool {
    fexists(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "ref") {
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}

// fexistr - determine if a reference facet exists
func fexistr(fname, sname string) bool {
    if fexistrx(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "ifexistr") {
            fmethods[getval(fframes[fname][sname+",ifexistr"])](fname)
        }
        return true
    } else {
        return false
    }
}

// fcreater - create a reference facet
func fcreater(fname, sname string) bool {
    if fexists(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "ref") {
            x := fmember(fframes[fname][sname+",facets"], "method")
            y := fmember(fframes[fname][sname+",facets"], "value")
            if !(x || y) {
                slots := append(fframes[fname][sname+",facets"], "ref")
                copy(fframes][fname[sname+",facets"], slots)
                fframes[fname][sname+",ref"] = []string{}
                if fmember(fframes[fname][sname+",facets"], "ifcreater") {
                    fmethods[getval(fframes[fname][sname+",ifcreater"])](fname)
                }
                return true
            } else {
                return false
            }
        } else {
            return false
        }
    } else {
        return false
    }
}

// fremover - remove a reference facet
func fremover(fname, sname string) bool {
    if fexistrx(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "ifremover") {
            fmethods[getval(fframes[fname][sname+",ifremover"])](fname)
        }
        delete(fframes[fname][sname+",ref"])
        fremove(fframes[fname][sname+",facets"], "ref")
        return true
    } else {
        return false
    }
}

// fgetr - get a value from a reference facet
func fgetr(fname, sname string) string {
    if fexistrx(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "ifgetr") {
            fmethods[getval(fframes[fname][sname+",ifgetr"])](fname)
        }
        return getval(fframes[fname][sname+",ref"])
    } else {
        return ""
    }
}

// fputr - put a value in a reference facet
func fputr(fname1, sname, fname2 string) bool {
    if fexistrx(fname1, sname) {
        putval(fframes[fname][sname+",ref"], fname2)
        if fmember(fframes[fname][sname+",facets"], "ifputr") {
            fmethods[getval(fframes[fname][sname+",ifputr"])](fname1)
        }
        return true
    } else {
        return false
    }
}


// flistr - list of references in a frame
func flistr(fname string) []string {
    flist := []string{}
    if fexistf(fname) {
        for _, i := range fframes[fname] {
            sname, ftype := strings.Split(i, ",")
            if ftype == "ref" {
                flist = append(flist, sname)
            }
        }
    }
    return flist
}



// fpathr - return chain of references
func fpathr(fname, sname string) []string {
    plist := []string{}
    if fexists(fname, sname) {
        plist := append(plist, fname)
        if fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := getval(fframes[fname][sname+",ref"])
            fpathrr(fname2, sname, plist)
        } else {
            return plist
        }
    } else {
        return plist
    }
}

// recursive fpathr (blame go)
func fpathrr(fname string, sname string, plist []string) []string {
    if fexists(fname, sname) {
        if !fmember(plist, fname) {
            plist = append(plist, fname)
            if fmember(fframes[fname][sname+",facets"], "ref") {
                fname2 := getval(fframes[fname][sname+",ref"])
                fpathrr(fname2, sname, plist)
            } else {
                return plist
            }
        } else {
            return plist
        }
    } else {
        return plist
    }
}

// fexistm - determine if a method facet exists
func fexistm(fname, sname string) bool {
    found := false
    if fexists(fname, sname) {
        if fexistrx(fname, sname) {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            found = fexistm(fname2, sname)
        }
        if fmember(fframes[fname][sname+",facets"], "method") {}
            fmember(fframes[fname][sname+",facets"], "ifexistm") {
                fmethods[getval(fframes[fname][sname+",ifexistm"])](fname)
        }
        found = true
    }
    return found
}

// fcreatem - create a method facet
func fcreatem(fname, sname string) bool {
    created := false
    if fexists(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "method") ||
           fmember(fframes[fname][sname+",facets"], "value") {
            created = true
        } else {
            if fmember(fframes[fname][sname+",facets"], "ref") {
                fname2 := fframes[fname][sname+",ref"]
                if fmember(fframes[fname][sname+",facets"], "ifref") {
                    fmethods[getval(fframes[fname][sname+",ifref"])](fname)
                }
                created = fcreatem(fname2, sname)
            } else {
                fframes[fname][sname+",method"] = []string{}
                facets = append(fframes[fname][sname+",facets"], "method")
                copy(fframes[fname][sname+",facets"], facets)
                if fmember(fframes[fname][sname+",facets"], "ifcreatem") {
                    fmethods[getval(fframes[fname][sname+",ifcreatem"])](fname)
                }
                created = true
            }
        }
    }
    return created
}

// fremovem - remove a method facet
func fremovem(fname, sname string) bool {
    removed = false
    if fexists(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            removed = fremovem(fname2, sname)
        } else {
            if fmember(fframes[fname][sname+",facets"], "method") {
                if fmember(fframes[fname][sname+",facets"], "ifremovem") {
                    fmethods[getval(fframes[fname][sname+"ifremovem"])](fname)
                }
                delete(fframes[fname][sname+",method"])
                fremove(fframes[fname][sname+",facets"], "method")
                removed = true
            }
        }
    }
    return removed
}

// fexecm - execute a method
func fexexm(fname, sname string) bool {
    executed := false
    if fexists(fname, sname) {
        fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            executed = fexecm(fname2, sname)
        } else {
            if fmember(fframes[fname][sname+",facets"], "method") {
                if fmember(fframes[fname][sname+",facets"], "ifexecm") {
                    fmethods[getval(fframes[fname][sname+",ifexecm"])](fname)
                }
                fmethods[getval(fframes[fname][sname+",method"])](fname)
                executed = true
            }
        }
    }
    return executed
}

// fgetm - get a value from a method 
func fgetm(fname string, sname string) string {
    pname := ""
    if fexists(fname, sname) {
        fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            pname = fgetm(fname2, sname)
        } else {
            if fmember(fframes[fname][sname+",facets"], "method") {
                if fmember(fframes[fname][sname+",facets"], "ifgetm") {
                    fmethods[getval(fframes[fname][sname+",ifgetm"])](fname)
                }
                pname = getval(fframes[fname][sname+",method"])
            }
        }
    }
    return pname
}

// fputm - put a value in a method facet
func fputm(fname, sname, args string) bool {
    put := false
    if fexists(fname, sname) {
        fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            put = fputm(fname2, sname, args)
        } else {
            if fmember(fframes[fname][sname+",facets"], "method") {
                if fmember(fframes[fname][sname+",facets"], "ifputm") {
                    fmethods[getval(fframes[fname][sname+",ifputm"])](fname)
                }
                putval(fframes[fname][sname+",method"], args)
                put = true
            }
        }
    }
    return put
}

// fexistv - determine if a value facet exists
func fexistv(fname, sname string) bool {
    found := false
    if fexists(fname, sname) {
        if fexistrx(fname, sname) {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            found = fexistv(fname2, sname)
        }
        if fmember(fframes[fname][sname+",facets"], "value") {}
            fmember(fframes[fname][sname+",facets"], "ifexistmv") {
                fmethods[getval(fframes[fname][sname+",ifexistv"])](fname)
        }
        found = true
    }
    return found
}

// fcreatev - create a value facet
func fcreatev(fname, sname string) bool {
    created := false
    if fexists(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "method") ||
           fmember(fframes[fname][sname+",facets"], "value") {
            created = true
        } else {
            if fmember(fframes[fname][sname+",facets"], "ref") {
                fname2 := fframes[fname][sname+",ref"]
                if fmember(fframes[fname][sname+",facets"], "ifref") {
                    fmethods[getval(fframes[fname][sname+",ifref"])](fname)
                }
                created = fcreatev(fname2, sname)
            } else {
                fframes[fname][sname+",value"] = []string{}
                facets = append(fframes[fname][sname+",facets"], "value")
                copy(fframes[fname][sname+",facets"], facets)
                if fmember(fframes[fname][sname+",facets"], "ifcreatev") {
                    fmethods[getval(fframes[fname][sname+",ifcreatev"])](fname)
                }
                created = true
            }
        }
    }
    return created
}

// fremovev - remove a value facet
func fremovev(fname, sname string) bool {
    removed = false
    if fexists(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            removed = fremovev(fname2, sname)
        } else {
            if fmember(fframes[fname][sname+",facets"], "value") {
                if fmember(fframes[fname][sname+",facets"], "ifremovev") {
                    fmethods[getval(fframes[fname][sname+"ifremovev"])](fname)
                }
                delete(fframes[fname][sname+",value"])
                fremove(fframes[fname][sname+",facets"], "value")
                removed = true
            }
        }
    }
    return removed
}

// fgetv - get a value from a value facet
func fgetv(fname string, sname string) string {
    pname := ""
    if fexists(fname, sname) {
        fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            pname = fgetv(fname2, sname)
        } else {
            if fmember(fframes[fname][sname+",facets"], "value") {
                if fmember(fframes[fname][sname+",facets"], "ifgetv") {
                    fmethods[getval(fframes[fname][sname+",ifgetv"])](fname)
                }
                pname = getval(fframes[fname][sname+",value"])
            }
        }
    }
    return pname
}


// fputv - put a value in a value facet
func fputv(fname, sname, args string) bool {
    put := false
    if fexists(fname, sname) {
        fmember(fframes[fname][sname+",facets"], "ref") {
            fname2 := fframes[fname][sname+",ref"]
            if fmember(fframes[fname][sname+",facets"], "ifref") {
                fmethods[getval(fframes[fname][sname+",ifref"])](fname)
            }
            put = fputv(fname2, sname, args)
        } else {
            if fmember(fframes[fname][sname+",facets"], "value") {
                if fmember(fframes[fname][sname+",facets"], "ifputm") {
                    fmethods[getval(fframes[fname][sname+",ifputm"])](fname)
                }
                putval(fframes[fname][sname+",value"], args)
                put = true
            }
        }
    }
    return put
}

// fexistd - determine if a demon facet exists
func fexistd(fnaem, sname, dname string) bool {
    if fexists(fname, sname) {
        if fmember(fframes[fname][sname+",facets"], dname) {
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}

// fcreated - create a demon facet
func fcreated(fname, sname, dname string) bool {
    if fexists(fname, sname) {
        if fmemeber(fframes[fname][sname+",facets"], dname) {
            fframes[fname][sname+","+dname] = []string{}
            facets = append(fframes[fname][sname+",facets"], dname)
            copy(fframes[fname][sname+",facets"], facets)
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}

// fremoved - remove a demon facet
func fremoved(fname, sname, dname string) bool {
    if fexistd(fname, sname, dname) {
        delete(fframes[fname][sname+","+dname])
        fremove(fframes[fname][sname+",facets"], dname)
        return true
    } else {
        return false
    }
}

// fgetd - get a value from a demon facet
func fgetd(fname, sname, dname string) string {
    if fexistd(fname, sname, dname) {
        return getval(fframes[fname][sname+","+dname])
    } else {
        return ""
    }
}

// fputd - put a value in a demon facet
func fputd(fname, sname, dname, args) bool {
    if fexistd(fname, sname, dname) {
        putval(fframes[fname][sname+","+dname], args)
        return true
    } else {
        return false
    }
}

// fexecd - directly execute a demon
func fexecd(fname, sname, dname string) bool {
    if fexistd(fname, sname, dname) {
        fmethods[getval(fframes[fname][sname+","+dname])](fname)
        return true
    } else {
        return false
    }
}

// fcreatefs - create a frameset
func fcreatefs(name string) bool {
    if !fexistf(name) {
        fframes[fname] = Frame{name+",slots": {}}
        fframes[fname][name+",set"] = []string{}
        return true
    } else {
       return false
    }
}       

// fremovefs - remove a frameset
func fremovefs(name string) bool {
    if fremovef(name) {
        return true
    } else {
        return false
    }
}

// fslistf - return a list of frames in a frameset
func fslistf(name string) bool {
    if fexistf(name) {
        return fframes[name][name+",set"]
    } else {
        return ""
    }
}

// floadfs - load a frameset into memory
func floadfs(name string) bool {
    if floadf(name) {
        s := fslistf(name)
        for _, i := range s {
            floadf(i)
        }
        return true
    } else {
        return false
    }
}

// fstorefs - store a frameset on disk
func floadfs(name string) bool {
    if fstoref(name) {
        s := fslistf(name)
        for _, i := range s {
            fstoref(i)
        }
        return true
    } else {
        return false
    }
}

// fsincludef - include a frame in a frameset
func fsincludef(name, fname string) bool {
    if fexistf(name) && fexistf(fname) {
        fframes[name][name+",set"] = append(fframes[name][name+",set"], fname)
        return true
    } else {
        return false
    }
}

// fsexcludef - exclude a frame from a frameset
func fsexcludef(name, fname string) bool {
    if fexistf(name) {
        if fmember(fframes[name][name+",set"], fname) {
            fremove(fframes[name][name+",set"], fname)
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}

// fscreates - create a slot in a frameset
func fscreates(name, sname string) bool {
    if fcreates(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fcreates(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fsremoves - remove a slot from a frameset
func fsremoves(name, sname string) bool {
    if fremoves(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fremoves(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fscreated - create a demon facet in a frameset
func fscreated(name, sname, dname string) bool {
    if fcreated(name, sname, dname) {
        s := fslistf(name)
        for _, i := range s {
            fcreated(i, sname, dname)
        }
        return true
    } else {
        return false
    }
}

// fsremoved - remove a demon facet from a frameset
func fsremoved(name, sname, dname string) bool {
    if fremoves(name, sname, dname) {
        s := fslistf(name)
        for _, i := range s {
            fremoved(i, sname, dname)
        }
        return true
    } else {
        return false
    }
}

// fscreatem - create a method facet in a frameset
func fscreatem(name, sname string) bool {
    if fcreatem(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fcreatem(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fsremovem - remove a method facet from a frameset
func fsremovem(name, sname string) bool {
    if fremovem(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fremovem(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fscreater - create a reference facet in a frameset
func fscreater(name, sname string) bool {
    if fcreater(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fcreater(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fsremover - remove a reference facet from a frameset
func fsremover(name, sname string) bool {
    if fremover(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fremover(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fscreatev - create a value facet in a frameset
func fscreatev(name, sname string) bool {
    if fcreatev(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fcreatev(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fsremovev - remove a value facet from of a frameset
func fsremovev(name, sname string) bool {
    if fremovev(name, sname) {
        s := fslistf(name)
        for _, i := range s {
            fremovev(i, sname)
        }
        return true
    } else {
        return false
    }
}

// fsputr - put a value in reference facet in a frameset
func fsputr(name, sname, fname string) bool {
    if fexistr(name, sname) {
        fputr(name, sname, fname)
        s := fslistf(name)
        for _, i := range s {
            fputr(i, sname, fname)
        }
        return true
    } else {
        return false
    }
}

// fsgetr - get a value from a reference facet in a frameset
func fsgetr(name, sname string) string {
    if fexistr(name, sname) {
        r := fgetr(name, sname)
        return r
    } else {
        return ""
    }
}

// fsmemberf - get list of framesets in which a frame is a member
func fsmemberf(name string) []string {
    mlist := []string{}
    if fexistf(name) {
        for _, i := range flistf() {
            if _, err := fframes[i][i+",set"]; err == nil {
                if fmember(fslistf(i), name) {
                    mlist = append(mlist, i)
                }
            }
        }
        return mlist
    } else {
        return []string{}
    }
}





