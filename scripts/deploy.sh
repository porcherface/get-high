#!/usr/bin/bash
# deploy script using makeself, once the manifest and the setup script are run
rm -r dist
mkdir dist

dist="dist"
work=$dist"/work"
spec=$dist
name=LGGH_test_unix
src="src/main.py"
specname=${spec}"/"$name".spec"
echo $specname
options="--onedir -y"

pyi-makespec $src --specpath $spec
mv $spec"/main.spec" $specname
pyinstaller $src --distpath $dist --workpath $work --specpath $spec -n $name $options

rm -r $work
#rm -r "${dist}/"*".spec"
