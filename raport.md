# Laboratorul 6 Informații invizibile

Popa Marius, grupa SI261  
Disciplina Tehnici de programare

## Lucrarea A

Mesajul din `probe/mesaj.txt` avea două straturi. Am desfăcut mai întâi codarea hex și apoi Base64. Mesajul final a fost `Mesajul secret al laboratorului 6`, așa cum apare și în `fisa.json`.

Pentru proba XOR, cheia din raportul original este `42`, iar textul rezultat este `Cheia XOR este patruzeci si doi`. Rezultatele pentru hash-urile de probă sunt în tabelul din `raport_lab6_PopaMarius.docx`, inclus în `lab6.7z`.

## Lucrarea B

Semnătura fișierului `foto.jpg` indică un JPEG, iar semnătura din `ascuns.png` indică o imagine PNG. În metadatele EXIF ale fotografiei apar modelul Canon EOS 5D Mark IV și coordonatele GPS `47.0245° N, 28.8322° E`, în Chișinău.

În `ascuns.png` am găsit o arhivă ZIP începând cu octetul 73. Arhiva conține `secret.txt`, cu mesajul `Mesajul ascuns in arhiva: LABORATOR_6_FORENSICS`.

Din ultimii biți ai canalelor RGB din `stego.png` am recuperat mesajul `FLAG{ascuns_in_pixeli}`. În implementarea din arhivă, primii 32 de biți stochează lungimea mesajului. Am verificat că cei 22 de octeți recuperați formează mesajul așteptat.

## Concluzii

Semnătura unui fișier ajută la identificarea formatului, iar metadatele unei fotografii pot arăta unde a fost făcută. Decodarea în straturi și citirea ultimilor biți ai pixelilor permit recuperarea mesajelor din probele de laborator.
