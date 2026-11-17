# -*- coding: utf-8 -*-
# Publica el visor 3D del cementerio de Raranga en GitHub Pages (idecstudioarq-142/cementerio-raranga-3d).
# Uso: py publicar.py   (despues de correr visor_export.py en Revit, que deja modelo.bin + modelo.json aqui).
# La direccion no cambia: https://idecstudioarq-142.github.io/cementerio-raranga-3d/  -> el QR de las laminas sigue valiendo.
import gzip, os, shutil, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
bin_, gz = os.path.join(D, "modelo.bin"), os.path.join(D, "modelo.bin.gz")
if not os.path.exists(bin_):
    sys.exit("Falta modelo.bin: corre primero visor_export.py en Revit")
with open(bin_, "rb") as a, open(gz, "wb") as f, gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=f, mtime=0) as b:
    shutil.copyfileobj(a, b)
def git(*args):
    return subprocess.run(["git", "-C", D] + list(args), capture_output=True, text=True)
git("add", "index.html", "modelo.json", "modelo.bin.gz")
if git("diff", "--cached", "--quiet").returncode == 0:
    print("sin cambios: no se publica nada"); sys.exit(0)
r = git("-c", "user.name=IDEC Arquitectura", "-c", "user.email=idecstudioarq-142@users.noreply.github.com",
        "commit", "-q", "-m", "Actualiza el modelo del visor")
if r.returncode: sys.exit(r.stderr)
r = git("push", "-q", "origin", "main")
print("publicado" if r.returncode == 0 else "ERROR al publicar: " + r.stderr)
print("tamano comprimido %.2f MB" % (os.path.getsize(gz) / 1048576.0))
