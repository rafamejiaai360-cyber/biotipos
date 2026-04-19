#!/usr/bin/env python3
# Auto-configure Homebrew native libs for WeasyPrint on macOS (must run before any import)
import os, sys
if sys.platform == "darwin":
    _hb = "/opt/homebrew/lib"
    if _hb not in os.environ.get("DYLD_LIBRARY_PATH", ""):
        os.environ["DYLD_LIBRARY_PATH"] = _hb + (":" + os.environ["DYLD_LIBRARY_PATH"] if os.environ.get("DYLD_LIBRARY_PATH") else "")
        os.execv(sys.executable, [sys.executable] + sys.argv)

"""
server.py — Servidor local para App Biotipos
- Sirve archivos estáticos en http://localhost:3000
- POST /api/save              → guarda resultado, genera PDF, envía email, syncs Notion
- POST /api/rating            → actualiza puntuacion en JSON y Notion
- POST /api/comment           → guarda comentario / aporte de experto
- GET  /api/users             → lista usuarios (admin)
- GET  /api/comments          → lista comentarios y aportes (admin)
- POST /api/approve-comment   → aprueba aporte experto → pasa a Fuentes
- GET  /api/pdf/<archivo>     → sirve PDF generado
- GET  /api/transcriptions    → lista fuentes de conocimiento (admin)
- POST /api/transcription     → guarda nueva fuente (admin)
- GET  /api/notebooklm-export → exporta todas las fuentes a .txt (admin)
- GET  /api/perfiles          → lista perfiles analizados desde el admin (admin)
- POST /api/perfiles          → guarda un perfil analizado desde el admin

Uso: python3 server.py
"""

import http.server
import json
import os
import datetime
import smtplib
import email.mime.multipart
import email.mime.text
import email.mime.application
import urllib.request
import urllib.error
from pathlib import Path

PORT = int(os.environ.get("PORT", 3000))
BASE_DIR    = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "resultados"
PDFS_DIR    = BASE_DIR / "pdfs"
TRANS_DIR   = BASE_DIR / "transcripciones"
COMMENTS_DIR = BASE_DIR / "comentarios"
PERFILES_DIR = BASE_DIR / "perfiles_analizados"
CONFIG_FILE = BASE_DIR / "config.json"

for d in [RESULTS_DIR, PDFS_DIR, TRANS_DIR, COMMENTS_DIR, PERFILES_DIR]:
    d.mkdir(exist_ok=True)


def load_config():
    # Leer config.json si existe (local), sino usar variables de entorno (Railway/cloud)
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {
            "admin": {
                "password": os.environ.get("ADMIN_PASSWORD", "")
            },
            "notion": {
                "enabled":     os.environ.get("NOTION_ENABLED", "false").lower() == "true",
                "token":       os.environ.get("NOTION_TOKEN", ""),
                "database_id": os.environ.get("NOTION_DATABASE_ID", ""),
            },
            "email": {
                "enabled": False
            }
        }


def send_email(cfg, to_email, to_name, pdf_bytes, pdf_filename):
    """Envía el PDF al correo del usuario. Devuelve (ok, msg)."""
    try:
        msg = email.mime.multipart.MIMEMultipart()
        msg["From"]    = f"{cfg['from_name']} <{cfg['from_email']}>"
        msg["To"]      = to_email
        msg["Subject"] = f"Tu perfil de temperamento Biotipos — {to_name}"

        body = f"""Hola {to_name},

Gracias por descubrir tu temperamento con Biotipos.

Adjunto encontrarás tu perfil personalizado en PDF con todas tus fortalezas,
áreas de mejora, recomendaciones y guía de conexión con otros.

¡Úsalo para crecer y conectar mejor con el mundo!

— Equipo Biotipos
"""
        msg.attach(email.mime.text.MIMEText(body, "plain", "utf-8"))

        part = email.mime.application.MIMEApplication(pdf_bytes, Name=pdf_filename)
        part["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'
        msg.attach(part)

        with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["smtp_user"], cfg["smtp_password"])
            server.sendmail(cfg["from_email"], to_email, msg.as_string())

        return True, "OK"
    except Exception as e:
        return False, str(e)


TYPE_NAMES = {"c": "Colérico", "s": "Sanguíneo", "f": "Flemático", "m": "Melancólico"}


def save_to_notion(cfg, payload, pdf_filename=None):
    """Crea una página en la base de datos de Notion. Devuelve (ok, page_id, msg)."""
    try:
        token       = cfg.get("token", "")
        database_id = cfg.get("database_id", "")
        if not token or not database_id:
            return False, None, "Token o database_id no configurados"

        dom = payload.get("dominant", "")
        sec = payload.get("secondary", "")
        dom_name = TYPE_NAMES.get(dom, dom)
        sec_name = TYPE_NAMES.get(sec, sec)
        scores   = payload.get("scores", {})
        nombre   = payload.get("nombre", "")
        apellido = payload.get("apellido", "")

        properties = {
            "Nombre": {
                "title": [{"text": {"content": nombre}}]
            },
            "Apellido": {
                "rich_text": [{"text": {"content": apellido}}]
            },
            "Email": {
                "email": payload.get("email", "")
            },
            "Temperamento Dominante": {
                "select": {"name": dom_name}
            },
            "Temperamento Secundario": {
                "select": {"name": sec_name}
            },
            "Perfil": {
                "rich_text": [{"text": {"content": payload.get("perfil", "")}}]
            },
            "Con Foto": {
                "select": {"name": "Sí" if payload.get("conFoto") else "No"}
            },
            "Puntaje Colérico":    {"number": scores.get("c", 0)},
            "Puntaje Sanguíneo":   {"number": scores.get("s", 0)},
            "Puntaje Flemático":   {"number": scores.get("f", 0)},
            "Puntaje Melancólico": {"number": scores.get("m", 0)},
        }

        body = json.dumps({
            "parent":     {"database_id": database_id},
            "properties": properties,
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.notion.com/v1/pages",
            data=body,
            headers={
                "Authorization":  f"Bearer {token}",
                "Content-Type":   "application/json",
                "Notion-Version": "2022-06-28",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result  = json.loads(resp.read())
            page_id = result.get("id", "")

        # Agregar el PDF como bloque de archivo dentro de la página
        if pdf_filename and page_id:
            _attach_pdf_block_to_notion(token, page_id, pdf_filename)

        return True, page_id, "OK"

    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        return False, None, f"HTTP {e.code}: {msg}"
    except Exception as e:
        return False, None, str(e)


def _attach_pdf_block_to_notion(token, page_id, pdf_filename):
    """Agrega un bloque con link al PDF dentro de la página de Notion."""
    pdf_url = f"http://localhost:{PORT}/api/pdf/{pdf_filename}"
    try:
        block_data = json.dumps({
            "children": [
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "📄 Reporte PDF"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": pdf_filename, "link": {"url": pdf_url}},
                            "annotations": {"bold": True, "color": "purple"}
                        }]
                    }
                }
            ]
        }).encode("utf-8")

        req = urllib.request.Request(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            data=block_data,
            headers={
                "Authorization":  f"Bearer {token}",
                "Content-Type":   "application/json",
                "Notion-Version": "2022-06-28",
            },
            method="PATCH",
        )
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        print(f"  ⚠️  PDF block en Notion: {e}")


def update_notion_rating(cfg, page_id, puntuacion):
    """Actualiza la columna Puntuación en una página de Notion existente."""
    try:
        body = json.dumps({
            "properties": {
                "Puntuación": {"number": puntuacion}
            }
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.notion.com/v1/pages/{page_id}",
            data=body,
            headers={
                "Authorization":  f"Bearer {cfg['token']}",
                "Content-Type":   "application/json",
                "Notion-Version": "2022-06-28",
            },
            method="PATCH",
        )
        with urllib.request.urlopen(req, timeout=10):
            return True, "OK"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()}"
    except Exception as e:
        return False, str(e)


def build_pdf_data(payload, result_file):
    """Construye el dict que espera generate_pdf()."""
    scores    = payload.get("scores", {})
    dominant  = payload.get("dominant", "")
    secondary = payload.get("secondary", "")

    dominant_name  = TYPE_NAMES.get(dominant,  dominant)
    secondary_name = TYPE_NAMES.get(secondary, secondary)

    return {
        "nombre":          payload.get("nombre", ""),
        "apellido":        payload.get("apellido", ""),
        "email":           payload.get("email", ""),
        "timestamp":       payload.get("timestamp", ""),
        "dominant_name":   dominant_name,
        "secondary_name":  secondary_name,
        "profile":         payload.get("profile", {}),
        "health_risks":    payload.get("health_risks", []),
        "health_cares":    payload.get("health_cares", []),
        "scores_display": {
            TYPE_NAMES.get(k, k): v
            for k, v in scores.items()
        },
    }


class BiotipesHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, fmt, *args):
        status = args[0]
        color  = "\033[32m" if str(status).startswith("2") else "\033[33m"
        print(f"  {color}{self.command} {self.path} → {status}\033[0m")

    def end_headers(self):
        if self.path.split("?")[0].endswith((".js", ".html", ".css")):
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.send_header("Pragma", "no-cache")
        super().end_headers()

    # ─── CORS ────────────────────────────────────────────────
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    # ─── ROUTING ─────────────────────────────────────────────
    def do_GET(self):
        if self.path == "/api/users":
            self._require_admin()
            self._handle_users()
        elif self.path.startswith("/api/pdf/"):
            self._handle_serve_pdf()
        elif self.path == "/api/transcriptions":
            self._require_admin()
            self._handle_list_transcriptions()
        elif self.path == "/api/notebooklm-export":
            self._require_admin()
            self._handle_notebooklm_export()
        elif self.path == "/api/comments":
            self._require_admin()
            self._handle_list_comments()
        elif self.path == "/api/perfiles":
            self._require_admin()
            self._handle_list_perfiles()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/save":
            self._handle_save()
        elif self.path == "/api/rating":
            self._handle_rating()
        elif self.path == "/api/comment":
            self._handle_save_comment()
        elif self.path == "/api/transcription":
            self._require_admin()
            self._handle_save_transcription()
        elif self.path == "/api/approve-comment":
            self._require_admin()
            self._handle_approve_comment()
        elif self.path == "/api/perfiles":
            self._require_admin()
            self._handle_save_perfil()
        elif self.path == "/api/delete-user":
            self._require_admin()
            self._handle_delete_user()
        else:
            self.send_error(404, "Endpoint no encontrado")

    # ─── AUTH ────────────────────────────────────────────────
    def _require_admin(self):
        cfg      = load_config()
        password = cfg.get("admin", {}).get("password", "")
        auth     = self.headers.get("Authorization", "")
        token    = auth.replace("Bearer ", "").strip()
        if token != password:
            self._respond(401, {"ok": False, "error": "No autorizado"})
            raise PermissionError("Unauthorized")

    # ─── SAVE ────────────────────────────────────────────────
    def _handle_save(self):
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))

            payload["timestamp"]          = datetime.datetime.now().isoformat()
            payload["guardado_en_notion"] = False

            email_slug = payload.get("email", "usuario").split("@")[0].replace(".", "_")
            ts_slug    = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name  = f"{ts_slug}_{email_slug}"
            json_file  = RESULTS_DIR / f"{base_name}.json"

            # Generar PDF
            pdf_filename = None
            pdf_ok       = False
            pdf_error    = ""
            pdf_bytes    = None
            try:
                from pdf_generator import generate_pdf
                pdf_data  = build_pdf_data(payload, json_file)
                pdf_bytes = generate_pdf(pdf_data)
                pdf_filename = f"{base_name}.pdf"
                (PDFS_DIR / pdf_filename).write_bytes(pdf_bytes)
                payload["pdf_filename"] = pdf_filename
                pdf_ok = True
                print(f"  📄 PDF generado: {pdf_filename}")
            except Exception as e:
                pdf_error = str(e)
                print(f"  ⚠️  PDF error: {e}")

            # Enviar email
            email_ok    = False
            email_error = ""
            cfg = load_config()
            email_cfg = cfg.get("email", {})
            if pdf_ok and email_cfg.get("enabled") and payload.get("email"):
                nombre = f"{payload.get('nombre','')} {payload.get('apellido','')}".strip()
                ok, msg = send_email(
                    email_cfg,
                    payload["email"],
                    nombre,
                    pdf_bytes,
                    pdf_filename,
                )
                email_ok    = ok
                email_error = "" if ok else msg
                print(f"  {'✉️ ' if ok else '⚠️ '} Email {'enviado' if ok else 'error: ' + msg}")

            # Guardar en Notion
            notion_ok    = False
            notion_error = ""
            notion_cfg   = cfg.get("notion", {})
            if notion_cfg.get("enabled"):
                n_ok, page_id, n_msg = save_to_notion(notion_cfg, payload, pdf_filename)
                notion_ok    = n_ok
                notion_error = "" if n_ok else n_msg
                if n_ok:
                    payload["guardado_en_notion"] = True
                    payload["notion_page_id"]     = page_id
                    print(f"  📋 Guardado en Notion: {page_id}")
                else:
                    print(f"  ⚠️  Notion error: {n_msg}")

            # Guardar JSON
            payload["email_enviado"] = email_ok
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

            print(f"  ✅ Resultado guardado: {json_file.name}")

            self._respond(200, {
                "ok":           True,
                "archivo":      json_file.name,
                "pdf":          pdf_filename,
                "pdf_ok":       pdf_ok,
                "pdf_error":    pdf_error,
                "email_ok":     email_ok,
                "email_error":  email_error,
                "notion_ok":    notion_ok,
                "notion_error": notion_error,
            })

        except Exception as e:
            print(f"  ❌ Error al guardar: {e}")
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── RATING ──────────────────────────────────────────────
    def _handle_rating(self):
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            archivo     = payload.get("archivo", "")
            puntuacion  = payload.get("puntuacion")

            if not archivo or puntuacion is None:
                self._respond(400, {"ok": False, "error": "Faltan datos"})
                return

            json_file = RESULTS_DIR / archivo
            if not json_file.exists():
                self._respond(404, {"ok": False, "error": "Archivo no encontrado"})
                return

            data = json.loads(json_file.read_text(encoding="utf-8"))
            data["puntuacion"] = int(puntuacion)

            notion_ok    = False
            notion_error = ""
            cfg = load_config()
            notion_cfg = cfg.get("notion", {})
            page_id = data.get("notion_page_id", "")
            if notion_cfg.get("enabled") and page_id:
                ok, msg = update_notion_rating(notion_cfg, page_id, int(puntuacion))
                notion_ok    = ok
                notion_error = "" if ok else msg
                if ok:
                    print(f"  ⭐ Puntuación {puntuacion}/10 actualizada en Notion")
                else:
                    print(f"  ⚠️  Notion rating error: {msg}")

            json_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            self._respond(200, {"ok": True, "notion_ok": notion_ok, "notion_error": notion_error})

        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── COMMENT / APORTE ────────────────────────────────────
    def _handle_save_comment(self):
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))

            comentario = payload.get("comentario", "").strip()
            if not comentario:
                self._respond(400, {"ok": False, "error": "Comentario vacío"})
                return

            ts_slug  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = COMMENTS_DIR / f"{ts_slug}.json"

            is_expert = payload.get("es_experto", False)
            data = {
                "nombre":      payload.get("nombre", ""),
                "email":       payload.get("email", ""),
                "perfil":      payload.get("perfil", ""),
                "temperamento": payload.get("temperamento", ""),
                "puntuacion":  payload.get("puntuacion"),
                "comentario":  comentario,
                "es_experto":  is_expert,
                "especialidad": payload.get("especialidad", ""),
                "credenciales": payload.get("credenciales", ""),
                "archivo_resultado": payload.get("archivo_resultado", ""),
                "fecha":       datetime.datetime.now().strftime("%Y-%m-%d"),
                "aprobado":    False,
            }
            filename.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            tipo = "experto" if is_expert else "usuario"
            print(f"  💬 Comentario de {tipo} guardado: {filename.name}")
            self._respond(200, {"ok": True, "archivo": filename.name})

        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _handle_list_comments(self):
        try:
            comments = []
            for f in sorted(COMMENTS_DIR.glob("*.json"), reverse=True):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    comments.append({
                        "archivo":     f.name,
                        "nombre":      data.get("nombre", ""),
                        "email":       data.get("email", ""),
                        "perfil":      data.get("perfil", ""),
                        "temperamento": data.get("temperamento", ""),
                        "puntuacion":  data.get("puntuacion"),
                        "comentario":  data.get("comentario", ""),
                        "es_experto":  data.get("es_experto", False),
                        "especialidad": data.get("especialidad", ""),
                        "credenciales": data.get("credenciales", ""),
                        "fecha":       data.get("fecha", ""),
                        "aprobado":    data.get("aprobado", False),
                    })
                except Exception:
                    pass
            self._respond(200, {"ok": True, "comments": comments})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _handle_approve_comment(self):
        """Aprueba un aporte de experto y lo convierte en fuente de conocimiento."""
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            archivo = payload.get("archivo", "")

            comment_file = COMMENTS_DIR / archivo
            if not comment_file.exists():
                self._respond(404, {"ok": False, "error": "Archivo no encontrado"})
                return

            data = json.loads(comment_file.read_text(encoding="utf-8"))
            data["aprobado"] = True
            comment_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

            # Crear automáticamente como fuente de conocimiento
            ts_slug  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            trans_file = TRANS_DIR / f"{ts_slug}_experto.json"
            autor = data.get("nombre", "Experto")
            if data.get("especialidad"):
                autor += f" — {data['especialidad']}"
            if data.get("credenciales"):
                autor += f" ({data['credenciales']})"

            trans_data = {
                "titulo":    f"Aporte de Experto: {data.get('perfil','Perfil')}",
                "tipo":      "opinion",
                "autor":     autor,
                "contenido": (
                    f"Perfil analizado: {data.get('perfil', '')} "
                    f"({data.get('temperamento', '')})\n"
                    f"Puntuacion de precision: {data.get('puntuacion', 'N/A')}/10\n\n"
                    f"Comentario del experto:\n{data.get('comentario', '')}"
                ),
                "fecha":  data.get("fecha", ""),
                "synced": False,
            }
            trans_file.write_text(json.dumps(trans_data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  🎓 Aporte de experto aprobado → fuente: {trans_file.name}")
            self._respond(200, {"ok": True, "fuente": trans_file.name})

        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── ELIMINAR RESULTADO ───────────────────────────────────
    def _handle_delete_user(self):
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            archivo = payload.get("archivo", "")
            if not archivo:
                self._respond(400, {"ok": False, "error": "Falta archivo"})
                return
            json_file = RESULTS_DIR / archivo
            if not json_file.exists():
                self._respond(404, {"ok": False, "error": "Resultado no encontrado"})
                return
            # Leer el JSON para saber el nombre del PDF asociado
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                pdf_name = data.get("pdf_filename", "")
            except Exception:
                pdf_name = ""
            # Borrar JSON
            json_file.unlink()
            # Borrar PDF si existe
            if pdf_name:
                pdf_file = PDFS_DIR / pdf_name
                if pdf_file.exists():
                    pdf_file.unlink()
            print(f"  🗑️  Resultado eliminado: {archivo}")
            self._respond(200, {"ok": True})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── PERFILES ANALIZADOS ─────────────────────────────────
    def _handle_save_perfil(self):
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))

            nombre = payload.get("nombre", "").strip()
            if not nombre:
                self._respond(400, {"ok": False, "error": "Nombre requerido"})
                return

            ts_slug  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = PERFILES_DIR / f"{ts_slug}.json"

            data = {
                "nombre":      nombre,
                "contexto":    payload.get("contexto", ""),
                "fisico":      payload.get("fisico", ""),
                "notas":       payload.get("notas", ""),
                "dominant":    payload.get("dominant", ""),
                "secondary":   payload.get("secondary", ""),
                "dominant_name":  payload.get("dominant_name", ""),
                "secondary_name": payload.get("secondary_name", ""),
                "perfil":      payload.get("perfil", ""),
                "confianza":   payload.get("confianza", 0),
                "scores":      payload.get("scores", {}),
                "profile":     payload.get("profile", {}),
                "linked_user": payload.get("linked_user", None),
                "fecha":       datetime.datetime.now().strftime("%Y-%m-%d"),
                "timestamp":   datetime.datetime.now().isoformat(),
            }
            filename.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  🔍 Perfil analizado guardado: {filename.name}")
            self._respond(200, {"ok": True, "archivo": filename.name})

        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _handle_list_perfiles(self):
        try:
            perfiles = []
            for f in sorted(PERFILES_DIR.glob("*.json"), reverse=True):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    perfiles.append({
                        "archivo":       f.name,
                        "nombre":        data.get("nombre", ""),
                        "contexto":      data.get("contexto", ""),
                        "dominant":      data.get("dominant", ""),
                        "secondary":     data.get("secondary", ""),
                        "dominant_name": data.get("dominant_name", ""),
                        "secondary_name": data.get("secondary_name", ""),
                        "perfil":        data.get("perfil", ""),
                        "confianza":     data.get("confianza", 0),
                        "linked_user":   data.get("linked_user"),
                        "fecha":         data.get("fecha", ""),
                        "profile":       data.get("profile", {}),
                        "scores":        data.get("scores", {}),
                    })
                except Exception:
                    pass
            self._respond(200, {"ok": True, "perfiles": perfiles})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── USERS LIST ──────────────────────────────────────────
    def _handle_users(self):
        try:
            users = []
            for f in sorted(RESULTS_DIR.glob("*.json"), reverse=True):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    dom  = data.get("dominant", "")
                    sec  = data.get("secondary", "")
                    users.append({
                        "archivo":    f.name,
                        "nombre":     data.get("nombre", ""),
                        "apellido":   data.get("apellido", ""),
                        "email":      data.get("email", ""),
                        "timestamp":  data.get("timestamp", ""),
                        "dominant":   dom,
                        "secondary":  sec,
                        "dominant_name":  TYPE_NAMES.get(dom, dom),
                        "secondary_name": TYPE_NAMES.get(sec, sec),
                        "perfil":     data.get("perfil", ""),
                        "con_foto":   data.get("conFoto", False),
                        "pdf":        data.get("pdf_filename", ""),
                        "email_enviado": data.get("email_enviado", False),
                        "profile":    data.get("profile", {}),
                        "scores":     data.get("scores", {}),
                        "puntuacion": data.get("puntuacion"),
                    })
                except Exception:
                    pass
            self._respond(200, {"ok": True, "users": users})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── SERVE PDF ───────────────────────────────────────────
    def _handle_serve_pdf(self):
        filename = self.path.replace("/api/pdf/", "").strip("/")
        pdf_path = PDFS_DIR / filename
        if not pdf_path.exists() or not filename.endswith(".pdf"):
            self._respond(404, {"ok": False, "error": "PDF no encontrado"})
            return
        data = pdf_path.read_bytes()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type",        "application/pdf")
        self.send_header("Content-Disposition", f'inline; filename="{filename}"')
        self.send_header("Content-Length",      str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ─── TRANSCRIPCIONES ─────────────────────────────────────
    def _handle_save_transcription(self):
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            titulo    = payload.get("titulo", "").strip()
            contenido = payload.get("contenido", "").strip()
            if not titulo or not contenido:
                self._respond(400, {"ok": False, "error": "Faltan campos"})
                return
            ts_slug  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = TRANS_DIR / f"{ts_slug}.json"
            data = {
                "titulo":    titulo,
                "tipo":      payload.get("tipo", "transcripcion"),
                "autor":     payload.get("autor", ""),
                "contenido": contenido,
                "fecha":     datetime.datetime.now().strftime("%Y-%m-%d"),
                "synced":    False,
            }
            filename.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  📚 Transcripción guardada: {filename.name}")
            self._respond(200, {"ok": True, "archivo": filename.name})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _handle_list_transcriptions(self):
        try:
            transcriptions = []
            for f in sorted(TRANS_DIR.glob("*.json"), reverse=True):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    transcriptions.append({
                        "archivo":  f.name,
                        "titulo":   data.get("titulo", ""),
                        "tipo":     data.get("tipo", ""),
                        "autor":    data.get("autor", ""),
                        "fecha":    data.get("fecha", ""),
                        "synced":   data.get("synced", False),
                    })
                except Exception:
                    pass
            self._respond(200, {"ok": True, "transcriptions": transcriptions})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _handle_notebooklm_export(self):
        try:
            files = sorted(TRANS_DIR.glob("*.json"))
            new_files = []
            all_data  = []
            for f in files:
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    all_data.append((f, data))
                    if not data.get("synced"):
                        new_files.append(f)
                except Exception:
                    pass

            if not all_data:
                self._respond(404, {"ok": False, "error": "No hay transcripciones"})
                return

            lines = [
                "═══════════════════════════════════════════════════════",
                "  BIOTIPOS — BASE DE CONOCIMIENTO EXPERTO",
                f"  Exportado: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
                f"  Total de fuentes: {len(all_data)}",
                "═══════════════════════════════════════════════════════",
                "",
            ]
            for _, data in all_data:
                lines += [
                    f"━━━ {data.get('titulo','Sin título')} ━━━",
                    f"Tipo: {data.get('tipo','')}",
                    f"Autor: {data.get('autor','Desconocido')}",
                    f"Fecha: {data.get('fecha','')}",
                    "",
                    data.get("contenido", ""),
                    "",
                    "",
                ]
            content = "\n".join(lines).encode("utf-8")

            for f in new_files:
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    data["synced"] = True
                    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                except Exception:
                    pass

            print(f"  📓 NotebookLM export: {len(all_data)} fuentes ({len(new_files)} nuevas)")

            self.send_response(200)
            self._cors()
            self.send_header("Content-Type",        "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=biotipos_fuentes.txt")
            self.send_header("Content-Length",      str(len(content)))
            self.send_header("X-New-Count",         str(len(new_files)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── HELPER ──────────────────────────────────────────────
    def _respond(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type",   "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    os.chdir(BASE_DIR)
    print(f"\n  🧬 App Biotipos — Servidor local")
    print(f"  ────────────────────────────────────")
    print(f"  URL:        http://localhost:{PORT}")
    print(f"  Resultados: {RESULTS_DIR}")
    print(f"  PDFs:       {PDFS_DIR}")
    print(f"  Ctrl+C para detener\n")
    httpd = http.server.HTTPServer(("", PORT), BiotipesHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor detenido.")
