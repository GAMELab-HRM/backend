from auth.auth_handler import signJWT,decodeJWT


# token = signJWT("EricChiu")
# print(token)
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkVyaWNDaGl1IiwiZXhwaXJlcyI6MTY0MzE4MzY5Ni41MzgyODc0fQ.N0otOvcE4ETgP2-YMMqIAOgf-3Us-v6srq_B6952e_g"
de = decodeJWT(token)
print(de)