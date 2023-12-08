#! bin\sh

FILE="./test.pdf"
END=100

for i in $(seq 1 $END); do
	cp $FILE "./dirPDF/"
	mv "./dirPDF/test.pdf" "./dirPDF/test"$i".pdf"
done