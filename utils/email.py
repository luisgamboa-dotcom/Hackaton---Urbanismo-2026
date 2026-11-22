"""Email service for sending notifications."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from config.settings import get_settings

settings = get_settings()


class EmailService:
    """Email service using SMTP."""

    def __init__(self) -> None:
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.smtp_use_tls = settings.smtp_use_tls
        self.email_from = settings.email_from or settings.smtp_username

    def is_configured(self) -> bool:
        """Check if email service is configured."""
        return bool(self.smtp_username and self.smtp_password and self.email_from)

    def _create_connection(self) -> smtplib.SMTP | smtplib.SMTP_SSL:
        """Create SMTP connection."""
        if self.smtp_port == 465:
            # SSL connection
            conn: smtplib.SMTP | smtplib.SMTP_SSL = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        else:
            # STARTTLS connection
            conn = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_use_tls:
                conn.starttls()

        if self.smtp_username and self.smtp_password:
            conn.login(self.smtp_username, self.smtp_password)

        return conn

    def send_email(
        self,
        to: str | list[str],
        subject: str,
        body_text: str,
        body_html: str | None = None,
    ) -> bool:
        """Send an email.

        Args:
            to: Recipient email address or list of addresses
            subject: Email subject
            body_text: Plain text body
            body_html: Optional HTML body

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_configured():
            print("Email service not configured, skipping send")
            return False

        if isinstance(to, str):
            to = [to]

        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.email_from
            msg["To"] = ", ".join(to)
            msg["Subject"] = subject

            # Add plain text part
            msg.attach(MIMEText(body_text, "plain", "utf-8"))

            # Add HTML part if provided
            if body_html:
                msg.attach(MIMEText(body_html, "html", "utf-8"))

            with self._create_connection() as conn:
                conn.send_message(msg)

            print(f"Email sent successfully to {', '.join(to)}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_request_notification(
        self,
        request_data: dict[str, Any],
        to: str | None = None,
    ) -> bool:
        """Send notification for a new citizen request.

        Args:
            request_data: Dictionary with request details
            to: Optional override for recipient email

        Returns:
            True if sent successfully
        """
        recipient = to or settings.email_to or self.email_from
        subject = f"[Green Tech] Nueva solicitud: {request_data.get('title', 'Sin título')}"

        body_text = f"""
Nueva solicitud ciudadana recibida en Green Tech.

DETALLES:
- Título: {request_data.get('title', 'N/A')}
- Categoría: {request_data.get('category', 'N/A')}
- Dirección: {request_data.get('address', 'N/A')}
- Comuna: {request_data.get('commune', 'N/A')}
- Coordenadas: {request_data.get('latitude', 'N/A')}, {request_data.get('longitude', 'N/A')}
- Área estimada: {request_data.get('estimated_area_m2', 'No especificada')} m²

DESCRIPCIÓN:
{request_data.get('description', 'Sin descripción')}

NECESIDADES:
{request_data.get('needs', 'Sin necesidades especificadas')}

SOLICITANTE:
- Nombre: {request_data.get('user_name', 'Anónimo')}
- Email: {request_data.get('user_email', 'No disponible')}
- Teléfono: {request_data.get('user_phone', 'No disponible')}
- Comuna: {request_data.get('user_commune', 'No disponible')}

---
Enviado automáticamente desde Green Tech
https://tramaurbanaverde.cl
        """.strip()

        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #2E7D32; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }}
        .field {{ margin-bottom: 12px; }}
        .label {{ font-weight: bold; color: #555; }}
        .value {{ color: #333; }}
        .section {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #888; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🌿 Nueva solicitud en Green Tech</h2>
    </div>
    <div class="content">
        <div class="section">
            <h3>Detalles de la solicitud</h3>
            <div class="field"><span class="label">Título:</span> <span class="value">{request_data.get('title', 'N/A')}</span></div>
            <div class="field"><span class="label">Categoría:</span> <span class="value">{request_data.get('category', 'N/A')}</span></div>
            <div class="field"><span class="label">Dirección:</span> <span class="value">{request_data.get('address', 'N/A')}</span></div>
            <div class="field"><span class="label">Comuna:</span> <span class="value">{request_data.get('commune', 'N/A')}</span></div>
            <div class="field"><span class="label">Coordenadas:</span> <span class="value">{request_data.get('latitude', 'N/A')}, {request_data.get('longitude', 'N/A')}</span></div>
            <div class="field"><span class="label">Área estimada:</span> <span class="value">{request_data.get('estimated_area_m2', 'No especificada')} m²</span></div>
        </div>
        <div class="section">
            <h3>Descripción</h3>
            <p>{request_data.get('description', 'Sin descripción').replace(chr(10), '<br>')}</p>
        </div>
        <div class="section">
            <h3>Necesidades identificadas</h3>
            <p>{request_data.get('needs', 'Sin necesidades especificadas').replace(chr(10), '<br>')}</p>
        </div>
        <div class="section">
            <h3>Solicitante</h3>
            <div class="field"><span class="label">Nombre:</span> <span class="value">{request_data.get('user_name', 'Anónimo')}</span></div>
            <div class="field"><span class="label">Email:</span> <span class="value">{request_data.get('user_email', 'No disponible')}</span></div>
            <div class="field"><span class="label">Teléfono:</span> <span class="value">{request_data.get('user_phone', 'No disponible')}</span></div>
            <div class="field"><span class="label">Comuna:</span> <span class="value">{request_data.get('user_commune', 'No disponible')}</span></div>
        </div>
        <div class="footer">
            Enviado automáticamente desde Green Tech<br>
            <a href="https://tramaurbanaverde.cl">https://tramaurbanaverde.cl</a>
        </div>
    </div>
</body>
</html>
        """.strip()

        return self.send_email(recipient, subject, body_text, body_html)

    def send_support_confirmation(
        self,
        request_data: dict[str, Any],
        supporter_email: str,
        supporter_name: str,
    ) -> bool:
        """Send confirmation email when someone supports a request."""
        subject = f"[Green Tech] Confirmación de apoyo: {request_data.get('title', 'Solicitud')}"

        body_text = f"""
¡Gracias por tu apoyo, {supporter_name}!

Has apoyado la solicitud: "{request_data.get('title', 'Sin título')}"

Esta solicitud ahora cuenta con {request_data.get('support_count', 0)} apoyo(s) ciudadano(s).

Tu apoyo ayuda a que esta iniciativa llegue a las autoridades correspondientes.

---
Green Tech
https://tramaurbanaverde.cl
        """.strip()

        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #2E7D32; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
        .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #888; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>✅ ¡Gracias por tu apoyo!</h2>
    </div>
    <div class="content">
        <p>Hola <strong>{supporter_name}</strong>,</p>
        <p>Has apoyado la solicitud: <strong>"{request_data.get('title', 'Sin título')}"</strong></p>
        <p>Esta solicitud ahora cuenta con <strong>{request_data.get('support_count', 0)} apoyo(s)</strong> ciudadano(s).</p>
        <p>Tu apoyo ayuda a que esta iniciativa llegue a las autoridades correspondientes.</p>
    </div>
    <div class="footer">
        Green Tech<br>
        <a href="https://tramaurbanaverde.cl">https://tramaurbanaverde.cl</a>
    </div>
</body>
</html>
        """.strip()

        return self.send_email(supporter_email, subject, body_text, body_html)

    def send_moderation_notification(
        self,
        request_data: dict[str, Any],
        action: str,
        reason: str | None = None,
        to: str | None = None,
    ) -> bool:
        """Send notification about moderation decision."""
        action_labels = {
            "approve": "Aprobada",
            "reject": "Rechazada",
            "request_changes": "Requiere cambios",
        }
        action_label = action_labels.get(action, action)

        recipient = to or settings.email_to or self.email_from
        subject = f"[Green Tech] Solicitud {action_label}: {request_data.get('title', 'Sin título')}"

        body_text = f"""
La solicitud "{request_data.get('title', 'Sin título')}" ha sido {action_label.lower()}.

{('Razón: ' + reason) if reason else ''}

Detalles:
- Categoría: {request_data.get('category', 'N/A')}
- Comuna: {request_data.get('commune', 'N/A')}
- Apoyos: {request_data.get('support_count', 0)}

---
Green Tech
https://tramaurbanaverde.cl
        """.strip()

        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
        .header.approve {{ background: #2E7D32; color: white; }}
        .header.reject {{ background: #C62828; color: white; }}
        .header.changes {{ background: #F57F17; color: white; }}
        .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #888; text-align: center; }}
    </style>
</head>
<body>
    <div class="header {action}">
        <h2>{'✅' if action == 'approve' else '❌' if action == 'reject' else '⚠️'} Solicitud {action_label}</h2>
    </div>
    <div class="content">
        <p>La solicitud <strong>"{request_data.get('title', 'Sin título')}"</strong> ha sido <strong>{action_label.lower()}</strong>.</p>
        {f'<p><strong>Razón:</strong> {reason}</p>' if reason else ''}
        <p>Categoría: {request_data.get('category', 'N/A')}<br>
        Comuna: {request_data.get('commune', 'N/A')}<br>
        Apoyos: {request_data.get('support_count', 0)}</p>
    </div>
    <div class="footer">
        Green Tech<br>
        <a href="https://tramaurbanaverde.cl">https://tramaurbanaverde.cl</a>
    </div>
</body>
</html>
        """.strip()

        return self.send_email(recipient, subject, body_text, body_html)

    def send_routing_notification(
        self,
        request_data: dict[str, Any],
        organization_data: dict[str, Any],
        to: str | None = None,
    ) -> bool:
        """Send notification when request is routed to an organization."""
        recipient = to or settings.email_to or self.email_from
        subject = f"[Green Tech] Solicitud enviada a {organization_data.get('name', 'organización')}"

        body_text = f"""
La solicitud "{request_data.get('title', 'Sin título')}" ha sido enviada a:

{organization_data.get('name', 'Organización')}
Tipo: {organization_data.get('type', 'N/A')}
Email: {organization_data.get('email', 'N/A')}

La organización tiene 15 días para responder.

---
Green Tech
https://tramaurbanaverde.cl
        """.strip()

        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1565C0; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #888; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>📤 Solicitud enviada a organización</h2>
    </div>
    <div class="content">
        <p>La solicitud <strong>"{request_data.get('title', 'Sin título')}"</strong> ha sido enviada a:</p>
        <p><strong>{organization_data.get('name', 'Organización')}</strong><br>
        Tipo: {organization_data.get('type', 'N/A')}<br>
        Email: {organization_data.get('email', 'N/A')}</p>
        <p>La organización tiene <strong>15 días</strong> para responder.</p>
    </div>
    <div class="footer">
        Green Tech<br>
        <a href="https://tramaurbanaverde.cl">https://tramaurbanaverde.cl</a>
    </div>
</body>
</html>
        """.strip()

        return self.send_email(recipient, subject, body_text, body_html)


# Global instance
email_service = EmailService()
