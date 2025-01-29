import datetime
import os
from os.path import isfile, join

now = datetime.datetime.now()
data = now.strftime("%H:%M:%S %d/%m/%Y")
with open("raport.html","w") as file1:
    file1.write(f"""
    <html>
        <head>
            <title> Raport z obliczania </title>
        </head>
        <body>
        <h1>{data}</h1>
        <table>
            <tr>
                <th>input</th>
                <th>output</th>
            <tr>
    """)
    a = ""
    b = ""
    wynik = ""
    filein = [file for file in os.listdir("input") if isfile(join("input",file))]
    for x in range(len(filein)):
        with open(f"input/dane{x+1}.txt","r") as file2:
            a = file2.readline().rstrip()
            b = file2.readline().rstrip()
        file1.write(""" <tr><td>""" + "(" + a + ")/(" + b + ")")
        file1.write("""</td>
            <td>""")
        with open(f"output/dane{x+1}.txt", "r") as file3:
            wynik = file3.readline().rstrip()
        file1.write(wynik)
        file1.write("""</td>
            </tr>""")
    file1.write("""
        </table>
        </body>
    </html>""")
