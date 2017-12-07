from __future__ import print_function

config_file = ".config"
eclipse_file = "../eclipse_SYMBOLS.xml"


def xml_start_end(file, isEnd=False):
    if (not isEnd):
        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        file.write("<cdtprojectproperties>\n")
        file.write("<section name=\"org.eclipse.cdt.internal.ui.wizards.settingswizards.Macros\">\n")
        file.write("<language name=\"holder for library settings\">\n</language>\n\n")
    else:
        file.write("</section>\n")
        file.write("</cdtprojectproperties>\n")


def writexml(file, name, val):
    file.write("<language name=\"Assembly\">\n")
    file.write("<macro>\n<name>{}</name><value>{}</value>\n</macro>\n".format(name,val))
    file.write("</language>\n")
    file.write("<language name=\"GNU C\">\n")
    file.write("<macro>\n<name>{}</name><value>{}</value>\n</macro>\n".format(name,val))
    file.write("</language>\n\n")
    file.write("<language name=\"GNU C++\">\n")
    file.write("<macro>\n<name>{}</name><value>{}</value>\n</macro>\n".format(name,val))
    file.write("</language>\n\n")


def config2xml():
    try:
        with open(config_file, "r") as fin, open(eclipse_file, "w") as fout:
            xml_start_end(fout)
            writexml(fout, "__KERNEL__", "")
            lines = fin.readlines()
            for l in lines:
                l = l.strip()
                if l.startswith("#") or (len(l) == 0):
                    pass
                else:
                    index = l.find("=")
                    name = l[:index]
                    val = l[index+1:]
                    if (val.lower() == "y"):
                        val = "1"
                    elif (val.lower() == "m"):
                        name = name + "_MODULE"
                        val = "1"
                    writexml(fout, name, val)
            xml_start_end(fout, True)
            print("Generate {} successfully...".format(eclipse_file))

    except Exception:
            print("read {} file FAILED!".format(config_file))


if __name__ == "__main__":
    config2xml()
