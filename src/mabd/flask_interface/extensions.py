from functools import wraps

from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID

class CredentialStore(dict):
    def __setitem__(self, sub, item):
        print("running setitem")
        return setattr(self, sub, item)

    def __getitem__(self, item):
        return getattr(self, item)

oidc_credentials = CredentialStore()

oidc = OpenIDConnect()

keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/auth/",
                                 client_id="vanilla",
                                 realm_name="demo",
                                 client_secret_key="843893fc-edb7-4302-85bf-fa858ff26212")
