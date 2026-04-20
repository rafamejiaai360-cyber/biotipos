#!/usr/bin/env python3
# Auto-configure Homebrew native libs for WeasyPrint on macOS (must run before any import)
import os, sys
if sys.platform == "darwin":
    _hb = "/opt/homebrew/lib"
    if _hb not in os.environ.get("DYLD_LIBRARY_PATH", ""):
        os.environ["DYLD_LIBRARY_PATH"] = _hb + (":" + os.environ["DYLD_LIBRARY_PATH"] if os.environ.get("DYLD_LIBRARY_PATH") else "")
        os.execv(sys.executable, [sys.executable] + sys.argv)

"""
server.py — Servidor App Biotipos
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
FOTOS_DIR      = BASE_DIR / "fotos"
CONOCIMIENTO_DIR = BASE_DIR / "conocimiento"
TRANS_DIR   = BASE_DIR / "transcripciones"
COMMENTS_DIR = BASE_DIR / "comentarios"
PERFILES_DIR = BASE_DIR / "perfiles_analizados"
CONFIG_FILE = BASE_DIR / "config.json"

for _d in (RESULTS_DIR, PDFS_DIR, FOTOS_DIR, CONOCIMIENTO_DIR, TRANS_DIR, COMMENTS_DIR, PERFILES_DIR):
    _d.mkdir(exist_ok=True)


def parse_conocimiento_text(text):
    """Parsea un .txt con secciones [BIOTIPO] y retorna dict {biotipo: [snippets]}."""
    import re
    tag_map = {
        "COLERICO": "c", "COLERICO": "c", "C": "c",
        "SANGUINEO": "s", "S": "s",
        "FLEMATICO": "f", "FLEMATICO": "f", "F": "f",
        "MELANCOLICO": "m", "M": "m",
        "GENERAL": "general", "G": "general",
    }
    sections = {}
    current_key = None
    current_lines = []

    def _flush():
        if current_key is None:
            return
        content = "\n".join(current_lines).strip()
        if content:
            sections.setdefault(current_key, []).append(content)

    for line in text.splitlines():
        m = re.match(r"^\[([A-ZÁÉÍÓÚÜÑ]+)\]\s*$", line.strip(), re.IGNORECASE)
        if m:
            _flush()
            tag = m.group(1).upper()
            tag = (tag.replace("Á","A").replace("É","E").replace("Í","I")
                      .replace("Ó","O").replace("Ú","U").replace("Ü","U").replace("Ñ","N"))
            current_key = tag_map.get(tag)
            current_lines = []
        elif current_key is not None:
            current_lines.append(line)
    _flush()
    return sections


def get_conocimiento_for_biotipo(biotipo):
    """Devuelve lista de snippets relevantes para el biotipo dado."""
    snippets = []
    for f in sorted(CONOCIMIENTO_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            secs = data.get("sections", {})
            snippets.extend(secs.get(biotipo, []))
            snippets.extend(secs.get("general", []))
        except Exception:
            pass
    return snippets


def load_config():
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {
            "admin": {
                "password": os.environ.get("ADMIN_PASSWORD", "")
            },
            "notion": {
                "enabled":              os.environ.get("NOTION_ENABLED", "false").lower() == "true",
                "token":                os.environ.get("NOTION_TOKEN", ""),
                "database_id":          os.environ.get("NOTION_DATABASE_ID", ""),
                "conocimiento_db_id":   os.environ.get("NOTION_CONOCIMIENTO_DB_ID", ""),
            },
            "email": {"enabled": False}
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

NOTION_VERSION = "2026-03-11"
NOTION_BASE    = "https://api.notion.com/v1"


def _notion_req(method, path, token, body=None, timeout=15):
    url  = f"{NOTION_BASE}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Authorization": f"Bearer {token}", "Notion-Version": NOTION_VERSION}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def notion_upload_file(token, file_bytes, filename, content_type):
    """Sube un archivo a Notion Files API. Devuelve upload_id o None."""
    try:
        # Paso 1: crear el objeto de upload
        result    = _notion_req("POST", "/file_uploads", token,
                                {"mode": "single_part", "filename": filename,
                                 "content_type": content_type})
        upload_id = result.get("id")
        if not upload_id:
            print(f"  ⚠️  Notion file upload: no se obtuvo ID — {result}")
            return None

        # Paso 2: enviar el archivo vía multipart/form-data
        boundary  = f"BiotipoBnd{int(datetime.datetime.now().timestamp())}"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

        send_req = urllib.request.Request(
            f"{NOTION_BASE}/file_uploads/{upload_id}/send",
            data=body,
            headers={
                "Authorization":  f"Bearer {token}",
                "Content-Type":   f"multipart/form-data; boundary={boundary}",
                "Notion-Version": NOTION_VERSION,
            },
            method="POST",
        )
        with urllib.request.urlopen(send_req, timeout=60) as resp:
            send_result = json.loads(resp.read())

        if send_result.get("status") != "uploaded":
            print(f"  ⚠️  Notion file upload status: {send_result.get('status')}")
            return None

        print(f"  ✅ Archivo subido a Notion: {filename}")
        return upload_id
    except urllib.error.HTTPError as e:
        print(f"  ⚠️  Notion file upload HTTP {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"  ⚠️  Notion file upload: {e}")
        return None


def notion_store_json_block(token, page_id, data_dict):
    """Guarda el JSON completo como code block en la página de Notion."""
    json_str = json.dumps(data_dict, ensure_ascii=False)
    chunks   = [json_str[i:i+2000] for i in range(0, len(json_str), 2000)]
    _notion_req("PATCH", f"/blocks/{page_id}/children", token, {
        "children": [{
            "object": "block", "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": c}} for c in chunks],
                "language": "json",
            },
        }]
    })


def save_conocimiento_to_notion(notion_cfg, doc_data):
    """Guarda un documento de conocimiento en la base de datos de Notion."""
    token  = notion_cfg.get("token", "")
    db_id  = notion_cfg.get("conocimiento_db_id", "")
    if not token or not db_id:
        return False
    try:
        result = _notion_req("POST", "/pages", token, {
            "parent":     {"database_id": db_id},
            "properties": {
                "Name": {"title": [{"text": {"content": doc_data.get("titulo", "Sin título")}}]},
            },
        })
        page_id = result.get("id", "")
        if page_id:
            notion_store_json_block(token, page_id, doc_data)
            print(f"  🧠 Conocimiento guardado en Notion: {doc_data.get('titulo')}")
            return True
    except Exception as e:
        print(f"  ⚠️  Error guardando conocimiento en Notion: {e}")
    return False


def restore_conocimiento_from_notion(notion_cfg):
    """Restaura los documentos de conocimiento desde Notion si la carpeta está vacía."""
    if list(CONOCIMIENTO_DIR.glob("*.json")):
        return
    token = notion_cfg.get("token", "")
    db_id = notion_cfg.get("conocimiento_db_id", "")
    if not token or not db_id:
        return
    print("  🔄 Restaurando base de conocimiento desde Notion...")
    restored = 0
    try:
        has_more = True
        cursor   = None
        while has_more:
            body = {"page_size": 100}
            if cursor:
                body["start_cursor"] = cursor
            result   = _notion_req("POST", f"/databases/{db_id}/query", token, body)
            has_more = result.get("has_more", False)
            cursor   = result.get("next_cursor")
            for page in result.get("results", []):
                page_id = page["id"]
                try:
                    blocks = _notion_req("GET", f"/blocks/{page_id}/children", token)
                    for block in blocks.get("results", []):
                        if block.get("type") != "code":
                            continue
                        json_str = "".join(
                            rt.get("text", {}).get("content", "")
                            for rt in block.get("code", {}).get("rich_text", [])
                        )
                        try:
                            data     = json.loads(json_str)
                            filename = data.get("filename") or f"{page_id[:8]}.json"
                            (CONOCIMIENTO_DIR / filename).write_text(
                                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
                            )
                            restored += 1
                        except Exception:
                            pass
                        break
                except Exception:
                    continue
        print(f"  ✅ Restaurados {restored} documentos de conocimiento")
    except Exception as e:
        print(f"  ⚠️  Error restaurando conocimiento: {e}")


def restore_from_notion(cfg):
    """Si resultados/ está vacío, descarga todos los registros desde Notion."""
    if list(RESULTS_DIR.glob("*.json")):
        return
    token       = cfg.get("token", "")
    database_id = cfg.get("database_id", "")
    if not token or not database_id:
        return

    print("  🔄 Restaurando datos desde Notion...")
    restored = 0
    has_more = True
    cursor   = None

    try:
        while has_more:
            body = {"page_size": 100}
            if cursor:
                body["start_cursor"] = cursor
            result   = _notion_req("POST", f"/databases/{database_id}/query", token, body)
            has_more = result.get("has_more", False)
            cursor   = result.get("next_cursor")

            for page in result.get("results", []):
                page_id = page["id"]
                try:
                    blocks = _notion_req("GET", f"/blocks/{page_id}/children", token)
                    for block in blocks.get("results", []):
                        if block.get("type") != "code":
                            continue
                        json_str = "".join(
                            rt.get("text", {}).get("content", "")
                            for rt in block.get("code", {}).get("rich_text", [])
                        )
                        try:
                            data = json.loads(json_str)
                        except Exception:
                            continue
                        archivo = data.get("archivo", "")
                        if not archivo:
                            ts   = data.get("timestamp", datetime.datetime.now().isoformat())
                            slug = data.get("email", "usuario").split("@")[0].replace(".", "_")
                            ts_s = ts[:19].replace("-","").replace(":","").replace("T","_")
                            archivo = f"{ts_s}_{slug}.json"
                        (RESULTS_DIR / archivo).write_text(
                            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
                        )
                        # Restaurar foto si tiene URL de Notion
                        foto_url  = data.get("notion_foto_url", "")
                        foto_name = data.get("foto_filename", "")
                        if foto_url and foto_name and not (FOTOS_DIR / foto_name).exists():
                            try:
                                with urllib.request.urlopen(foto_url, timeout=15) as r:
                                    (FOTOS_DIR / foto_name).write_bytes(r.read())
                            except Exception:
                                pass
                        restored += 1
                        break
                except Exception:
                    continue

        print(f"  ✅ Restaurados {restored} registros desde Notion")
    except Exception as e:
        print(f"  ⚠️  Error restaurando desde Notion: {e}")


def save_to_notion(cfg, payload, pdf_filename=None, photo_bytes=None,
                   photo_mime=None, pdf_bytes=None):
    """Crea página en Notion, sube foto y PDF, guarda JSON completo como backup."""
    try:
        token       = cfg.get("token", "")
        database_id = cfg.get("database_id", "")
        if not token or not database_id:
            return False, None, "Token o database_id no configurados"

        dom      = payload.get("dominant", "")
        sec      = payload.get("secondary", "")
        scores   = payload.get("scores", {})
        nombre   = payload.get("nombre", "")
        apellido = payload.get("apellido", "")

        properties = {
            "Nombre":                 {"title":     [{"text": {"content": nombre}}]},
            "Apellido":               {"rich_text": [{"text": {"content": apellido}}]},
            "Email":                  {"email":     payload.get("email", "")},
            "Temperamento Dominante": {"select":    {"name": TYPE_NAMES.get(dom, dom)}},
            "Temperamento Secundario":{"select":    {"name": TYPE_NAMES.get(sec, sec)}},
            "Perfil":                 {"rich_text": [{"text": {"content": payload.get("perfil", "")[:2000]}}]},
            "Con Foto":               {"select":    {"name": "Sí" if payload.get("conFoto") else "No"}},
            "Puntaje Colérico":    {"number": scores.get("c", 0)},
            "Puntaje Sanguíneo":   {"number": scores.get("s", 0)},
            "Puntaje Flemático":   {"number": scores.get("f", 0)},
            "Puntaje Melancólico": {"number": scores.get("m", 0)},
        }

        result  = _notion_req("POST", "/pages", token,
                              {"parent": {"database_id": database_id}, "properties": properties})
        page_id = result.get("id", "")
        if not page_id:
            return False, None, "No se obtuvo page_id"

        extra_blocks = []

        # ── Subir foto como adjunto en columna "Foto" ────────
        if photo_bytes and photo_mime:
            foto_name = payload.get("foto_filename", "foto.jpg")
            print(f"  🔄 Iniciando upload foto: {foto_name} ({len(photo_bytes)} bytes, {photo_mime})")
            fid = notion_upload_file(token, photo_bytes, foto_name, photo_mime)
            print(f"  🔑 foto upload_id: {fid}")
            if fid:
                try:
                    _notion_req("PATCH", f"/pages/{page_id}", token, {
                        "properties": {
                            "Foto": {"files": [
                                {"type": "file_upload", "file_upload": {"id": fid}, "name": foto_name}
                            ]}
                        }
                    })
                    print(f"  📸 Foto adjunta en Notion")
                except urllib.error.HTTPError as e:
                    print(f"  ⚠️  PATCH Foto HTTP {e.code}: {e.read().decode()}")
                except Exception as e:
                    print(f"  ⚠️  PATCH Foto: {e}")

        # ── Subir PDF como adjunto en columna "PDF" ──────────
        if pdf_bytes and pdf_filename:
            print(f"  🔄 Iniciando upload PDF: {pdf_filename} ({len(pdf_bytes)} bytes)")
            pid = notion_upload_file(token, pdf_bytes, pdf_filename, "application/pdf")
            print(f"  🔑 PDF upload_id: {pid}")
            if pid:
                try:
                    _notion_req("PATCH", f"/pages/{page_id}", token, {
                        "properties": {
                            "PDF": {"files": [
                                {"type": "file_upload", "file_upload": {"id": pid}, "name": pdf_filename}
                            ]}
                        }
                    })
                    print(f"  📄 PDF adjunto en Notion")
                except urllib.error.HTTPError as e:
                    print(f"  ⚠️  PATCH PDF HTTP {e.code}: {e.read().decode()}")
                except Exception as e:
                    print(f"  ⚠️  PATCH PDF: {e}")

        if extra_blocks:
            _notion_req("PATCH", f"/blocks/{page_id}/children", token, {"children": extra_blocks})

        # ── Guardar JSON completo como código (backup para restore) ──
        try:
            notion_store_json_block(token, page_id, payload)
        except Exception as e:
            print(f"  ⚠️  JSON block en Notion: {e}")

        return True, page_id, "OK"

    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        return False, None, f"HTTP {e.code}: {msg}"
    except Exception as e:
        return False, None, str(e)


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
                "Notion-Version": NOTION_VERSION,
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
        elif self.path.startswith("/api/foto/"):
            self._handle_serve_foto()
        elif self.path == "/api/conocimiento":
            self._require_admin()
            self._handle_list_conocimiento()
        elif self.path.startswith("/api/conocimiento/"):
            self._handle_conocimiento_biotipo()
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
        elif self.path == "/api/test-notion":
            self._require_admin()
            self._handle_test_notion()
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
        elif self.path == "/api/conocimiento":
            self._require_admin()
            self._handle_upload_conocimiento()
        elif self.path == "/api/delete-conocimiento":
            self._require_admin()
            self._handle_delete_conocimiento()
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

            # Guardar nombre de archivo en el JSON (para restore desde Notion)
            payload["archivo"] = json_file.name

            # Guardar foto si viene en el payload
            foto_filename = None
            photo_bytes   = None
            photo_b64  = payload.pop("photoBase64",  None)
            photo_mime = payload.pop("photoMimeType", None) or "image/jpeg"
            if photo_b64:
                import base64
                photo_bytes = base64.b64decode(photo_b64)
                ext = photo_mime.split("/")[-1].split(";")[0] or "jpg"
                foto_filename = f"{base_name}.{ext}"
                (FOTOS_DIR / foto_filename).write_bytes(photo_bytes)
                payload["foto_filename"] = foto_filename
                print(f"  🖼️  Foto guardada: {foto_filename}")

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
                n_ok, page_id, n_msg = save_to_notion(
                    notion_cfg, payload, pdf_filename,
                    photo_bytes=photo_bytes, photo_mime=photo_mime,
                    pdf_bytes=pdf_bytes,
                )
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
            # Restaurar desde Notion si no hay archivos locales (post-redeploy)
            if not list(RESULTS_DIR.glob("*.json")):
                cfg = load_config()
                if cfg.get("notion", {}).get("enabled"):
                    restore_from_notion(cfg.get("notion", {}))

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
                        "con_foto":      data.get("conFoto", False),
                        "foto_filename": data.get("foto_filename", ""),
                        "pdf":           data.get("pdf_filename", ""),
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
        if not filename.endswith(".pdf"):
            self._respond(404, {"ok": False, "error": "PDF no encontrado"})
            return
        if not pdf_path.exists():
            # Intentar regenerar desde JSON local
            base      = filename[:-4]
            json_path = RESULTS_DIR / f"{base}.json"
            if not json_path.exists():
                # Intentar restaurar desde Notion primero
                cfg = load_config()
                if cfg.get("notion", {}).get("enabled"):
                    restore_from_notion(cfg.get("notion", {}))
            if json_path.exists():
                try:
                    from pdf_generator import generate_pdf
                    data      = json.loads(json_path.read_text(encoding="utf-8"))
                    pdf_data  = build_pdf_data(data, json_path)
                    pdf_bytes = generate_pdf(pdf_data)
                    pdf_path.write_bytes(pdf_bytes)
                    print(f"  📄 PDF regenerado: {filename}")
                except Exception as e:
                    print(f"  ⚠️  No se pudo regenerar PDF: {e}")
                    self._respond(404, {"ok": False, "error": "PDF no disponible"})
                    return
            else:
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

    # ─── SERVE FOTO ──────────────────────────────────────────
    def _handle_serve_foto(self):
        filename  = self.path.replace("/api/foto/", "").strip("/")
        foto_path = FOTOS_DIR / filename
        if not foto_path.exists():
            # Buscar notion_foto_url en el JSON correspondiente
            base = filename.rsplit(".", 1)[0]
            json_path = RESULTS_DIR / f"{base}.json"
            notion_url = ""
            if json_path.exists():
                try:
                    notion_url = json.loads(json_path.read_text(encoding="utf-8")).get("notion_foto_url", "")
                except Exception:
                    pass
            if notion_url:
                try:
                    with urllib.request.urlopen(notion_url, timeout=15) as r:
                        foto_bytes = r.read()
                    foto_path.write_bytes(foto_bytes)
                except Exception:
                    self._respond(404, {"ok": False, "error": "Foto no disponible"})
                    return
            else:
                self._respond(404, {"ok": False, "error": "Foto no encontrada"})
                return
        ext = filename.rsplit(".", 1)[-1].lower()
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "gif": "image/gif", "webp": "image/webp", "heic": "image/heic",
                "avif": "image/avif"}.get(ext, "image/jpeg")
        data = foto_path.read_bytes()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type",   mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ─── BASE DE CONOCIMIENTO ────────────────────────────────
    def _handle_upload_conocimiento(self):
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            titulo   = payload.get("titulo", "").strip()
            contenido = payload.get("contenido", "").strip()
            if not titulo or not contenido:
                self._respond(400, {"ok": False, "error": "Faltan campos"})
                return
            sections = parse_conocimiento_text(contenido)
            ts_slug  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{ts_slug}.json"
            data = {
                "filename":  filename,
                "titulo":    titulo,
                "timestamp": datetime.datetime.now().isoformat(),
                "contenido": contenido,
                "sections":  sections,
            }
            (CONOCIMIENTO_DIR / filename).write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            # Guardar también en Notion
            cfg = load_config()
            notion_cfg = cfg.get("notion", {})
            if notion_cfg.get("enabled"):
                save_conocimiento_to_notion(notion_cfg, data)
            print(f"  🧠 Conocimiento cargado: {filename} — secciones: {list(sections.keys())}")
            self._respond(200, {"ok": True, "filename": filename, "sections": list(sections.keys())})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _handle_list_conocimiento(self):
        try:
            docs = []
            for f in sorted(CONOCIMIENTO_DIR.glob("*.json"), reverse=True):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    docs.append({
                        "filename":  f.name,
                        "titulo":    data.get("titulo", ""),
                        "timestamp": data.get("timestamp", ""),
                        "secciones": list(data.get("sections", {}).keys()),
                    })
                except Exception:
                    pass
            self._respond(200, {"ok": True, "docs": docs})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _handle_conocimiento_biotipo(self):
        biotipo = self.path.replace("/api/conocimiento/", "").strip("/")
        snippets = get_conocimiento_for_biotipo(biotipo)
        self._respond(200, {"ok": True, "biotipo": biotipo, "snippets": snippets})

    def _handle_delete_conocimiento(self):
        try:
            length   = int(self.headers.get("Content-Length", 0))
            payload  = json.loads(self.rfile.read(length))
            filename = payload.get("filename", "")
            path     = CONOCIMIENTO_DIR / filename
            if not path.exists() or not filename.endswith(".json"):
                self._respond(404, {"ok": False, "error": "Documento no encontrado"})
                return
            path.unlink()
            self._respond(200, {"ok": True})
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    # ─── DIAGNÓSTICO NOTION ──────────────────────────────────
    def _handle_test_notion(self):
        """GET /api/test-notion — prueba la integración con Notion Files API."""
        cfg = load_config()
        notion_cfg = cfg.get("notion", {})
        results = {}

        if not notion_cfg.get("enabled") or not notion_cfg.get("token"):
            self._respond(200, {"ok": False, "error": "Notion no configurado"})
            return

        token = notion_cfg["token"]

        # Test 1: Query database
        try:
            r = _notion_req("POST", f"/databases/{notion_cfg['database_id']}/query", token, {"page_size": 1})
            results["database_query"] = "OK"
        except Exception as e:
            results["database_query"] = str(e)

        # Test 2: Create file upload object (1x1 pixel PNG)
        import base64
        tiny_png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )
        try:
            r = _notion_req("POST", "/file_uploads", token, {
                "mode": "single_part",
                "filename": "test.png",
                "content_type": "image/png",
            })
            upload_id = r.get("id")
            results["create_upload"] = f"OK — id={upload_id}"

            # Test 3: Send file
            if upload_id:
                boundary = "BiotipoDiag"
                body = (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="file"; filename="test.png"\r\n'
                    f"Content-Type: image/png\r\n\r\n"
                ).encode("utf-8") + tiny_png + f"\r\n--{boundary}--\r\n".encode("utf-8")
                send_req = urllib.request.Request(
                    f"{NOTION_BASE}/file_uploads/{upload_id}/send",
                    data=body,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": f"multipart/form-data; boundary={boundary}",
                        "Notion-Version": NOTION_VERSION,
                    },
                    method="POST",
                )
                try:
                    with urllib.request.urlopen(send_req, timeout=30) as resp:
                        sr = json.loads(resp.read())
                    results["send_file"] = f"OK — status={sr.get('status')}"
                except urllib.error.HTTPError as e:
                    results["send_file"] = f"HTTP {e.code}: {e.read().decode()}"
                except Exception as e:
                    results["send_file"] = str(e)
        except urllib.error.HTTPError as e:
            results["create_upload"] = f"HTTP {e.code}: {e.read().decode()}"
        except Exception as e:
            results["create_upload"] = str(e)

        self._respond(200, {"ok": True, "tests": results})

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
    print(f"  Ctrl+C para detener\n")

    # Restaurar datos desde Notion si el servidor arrancó sin archivos locales
    _startup_cfg    = load_config()
    _startup_notion = _startup_cfg.get("notion", {})
    if _startup_notion.get("enabled"):
        restore_from_notion(_startup_notion)
        restore_conocimiento_from_notion(_startup_notion)

    httpd = http.server.HTTPServer(("", PORT), BiotipesHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor detenido.")
