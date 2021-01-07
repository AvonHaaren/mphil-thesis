files=$(find . -iname '*.tex' -not -iname '*appendix*.tex')
labels=$(gsed -E "s/^[ \t]*[^%]*\\\label\{([^}]+)\}.*/\1/g;t;d" $files)
# for label in $labels; do
# echo $label
# done
for label in $labels; do
grep -Eq "^[ \t]*[^%]*ref{[^}]*$label[},]" $files || echo "Label '$label' not referenced"
done