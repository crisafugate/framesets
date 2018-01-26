package framesets2

import (
	"bufio"
	"os"
	"sort"
	"strings"
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
func Getval(vector []string) string {
	if len(vector) == 0 {
		return ""
	} else {
		return vector[0]
	}
}

func Putval(vector *[]string, value string) {
	if len(*vector) == 0 {
		*vector = append(*vector, value)
	} else {
		(*vector)[0] = value
	}
}

// set operations

// fcompress - order and remove duplicates from a list
func Fcompress(lista *[]string) {
	if len(*lista) > 0 {
		listx := *lista
		sort.Strings(listx)
		listy := []string{}
		listy = append(listy, listx[0])
		elema := listx[0]
		for _, i := range listx {
			if strings.Compare(elema, i) != 0 {
				listy = append(listy, i)
			}
			elema = i
		}
		*lista = listy
	}
}

// fmember - determine if an element is a member of a list
func Fmember(lista []string, elema string) bool {
	for _, i := range lista {
		if elema == i {
			return true
		}
	}
	return false
}

// fremove - remove all occurances of an element from a list
func Fremove(lista *[]string, elema string) {
	listx := *lista
	listy := []string{}
	for _, i := range listx {
		if elema != i {
			listy = append(listy, i)
		}
	}
	*lista = listy
}

// funion - return union of two lists
func Funion(lista, listb []string) []string {
	listx := append(lista, listb...)
	Fcompress(&listx)
	return listx
}

// fintersection - return intersection of two lists
func Fintersection(lista, listb []string) []string {
	listx := []string{}
	Fcompress(&lista)
	Fcompress(&listb)
	for _, i := range lista {
		if Fmember(listb, i) {
			listx = append(listx, i)
		}
	}
	return listx
}

// fdifference - return difference of two lists
func Fdifference(lista, listb []string) []string {
	listx := []string{}
	Fcompress(&lista)
	Fcompress(&listb)
	for _, i := range lista {
		if !Fmember(listb, i)  {
			listx = append(listx, i)
		}
	}
	return listx
}

// fdisjunction - return disjunction of two lists
func Fdisjunction(lista, listb []string) []string {
	listx := []string{}
	Fcompress(&lista)
	Fcompress(&listb)
	for _, i := range lista {
		if !Fmember(listb, i) {
			listx = append(listx, i)
		}
	}
	for _, i := range listb {
		if !Fmember(lista, i) {
			listx = append(listx, i)
		}
	}
	sort.Strings(listx)
	return listx
}

// fequivalence - determine if two lists are equivalent
func Fequivalence(lista, listb []string) bool {
	Fcompress(&lista)
	Fcompress(&listb)
	if strings.Compare(strings.Join(lista, ","), strings.Join(listb, ",")) == 0 {
		return true
	} else {
		return false
	}
}

// fsubset - determine if a list is a subset of another list
func Fsubset(lista, listb []string) bool {
	found := 0
	Fcompress(&lista)
	Fcompress(&listb)
	for _, i := range lista {
		if Fmember(listb, i) {
			found++
		}
	}
	if found < len(lista) {
		return false
	} else {
		return true
	}
}

// ffind - find all frames having a given value facet
func Ffind(sname string) []string {
	listx := []string{}
	for _, i := range Flistf() {
		if Fexistv(i, sname) {
			listx = append(listx, i)
		}
	}
	return listx
}

// ffindeq - find all frames having a given value for a given value facet
func Ffindeq(sname string, args string) []string {
	listx := []string{}
	for _, i := range Flistf() {
		if Fexistv(i, sname) {
			if Fgetv(i, sname) == args {
				listx = append(listx, i)
			}
		}
	}
	return listx
}

// ffindne - find all frames not having a given value for a given value facet
func Ffindne(sname string, args string) []string {
	listx := []string{}
	for _, i := range Flistf() {
		if Fexistv(i, sname) {
			if Fgetv(i, sname) != args {
				listx = append(listx, i)
			}
		}
	}
	return listx
}

// frames functions

// fexistf - determine if a frame exists
func Fexistf(fname string) bool {
	frames := []string{}
	for k, _ := range fframes {
		frames = append(frames, k)
	}
	return Fmember(frames, fname)
}

// fcreatef - create a frame
func Fcreatef(fname string) bool {
	if !Fexistf(fname) {
		fframes[fname] = Frame{fname + ",slots": {}}
		return true
	} else {
		return false
	}
}

// fremovef - remove a frame
func Fremovef(fname string) bool {
	if Fexistf(fname) {
		delete(fframes, fname)
		return true
	} else {
		return false
	}
}

// flistf - return list of frames
func Flistf() []string {
	frames := []string{}
	for k, _ := range fframes {
		frames = append(frames, k)
	}
	return frames
}

// fcopyf - create a new frame based on another frame
func Fcopyf(fname1, fname2 string) bool {
	if Fexistf(fname1) {
		Fremovef(fname2)
		Fcreatef(fname2)
		for k, _ := range fframes[fname1] {
			if strings.HasSuffix(k, "slots") {
				slots := []string{}
				slots = append(slots, fframes[fname1][fname1+",slots"]...)
				fframes[fname2][fname2+",slots"] = slots
			} else {
				elem := []string{}
				elem = append(elem, fframes[fname1][k]...)
				fframes[fname2][k] = elem
			}
		}
		return true
	} else {
		return false
	}
}

// fcomparef - determine if two frames are equivalent
func Fcomparef(fname1, fname2 string) bool {
	if Fexistf(fname1) && Fexistf(fname2) {
		x := fframes[fname1][fname1+",slots"]
		y := fframes[fname2][fname2+",slots"]
		if Fequivalence(x, y) {
			return true
		} else {
			return false
		}
	} else {
		return false
	}
}

// fmergef - merge slots of one frame into another frame
func Fmergef(fname1, fname2 string) bool {
	if Fexistf(fname1) && Fexistf(fname2) {
		y := fframes[fname2][fname2+",slots"]
		for k, _ := range fframes[fname1] {
			if k != fname1+",set" && k != fname1+",slots" {
				sname := strings.Split(k, ",")[0]
				if !Fmember(y, sname) {
					fframes[fname2][k] = append(fframes[fname2][k], fframes[fname1][k]...)
					slots := append(fframes[fname2][fname2+",slots"], sname)
					fframes[fname2][fname2+",slots"] = slots
				}
			}
		}
		return true
	} else {
		return false
	}
}

// floadf - load a frame into memory
func Floadf(fname string) bool {
	if _, err := os.Stat(fname); os.IsExist(err) {
		if !Fexistf(fname) {
			Fcreatef(fname)
			fh, _ := os.Open(fname)
			defer fh.Close()
			reader := bufio.NewReader(fh)
			for {
				line, _, err := reader.ReadLine()
				if err != nil {
					break
				}
				aname := strings.Split(string(line), " ")[0]
				avalue := strings.TrimPrefix(string(line), aname+" ")
				fframes[fname][aname] = strings.Split(avalue, ",")
			}
			return true
		}
		return false
	}
	return false
}

// fstoref - store a frame on disk
func Fstoref(fname string) bool {
	if Fexistf(fname) {
		fh, _ := os.Create(fname)
		defer fh.Close()
		writer := bufio.NewWriter(fh)
		for k, _ := range fframes[fname] {
			writer.WriteString(k + " " + strings.Join(fframes[fname][k], ",") + "\n")
		}
		writer.Flush()
		return true
	}
	return false
}

// fupdatef - update structure of a frame from another frame
func Fupdatef(fname1, fname2 string) bool {
	if Fexistf(fname1) && Fexistf(fname2) {
		copy(fframes[fname2][fname2+",slots"], fframes[fname1][fname1+",slots"])
		for k, _ := range fframes[fname2] {
			if !strings.HasSuffix(k, "set") && !strings.HasSuffix(k, "slots") {
				if _, err := fframes[fname1][k]; err {
					delete(fframes[fname2], k)
				}
			}
		}
		for k, _ := range fframes[fname1] {
			if !strings.HasSuffix(k, "set") && !strings.HasSuffix(k, "slots") {
				if _, err := fframes[fname2][k]; err {
					copy(fframes[fname2][k], fframes[fname1][k])
				}
			}
		}
		return true
	} else {
		return false
	}
}

// ffilterf - filter slots of a frame based on another frame
func Ffilterf(fname1, fname2 string) bool {
	if Fexistf(fname1) && Fexistf(fname2) {
		for k, _ := range fframes[fname2] {
			if !strings.HasSuffix(k, "set") && !strings.HasSuffix(k, "slots") {
				if _, err := fframes[fname1][k]; err {
					delete(fframes[fname2], k)
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
func Fcreatex(mname string) bool {
	if _, err := fmethods[mname]; !err {
		fmethods[mname] = func(string) {}
		return true
	} else {
		return false
	}
}

// fremovex - remove a method from fmethods
func Fremovex(mname string) bool {
	if _, err := fmethods[mname]; err {
		delete(fmethods, mname)
		return true
	} else {
		return false
	}

}

// fexistx - determine if a method exists in fmethods
func Fexistx(mname string) bool {
	if _, err := fmethods[mname]; err {
		return true
	} else {
		return false
	}
}

// flistx - return list of methods in fmethods
func Flistx() []string {
	methods := []string{}
	for k, _ := range fmethods {
		methods = append(methods, k)
	}
	return methods
}

// fgetx - get a method from fmethods
func Fgetx(mname string) (func(string), bool) {
	if _, err := fmethods[mname]; err {
		return fmethods[mname], true
	} else {
		return func(string) {}, false
	}
}

// fputx - put a method in fmethods
func Fputx(mname string, method func(string)) bool {
	if _, err := fmethods[mname]; err {
		fmethods[mname] = method
		return true
	} else {
		return false
	}
}

// slot functions

// fexists - determine if a slot exists
func Fexists(fname, sname string) bool {
	if Fexistf(fname) {
		if Fmember(fframes[fname][fname+",slots"], sname) {
			return true
		} else {
			return false
		}
	} else {
		return false
	}
}

// fcreates - create a slot
func Fcreates(fname, sname string) bool {
	if Fexistf(fname) {
		if !Fmember(fframes[fname][fname+",slots"], sname) {
			slots := append(fframes[fname][fname+",slots"], sname)
			fframes[fname][fname+",slots"] = slots
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
func Fremoves(fname, sname string) bool {
	if Fexists(fname, sname) {
		for k, _ := range fframes[fname] {
			sname2 := strings.Split(k, ",")[0]
			if sname == sname2 {
				delete(fframes[fname], k)
			}
		}
		slots := fframes[fname][fname+",slots"]
		Fremove(&slots, sname)
		fframes[fname][fname+",slots"] = slots
		return true
	} else {
		return false
	}
}

// flists - list slots of a frame
func Flists(fname string) []string {
	if Fexistf(fname) {
		return fframes[fname][fname+",slots"]
	} else {
		return []string{}
	}
}

// fcopys - copy a slot into another frame
func Fcopys(fname1, sname, fname2 string) bool {
	if Fexists(fname1, sname) && Fexistf(fname2) {
		if !Fmember(fframes[fname2][fname2+",slots"], sname) {
			slots := append(fframes[fname2][fname2+",slots"], sname)
			fframes[fname2][fname2+",slots"] = slots
		}
		for k, _ := range fframes[fname1] {
			sname2 := strings.Split(k, ",")[0]
			if sname == sname2 {
				copy(fframes[fname2][k], fframes[fname1][k])
			}
		}
		return true
	} else {
		return false
	}
}

// fcompares - compare a slot in two frames
func Fcompares(fname1, sname, fname2 string) bool {
	cmp := true
	if Fexists(fname1, sname) && Fexists(fname2, sname) {
		x := fframes[fname1][sname+",facets"]
		y := fframes[fname2][sname+",facets"]
		if Fequivalence(x, y) {
			for k, _ := range fframes[fname1] {
				sname2 := strings.Split(k, ",")[0]
				if sname == sname2 {
					x = fframes[fname1][k]
					y = fframes[fname2][k]
					if strings.Compare(strings.Join(x, ","), strings.Join(y, ",")) != 0 {
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
func Flistt(fname, sname string) []string {
	if Fexists(fname, sname) {
		return fframes[fname][sname+",facets"]
	} else {
		return []string{}
	}
}

// fexistrx - determine if a reference facet exists (internal)
func Fexistrx(fname, sname string) bool {
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			return true
		} else {
			return false
		}
	} else {
		return false
	}
}

// fexistr - determine if a reference facet exists
func Fexistr(fname, sname string) bool {
	if Fexistrx(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ifexistr") {
			fmethods[Getval(fframes[fname][sname+",ifexistr"])](fname)
		}
		return true
	} else {
		return false
	}
}

// fcreater - create a reference facet
func Fcreater(fname, sname string) bool {
	if Fexists(fname, sname) {
		if !Fmember(fframes[fname][sname+",facets"], "ref") {
			x := Fmember(fframes[fname][sname+",facets"], "method")
			y := Fmember(fframes[fname][sname+",facets"], "value")
			if !(x || y) {
				slots := append(fframes[fname][sname+",facets"], "ref")
				fframes[fname][sname+",facets"] = slots
				fframes[fname][sname+",ref"] = []string{}
				if Fmember(fframes[fname][sname+",facets"], "ifcreater") {
					fmethods[Getval(fframes[fname][sname+",ifcreater"])](fname)
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
func Fremover(fname, sname string) bool {
	if Fexistrx(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ifremover") {
			fmethods[Getval(fframes[fname][sname+",ifremover"])](fname)
		}
		delete(fframes[fname], sname+",ref")
		facets := fframes[fname][sname+",facets"]
		Fremove(&facets, "ref")
		fframes[fname][sname+",facets"] = facets
		return true
	} else {
		return false
	}
}

// fgetr - get a value from a reference facet
func Fgetr(fname, sname string) string {
	if Fexistrx(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ifgetr") {
			fmethods[Getval(fframes[fname][sname+",ifgetr"])](fname)
		}
		return Getval(fframes[fname][sname+",ref"])
	} else {
		return ""
	}
}

// fputr - put a value in a reference facet
func Fputr(fname1, sname, fname2 string) bool {
	if Fexistrx(fname1, sname) {
		ref := fframes[fname1][sname+",ref"]
		Putval(&ref, fname2)
		fframes[fname1][sname+",ref"] = ref
		if Fmember(fframes[fname1][sname+",facets"], "ifputr") {
			fmethods[Getval(fframes[fname1][sname+",ifputr"])](fname1)
		}
		return true
	} else {
		return false
	}
}

// flistr - list of references in a frame
func Flistr(fname string) []string {
	flist := []string{}
	if Fexistf(fname) {
		for k, _ := range fframes[fname] {
			sname := strings.Split(k, ",")[0]
			ftype := strings.Split(k, ",")[1]
			if ftype == "ref" {
				flist = append(flist, sname)
			}
		}
	}
	return flist
}

// fpathr - return chain of references
func Fpathr(fname, sname string) []string {
	plist := []string{}
	if Fexists(fname, sname) {
		plist := append(plist, fname)
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := Getval(fframes[fname][sname+",ref"])
			fpathrr(fname2, sname, plist)
		} else {
			return plist
		}
	} else {
		return plist
	}
	// useless return statement
	return plist
}

// recursive fpathr (blame go)
func fpathrr(fname string, sname string, plist []string) []string {
	if Fexists(fname, sname) {
		if !Fmember(plist, fname) {
			plist = append(plist, fname)
			if Fmember(fframes[fname][sname+",facets"], "ref") {
				fname2 := Getval(fframes[fname][sname+",ref"])
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
	// useless return statement
	return plist
}

// fexistm - determine if a method facet exists
func Fexistm(fname, sname string) bool {
	found := false
	if Fexists(fname, sname) {
		if Fexistrx(fname, sname) {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			found = Fexistm(fname2, sname)
		}
		if Fmember(fframes[fname][sname+",facets"], "method") {
			if Fmember(fframes[fname][sname+",facets"], "ifexistm") {
				fmethods[Getval(fframes[fname][sname+",ifexistm"])](fname)
			}
			found = true
		}
	}
	return found
}

// fcreatem - create a method facet
func Fcreatem(fname, sname string) bool {
	created := false
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "method") ||
			Fmember(fframes[fname][sname+",facets"], "value") {
			created = false
		} else {
			if Fmember(fframes[fname][sname+",facets"], "ref") {
				fname2 := fframes[fname][sname+",ref"][0]
				if Fmember(fframes[fname][sname+",facets"], "ifref") {
					fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
				}
				created = Fcreatem(fname2, sname)
			} else {
				fframes[fname][sname+",method"] = []string{}
				facets := append(fframes[fname][sname+",facets"], "method")
				fframes[fname][sname+",facets"] = facets
				if Fmember(fframes[fname][sname+",facets"], "ifcreatem") {
					fmethods[Getval(fframes[fname][sname+",ifcreatem"])](fname)
				}
				created = true
			}
		}
	}
	return created
}

// fremovem - remove a method facet
func Fremovem(fname, sname string) bool {
	removed := false
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			removed = Fremovem(fname2, sname)
		} else {
			if Fmember(fframes[fname][sname+",facets"], "method") {
				if Fmember(fframes[fname][sname+",facets"], "ifremovem") {
					fmethods[Getval(fframes[fname][sname+"ifremovem"])](fname)
				}
				delete(fframes[fname], sname+",method")
				facets := fframes[fname][sname+",facets"]
				Fremove(&facets, "method")
				fframes[fname][sname+",facets"] = facets
				removed = true
			}
		}
	}
	return removed
}

// fexecm - execute a method
func Fexecm(fname, sname string) bool {
	executed := false
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			executed = Fexecm(fname2, sname)
		} else {
			if Fmember(fframes[fname][sname+",facets"], "method") {
				if Fmember(fframes[fname][sname+",facets"], "ifexecm") {
					fmethods[Getval(fframes[fname][sname+",ifexecm"])](fname)
				}
				fmethods[Getval(fframes[fname][sname+",method"])](fname)
				executed = true
			}
		}
	}
	return executed
}

// fgetm - get a value from a method
func Fgetm(fname string, sname string) string {
	pname := ""
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			pname = Fgetm(fname2, sname)
		} else {
			if Fmember(fframes[fname][sname+",facets"], "method") {
				if Fmember(fframes[fname][sname+",facets"], "ifgetm") {
					fmethods[Getval(fframes[fname][sname+",ifgetm"])](fname)
				}
				pname = Getval(fframes[fname][sname+",method"])
			}
		}
	}
	return pname
}

// fputm - put a value in a method facet
func Fputm(fname, sname, args string) bool {
	put := false
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			put = Fputm(fname2, sname, args)
		} else {
			if Fmember(fframes[fname][sname+",facets"], "method") {
				if Fmember(fframes[fname][sname+",facets"], "ifputm") {
					fmethods[Getval(fframes[fname][sname+",ifputm"])](fname)
				}
				method := fframes[fname][sname+",method"]
				Putval(&method, args)
				fframes[fname][sname+",method"] = method
				put = true
			}
		}
	}
	return put
}

// fexistv - determine if a value facet exists
func Fexistv(fname, sname string) bool {
	found := false
	if Fexists(fname, sname) {
		if Fexistrx(fname, sname) {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			found = Fexistv(fname2, sname)
		}
		if Fmember(fframes[fname][sname+",facets"], "value") {		
			if Fmember(fframes[fname][sname+",facets"], "ifexistmv") {
				fmethods[Getval(fframes[fname][sname+",ifexistv"])](fname)
			}
			found = true
		}
	}
	return found
}

// fcreatev - create a value facet
func Fcreatev(fname, sname string) bool {
	created := false
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "method") ||
			Fmember(fframes[fname][sname+",facets"], "value") {
			created = false
		} else {
			if Fmember(fframes[fname][sname+",facets"], "ref") {
				fname2 := fframes[fname][sname+",ref"][0]
				if Fmember(fframes[fname][sname+",facets"], "ifref") {
					fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
				}
				created = Fcreatev(fname2, sname)
			} else {
				fframes[fname][sname+",value"] = []string{}
				facets := append(fframes[fname][sname+",facets"], "value")
				fframes[fname][sname+",facets"] = facets
				if Fmember(fframes[fname][sname+",facets"], "ifcreatev") {
					fmethods[Getval(fframes[fname][sname+",ifcreatev"])](fname)
				}
				created = true
			}
		}
	}
	return created
}

// fremovev - remove a value facet
func Fremovev(fname, sname string) bool {
	removed := false
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			removed = Fremovev(fname2, sname)
		} else {
			if Fmember(fframes[fname][sname+",facets"], "value") {
				if Fmember(fframes[fname][sname+",facets"], "ifremovev") {
					fmethods[Getval(fframes[fname][sname+"ifremovev"])](fname)
				}
				delete(fframes[fname], sname+",value")
				facets := fframes[fname][sname+",facets"]
				Fremove(&facets, "value")
				fframes[fname][sname+",facets"] = facets
				removed = true
			}
		}
	}
	return removed
}

// fgetv - get a value from a value facet
func Fgetv(fname string, sname string) string {
	pname := ""
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			pname = Fgetv(fname2, sname)
		} else {
			if Fmember(fframes[fname][sname+",facets"], "value") {
				if Fmember(fframes[fname][sname+",facets"], "ifgetv") {
					fmethods[Getval(fframes[fname][sname+",ifgetv"])](fname)
				}
				pname = Getval(fframes[fname][sname+",value"])
			}
		}
	}
	return pname
}

// fputv - put a value in a value facet
func Fputv(fname, sname, args string) bool {
	put := false
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], "ref") {
			fname2 := fframes[fname][sname+",ref"][0]
			if Fmember(fframes[fname][sname+",facets"], "ifref") {
				fmethods[Getval(fframes[fname][sname+",ifref"])](fname)
			}
			put = Fputv(fname2, sname, args)
		} else {
			if Fmember(fframes[fname][sname+",facets"], "value") {
				if Fmember(fframes[fname][sname+",facets"], "ifputm") {
					fmethods[Getval(fframes[fname][sname+",ifputm"])](fname)
				}
				value := fframes[fname][sname+",value"]
				Putval(&value, args)
				fframes[fname][sname+",value"] = value
				put = true
			}
		}
	}
	return put
}

// fexistd - determine if a demon facet exists
func Fexistd(fname, sname, dname string) bool {
	if Fexists(fname, sname) {
		if Fmember(fframes[fname][sname+",facets"], dname) {
			return true
		} else {
			return false
		}
	} else {
		return false
	}
}

// fcreated - create a demon facet
func Fcreated(fname, sname, dname string) bool {
	if Fexists(fname, sname) {
		if !Fmember(fframes[fname][sname+",facets"], dname) {
			fframes[fname][sname+","+dname] = []string{}
			facets := append(fframes[fname][sname+",facets"], dname)
			fframes[fname][sname+",facets"] = facets
			return true
		} else {
			return false
		}
	} else {
		return false
	}
}

// fremoved - remove a demon facet
func Fremoved(fname, sname, dname string) bool {
	if Fexistd(fname, sname, dname) {
		delete(fframes[fname], sname+","+dname)
		facets:= fframes[fname][sname+",facets"]
		Fremove(&facets, dname)
		fframes[fname][sname+",facets"] = facets
		return true
	} else {
		return false
	}
}

// fgetd - get a value from a demon facet
func Fgetd(fname, sname, dname string) string {
	if Fexistd(fname, sname, dname) {
		return Getval(fframes[fname][sname+","+dname])
	} else {
		return ""
	}
}

// fputd - put a value in a demon facet
func Fputd(fname, sname, dname, args string) bool {
	if Fexistd(fname, sname, dname) {
		demon := fframes[fname][sname+","+dname]
		Putval(&demon, args)
		fframes[fname][sname+","+dname] = demon
		return true
	} else {
		return false
	}
}

// fexecd - directly execute a demon
func Fexecd(fname, sname, dname string) bool {
	if Fexistd(fname, sname, dname) {
		fmethods[Getval(fframes[fname][sname+","+dname])](fname)
		return true
	} else {
		return false
	}
}

// fcreatefs - create a frameset
func Fcreatefs(name string) bool {
	if !Fexistf(name) {
		fframes[name] = Frame{name + ",slots": {}}
		fframes[name][name+",set"] = []string{}
		return true
	} else {
		return false
	}
}

// fremovefs - remove a frameset
func Fremovefs(name string) bool {
	if Fremovef(name) {
		return true
	} else {
		return false
	}
}

// fslistf - return a list of frames in a frameset
func Fslistf(name string) []string {
	if Fexistf(name) {
		return fframes[name][name+",set"]
	} else {
		return []string{}
	}
}

// floadfs - load a frameset into memory
func Floadfs(name string) bool {
	if Floadf(name) {
		s := Fslistf(name)
		for _, i := range s {
			Floadf(i)
		}
		return true
	} else {
		return false
	}
}

// fstorefs - store a frameset on disk
func Fstorefs(name string) bool {
	if Fstoref(name) {
		s := Fslistf(name)
		for _, i := range s {
			Fstoref(i)
		}
		return true
	} else {
		return false
	}
}

// fsincludef - include a frame in a frameset
func Fsincludef(name, fname string) bool {
	if Fexistf(name) && Fexistf(fname) {
		set := append(fframes[name][name+",set"], fname)
		fframes[name][name+",set"] = set
		return true
	} else {
		return false
	}
}

// fsexcludef - exclude a frame from a frameset
func Fsexcludef(name, fname string) bool {
	if Fexistf(name) {
		if Fmember(fframes[name][name+",set"], fname) {
			set := fframes[name][name+",set"]
			Fremove(&set, fname)
			fframes[name][name+",set"] = set
			return true
		} else {
			return false
		}
	} else {
		return false
	}
}

// fscreates - create a slot in a frameset
func Fscreates(name, sname string) bool {
	if Fcreates(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fcreates(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fsremoves - remove a slot from a frameset
func Fsremoves(name, sname string) bool {
	if Fremoves(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fremoves(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fscreated - create a demon facet in a frameset
func Fscreated(name, sname, dname string) bool {
	if Fcreated(name, sname, dname) {
		s := Fslistf(name)
		for _, i := range s {
			Fcreated(i, sname, dname)
		}
		return true
	} else {
		return false
	}
}

// fsremoved - remove a demon facet from a frameset
func Fsremoved(name, sname, dname string) bool {
	if Fremoved(name, sname, dname) {
		s := Fslistf(name)
		for _, i := range s {
			Fremoved(i, sname, dname)
		}
		return true
	} else {
		return false
	}
}

// fscreatem - create a method facet in a frameset
func Fscreatem(name, sname string) bool {
	if Fcreatem(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fcreatem(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fsremovem - remove a method facet from a frameset
func Fsremovem(name, sname string) bool {
	if Fremovem(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fremovem(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fscreater - create a reference facet in a frameset
func Fscreater(name, sname string) bool {
	if Fcreater(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fcreater(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fsremover - remove a reference facet from a frameset
func Fsremover(name, sname string) bool {
	if Fremover(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fremover(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fscreatev - create a value facet in a frameset
func Fscreatev(name, sname string) bool {
	if Fcreatev(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fcreatev(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fsremovev - remove a value facet from of a frameset
func Fsremovev(name, sname string) bool {
	if Fremovev(name, sname) {
		s := Fslistf(name)
		for _, i := range s {
			Fremovev(i, sname)
		}
		return true
	} else {
		return false
	}
}

// fsputr - put a value in reference facet in a frameset
func Fsputr(name, sname, fname string) bool {
	if Fexistr(name, sname) {
		Fputr(name, sname, fname)
		s := Fslistf(name)
		for _, i := range s {
			Fputr(i, sname, fname)
		}
		return true
	} else {
		return false
	}
}

// fsgetr - get a value from a reference facet in a frameset
func Fsgetr(name, sname string) string {
	if Fexistr(name, sname) {
		r := Fgetr(name, sname)
		return r
	} else {
		return ""
	}
}

// fsmemberf - get list of framesets in which a frame is a member
func Fsmemberf(name string) []string {
	mlist := []string{}
	if Fexistf(name) {
		for _, i := range Flistf() {
			if _, err := fframes[i][i+",set"]; err {
				if Fmember(Fslistf(i), name) {
					mlist = append(mlist, i)
				}
			}
		}
		return mlist
	} else {
		return []string{}
	}
}
