# Virtual Environment #

Under the bash load it with:
source ./bin/activate

# Start #

Take a look at main.py, probably you will need to change it to use it with your account.

Leider sind in meiner Bibliothek noch ein par Pfade so verwendet, dass es aus dem source
folder gestartet werden muss.

# Übersicht #

templates.py

Bietet mail title, inhalt und Referenz zur pdf/tex

model.py

Enthält die Datenstrukturen, die ich für die Implementierung von den templates benutze.

logic.py

Nutzt unter anderem die SMTP Bibliothek um die Mail zu versenden

main.py

Hier lässt sich der Aufruf der Bibliothek nachvollziehen.

