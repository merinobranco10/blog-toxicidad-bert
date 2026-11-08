import json, os
import moderador

casos = [
  ("valido_neutro", "I respectfully disagree with the council's decision, but I appreciate the open discussion.", "No tóxico"),
  ("valido_toxico", "You are a complete idiot and nobody wants you here.", "Tóxico"),
]
res = []
for nombre, texto, esperado in casos:
    r = moderador.predecir(texto)
    res.append({"caso": nombre, "esperado": esperado, **r})
    assert r["etiqueta"] == esperado, f"{nombre}: se obtuvo {r['etiqueta']}"

for nombre, texto in [("vacio", "   "), ("sin_letras", "!!! 123 ???"), ("none", None)]:
    try:
        moderador.predecir(texto); raise SystemExit(f"{nombre}: debía fallar")
    except moderador.ErrorEntrada as e:
        res.append({"caso": nombre, "error": str(e)})

r = moderador.predecir("Esto es muy malo y no me gusta para nada lo que dices en este comentario.")
assert r["advertencias"], "debía advertir idioma"
res.append({"caso": "advertencia_espanol", **r})

os.makedirs("evidencias", exist_ok=True)
json.dump(res, open("evidencias/resultados_ci.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK: todas las pruebas pasaron")
