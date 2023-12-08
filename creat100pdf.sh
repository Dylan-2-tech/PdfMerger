#! bin\sh

FILE="./b.pdf"
END=100

for i in $(seq 1 $END); do
	cp $FILE "./dirPDF/"
	mv "./dirPDF/b.pdf" "./dirPDF/b"$i".pdf"
done