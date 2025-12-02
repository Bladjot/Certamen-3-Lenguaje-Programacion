# Construye un índice invertido desde los archivos en docs/.
# Ejecutar: awk -f build_index.awk docs/*.txt

BEGIN {
    system("mkdir -p inverted_index")
}

function basename(path,    parts, n) {
    n = split(path, parts, "/")
    return parts[n]
}

function docname(file,     base, parts, n) {
    base = basename(file)
    n = split(base, parts, ".")
    return parts[1]
}

{
    doc = docname(FILENAME)
    line = tolower($0)
    gsub(/[[:punct:]]/, " ", line)
    split(line, words, /[[:space:]]+/)
    for (i in words) {
        w = words[i]
        if (w == "") {
            continue
        }
        key = w SUBSEP doc
        if (!(key in seen)) {
            outfile = "inverted_index/" w ".txt"
            print doc >> outfile
            seen[key] = 1
        }
    }
}
