def normalize_email(email):
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email.strip() if email else ""
    try:
        email_name, domain_part = email.rsplit("@", 1)
    except ValueError:
        return email
    else:
        return email_name + "@" + domain_part.lower()
