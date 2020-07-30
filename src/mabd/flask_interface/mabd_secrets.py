from .. import utilities

admin_email = utilities.get_env_var_checked('MABD_FLASK_ADMIN_EMAIL')
admin_emails_list = [admin_email]
