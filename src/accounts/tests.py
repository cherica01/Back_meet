import smtplib

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "ghleomyre@gmail.com"
EMAIL_HOST_PASSWORD = "mgsh bkgt wgkj fars"

try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("Connexion SMTP réussie ✅")
    server.sendmail(
        EMAIL_HOST_USER,
        "ghosth.leomyre@gmail.com",
        "Sujet: Test SMTP\n\nCeci est un test."
    )
    print("E-mail envoyé avec succès ✅")
    server.quit()
except Exception as e:
    print(f"Erreur SMTP ❌: {e}")
