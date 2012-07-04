function addContents {
    sec=`echo $1 | sed s/-.*//`
    echo "<li><a href='#$sec'>$1</a></li>" >> out.html
}

function addSection {
    sec=`echo $1 | sed s/-.*//`
    echo "<a name='$sec'></a><a href='#contents'><h1>$1</h1></a>" >> out.html
    cat "$1" | sed 's/\xE2\x80\x99/\x27/g' | sed 's/\xE2\x80\x93/\&ndash;/g' |sed 's/\xE2\x80\x94/ \&mdash; /g' | sed 's/\xE2\x80\x9C/\&ldquo;/g' | sed 's/\xE2\x80\x9D/\&rdquo;/g' | sed "s/\xE2\x80\x98/'/g" | sed 's/\xC2\xB7/\&bull;/g' | sed 's/\xE2\x80\xA6/\&hellip;/g' | sed 's/\xC3\x97/\&times;/g' | sed 's/\xC3\xAA/\&ecirc;/g' | sed 's/\xC3\xA4/\&auml;/g' | sed 's/aid:.style=/class=/g' >> out.html
    echo "<hr/>" >> out.html
}

echo "<html><head>" > out.html
echo "<style>" >> out.html
echo ".Example { margin-left: 5em; padding-left: 0.5em; border: 1px solid black; background-color: #eee; }" >> out.html
echo ".MonsterName { font-weight: bold; font-size: 18pt; }" >> out.html
echo ".Tags { font-style: oblique; font-weight: normal; font-size: 12pt; }" >> out.html
echo "span.SpellName { font-weight: bold; font-size: 14pt; }" >> out.html
echo "</style>" >> out.html
echo "</head><body>" >> out.html

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

echo "<h3><a name='contents'>Contents</a></h3><ul>" >> out.html
for file in `ls *.xml | sed 's/\([a-z]-\)/.99\1/' | sed 's/^a/99a/' | sort -n | sed 's/\.\?99//'` ; do
    addContents "$file";
done
echo "</ul>" >> out.html

for file in `ls *.xml | sed 's/\([a-z]-\)/.99\1/' | sed 's/^a/99a/' | sort -n | sed 's/\.\?99//'` ; do
    echo $file
    addSection "$file";
done

IFS=$SAVEIFS

echo "</body></html>" >> out.html
