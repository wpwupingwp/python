from sys import argv
import pikepdf 


pdf = pikepdf.open(argv[1])
for page in pdf.pages:
    for key in page['/Resources']['/XObject'].keys():
        print(key)
        print(page['/Resources']['/XObject'][key])
        if key.startswith('/Fm'):
            del page['/Resources']['/XObject'][key]
pdf.save(argv[2])
