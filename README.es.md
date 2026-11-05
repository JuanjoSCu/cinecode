# cinecode para Codex

[Türkçe](README.md) · [English](README.en.md) · [Repositorio](https://github.com/JuanjoSCu/cinecode)

**cinecode** permite crear cortometrajes, anuncios y vídeos explicativos con código y entregar un MP4. Esta adaptación funciona como skill nativa de **Codex**: no requiere Claude Code. Codex lee [SKILL.md](SKILL.md), pregunta por el **modo** (Rápido o Film) y el **propósito** (cinematográfico o anuncio/producto) cuando no estén resueltos, respeta las decisiones delegadas y guía la creación y revisión del vídeo.

La obra original es de [Sarp Yıldız](https://github.com/sarpstar/cinecode); la adaptación para Codex es de [JuanjoSC](https://github.com/JuanjoSCu). Se conserva intacta la licencia [MIT](LICENSE) original.

## Requisitos

- Codex con acceso a herramientas locales; Node.js **22+**, Python **3.9+**, **ffmpeg** y **Google Chrome** (o Chromium/Edge). Git sirve para instalar y actualizar el kit.
- Un equipo donde Chrome pueda renderizar. Conviene tener GPU y espacio libre: unos cientos de MB para un vídeo corto y varios GB para proyectos largos.
- En Windows, usa PowerShell. Si `python3` no existe, usa `python` o `py -3`. La producción creativa completa de una película en Windows aún no se ha validado de principio a fin. Con Python 3.11 y Node 24 se capturaron 192 fotogramas deterministas mediante Chrome nativo para una muestra H.264/AAC de 8 segundos a 360×640.
- La narración y las claves de Gemini o ElevenLabs son **opcionales**; no hacen falta para renderizar un vídeo sin esa voz.

## Instalación en Codex

Puedes pedir a Codex: **«Instala el skill cinecode desde https://github.com/JuanjoSCu/cinecode en mi carpeta de skills de Codex»**. La ubicación habitual es `~/.codex/skills/cinecode`; si has definido `CODEX_HOME`, utiliza `$CODEX_HOME/skills/cinecode`.

Instalación manual en PowerShell:

```powershell
$skills = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex/skills' }
New-Item -ItemType Directory -Force -Path $skills | Out-Null
git clone https://github.com/JuanjoSCu/cinecode.git (Join-Path $skills 'cinecode')
```

En macOS/Linux, crea `~/.codex/skills` y clona allí: `git clone https://github.com/JuanjoSCu/cinecode.git ~/.codex/skills/cinecode`. Para actualizar una instalación Git: `git -C <ruta-del-skill> pull --ff-only`. Úsalo en tu siguiente turno; si el skill todavía no aparece, abre un chat nuevo de Codex. Mantén una sola copia del skill.

## Crear una película

1. Abre en Codex una **carpeta de proyecto nueva y vacía**, separada de la carpeta del skill. Los archivos de cada película y el MP4 se crean en ese proyecto; no dentro de este repositorio.
2. Escribe, por ejemplo: **«Usa $cinecode para crear un corto de 30 segundos sobre una ciudad bajo la lluvia»**. También puedes decir simplemente «Quiero hacer un cortometraje con código».
3. Responde solo a las decisiones que falten. Puedes delegar el estilo y pedir directamente la entrega final. Codex mostrará el plan, las escenas y el borrador cuando corresponda, y continuará con lo ya autorizado.

El kit ofrece un arranque rápido con `film.html` y un flujo Film para obras más largas. Las instrucciones de dirección, sonido, tipografía y control de calidad están en [SKILL.md](SKILL.md) y `references/`.

## Comprobaciones y herramientas

Desde la carpeta del kit, `python -X utf8 -m unittest discover -s tests` ejecuta las pruebas. En Windows puedes sustituir `python` por `py -3`. Al iniciar un proyecto, el kit copia las herramientas a su carpeta `tools/`. Allí, `python tools/make.py --help` y `python tools/qc.py --help` muestran cómo renderizar y revisar la película.

Las utilidades Python del guard de la integración original se conservan como material heredado. Los hooks de sesión y transcripción exclusivos de Claude **no se instalan ni están activos en Codex**. Las comprobaciones de `make.py` y `qc.py` son independientes de esos hooks.

Para la explicación completa y la galería de ejemplos, consulta la [guía original en turco](README.md) o la [versión inglesa](README.en.md).
