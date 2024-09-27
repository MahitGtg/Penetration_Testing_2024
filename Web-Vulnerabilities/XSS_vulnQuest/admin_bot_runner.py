import base64

# Encoded content of admin_bot.py (this will be very long)
encoded_script = """
aW1wb3J0IHJlcXVlc3RzCmltcG9ydCB0aW1lCmltcG9ydCByYW5kb20KCiMgQ29uc3RhbnRzCkJB
U0VfVVJMID0gJ2h0dHA6Ly8wLjAuMC4wOjUwMDQnCkxPR0lOX1VSTCA9IGYne0JBU0VfVVJMfS9s
b2dpbicKSE9NRV9VUkwgPSBmJ3tCQVNFX1VSTH0vaG9tZScKTE9HT1VUX1VSTCA9IGYne0JBU0Vf
VVJMfS9sb2dvdXQnClNFU1NJT05fSU5GT19VUkwgPSBmJ3tCQVNFX1VSTH0vc2Vzc2lvbl9pbmZv
JwpTRVNTSU9OID0gcmVxdWVzdHMuU2Vzc2lvbigpCgojIEFkbWluIGNyZWRlbnRpYWxzCkFETUlO
X0NSRURFTlRJQUxTID0gewogICAgJ3VzZXJuYW1lJzogJ2FkbWluJywKICAgICdwYXNzd29yZCc6
ICdhZG1pbnBhc3N3b3JkQDg5Jwp9CgpkZWYgYWRtaW5fbG9naW4oKToKICAgIHByaW50KCJbKl0g
QWRtaW4gaXMgdHJ5aW5nIHRvIGxvZyBpbi4uLiIpCiAgICByZXNwb25zZSA9IFNFU1NJT04ucG9z
dChMT0dJTl9VUkwsIGRhdGE9QURNSU5fQ1JFREVOVElBTFMpCiAgICAKICAgICMgQ2hlY2sgaWYg
dGhlIGxvZ2luIHdhcyBzdWNjZXNzZnVsIGFuZCByZXRyaWV2ZSBzZXNzaW9uIGtleQogICAgaWYg
IldlbGNvbWUsIGFkbWluIiBpbiByZXNwb25zZS50ZXh0OgogICAgICAgIHByaW50KCJbK10gQWRt
aW4gbG9nZ2VkIGluIHN1Y2Nlc3NmdWxseS4iKQogICAgICAgICMgUHJpbnQgdGhlIHNlc3Npb24g
a2V5IGZyb20gdGhlIGNvb2tpZXMKICAgICAgICBpZiAnc2Vzc2lvbicgaW4gU0VTU0lPTi5jb29r
aWVzOgogICAgICAgICAgICBzZXNzaW9uX2tleSA9IFNFU1NJT04uY29va2llc1snc2Vzc2lvbidd
CiAgICAgICAgICAgICMgcHJpbnQoZiJbK10gQWRtaW4gc2Vzc2lvbiBrZXk6IHtzZXNzaW9uX2tl
eX0iKSAtLSByZW1vdmUgdGhpcyBsaW5lIGluIGZpbmFsIHZtCiAgICAgICAgICAgIHByaW50KCJb
Kl0gUmV0cmlldmluZyBmdWxsIHNlc3Npb24gZGF0YS4uLiIpCiAgICAgICAgICAgIHNlc3Npb25f
ZGF0YSA9IFNFU1NJT04uZ2V0KFNFU1NJT05fSU5GT19VUkwpLnRleHQKICAgICAgICAgICAgcHJp
bnQoZiJbK10gRnVsbCBzZXNzaW9uIGRhdGE6IHtzZXNzaW9uX2RhdGF9IikKICAgICAgICBlbHNl
OgogICAgICAgICAgICBwcmludCgiWy1dIE5vIHNlc3Npb24ga2V5IGZvdW5kLiIpCiAgICBlbHNl
OgogICAgICAgIHByaW50KCJbLV0gQWRtaW4gZmFpbGVkIHRvIGxvZyBpbi4iKQoKZGVmIHZpc2l0
X2hvbWUoKToKICAgIHByaW50KCJbKl0gQWRtaW4gaXMgdmlzaXRpbmcgdGhlIGhvbWUgcGFnZS4u
LiIpCiAgICByZXNwb25zZSA9IFNFU1NJT04uZ2V0KEhPTUVfVVJMKQogICAgaWYgIkNvbW1lbnRz
OiIgaW4gcmVzcG9uc2UudGV4dDoKICAgICAgICBwcmludCgiWytdIEFkbWluIHZpZXdlZCB0aGUg
Y29tbWVudHMgc3VjY2Vzc2Z1bGx5LiIpCiAgICBlbHNlOgogICAgICAgIHByaW50KCJbLV0gQWRt
aW4gY291bGQgbm90IGFjY2VzcyB0aGUgaG9tZSBwYWdlLiIpCgpkZWYgYWRtaW5fbG9nb3V0KCk6
CiAgICBwcmludCgiWypdIEFkbWluIGlzIGxvZ2dpbmcgb3V0Li4uIikKICAgIHJlc3BvbnNlID0g
U0VTU0lPTi5nZXQoTE9HT1VUX1VSTCkKICAgIGlmIHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIw
MDoKICAgICAgICBwcmludCgiWytdIEFkbWluIGxvZ2dlZCBvdXQgc3VjY2Vzc2Z1bGx5LiIpCiAg
ICBlbHNlOgogICAgICAgIHByaW50KCJbLV0gQWRtaW4gZmFpbGVkIHRvIGxvZyBvdXQuIikKCmRl
ZiBzaW11bGF0ZV9hZG1pbl9hY3Rpdml0eSgpOgogICAgd2hpbGUgVHJ1ZToKICAgICAgICBhZG1p
bl9sb2dpbigpCiAgICAgICAgdmlzaXRfaG9tZSgpCiAgICAgICAgYWRtaW5fbG9nb3V0KCkKICAg
ICAgICAjIFdhaXQgZm9yIGEgcmFuZG9tIHRpbWUgYmV0d2VlbiAxMCB0byAzMCBzZWNvbmRzIGJl
Zm9yZSBuZXh0IGFjdGl2aXR5CiAgICAgICAgdGltZS5zbGVlcChyYW5kb20ucmFuZGludCg2MCwg
MTgwKSkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICBzaW11bGF0ZV9hZG1pbl9hY3Rp
dml0eSgpCg==
"""

# Decode and execute the script
exec(base64.b64decode(encoded_script).decode('utf-8'))
